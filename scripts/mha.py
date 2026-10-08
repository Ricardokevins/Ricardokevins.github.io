"""Causal self-attention in NumPy (multi-head, with triangular mask).

    python3 mha.py                # demo
    .venv/bin/python mha.py --align   # check against torch
"""

from __future__ import annotations

import argparse

import numpy as np


def softmax(x: np.ndarray) -> np.ndarray:
    shifted = x - np.max(x, axis=-1, keepdims=True)
    exp_x = np.exp(shifted)
    return exp_x / np.sum(exp_x, axis=-1, keepdims=True)


def causal_mask(T: int) -> np.ndarray:
    """Additive (T, T) mask: upper-triangle = -inf, else 0 (PyTorch convention)."""
    m = np.zeros((T, T), dtype=np.float32)
    m[np.triu_indices(T, k=1)] = -np.inf
    return m


def scaled_dot_product_attention(
    q: np.ndarray, k: np.ndarray, v: np.ndarray,
    additive_mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """q/k/v: (B, H, T, d_head). additive_mask: (T, T) or broadcastable."""
    d = q.shape[-1]
    scores = (q @ k.swapaxes(-1, -2)) / np.sqrt(d)
    if additive_mask is not None:
        scores = scores + additive_mask           # -inf positions -> 0 after softmax
    weights = softmax(scores)
    return weights @ v, weights


def _split_heads(x: np.ndarray, H: int) -> np.ndarray:
    B, T, D = x.shape
    return x.reshape(B, T, H, D // H).transpose(0, 2, 1, 3)


def _merge_heads(x: np.ndarray) -> np.ndarray:
    B, H, T, d = x.shape
    return x.transpose(0, 2, 1, 3).reshape(B, T, H * d)


class CausalSelfAttention:
    """Multi-head self-attention with a causal (lower-triangular) mask.

    Each token can only attend to itself and earlier positions — used by
    decoder-only models (GPT-style). Weight layout matches torch.nn.Linear:
    ``x @ W.T + b``.
    """

    def __init__(self, embed_dim: int, num_heads: int) -> None:
        assert embed_dim % num_heads == 0
        self.embed_dim = embed_dim
        self.num_heads = num_heads

        def _lin(out_dim: int, in_dim: int) -> tuple[np.ndarray, np.ndarray]:
            bound = np.sqrt(6.0 / (in_dim + out_dim))
            return (np.random.uniform(-bound, bound, (out_dim, in_dim)).astype(np.float32),
                    np.zeros(out_dim, dtype=np.float32))

        (self.q_w, self.q_b) = _lin(embed_dim, embed_dim)
        (self.k_w, self.k_b) = _lin(embed_dim, embed_dim)
        (self.v_w, self.v_b) = _lin(embed_dim, embed_dim)
        (self.o_w, self.o_b) = _lin(embed_dim, embed_dim)

    def forward(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """x: (B, T, D) -> output (B, T, D), weights (B, H, T, T)."""
        q = _split_heads(x @ self.q_w.T + self.q_b, self.num_heads)
        k = _split_heads(x @ self.k_w.T + self.k_b, self.num_heads)
        v = _split_heads(x @ self.v_w.T + self.v_b, self.num_heads)

        # (T, T) additive mask broadcasts over (B, H, T, T).
        ctx, weights = scaled_dot_product_attention(
            q, k, v, additive_mask=causal_mask(x.shape[1])
        )
        out = _merge_heads(ctx) @ self.o_w.T + self.o_b
        return out, weights


# ---------------------------------------------------------------------------
# Demo + (optional) torch alignment
# ---------------------------------------------------------------------------
def _demo() -> None:
    np.random.seed(0)
    B, T, D, H = 2, 4, 8, 2
    x = np.random.randn(B, T, D).astype(np.float32)

    attn = CausalSelfAttention(D, H)
    out, w = attn.forward(x)
    print("input :", x.shape, "-> output:", out.shape)
    print("weights shape:", w.shape)
    print("\nweights[0, 0] (batch 0, head 0) — lower-triangular:")
    print(np.round(w[0, 0], 3))


def _align_with_torch() -> None:
    """Compare against torch.nn.MultiheadAttention fed the same causal mask."""
    import torch

    torch.manual_seed(42)
    np.random.seed(42)

    B, T, D, H = 2, 5, 16, 4
    x_np = np.random.randn(B, T, D).astype(np.float32)
    x = torch.from_numpy(x_np)

    ref = torch.nn.MultiheadAttention(D, H, batch_first=True, bias=True).eval()
    with torch.no_grad():
        out_ref, w_ref = ref(
            x, x, x,
            attn_mask=torch.from_numpy(causal_mask(T)),   # additive (T, T)
            need_weights=True, average_attn_weights=False,
        )

    ours = CausalSelfAttention(D, H)
    # Copy weights: torch in_proj is (3D, D), out_proj is (D, D).
    in_w = ref.in_proj_weight.detach().numpy()
    in_b = ref.in_proj_bias.detach().numpy()
    ours.q_w, ours.k_w, ours.v_w = in_w[:D], in_w[D:2 * D], in_w[2 * D:]
    ours.q_b, ours.k_b, ours.v_b = in_b[:D], in_b[D:2 * D], in_b[2 * D:]
    ours.o_w = ref.out_proj.weight.detach().numpy()
    ours.o_b = ref.out_proj.bias.detach().numpy()

    out_np, w_np = ours.forward(x_np)
    out_diff = np.abs(out_np - out_ref.numpy()).max()
    w_diff = np.abs(w_np - w_ref.numpy()).max()
    print("=== Alignment with torch.nn.MultiheadAttention (causal) ===")
    print(f"output  max|Δ| = {out_diff:.3e}")
    print(f"weights max|Δ| = {w_diff:.3e}")
    assert out_diff < 1e-4 and w_diff < 1e-5
    print("PASS.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--align", action="store_true")
    args = parser.parse_args()
    _demo()
    if args.align:
        print()
        _align_with_torch()


if __name__ == "__main__":
    main()
