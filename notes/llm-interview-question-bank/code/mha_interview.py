"""Minimal NumPy Multi-Head Attention for interview practice.

Contract:
    inputs: (B, T, D), batch-first
    projection weights: (D, D), stored like ``nn.Linear.weight``
    attention_mask[b, j] == True means key position j is readable
    returned attention weights: (B, H, T, T)

This file uses NumPy only for array operations.  It does not call a ready-made
attention layer from PyTorch, Transformers, or another model library.
"""

from __future__ import annotations

import math
from typing import Optional, Tuple

import numpy as np


def _as_float_array(value, name: str) -> np.ndarray:
    array = np.asarray(value)
    if not np.issubdtype(array.dtype, np.floating):
        array = array.astype(np.float64)
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{name} contains NaN or infinity")
    return array


def _check_matrix(matrix: np.ndarray, name: str, shape: Tuple[int, int]) -> None:
    if matrix.ndim != 2 or tuple(matrix.shape) != shape:
        raise ValueError(f"{name} must have shape {shape}, got {matrix.shape}")


def _add_bias(values: np.ndarray, bias: Optional[np.ndarray], width: int) -> np.ndarray:
    if bias is None:
        return values
    if bias.ndim != 1 or bias.shape[0] != width:
        raise ValueError(f"bias must have shape ({width},), got {bias.shape}")
    return values + bias


def _stable_softmax(scores: np.ndarray, allowed: np.ndarray) -> np.ndarray:
    """Softmax over the last dimension without NaN on an all-masked row."""

    masked_scores = np.where(allowed, scores, -np.inf)
    has_valid_key = allowed.any(axis=-1, keepdims=True)
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        maximum = np.max(masked_scores, axis=-1, keepdims=True)
        shifted = np.where(has_valid_key, masked_scores - maximum, 0.0)
        exponentials = np.where(allowed, np.exp(shifted), 0.0)
    denominator = exponentials.sum(axis=-1, keepdims=True)
    return np.divide(
        exponentials,
        denominator,
        out=np.zeros_like(exponentials),
        where=denominator != 0,
    )


def multi_head_attention(
    inputs,
    w_q,
    w_k,
    w_v,
    w_o,
    num_heads: int,
    b_q=None,
    b_k=None,
    b_v=None,
    b_o=None,
    causal: bool = True,
    attention_mask=None,
) -> Tuple[np.ndarray, np.ndarray]:
    """Compute a self-attention forward pass.

    The implementation follows the reference equations exactly:

        Q = X @ Wq.T + bq
        K = X @ Wk.T + bk
        V = X @ Wv.T + bv
        A = softmax(mask(Q @ K.T / sqrt(head_dim)))
        Y = merge_heads(A @ V) @ Wo.T + bo

    Dropout is intentionally absent; compare in evaluation mode when matching
    a framework implementation.
    """

    x = _as_float_array(inputs, "inputs")
    wq = _as_float_array(w_q, "w_q")
    wk = _as_float_array(w_k, "w_k")
    wv = _as_float_array(w_v, "w_v")
    wo = _as_float_array(w_o, "w_o")
    if x.ndim != 3:
        raise ValueError(f"inputs must have shape (B, T, D), got {x.shape}")
    batch_size, sequence_length, d_model = x.shape
    if num_heads <= 0 or d_model % num_heads != 0:
        raise ValueError("d_model must be divisible by a positive num_heads")
    _check_matrix(wq, "w_q", (d_model, d_model))
    _check_matrix(wk, "w_k", (d_model, d_model))
    _check_matrix(wv, "w_v", (d_model, d_model))
    _check_matrix(wo, "w_o", (d_model, d_model))

    dtype = np.result_type(x.dtype, wq.dtype, wk.dtype, wv.dtype, wo.dtype)
    x, wq, wk, wv, wo = [
        array.astype(dtype, copy=False)
        for array in (x, wq, wk, wv, wo)
    ]
    bq = None if b_q is None else _as_float_array(b_q, "b_q").astype(dtype, copy=False)
    bk = None if b_k is None else _as_float_array(b_k, "b_k").astype(dtype, copy=False)
    bv = None if b_v is None else _as_float_array(b_v, "b_v").astype(dtype, copy=False)
    bo = None if b_o is None else _as_float_array(b_o, "b_o").astype(dtype, copy=False)

    # (B, T, D): all three full projections have the same shape in self-attention.
    q = _add_bias(x @ wq.T, bq, d_model)
    k = _add_bias(x @ wk.T, bk, d_model)
    v = _add_bias(x @ wv.T, bv, d_model)

    head_dim = d_model // num_heads
    # (B, T, D) -> (B, H, T, head_dim)
    q = q.reshape(batch_size, sequence_length, num_heads, head_dim).transpose(0, 2, 1, 3)
    k = k.reshape(batch_size, sequence_length, num_heads, head_dim).transpose(0, 2, 1, 3)
    v = v.reshape(batch_size, sequence_length, num_heads, head_dim).transpose(0, 2, 1, 3)

    # (B, H, T, head_dim) @ (B, H, head_dim, T) -> (B, H, T, T)
    scores = q @ np.swapaxes(k, -1, -2) / math.sqrt(head_dim)
    allowed = np.ones((batch_size, 1, sequence_length, sequence_length), dtype=bool)
    if causal:
        allowed &= np.tril(np.ones((sequence_length, sequence_length), dtype=bool))
    if attention_mask is not None:
        mask = np.asarray(attention_mask, dtype=bool)
        if mask.shape != (batch_size, sequence_length):
            raise ValueError(
                "attention_mask must have shape "
                f"({batch_size}, {sequence_length}), got {mask.shape}"
            )
        allowed &= mask[:, None, None, :]

    attention_weights = _stable_softmax(scores, allowed)
    # (B, H, T, T) @ (B, H, T, head_dim) -> (B, H, T, head_dim)
    context = attention_weights @ v
    # (B, H, T, head_dim) -> (B, T, D)
    context = context.transpose(0, 2, 1, 3).reshape(batch_size, sequence_length, d_model)
    output = _add_bias(context @ wo.T, bo, d_model)
    return output, attention_weights


def demo() -> None:
    identity = np.eye(4, dtype=np.float64)
    inputs = np.array(
        [[[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0]]],
        dtype=np.float64,
    )
    output, weights = multi_head_attention(
        inputs, identity, identity, identity, identity, num_heads=2, causal=True
    )
    print("input shape:", inputs.shape)
    print("Q/K/V shape:", inputs.shape)
    print("attention shape:", weights.shape)
    print("head 0 weights:\n", weights[0, 0])
    print("output:\n", output)


if __name__ == "__main__":
    demo()
