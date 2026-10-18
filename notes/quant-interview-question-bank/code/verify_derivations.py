"""核验新增推导的覆盖、关键精确数值与拆分贪心；仅使用标准库。"""

from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, permutations, product
from math import comb, isclose
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def solve(matrix, rhs):
    """用有理数高斯消元核验小型状态方程，避免近似值掩盖误差。"""
    rows = [[F(v) for v in row] + [F(value)] for row, value in zip(matrix, rhs)]
    n = len(rows)
    for col in range(n):
        pivot = next(row for row in range(col, n) if rows[row][col])
        rows[col], rows[pivot] = rows[pivot], rows[col]
        factor = rows[col][col]
        rows[col] = [v / factor for v in rows[col]]
        for row in range(n):
            if row != col:
                factor = rows[row][col]
                rows[row] = [a - factor * b for a, b in zip(rows[row], rows[col])]
    return [row[-1] for row in rows]


def waiting(pattern):
    """从模式本身构造最长前后缀自动机，独立核验等待递推。"""
    n = len(pattern)
    matrix = [[F(i == j) for j in range(n)] for i in range(n)]
    for state in range(n):
        for face in "HT":
            text = pattern[:state] + face
            target = max(k for k in range(n + 1) if text.endswith(pattern[:k]))
            if target < n:
                matrix[state][target] -= F(1, 2)
    return solve(matrix, [1] * n)[0]


@lru_cache(None)
def partitions(value, minimum=1):
    """枚举整数的全部非降拆分，与贪心采用不同求解路径。"""
    result = [(value,)] if value >= minimum else []
    for first in range(minimum, value // 2 + 1):
        result.extend((first,) + tail for tail in partitions(value - first, first))
    return tuple(result)


def exhaustive_splits(values):
    states = {0: 0}
    for value in values:
        following = {}
        for last, cost in states.items():
            for pieces in partitions(value):
                if pieces[0] >= last:
                    end = pieces[-1]
                    following[end] = min(following.get(end, 10**9), cost + len(pieces) - 1)
        states = following
    return min(states.values(), default=0)


def greedy_splits(values):
    limit, operations = values[-1], 0
    for value in reversed(values[:-1]):
        pieces = (value + limit - 1) // limit
        operations += pieces - 1
        limit = value // pieces
    return operations


def main():
    covered = 0
    for chapter in range(1, 41):
        text = (ROOT / "chapters" / f"{chapter:03d}.html").read_text()
        expected = text.count('class="worked-example"')
        actual = re.findall(r'data-derivation="([^"]+)"', text)
        assert expected == len(actual) == len(set(actual)), chapter
        covered += len(actual)
    for chapter, expected in ((43, 30), (44, 120)):
        text = (ROOT / "chapters" / f"{chapter:03d}.html").read_text()
        actual = re.findall(r'data-derivation="([^"]+)"', text)
        assert len(actual) == len(set(actual)) == expected, chapter
        assert '../assets/quant-bank.js' in text
        covered += expected

    # 逐序列计数：递推公式之外的独立有限样本核验。
    assert sum(all(p[i] != i for i in range(5)) for p in permutations(range(5))) == 44
    assert sum(len(set(p)) == 3 for p in product(range(3), repeat=6)) == 540
    assert sum(len(set(p)) == 4 for p in product(range(4), repeat=6)) == 1560
    assert sum(k.bit_length() for k in range(1, 1001)) == 8987
    assert pow(7, 2026, 1000) == 649
    assert [n for n in range(100) if n**3 % 100 == 11] == [71]
    assert next(n for n in range(100) if str(2**n).startswith("9")) == 53
    assert 4 * sum(k * k for k in range(1, 12)) == 2024
    assert 4 * sum(k * k for k in range(1, 8)) == 560
    assert comb(52, 2) - comb(48, 2) == 198
    assert F(comb(4, 2), 198) == F(1, 33)
    assert F(12, 15) * F(8, 14) * F(4, 13) == F(64, 455)

    # 从原始座位排列直接计算均值与方差，而不复用文中指示变量推导。
    fixed = [sum(p[i] == i for i in range(5)) for p in permutations(range(5))]
    assert F(sum(fixed), len(fixed)) == 1
    assert F(sum(v * v for v in fixed), len(fixed)) - 1 == 1
    swaps = [sum(p[i] == j and p[j] == i for i, j in combinations(range(5), 2))
             for p in permutations(range(5))]
    assert F(sum(swaps), len(swaps)) == F(1, 2)
    assert F(sum(v * v for v in swaps), len(swaps)) - F(1, 4) == F(1, 2)

    assert waiting("HH") == 6
    assert waiting("HT") == 4
    assert waiting("HTH") == 10
    assert waiting("HHHH") == 30
    assert waiting("HTTH") == 18
    assert waiting("HHHHH") == 62
    assert sum(6**k for k in range(1, 7)) == 55986
    values = [F(7, 2)]
    for _ in range(2):
        values.append(sum(max(F(x), values[-1]) for x in range(1, 7)) / 6)
    assert values == [F(7, 2), F(17, 4), F(14, 3)]
    assert sum(1 - F(k, 6)**3 for k in range(6)) == F(119, 24)
    assert solve([[1, -F(2, 5)], [-F(3, 5), 1]], [F(3, 5), 0]) == [F(15, 19), F(9, 19)]
    assert solve([[1, -F(1, 2), 0, 0], [-F(1, 2), 1, -F(1, 2), 0],
                  [0, -F(1, 2), 1, -F(1, 2)], [0, 0, -1, 1]], [1, 1, 1, 1])[1] == 12

    # 精确二项检验能区分未经连续性校正的近似所造成的临界翻转。
    tail = F(sum(comb(100, k) for k in range(60, 101)), 2**100)
    assert isclose(float(2 * tail), 0.05688793364098078, abs_tol=1e-14)
    assert F(1, 27) == 1 - 4 * F(2, 3)**3 + 6 * F(1, 3)**3
    assert F(36, 100) * F(14, 10) / (1 - F(24, 100)) == F(63, 95)

    # 直接重新计算删零的样本标准差，核验两种口径的倍率公式。
    xs = [F(1), F(2), F(4), F(-1)]
    n, mean = len(xs), sum(xs) / len(xs)
    deviation = sum((x - mean)**2 for x in xs)
    full = xs + [F(0)] * n
    full_mean = sum(full) / len(full)
    full_var = sum((x - full_mean)**2 for x in full) / (len(full) - 1)
    ratio_sq = mean**2 / (deviation / (n - 1)) / (full_mean**2 / full_var)
    assert ratio_sq == F(n - 1, 2 * n - 1) * (4 + 2 * n * mean**2 / deviation)

    split_cases = 0
    for length in range(1, 5):
        for array in product(range(1, 6), repeat=length):
            assert greedy_splits(array) == exhaustive_splits(array), array
            split_cases += 1
    print(f"覆盖 {covered} 个逐题增补；精确计数、等待状态、二项检验、夏普倍率均通过；"
          f"拆分贪心与穷举独立比较 {split_cases} 组全部一致。")


if __name__ == "__main__":
    main()
