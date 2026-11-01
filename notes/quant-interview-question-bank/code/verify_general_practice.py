#!/usr/bin/env python3
"""Check source coverage and execute code extracted from the actual handbook HTML.

Coverage/anchor checks do not prove the prose: the manifest also records the
manually reviewed subquestions and source ambiguities. Optional --source-pdf
checks the original bytes, section counts and explicit lettered subquestions.
Numerical and exhaustive tests below use independent oracles, not code copies.
Requires BeautifulSoup and a C++17 compiler; no network or repository writes.
"""

import argparse
from collections import Counter
from decimal import Decimal
from fractions import Fraction as F
import hashlib
from itertools import permutations
import json
from math import comb, isclose, sqrt
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"B": 10, "P": 88, "GT": 11, "S": 46, "C": 75, "F": 35}


def load(chapter):
    return BeautifulSoup((ROOT / "chapters" / f"{chapter:03}.html").read_text(), "html.parser")


def check_coverage(source_pdf=None):
    manifest = json.loads((ROOT / "code/general_practice_coverage.json").read_text())
    questions = manifest["questions"]
    expected_ids = {f"{group}{i}" for group, count in EXPECTED.items() for i in range(1, count + 1)}
    assert len(questions) == 265
    assert {q["id"] for q in questions} == expected_ids
    pages = {f"{i:03}.html": load(i) for i in range(1, 41)}
    children = []
    for item in questions + manifest["outline"]:
        assert item["targets"], item["id"]
        for part in [item] + item.get("subquestions", []):
            if "." in part["id"]:
                children.append(part["id"])
            for target in part["targets"]:
                relative, anchor = target.split("#")
                soup = pages[Path(relative).name]
                node = soup.find(id=anchor)
                assert node is not None, (part["id"], target)
                assert part["id"] in node.get("data-source-questions", "").split(), (part["id"], target)
                assert len(node.get_text(strip=True)) > 5, target
    assert len(manifest["outline"]) == 28
    assert len(set(children)) == len(children)
    reading_text = pages["001.html"].select_one("#reading-coverage").get_text(" ", strip=True)
    assert "Trading and Exchanges" in reading_text and "Complete guide to capital markets" in reading_text
    for filename, soup in pages.items():
        ids = [node["id"] for node in soup.select("[id]")]
        assert len(ids) == len(set(ids)), filename
        for card in soup.select(".worked-example"):
            assert card.get("id"), filename
            assert len(card.select("[data-derivation]")) == 1, (filename, card["id"])
        for link in soup.select("main a[href]"):
            href = link["href"]
            if href.startswith(("https:", "http:", "mailto:")) or not href or "#" not in href:
                continue
            relative, anchor = href.split("#", 1)
            target_file = (ROOT / "chapters" / (relative or filename)).resolve()
            if target_file.parent != ROOT / "chapters" or target_file.suffix != ".html":
                continue
            assert target_file.exists(), href
            assert pages[target_file.name].find(id=anchor), (filename, href)
    if source_pdf:
        data = Path(source_pdf).read_bytes()
        assert hashlib.sha256(data).hexdigest() == manifest["source"]["sha256"], "source PDF differs"
        text = subprocess.check_output(["pdftotext", "-layout", str(source_pdf), "-"], text=True)
        headings = {"BRAINTEASERS": "B", "PROBABILITY": "P", "GAME THEORY": "GT",
                    "STATISTICS/MATHEMATICS": "S", "PROGRAMMING QUESTIONS": "C",
                    "STATISTICAL FINANCE/FINANCIAL INTUITION": "F"}
        actual, actual_children = [], []
        group = current = None
        for line in text.splitlines():
            if line.strip() in headings:
                group, current = headings[line.strip()], None
            elif group:
                match = re.match(r"\s*(\d+)\.\s+", line)
                if match:
                    current = f"{group}{match[1]}"
                    actual.append(current)
                else:
                    child = re.match(r"\s*([a-z])\.\s+", line)
                    if current and child:
                        actual_children.append(f"{current}.{child[1]}")
        assert set(actual) == expected_ids and len(actual) == 265
        assert set(actual_children) == set(children), (actual_children, children)
    return {"source_items": len(questions), "lettered_subquestions": len(children),
            "outline_items": 28, "explicit_boundaries": sum("boundary" in q for q in questions)}


def block(chapter, symbol):
    candidates = [code.get_text() for code in load(chapter).select("main pre code") if symbol in code.get_text()]
    assert len(candidates) == 1, (chapter, symbol, len(candidates))
    return candidates[0]


CPP_TESTS = r'''
long long checks = 0;
void verify(bool ok, const string& label) {
    ++checks;
    if (!ok) { cerr << "FAILED: " << label << '\n'; abort(); }
}
template<class Function>
void arrays(int maxLength, int low, int high, Function f) {
    vector<int> a;
    function<void()> visit = [&]() {
        f(a);
        if ((int)a.size() == maxLength) return;
        for (int value = low; value <= high; ++value) { a.push_back(value); visit(); a.pop_back(); }
    };
    visit();
}
int bruteLIS(const vector<int>& a) {
    int best = 0;
    for (int mask = 0; mask < (1 << a.size()); ++mask) {
        bool valid = true, first = true;
        int last = 0, count = 0;
        for (int i = 0; i < (int)a.size(); ++i) if (mask >> i & 1) {
            if (!first && a[i] <= last) valid = false;
            first = false; last = a[i]; ++count;
        }
        if (valid) best = max(best, count);
    }
    return best;
}
long long bruteHalving(vector<long long> a, int k, bool up) {
    if (k == 0 || a.empty()) return accumulate(a.begin(), a.end(), 0LL);
    long long best = LLONG_MAX;
    for (int i = 0; i < (int)a.size(); ++i) {
        auto next = a;
        next[i] = up ? (a[i] + 1) / 2 : a[i] / 2;
        best = min(best, bruteHalving(next, k - 1, up));
    }
    return best;
}
int bruteMovieDays(const vector<int>& a, int capacity) {
    if (a.empty()) return 0;
    // Subset DP has a different state from the page's assignment search.
    vector<pair<int, int>> dp(1 << a.size(), {INT_MAX, INT_MAX});
    dp[0] = {1, 0};
    for (int mask = 1; mask < (1 << a.size()); ++mask)
        for (int i = 0; i < (int)a.size(); ++i) if (mask >> i & 1) {
            auto previous = dp[mask ^ (1 << i)];
            if (previous.second + a[i] <= capacity) previous.second += a[i];
            else { ++previous.first; previous.second = a[i]; }
            dp[mask] = min(dp[mask], previous);
        }
    return dp.back().first;
}
int bruteFiles(const string& s, int i, bool aligned) {
    while (i < (int)s.size() && s[i] != '.') ++i;
    if (i == (int)s.size()) return 0;
    int best = INT_MAX;
    for (int length = 1; i + length <= (int)s.size(); length *= 2) {
        bool free = true;
        for (int j = i; j < i + length; ++j) if (s[j] != '.') free = false;
        if (free && (!aligned || i % length == 0))
            best = min(best, 1 + bruteFiles(s, i + length, aligned));
    }
    return best;
}
int main() {
    arrays(5, -2, 2, [&](const vector<int>& a) {
        vector<long long> wide(a.begin(), a.end());
        long long difference = -1;
        for (int i = 0; i < (int)a.size(); ++i) for (int j = i + 1; j < (int)a.size(); ++j)
            if (a[j] > a[i]) difference = max(difference, (long long)a[j] - a[i]);
        verify(maxPositiveDiff(wide) == difference, "C49 positive ordered difference");
        long long weighted = LLONG_MIN;
        int chunks = 0, nonnegative = 0;
        for (int mask = 0; mask < (1 << a.size()); ++mask) {
            auto swapped = a;
            bool valid = true;
            for (int i = 0; i < (int)a.size(); ++i) if (mask >> i & 1) {
                if (i + 1 == (int)a.size() || (i > 0 && (mask >> (i-1) & 1))) { valid = false; break; }
                swap(swapped[i], swapped[i+1]);
            }
            long long score = 0;
            for (int i = 0; i < (int)a.size(); ++i) score += 1LL * (i+1) * swapped[i];
            if (valid) weighted = max(weighted, score);
            long long sum = 0; int count = 0;
            bool feasible = true;
            for (int i = 0; i < (int)a.size(); ++i) if (mask >> i & 1) {
                sum += a[i]; ++count; if (sum < 0) feasible = false;
            }
            if (feasible) nonnegative = max(nonnegative, count);
        }
        verify(maxWeightedSum(a) == weighted, "C7 disjoint adjacent swaps");
        auto copy = a;
        verify(longestNonnegPrefix(copy) == nonnegative, "C62 longest feasible subsequence");
        if (!a.empty()) for (int mask = 0; mask < (1 << (a.size()-1)); ++mask) {
            auto sortedChunks = a;
            int left = 0, count = 0;
            for (int right = 0; right < (int)a.size(); ++right)
                if (right+1 == (int)a.size() || (mask >> right & 1)) {
                    sort(sortedChunks.begin()+left, sortedChunks.begin()+right+1);
                    left=right+1; ++count;
                }
            if (is_sorted(sortedChunks.begin(), sortedChunks.end())) chunks=max(chunks,count);
        }
        verify(maxParts(a) == chunks, "C28 freely chosen sorting chunks");
        auto lis = longestIncreasingSubsequence(a);
        verify((int)lis.size() == bruteLIS(a), "C2/C5 LIS length");
        int cursor = 0;
        for (int x : a) if (cursor < (int)lis.size() && x == lis[cursor]) ++cursor;
        verify(cursor == (int)lis.size() && adjacent_find(lis.begin(), lis.end(), greater_equal<int>()) == lis.end(), "C5 actual strict path");
        auto selected = shorterGreaterSubset(wide);
        bool any = false;
        for (int mask = 1; mask < (1 << a.size()); ++mask) {
            int count = __builtin_popcount((unsigned)mask);
            if (2 * count >= (int)a.size()) continue;
            long long sum = 0;
            for (int i = 0; i < (int)a.size(); ++i) if (mask >> i & 1) sum += a[i];
            if (sum > accumulate(a.begin(), a.end(), 0LL) - sum) any = true;
        }
        verify(!selected.empty() == any, "C17 arbitrary partition existence");
        if (!selected.empty()) {
            long long sum = 0;
            for (int i : selected) sum += a[i];
            verify(2 * selected.size() < a.size() && sum > accumulate(a.begin(), a.end(), 0LL) - sum, "C17 returned partition");
        }
        for (int target = -4; target <= 4; ++target) {
            bool reachable = false;
            for (int mask = 0; mask < (1 << a.size()); ++mask) {
                long long sum = 0;
                for (int i = 0; i < (int)a.size(); ++i) if (mask >> i & 1) sum += a[i];
                reachable |= sum == target;
            }
            verify(canReachIntegers(a, target) == reachable, "C25 signed subset sum");
        }
        for (int k = -3; k <= 3; ++k) {
            set<pair<int, int>> values;
            long long indices = 0;
            for (int x : a) for (int y : a) if (y - x == k) values.insert({x, y});
            for (int i = 0; i < (int)a.size(); ++i) for (int j = i + 1; j < (int)a.size(); ++j)
                if (abs(a[i] - a[j]) == abs(k)) ++indices;
            verify(countValuePairs(a, k) == (long long)values.size(), "C51 distinct values");
            verify(countIndexPairs(a, k) == indices, "C51 index-pair alternative");
        }
        if (!a.empty()) for (int k = 1; k <= (int)a.size(); ++k) {
            auto medians = slidingMedian(a, k);
            for (int i = 0; i + k <= (int)a.size(); ++i) {
                vector<int> window(a.begin() + i, a.begin() + i + k);
                sort(window.begin(), window.end());
                double expected = ((double)window[(k - 1) / 2] + window[k / 2]) / 2;
                verify(medians[i] == expected, "C40 sliding median");
            }
        }
    });
    verify(freqSort({3,5,2,2,4}) == vector<int>({2,2,3,4,5}), "C71 PDF example");
    verify(freqSort({3,5,2,2,4}, false) == vector<int>({3,4,5,2,2}), "C71 ascending alternative");
    verify(countValuePairs({1}, 0, false) == 0 && countValuePairs({1,1}, 0, false) == 1, "C51 disallow self");
    verify(countValuePairs({INT_MIN,INT_MAX}, 1) == 0, "C51 key overflow");
    arrays(3, 0, 5, [&](const vector<int>& a) {
        if (a.empty()) return;
        vector<long long> wide(a.begin(), a.end());
        for (int k = 0; k <= 4; ++k) for (bool up : {false, true})
            verify(minSumAfterOps(wide, k, up) == bruteHalving(wide, k, up), "C13 conditional halving");
    });
    arrays(6, 1, 4, [&](const vector<int>& a) {
        verify(minDaysMinutesExact(a, 5) == bruteMovieDays(a, 5), "C29 exact bin packing");
    });
    verify(minDaysMinutesExact({60,60,60,60,60}) == 2, "C29 arbitrary movie count");
    verify(minDaysMinutesExact({181}) == -1, "C29 infeasible film");
    for (int n = 1; n <= 3; ++n) {
        arrays(n, 0, 2, [&](const vector<int>& allA) {
            if ((int)allA.size() != n) return;
            arrays(n, 0, 2, [&](const vector<int>& allB) {
                if ((int)allB.size() != n) return;
                using State = pair<vector<int>, vector<int>>;
                set<State> states{{allA, allB}};
                for (int k = 0; k <= 4; ++k) {
                    int best = 0;
                    for (const auto& [a,b] : states) best = max(best, (int)set<int>(a.begin(), a.end()).size());
                    verify(maxDistinctAfterK(allA, allB, k) == best, "C19 exact k swaps");
                    set<State> next;
                    for (auto [a,b] : states) for (int i = 0; i < n; ++i) for (int j = 0; j < n; ++j) {
                        swap(a[i], b[j]); next.insert({a,b}); swap(a[i], b[j]);
                    }
                    states = std::move(next);
                }
            });
        });
    }
    for (int n = 0; n <= 9; ++n) for (int mask = 0; mask < (1 << n); ++mask) {
        string slots(n, '.');
        for (int i = 0; i < n; ++i) if (mask >> i & 1) slots[i] = '#';
        for (bool aligned : {false,true}) verify(minFiles(slots, aligned) == bruteFiles(slots,0,aligned), "C30 aligned/unaligned blocks");
    }
    arrays(6, 0, 3, [&](const vector<int>& a) {
        if (a.empty()) return;
        for (bool global : {false,true}) {
            auto [score, path] = frogWaitPath(a, global);
            long long optimum = LLONG_MAX;
            for (int mask = 0; mask < (1 << a.size()); ++mask) {
                if (!(mask & 1) || !(mask >> (a.size()-1) & 1)) continue;
                int last = -1, omitted = 0;
                bool valid = true;
                long long total = 0;
                for (int i = 0; i < (int)a.size(); ++i) {
                    if (!(mask >> i & 1)) { ++omitted; continue; }
                    if (last != -1 && i-last > 2) valid = false;
                    last=i; total += a[i];
                }
                if (valid && (!global || omitted <= 1)) optimum = min(optimum, total);
            }
            long long total = 0;
            for (int i : path) total += a[i];
            verify(score == optimum && total == score && path.front() == 0 && path.back() == (int)a.size()-1, "C64 optimal waiting and path");
        }
    });
    arrays(5,-2,2,[&](const vector<int>& a) {
        if (a.empty()) return;
        long long best=LLONG_MIN;
        // At these sizes only prime step 3 is present; enumerate subsets of landings.
        for (int mask=1; mask<(1<<a.size()); ++mask) {
            if (!(mask>>(a.size()-1)&1)) continue;
            int last=-1; long long total=0; bool valid=true;
            for (int i=0;i<(int)a.size();++i) if(mask>>i&1) {
                if(i-last!=1 && i-last!=3) valid=false;
                total+=a[i]; last=i;
            }
            if(valid) best=max(best,total);
        }
        auto [score,path]=maxScorePath(a);
        long long total=0; int last=-1;
        for(int i:path) { verify(i-last==1||i-last==3,"C46 legal step"); total+=a[i]; last=i; }
        verify(score==best&&total==score&&last==(int)a.size()-1,"C46 best score and reconstructed path");
    });
    verify(maxScorePath({20,10,-30,40}).second == vector<int>({0,3}), "C46 source example path");
    for (int a=1;a<=4;++a) for(int b=a;b<=4;++b) for(int c=b;c<=4;++c) for(int d=c;d<=4;++d) {
        vector<long long> all{a+b,a+c,a+d,b+c,b+d,c+d};
        for(int omitted=0;omitted<6;++omitted) {
            auto known=all; known.erase(known.begin()+omitted);
            set<array<long long,4>> brute;
            int limit=*max_element(known.begin(),known.end());
            for(int w=1;w<limit;++w) for(int x=w;x<limit;++x)
                for(int y=x;y<limit;++y) for(int z=y;z<limit;++z) {
                    multiset<long long> candidate{w+x,w+y,w+z,x+y,x+z,y+z};
                    bool ok=true;
                    for(auto sum:known) { auto it=candidate.find(sum); if(it==candidate.end()){ok=false;break;} candidate.erase(it); }
                    if(ok) brute.insert({w,x,y,z});
                }
            verify(recoverFour(known)==brute,"B8 all missing-edge positions and multiplicity");
        }
    }
    for(int n=0;n<=4;++n) {
        vector<pair<int,int>> edges;
        for(int u=0;u<n;++u) for(int v=0;v<n;++v) if(u!=v) edges.push_back({u,v});
        for(int mask=0;mask<(1<<edges.size());++mask) {
            vector<vector<int>> graph(n), reach(n,vector<int>(n));
            for(int i=0;i<n;++i) reach[i][i]=1;
            for(int e=0;e<(int)edges.size();++e) if(mask>>e&1) {
                auto [u,v]=edges[e];graph[u].push_back(v);reach[u][v]=1;
            }
            for(int k=0;k<n;++k) for(int i=0;i<n;++i) for(int j=0;j<n;++j) reach[i][j]|=reach[i][k]&&reach[k][j];
            auto ids=stronglyConnectedComponents(graph);
            for(int i=0;i<n;++i) for(int j=0;j<n;++j)
                verify((ids[i]==ids[j]) == (reach[i][j]&&reach[j][i]),"A20 SCC versus transitive closure");
        }
    }
    TreeNode n1(1),n2(2),n3(3),n4(4); n1.left=&n2;n1.right=&n3;n2.right=&n4;
    vector<int> pre,in,post;traversalsRecursive(&n1,pre,in,post);
    verify(pre==vector<int>({1,2,4,3})&&in==vector<int>({2,4,1,3})&&post==vector<int>({4,2,3,1}),"A13 recursive three traversals");
    verify(postorderIterative(&n1)==post,"A13 iterative postorder");
    verify(levelOrderIterative(&n1)==vector<vector<int>>({{1},{2,3},{4}}),"A13 queue levels");
    verify(levelOrderRecursive(&n1)==levelOrderIterative(&n1),"A13 recursive depth grouping");
    verify(postorderIterative(nullptr).empty()&&levelOrderRecursive(nullptr).empty(),"A13 empty tree");
    verify(hasCycleUndirected(2,{{0,1},{0,1}}),"A17 parallel edges");
    verify(hasCycleUndirected(1,{{0,0}}),"A17 self loop");
    verify(!hasCycleUndirected(4,{{0,1},{1,2},{2,3}}),"A17 acyclic chain");
    verify(hasCycleUndirected(4,{{0,1},{1,2},{1,2},{2,3}}),"A17 parallel edges below root");
    RunningMedian median;median.add(INT_MAX);median.add(INT_MAX);
    verify(median.median()==(double)INT_MAX,"C66 integer addition overflow");
    verify(slidingMedian({},0).empty()&&slidingMedian({1},2).empty(),"C40 invalid windows");
    vector<pair<long long,long long>> intervals{{LLONG_MIN,LLONG_MAX},{2,3}};
    verify(intervalCoverage(intervals,vector<long long>{LLONG_MIN,2,3,LLONG_MAX})==vector<int>({1,2,2,1}),"C70 closed extreme endpoints");
    verify(signalsInAll(intervals,vector<long long>{1,2,3,4})==2,"C65 all filters");
    verify(signalsInAll(vector<pair<int,int>>{},vector<int>{1,2})==2,"C65 empty filters");
    verify(intervalCoverage(vector<pair<double,double>>{{0.5,1.5},{1.5,2.5}},vector<double>{0.5,1.5,2.5})==vector<int>({1,2,1}),"C70 real endpoints");
    verify(firstNNonPrimes(6)==vector<int>({1,4,6,8,9,10}),"C39 nonprime includes 1");
    verify(firstNNonPrimes(6,false)==vector<int>({4,6,8,9,10,12}),"C39 composite alternative");
    verify(fibonacci(0)==0&&fibonacci(10)==55&&fibonacci(93)==12200160415121876738ULL,"C4 Fibonacci range");
    for (long long high=0;high<=150;++high) for(long long low=0;low<=high;low+=7) {
        map<int,long long> counts;
        for(long long value=low;value<=high;++value) {
            int sum=0;long long x=value;
            do {sum+=x%10;x/=10;} while(x);
            ++counts[sum];
        }
        long long smallest=LLONG_MAX,largest=0;
        for(auto [sum,count]:counts){smallest=min(smallest,count);largest=max(largest,count);}
        verify(couponStats(low,high)==make_tuple((long long)counts.size(),smallest,largest),"C69 digit DP versus coupon enumeration");
    }
    mt19937 rng(12);
    for(int trial=0;trial<160;++trial) {
        int n=1+rng()%6;
        vector<long long> prices(n);vector<int> categories(n),order(n);
        for(int i=0;i<n;++i){prices[i]=rng()%7;categories[i]=rng()%3;order[i]=i;}
        long long best=LLONG_MIN;
        do {
            set<int> sold;long long score=0;
            for(int i:order){sold.insert(categories[i]);score+=prices[i]*sold.size();}
            best=max(best,score);
        } while(next_permutation(order.begin(),order.end()));
        verify(maxCategoryProfit(prices,categories)==best,"C74 category profit versus every ordering");
    }
    cout << "C++ source-extracted exhaustive checks: " << checks << '\n';
}
'''


def check_cpp():
    requested = [(13, "recoverFour("), (31, "longestIncreasingSubsequence("),
                 (32, "unsigned long long fibonacci("), (32, "minDaysMinutesExact("),
                 (32, "minSumAfterOps("), (32, "maxDistinctAfterK("),
                 (32, "shorterGreaterSubset("), (32, "canReachIntegers("),
                 (32, "long long maxWeightedSum("), (32, "int maxParts("),
                 (34, "maxPositiveDiff("), (34, "countValuePairs("), (34, "freqSort("),
                 (34, "int longestNonnegPrefix("),
                 (35, "firstNNonPrimes("), (35, "maxScorePath("), (35, "frogWaitPath("),
                 (35, "long long maxCategoryProfit("), (36, "couponStats("),
                 (35, "vector<int> intervalCoverage("), (36, "class RunningMedian"),
                 (36, "vector<double> slidingMedian("), (36, "long long minFiles("),
                 (3, "void traversalsRecursive("), (6, "stronglyConnectedComponents("),
                 (6, "bool hasCycleUndirected(")]
    snippets = [block(chapter, symbol) for chapter, symbol in requested]
    assert len(snippets) == len(set(snippets))
    headers = """#include <algorithm>
#include <array>
#include <cassert>
#include <climits>
#include <cmath>
#include <functional>
#include <iostream>
#include <limits>
#include <map>
#include <numeric>
#include <queue>
#include <random>
#include <set>
#include <stack>
#include <stdexcept>
#include <string>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>
using namespace std;
struct TreeNode { int val; TreeNode *left=nullptr, *right=nullptr; explicit TreeNode(int x):val(x){} };
"""
    compiler = shutil.which("clang++") or shutil.which("g++")
    assert compiler, "C++17 compiler required"
    with tempfile.TemporaryDirectory(prefix="quant-general-practice-") as directory:
        source, executable = Path(directory) / "check.cpp", Path(directory) / "check"
        source.write_text(headers + "\n".join(snippets) + CPP_TESTS)
        subprocess.run([compiler, "-std=c++17", "-O1", "-fsanitize=undefined",
                        "-fno-sanitize-recover=undefined", str(source), "-o", str(executable)], check=True)
        subprocess.run([str(executable)], check=True, timeout=120)
    return len(snippets)


def check_python_and_math():
    # Check the prose's worked numbers too, rather than only the implementation.
    paragraph = next(p.get_text(" ", strip=True) for p in load(32).select("#q-032-10 p")
                     if "手算" in p.get_text() and "原加权和" in p.get_text())
    values = json.loads(re.search(r"手算\s*\\\((\[[^\]]+\])\\\)", paragraph)[1])
    claimed = re.search(r"原加权和\s*\\\((\d+)\\\)，优化后\s*\\\((\d+)\\\)", paragraph)
    base = sum((i + 1) * x for i, x in enumerate(values))
    best = base
    for mask in range(1 << (len(values) - 1)):
        if mask & (mask << 1):
            continue
        swapped = list(values)
        for i in range(len(values) - 1):
            if mask >> i & 1:
                swapped[i], swapped[i + 1] = swapped[i + 1], swapped[i]
        best = max(best, sum((i + 1) * x for i, x in enumerate(swapped)))
    assert (int(claimed[1]), int(claimed[2])) == (base, best)
    namespace = {}
    exec(block(35, "def sqrt_digits("), namespace)
    root = namespace["sqrt_digits"]
    assert [root(3, p) for p in range(3)] == ["1", "1.7", "1.73"]
    for numerator in range(501):
        value = Decimal(numerator) / 100
        fraction = F(value)
        for precision in range(6):
            result = Decimal(root(str(value), precision))
            scale = 10 ** precision
            integer = int(result * scale)
            assert integer**2 * fraction.denominator <= fraction.numerator * scale**2
            assert (integer + 1)**2 * fraction.denominator > fraction.numerator * scale**2
    for value in ["0", "2.25", "1e-40", "1e40"]:
        assert len(root(value, 100).split(".")[1]) == 100
    for value in ["-1", "NaN", "Infinity"]:
        try:
            root(value, 2)
        except ValueError:
            pass
        else:
            raise AssertionError(value)
    exec(block(40, "def draw_correlated_pair("), namespace)
    rng = namespace["random"].Random(123)
    for rho in [-1, -0.5, 0, 0.5, 1]:
        pairs = [namespace["draw_correlated_pair"](rho, rng) for _ in range(25000)]
        mx = sum(x for x, _ in pairs) / len(pairs)
        my = sum(y for _, y in pairs) / len(pairs)
        vx = sum((x - mx)**2 for x, _ in pairs) / len(pairs)
        vy = sum((y - my)**2 for _, y in pairs) / len(pairs)
        covariance = sum((x - mx) * (y - my) for x, y in pairs) / len(pairs)
        assert abs(vx - 1) < 0.04 and abs(vy - 1) < 0.04
        assert abs(covariance / sqrt(vx * vy) - rho) < 0.025
    # P18: simulate actual next adjacent collision, independently of record maxima.
    for n in range(1, 7):
        survivors = 0
        for ordering in permutations(range(1, n + 1)):
            positions, speeds = list(map(F, range(n))), list(ordering)
            while True:
                events = [(F(positions[i+1] - positions[i], speeds[i] - speeds[i+1]), i)
                          for i in range(len(speeds)-1) if speeds[i] > speeds[i+1]]
                if not events:
                    break
                time, i = min(events)
                positions = [x + v * time for x, v in zip(positions, speeds)]
                del positions[i+1]
                del speeds[i+1]
            survivors += len(speeds)
        from math import factorial
        assert F(survivors, factorial(n)) == sum((F(1, k) for k in range(1, n+1)), F())
    # P84: enumerate latent value/report/action states, retaining the right baseline.
    baseline = F(2)
    for short, expected in [(False, F(7, 2)), (True, F(7))]:
        utility = F()
        for report in [False, True]:
            probability = F()
            cashflow = F()
            for price in [12, 24, 60]:
                weight = F(1, 3) * (F(3, 4) if (price == 60) == report else F(1, 4))
                probability += weight
                cashflow += weight * (price - 30)
            utility += max(F(), cashflow, -cashflow if short else F())
        assert utility - baseline == expected
    # GT1: check every supported action has the same win probability.
    low, high = 0.0, 1.0
    for _ in range(100):
        r = (low + high) / 2
        if r**3 + r*r + r < 1:
            low = r
        else:
            high = r
    r = (low + high) / 2
    for k in range(1, 40):
        win = r**(2*k) + sum(((1-r)*r**(j-1))**2 for j in range(1,k))
        assert isclose(win, r*r, abs_tol=1e-12)
    assert isclose(float((F(3,2)-1)/(F(3,2)**10-1)), 0.00882378285221887)
    assert 2 * F(sum(comb(100,k) for k in range(60,101)),2**100) > F(5,100)
    assert F(119,24)-F(89,18) == F(1,72)
    return {"sqrt_decimal_cases": 3006, "normal_pair_samples": 125000, "collision_permutations": 873}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-pdf", type=Path)
    args = parser.parse_args()
    coverage = check_coverage(args.source_pdf)
    print(json.dumps({"coverage": coverage}, ensure_ascii=False), flush=True)
    count = check_cpp()
    numeric = check_python_and_math()
    print(json.dumps({"cpp_html_blocks": count, "numeric": numeric, "result": "passed"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
