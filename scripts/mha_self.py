"""Causal self-attention — practice template.

Fill in the TODO bodies, then run:
    python3 mha_self.py              # demo (shapes + lower-triangular check)
    .venv/bin/python mha_self.py --align   # compare to torch.nn.MultiheadAttention

Reference solution: see mha.py.
"""

from __future__ import annotations

import argparse

import numpy as np


# ---------------------------------------------------------------------------
# TODO 1: numerically stable softmax over the last dim
# ---------------------------------------------------------------------------

test_input = np.array([[1,2],[2,3]])

def softmax(x: np.ndarray) -> np.ndarray:
    """softmax(x)[i] = exp(x[i]) / sum_j exp(x[j]), computed stably."""
    # Hint: subtract per-row max before exp to avoid overflow.
    x_max = np.max(x, axis=-1, keepdims=True)
    x_shift = x - x_max
    x_shift = np.exp(x_shift) 
    x_shift = x_shift / np.sum(x_shift, axis=-1, keepdims=True)
    #print(x_shift)
    return x_shift

print(softmax(test_input))


exit()
# ---------------------------------------------------------------------------
# TODO 2: additive causal mask (upper-triangle = -inf, else 0)
# ---------------------------------------------------------------------------
def causal_mask(T: int) -> np.ndarray:
    """Return a (T, T) float32 mask matching PyTorch's attn_mask convention.

    Position (i, j) = 0 if j <= i (allowed), -inf if j > i (blocked).
    Use np.triu_indices(T, k=1) to find the upper-triangle positions.
    """
    mask = np.zeros((T, T), dtype=np.float32)   # 全 0
    mask[np.triu_indices(T, k=1)] = -np.inf     # 严格上三角 = -inf
    return mask

    #raise NotImplementedError


# ---------------------------------------------------------------------------
# TODO 3: scaled dot-product attention
# ---------------------------------------------------------------------------
def scaled_dot_product_attention(
    q: np.ndarray, k: np.ndarray, v: np.ndarray,
    additive_mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """q/k/v: (B, H, T, d_head). Returns (output, weights).

    Steps:
        1. scores = q @ k^T / sqrt(d_head)        # (B, H, T, T)
        2. if mask given, scores = scores + mask   # -inf blocks -> weight 0
        3. weights = softmax(scores)
        4. output  = weights @ v                   # (B, H, T, d_head)
    Remember: transpose the last two dims of k, NOT reshape.
    """

    scores = q 
    raise NotImplementedError


# ---------------------------------------------------------------------------
# TODO 4 & 5: head split / merge
# ---------------------------------------------------------------------------
def _split_heads(x: np.ndarray, H: int) -> np.ndarray:
    """(B, T, D) -> (B, H, T, d_head).

    Hint: reshape to (B, T, H, d_head), then transpose axes to put H second.
    """
    
    raise NotImplementedError


def _merge_heads(x: np.ndarray) -> np.ndarray:
    """(B, H, T, d_head) -> (B, T, D). Inverse of _split_heads."""
    raise NotImplementedError


# ---------------------------------------------------------------------------
# CausalSelfAttention: fill __init__ and forward
# ---------------------------------------------------------------------------
class CausalSelfAttention:
    """Multi-head self-attention with a lower-triangular (causal) mask.

    Weight layout matches torch.nn.Linear: ``y = x @ W.T + b``.
    """

    def __init__(self, embed_dim: int, num_heads: int) -> None:
        assert embed_dim % num_heads == 0
        self.embed_dim = embed_dim
        self.num_heads = num_heads

        # TODO 6: create four Linear-style params (W, b) for q/k/v/o.
        # Each W has shape (embed_dim, embed_dim); each b has shape (embed_dim,).
        # Use Glorot-uniform init: bound = sqrt(6 / (in + out)).
        # Store them as self.q_w, self.q_b, self.k_w, self.k_b,
        #                  self.v_w, self.v_b, self.o_w, self.o_b.
        raise NotImplementedError

    def forward(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """x: (B, T, D) -> (output (B, T, D), weights (B, H, T, T)).

        Pipeline:
            1. project x to q, k, v with the three Linear layers
            2. split each into heads (B, H, T, d_head)
            3. run SDPA with additive causal_mask(T)
            4. merge heads back to (B, T, D)
            5. apply output projection
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Tests (do not modify — run these to check your implementation)
# ---------------------------------------------------------------------------
def _demo() -> None:
    np.random.seed(0)
    B, T, D, H = 2, 4, 8, 2
    x = np.random.randn(B, T, D).astype(np.float32)

    attn = CausalSelfAttention(D, H)
    out, w = attn.forward(x)
    print("input :", x.shape, "-> output:", out.shape)
    print("weights shape:", w.shape)

    # Sanity check: weights rows must sum to 1, upper-triangle must be 0.
    row_sums = w.sum(axis=-1)
    print("row-sum range:", row_sums.min(), row_sums.max())
    assert np.allclose(row_sums, 1.0, atol=1e-5), "rows must sum to 1"

    triu = np.triu(np.ones((T, T)), k=1).astype(bool)   # upper-triangle (j > i)
    assert np.allclose(w[:, :, triu], 0.0, atol=1e-6), \
        "upper-triangle of weights must be zero (causal)"

    print("\nweights[0, 0] (batch 0, head 0):")
    print(np.round(w[0, 0], 3))


def _align_with_torch() -> None:
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
            attn_mask=torch.from_numpy(causal_mask(T)),
            need_weights=True, average_attn_weights=False,
        )

    ours = CausalSelfAttention(D, H)
    # Load the same weights torch uses.
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
