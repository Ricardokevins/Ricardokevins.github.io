"""A small decoder-only Transformer implemented with Python's standard library.

The implementation deliberately avoids tensor frameworks.  It uses nested
Python lists so that every shape change in attention remains visible:

    token ids -> embeddings -> Q/K/V -> attention weights -> residual block
              -> FFN -> logits

This is an interview-study implementation, not a production inference
engine.  In particular, generation recomputes the whole context each step and
does not implement a KV cache.
"""

from __future__ import annotations

import math
import random
from typing import List, Optional, Sequence, Tuple


Vector = List[float]
Matrix = List[Vector]
Batch = List[Matrix]
AttentionWeights = List[List[List[List[float]]]]


def _validate_matrix(matrix: Matrix, name: str) -> Tuple[int, int]:
    """Return ``(rows, columns)`` and reject ragged matrices."""

    if not matrix:
        raise ValueError(f"{name} must not be empty")
    columns = len(matrix[0])
    if columns == 0:
        raise ValueError(f"{name} must contain at least one column")
    for row in matrix:
        if len(row) != columns:
            raise ValueError(f"{name} is ragged")
    return len(matrix), columns


def _validate_batch(batch: Batch, name: str) -> Tuple[int, int, int]:
    """Return ``(batch_size, sequence_length, width)`` for a 3-D list."""

    if not batch:
        raise ValueError(f"{name} must not be empty")
    sequence_length, width = _validate_matrix(batch[0], f"{name}[0]")
    for index, sequence in enumerate(batch[1:], start=1):
        rows, columns = _validate_matrix(sequence, f"{name}[{index}]")
        if rows != sequence_length or columns != width:
            raise ValueError(f"all {name} sequences must have the same shape")
    return len(batch), sequence_length, width


def zeros(rows: int, columns: int) -> Matrix:
    if rows <= 0 or columns <= 0:
        raise ValueError("matrix dimensions must be positive")
    return [[0.0 for _ in range(columns)] for _ in range(rows)]


def matrix_multiply(left: Matrix, right: Matrix) -> Matrix:
    """Multiply two 2-D matrices without delegating to a tensor library."""

    left_rows, left_columns = _validate_matrix(left, "left")
    right_rows, right_columns = _validate_matrix(right, "right")
    if left_columns != right_rows:
        raise ValueError(
            f"incompatible shapes: ({left_rows}, {left_columns}) x "
            f"({right_rows}, {right_columns})"
        )

    result = zeros(left_rows, right_columns)
    for row in range(left_rows):
        for column in range(right_columns):
            value = 0.0
            for shared in range(left_columns):
                value += left[row][shared] * right[shared][column]
            result[row][column] = value
    return result


def matrix_add(left: Matrix, right: Matrix) -> Matrix:
    left_rows, left_columns = _validate_matrix(left, "left")
    right_rows, right_columns = _validate_matrix(right, "right")
    if (left_rows, left_columns) != (right_rows, right_columns):
        raise ValueError("matrix_add requires equal shapes")
    return [
        [left[row][column] + right[row][column] for column in range(left_columns)]
        for row in range(left_rows)
    ]


def vector_dot(left: Sequence[float], right: Sequence[float]) -> float:
    if len(left) != len(right):
        raise ValueError("vector_dot requires equal lengths")
    value = 0.0
    for index in range(len(left)):
        value += left[index] * right[index]
    return value


def stable_softmax(values: Sequence[float], allowed: Optional[Sequence[bool]] = None) -> Vector:
    """Compute a masked, numerically stable softmax.

    Subtracting the largest allowed logit prevents ``exp`` overflow.  A row
    with no allowed positions returns all zeros instead of NaN; this is useful
    when a padding mask hides an entire query row.
    """

    if not values:
        raise ValueError("softmax input must not be empty")
    if allowed is None:
        allowed = [True for _ in values]
    if len(values) != len(allowed):
        raise ValueError("softmax mask must match the number of logits")

    valid_values = [values[index] for index, ok in enumerate(allowed) if ok]
    if not valid_values:
        return [0.0 for _ in values]

    maximum = max(valid_values)
    exponentials = [
        math.exp(values[index] - maximum) if allowed[index] else 0.0
        for index in range(len(values))
    ]
    denominator = sum(exponentials)
    return [value / denominator for value in exponentials]


def gelu(value: float) -> float:
    """The exact GELU used by the educational FFN."""

    return 0.5 * value * (1.0 + math.erf(value / math.sqrt(2.0)))


def argmax(values: Sequence[float]) -> int:
    if not values:
        raise ValueError("argmax input must not be empty")
    best_index = 0
    for index in range(1, len(values)):
        if values[index] > values[best_index]:
            best_index = index
    return best_index


class Linear:
    """A row-vector linear layer with weights stored as [out][in]."""

    def __init__(self, in_features: int, out_features: int, rng: random.Random):
        if in_features <= 0 or out_features <= 0:
            raise ValueError("linear dimensions must be positive")
        self.in_features = in_features
        self.out_features = out_features
        limit = math.sqrt(6.0 / (in_features + out_features))
        self.weights: Matrix = [
            [rng.uniform(-limit, limit) for _ in range(in_features)]
            for _ in range(out_features)
        ]
        self.bias: Vector = [0.0 for _ in range(out_features)]

    def forward(self, inputs: Matrix) -> Matrix:
        rows, width = _validate_matrix(inputs, "linear inputs")
        if width != self.in_features:
            raise ValueError(
                f"expected {self.in_features} input features, got {width}"
            )

        outputs = zeros(rows, self.out_features)
        for row in range(rows):
            for output_feature in range(self.out_features):
                value = self.bias[output_feature]
                for input_feature in range(self.in_features):
                    value += (
                        inputs[row][input_feature]
                        * self.weights[output_feature][input_feature]
                    )
                outputs[row][output_feature] = value
        return outputs

    @property
    def parameter_count(self) -> int:
        return self.in_features * self.out_features + self.out_features


class Embedding:
    def __init__(self, vocab_size: int, embedding_dim: int, rng: random.Random):
        if vocab_size <= 0 or embedding_dim <= 0:
            raise ValueError("embedding dimensions must be positive")
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        limit = 1.0 / math.sqrt(embedding_dim)
        self.table: Matrix = [
            [rng.uniform(-limit, limit) for _ in range(embedding_dim)]
            for _ in range(vocab_size)
        ]

    def forward(self, token_ids: Sequence[Sequence[int]]) -> Batch:
        if not token_ids:
            raise ValueError("token_ids must not be empty")
        batch: Batch = []
        for sequence in token_ids:
            if not sequence:
                raise ValueError("token sequences must not be empty")
            embeddings: Matrix = []
            for token_id in sequence:
                if token_id < 0 or token_id >= self.vocab_size:
                    raise ValueError(f"token id {token_id} is outside the vocabulary")
                embeddings.append(self.table[token_id][:])
            batch.append(embeddings)
        _validate_batch(batch, "embeddings")
        return batch

    @property
    def parameter_count(self) -> int:
        return self.vocab_size * self.embedding_dim


class SinusoidalPositionEncoding:
    """Non-learned positional encoding, included to keep the model self-contained."""

    def __init__(self, max_sequence_length: int, embedding_dim: int):
        if max_sequence_length <= 0 or embedding_dim <= 0:
            raise ValueError("position-encoding dimensions must be positive")
        self.max_sequence_length = max_sequence_length
        self.embedding_dim = embedding_dim
        self.values: Matrix = zeros(max_sequence_length, embedding_dim)
        for position in range(max_sequence_length):
            for dimension in range(embedding_dim):
                exponent = (2 * (dimension // 2)) / embedding_dim
                angle = position / (10000.0**exponent)
                self.values[position][dimension] = (
                    math.sin(angle) if dimension % 2 == 0 else math.cos(angle)
                )

    def add_to_batch(self, batch: Batch) -> Batch:
        batch_size, sequence_length, width = _validate_batch(batch, "position input")
        if width != self.embedding_dim:
            raise ValueError("position encoding width must match the input width")
        if sequence_length > self.max_sequence_length:
            raise ValueError("sequence is longer than the configured context window")

        return [
            [
                [
                    sequence[position][dimension] + self.values[position][dimension]
                    for dimension in range(width)
                ]
                for position in range(sequence_length)
            ]
            for sequence in batch
        ]


class LayerNorm:
    def __init__(self, normalized_dim: int, epsilon: float = 1e-5):
        if normalized_dim <= 0:
            raise ValueError("normalized_dim must be positive")
        self.normalized_dim = normalized_dim
        self.epsilon = epsilon
        self.gamma: Vector = [1.0 for _ in range(normalized_dim)]
        self.beta: Vector = [0.0 for _ in range(normalized_dim)]

    def forward(self, inputs: Matrix) -> Matrix:
        rows, width = _validate_matrix(inputs, "layer norm inputs")
        if width != self.normalized_dim:
            raise ValueError("layer norm width does not match normalized_dim")

        outputs = zeros(rows, width)
        for row in range(rows):
            mean = sum(inputs[row]) / width
            variance = sum(
                (value - mean) * (value - mean) for value in inputs[row]
            ) / width
            inverse_std = 1.0 / math.sqrt(variance + self.epsilon)
            for dimension in range(width):
                normalized = (inputs[row][dimension] - mean) * inverse_std
                outputs[row][dimension] = (
                    self.gamma[dimension] * normalized + self.beta[dimension]
                )
        return outputs

    @property
    def parameter_count(self) -> int:
        return 2 * self.normalized_dim


class MultiHeadAttention:
    """Causal self-attention with explicit multi-head list operations."""

    def __init__(self, d_model: int, num_heads: int, rng: random.Random):
        if d_model <= 0 or num_heads <= 0:
            raise ValueError("attention dimensions must be positive")
        if d_model % num_heads != 0:
            raise ValueError("d_model must be divisible by num_heads")
        self.d_model = d_model
        self.num_heads = num_heads
        self.head_dim = d_model // num_heads
        self.query_projection = Linear(d_model, d_model, rng)
        self.key_projection = Linear(d_model, d_model, rng)
        self.value_projection = Linear(d_model, d_model, rng)
        self.output_projection = Linear(d_model, d_model, rng)

    def forward(
        self,
        inputs: Batch,
        key_padding_mask: Optional[Sequence[Sequence[bool]]] = None,
        causal: bool = True,
    ) -> Tuple[Batch, AttentionWeights]:
        batch_size, sequence_length, width = _validate_batch(inputs, "attention inputs")
        if width != self.d_model:
            raise ValueError("attention input width does not match d_model")
        if key_padding_mask is not None:
            if len(key_padding_mask) != batch_size:
                raise ValueError("padding mask batch size does not match inputs")
            for mask in key_padding_mask:
                if len(mask) != sequence_length:
                    raise ValueError("padding mask length does not match the sequence")

        projected_q = [self.query_projection.forward(sequence) for sequence in inputs]
        projected_k = [self.key_projection.forward(sequence) for sequence in inputs]
        projected_v = [self.value_projection.forward(sequence) for sequence in inputs]

        outputs: Batch = []
        all_weights: AttentionWeights = []
        scale = math.sqrt(self.head_dim)

        for batch_index in range(batch_size):
            sequence_output = zeros(sequence_length, self.d_model)
            batch_weights: List[List[List[float]]] = []

            for head in range(self.num_heads):
                head_output = zeros(sequence_length, self.head_dim)
                head_weights: List[List[float]] = []
                head_offset = head * self.head_dim

                for query_position in range(sequence_length):
                    scores: Vector = []
                    allowed: List[bool] = []
                    query = projected_q[batch_index][query_position]

                    for key_position in range(sequence_length):
                        key = projected_k[batch_index][key_position]
                        score = 0.0
                        for dimension in range(self.head_dim):
                            score += (
                                query[head_offset + dimension]
                                * key[head_offset + dimension]
                            )
                        scores.append(score / scale)
                        can_read_key = (
                            not causal or key_position <= query_position
                        ) and (
                            key_padding_mask is None
                            or key_padding_mask[batch_index][key_position]
                        )
                        allowed.append(can_read_key)

                    weights = stable_softmax(scores, allowed)
                    head_weights.append(weights)
                    for key_position in range(sequence_length):
                        weight = weights[key_position]
                        value = projected_v[batch_index][key_position]
                        for dimension in range(self.head_dim):
                            head_output[query_position][dimension] += (
                                weight * value[head_offset + dimension]
                            )

                batch_weights.append(head_weights)
                for position in range(sequence_length):
                    for dimension in range(self.head_dim):
                        sequence_output[position][head_offset + dimension] = (
                            head_output[position][dimension]
                        )

            outputs.append(self.output_projection.forward(sequence_output))
            all_weights.append(batch_weights)

        return outputs, all_weights

    @property
    def parameter_count(self) -> int:
        return (
            self.query_projection.parameter_count
            + self.key_projection.parameter_count
            + self.value_projection.parameter_count
            + self.output_projection.parameter_count
        )


class FeedForward:
    """The position-wise MLP inside one Transformer block."""

    def __init__(self, d_model: int, d_ff: int, rng: random.Random):
        self.up_projection = Linear(d_model, d_ff, rng)
        self.down_projection = Linear(d_ff, d_model, rng)

    def forward(self, inputs: Matrix) -> Matrix:
        hidden = self.up_projection.forward(inputs)
        activated = [
            [gelu(value) for value in row]
            for row in hidden
        ]
        return self.down_projection.forward(activated)

    @property
    def parameter_count(self) -> int:
        return self.up_projection.parameter_count + self.down_projection.parameter_count


def _batch_add(left: Batch, right: Batch) -> Batch:
    if len(left) != len(right):
        raise ValueError("batch_add requires equal batch sizes")
    return [matrix_add(left[index], right[index]) for index in range(len(left))]


class TransformerBlock:
    """A pre-norm decoder block: LN -> attention -> residual -> LN -> FFN -> residual."""

    def __init__(self, d_model: int, num_heads: int, d_ff: int, rng: random.Random):
        self.attention_norm = LayerNorm(d_model)
        self.attention = MultiHeadAttention(d_model, num_heads, rng)
        self.ffn_norm = LayerNorm(d_model)
        self.feed_forward = FeedForward(d_model, d_ff, rng)

    def forward(
        self,
        inputs: Batch,
        key_padding_mask: Optional[Sequence[Sequence[bool]]] = None,
    ) -> Tuple[Batch, AttentionWeights]:
        normalized_for_attention = [
            self.attention_norm.forward(sequence) for sequence in inputs
        ]
        attention_output, weights = self.attention.forward(
            normalized_for_attention,
            key_padding_mask=key_padding_mask,
            causal=True,
        )
        after_attention = _batch_add(inputs, attention_output)

        normalized_for_ffn = [
            self.ffn_norm.forward(sequence) for sequence in after_attention
        ]
        feed_forward_output = [
            self.feed_forward.forward(sequence) for sequence in normalized_for_ffn
        ]
        return _batch_add(after_attention, feed_forward_output), weights

    @property
    def parameter_count(self) -> int:
        return (
            self.attention_norm.parameter_count
            + self.attention.parameter_count
            + self.ffn_norm.parameter_count
            + self.feed_forward.parameter_count
        )


class DecoderOnlyTransformer:
    """A minimal decoder-only Transformer that returns next-token logits."""

    def __init__(
        self,
        vocab_size: int,
        d_model: int,
        num_heads: int,
        num_layers: int,
        d_ff: int,
        max_sequence_length: int,
        seed: int = 0,
    ):
        if num_layers <= 0:
            raise ValueError("num_layers must be positive")
        self.vocab_size = vocab_size
        self.d_model = d_model
        self.max_sequence_length = max_sequence_length
        rng = random.Random(seed)

        self.embedding = Embedding(vocab_size, d_model, rng)
        self.position_encoding = SinusoidalPositionEncoding(
            max_sequence_length, d_model
        )
        self.blocks = [
            TransformerBlock(d_model, num_heads, d_ff, rng)
            for _ in range(num_layers)
        ]
        self.final_norm = LayerNorm(d_model)
        self.language_model_head = Linear(d_model, vocab_size, rng)

    def forward(
        self,
        token_ids: Sequence[Sequence[int]],
        return_attention: bool = False,
    ):
        embedded = self.embedding.forward(token_ids)
        batch_size, sequence_length, _ = _validate_batch(embedded, "embedded inputs")
        if sequence_length > self.max_sequence_length:
            raise ValueError("sequence is longer than the configured context window")

        hidden = self.position_encoding.add_to_batch(embedded)
        all_attention: List[AttentionWeights] = []
        for block in self.blocks:
            hidden, weights = block.forward(hidden)
            all_attention.append(weights)

        normalized = [self.final_norm.forward(sequence) for sequence in hidden]
        logits = [self.language_model_head.forward(sequence) for sequence in normalized]
        if return_attention:
            return logits, all_attention
        return logits

    def generate(self, token_ids: Sequence[int], max_new_tokens: int) -> List[int]:
        """Greedy generation; deliberately recomputes the context each step."""

        if not token_ids:
            raise ValueError("generation needs at least one prompt token")
        if max_new_tokens < 0:
            raise ValueError("max_new_tokens must be non-negative")
        if len(token_ids) > self.max_sequence_length:
            raise ValueError("generation prompt is longer than the context window")

        sequence = list(token_ids)
        for _ in range(max_new_tokens):
            context = sequence[-self.max_sequence_length :]
            logits = self.forward([context])
            next_token = argmax(logits[0][-1])
            sequence.append(next_token)
        return sequence

    @property
    def parameter_count(self) -> int:
        return (
            self.embedding.parameter_count
            + sum(block.parameter_count for block in self.blocks)
            + self.final_norm.parameter_count
            + self.language_model_head.parameter_count
        )


def demo() -> None:
    """Run one small forward pass so the data flow is observable from a shell."""

    model = DecoderOnlyTransformer(
        vocab_size=16,
        d_model=8,
        num_heads=2,
        num_layers=2,
        d_ff=16,
        max_sequence_length=8,
        seed=7,
    )
    prompt = [[1, 4, 3, 2]]
    logits, attention = model.forward(prompt, return_attention=True)
    print(f"logits shape: ({len(logits)}, {len(logits[0])}, {len(logits[0][0])})")
    print(
        "attention shape: "
        f"({len(attention)}, {len(attention[0])}, "
        f"{len(attention[0][0])}, {len(attention[0][0][0])}, "
        f"{len(attention[0][0][0][0])})"
    )
    print(f"first layer, first head, last query weights: {attention[0][0][-1]}")
    print(f"parameter count: {model.parameter_count}")
    print(f"greedy continuation: {model.generate(prompt[0], max_new_tokens=3)}")


if __name__ == "__main__":
    demo()
