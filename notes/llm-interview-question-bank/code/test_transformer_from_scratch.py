import ast
import math
import random
import unittest
from pathlib import Path

from transformer_from_scratch import (
    DecoderOnlyTransformer,
    MultiHeadAttention,
    stable_softmax,
)


class TransformerFromScratchTests(unittest.TestCase):
    def test_softmax_is_stable_and_sums_to_one(self):
        probabilities = stable_softmax([1000.0, 1001.0, 999.0])
        self.assertTrue(all(math.isfinite(value) for value in probabilities))
        self.assertAlmostEqual(sum(probabilities), 1.0, places=12)

    def test_masked_softmax_returns_zero_for_disallowed_positions(self):
        probabilities = stable_softmax(
            [2.0, 1000.0, 1.0], allowed=[True, False, True]
        )
        self.assertEqual(probabilities[1], 0.0)
        self.assertAlmostEqual(sum(probabilities), 1.0, places=12)

    def test_causal_attention_cannot_read_future_positions(self):
        attention = MultiHeadAttention(d_model=4, num_heads=2, rng=random.Random(3))
        inputs = [[[0.1, 0.2, 0.3, 0.4], [0.5, 0.6, 0.7, 0.8], [0.9, 1.0, 1.1, 1.2]]]
        _, weights = attention.forward(inputs, causal=True)
        for head in weights[0]:
            for query_position, row in enumerate(head):
                for key_position in range(query_position + 1, len(row)):
                    self.assertEqual(row[key_position], 0.0)
                self.assertAlmostEqual(sum(row), 1.0, places=12)

    def test_padding_mask_hides_padded_keys(self):
        attention = MultiHeadAttention(d_model=4, num_heads=2, rng=random.Random(4))
        inputs = [[[0.1, 0.2, 0.3, 0.4], [0.5, 0.6, 0.7, 0.8], [0.9, 1.0, 1.1, 1.2]]]
        _, weights = attention.forward(
            inputs,
            key_padding_mask=[[True, True, False]],
            causal=False,
        )
        for head in weights[0]:
            for row in head:
                self.assertEqual(row[2], 0.0)
                self.assertAlmostEqual(sum(row), 1.0, places=12)

    def test_decoder_forward_and_generation_shapes(self):
        model = DecoderOnlyTransformer(
            vocab_size=11,
            d_model=8,
            num_heads=2,
            num_layers=2,
            d_ff=16,
            max_sequence_length=6,
            seed=5,
        )
        logits, attention = model.forward([[1, 2, 3]], return_attention=True)
        self.assertEqual(
            (len(logits), len(logits[0]), len(logits[0][0])),
            (1, 3, 11),
        )
        self.assertEqual((len(attention), len(attention[0]), len(attention[0][0])), (2, 1, 2))
        self.assertEqual((len(attention[0][0][0]), len(attention[0][0][0][0])), (3, 3))
        generated = model.generate([1, 2, 3], max_new_tokens=4)
        self.assertEqual(len(generated), 7)
        self.assertTrue(all(0 <= token < 11 for token in generated))
        self.assertGreater(model.parameter_count, 0)
        with self.assertRaises(ValueError):
            model.generate([1, 2, 3, 4, 5, 6, 7], max_new_tokens=0)

    def test_causal_property_for_earlier_logits(self):
        model = DecoderOnlyTransformer(
            vocab_size=13,
            d_model=8,
            num_heads=2,
            num_layers=2,
            d_ff=16,
            max_sequence_length=8,
            seed=6,
        )
        first = model.forward([[1, 2, 3, 4]])[0]
        changed_future = model.forward([[1, 2, 9, 4]])[0]
        for position in (0, 1):
            for left, right in zip(first[position], changed_future[position]):
                self.assertAlmostEqual(left, right, places=12)

    def test_source_has_no_external_tensor_imports(self):
        source_path = Path(__file__).with_name("transformer_from_scratch.py")
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        forbidden = {"torch", "numpy", "transformers"}
        imported_roots = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.extend(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.append(node.module.split(".")[0])
        self.assertTrue(forbidden.isdisjoint(imported_roots), imported_roots)


if __name__ == "__main__":
    unittest.main()
