import ast
import unittest
from pathlib import Path

import numpy as np

from mha_interview import multi_head_attention


class InterviewMhaTests(unittest.TestCase):
    def test_identity_projection_matches_manual_causal_case(self):
        inputs = np.array([[[1.0, 0.0], [0.0, 1.0]]])
        identity = np.eye(2)
        output, attention = multi_head_attention(
            inputs, identity, identity, identity, identity, num_heads=1, causal=True
        )

        np.testing.assert_allclose(
            attention,
            [[[[1.0, 0.0], [0.3302384507, 0.6697615493]]]],
            atol=1e-9,
        )
        np.testing.assert_allclose(
            output,
            [[[1.0, 0.0], [0.3302384507, 0.6697615493]]],
            atol=1e-9,
        )

    def test_multi_head_shapes_and_causal_mask(self):
        inputs = np.eye(4, dtype=np.float64)[None, :3]
        identity = np.eye(4)
        output, attention = multi_head_attention(
            inputs, identity, identity, identity, identity, num_heads=2, causal=True
        )

        self.assertEqual(output.shape, (1, 3, 4))
        self.assertEqual(attention.shape, (1, 2, 3, 3))
        np.testing.assert_allclose(attention.sum(axis=-1), 1.0, atol=1e-12)
        for query_position in range(3):
            self.assertTrue(
                np.all(attention[:, :, query_position, query_position + 1 :] == 0.0)
            )

    def test_attention_mask_hides_keys(self):
        inputs = np.array([[[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]])
        identity = np.eye(2)
        _, attention = multi_head_attention(
            inputs,
            identity,
            identity,
            identity,
            identity,
            num_heads=1,
            causal=False,
            attention_mask=np.array([[True, True, False]]),
        )
        self.assertTrue(np.all(attention[..., 2] == 0.0))
        np.testing.assert_allclose(attention.sum(axis=-1), 1.0, atol=1e-12)

    def test_float32_is_preserved_for_reference_comparison(self):
        inputs = np.eye(4, dtype=np.float32)[None]
        identity = np.eye(4, dtype=np.float32)
        output, attention = multi_head_attention(
            inputs, identity, identity, identity, identity, num_heads=2
        )
        self.assertEqual(output.dtype, np.float32)
        self.assertEqual(attention.dtype, np.float32)

    def test_source_does_not_import_ready_mha(self):
        source_path = Path(__file__).with_name("mha_interview.py")
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        forbidden = {"torch", "transformers"}
        imported_roots = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.extend(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.append(node.module.split(".")[0])
        self.assertTrue(forbidden.isdisjoint(imported_roots), imported_roots)


if __name__ == "__main__":
    unittest.main()
