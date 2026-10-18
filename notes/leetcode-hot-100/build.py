"""Hot 100 教材的数据与可复现 HTML 构建。仅使用 Python 标准库。"""
from pathlib import Path
from html import escape
from textwrap import dedent

BANK = []
GROUPS = {}

def group(key, title, lesson):
    GROUPS[key] = (title, lesson)

def q(n, title, slug, kind, task, idea, steps, pitfall, cost, code, example):
    BANK.append(dict(id=n, title=title, slug=slug, kind=kind, task=task,
        idea=idea, steps=steps.split('；'), pitfall=pitfall, cost=cost,
        code=dedent(code).strip(), example=example))

group('hash', '01 · 哈希：把搜索换成查询', '先问“我重复搜索的是什么？”两数之和存补数，异位词存规范表示，连续序列存成员关系。字典/集合的查询平均 O(1)，最坏情形取决于散列；遍历时明确表里是当前项之前的数据，还是完整数据。')
q(1,'两数之和','two-sum','hash','返回数组中两个不同下标，使对应数之和等于 target。题目保证恰有一解。','固定当前数 x 后，唯一需要寻找的是 target-x；用字典保存此前数值到下标。','从左到右枚举 i,x；先查询 target-x，存在就返回两个下标；查询后才存 x，确保不会用同一个元素两次','[3,3], target=6 需要两个不同位置；先存后查会错误地匹配自己。','时间 O(n)，额外空间 O(n)。','''
def twoSum(nums, target):
    seen = {}
    for i, x in enumerate(nums):
        if target - x in seen:
            return [seen[target - x], i]
        seen[x] = i
''','[2,7,11,15], target=9 → [0,1]；读到 7 时，字典已有 2。')
q(49,'字母异位词分组','group-anagrams','hash','把只因字母排列不同的字符串放在同一组，组的顺序不限。','把字符串排序成同一个规范键；相同键对应相同的字母多重集合。','为每个单词建立排序后字符串键；把原单词加入该键的列表；最后取所有组','不能用字符集合做键，因为 ab 与 aab 的重复次数不同；空串也必须保留。','总字符数 L、最长词长 k：时间 O(L log k)，空间 O(L)。','''
def groupAnagrams(strs):
    groups = {}
    for s in strs:
        key = ''.join(sorted(s))
        groups.setdefault(key, []).append(s)
    return list(groups.values())
''','["eat","tea","tan","ate"] → [["eat","tea","ate"],["tan"]]。')
q(128,'最长连续序列','longest-consecutive-sequence','hash','无序整数数组中，求数值连续序列的最长长度，不要求原数组相邻。','只有没有前驱 x-1 的数才是序列起点；从起点扩张，每个唯一元素只被向后扫描一次。','去重成集合；枚举集合中的 x，若 x-1 存在则跳过；否则从 x 不断找 x+1 并更新长度','必须遍历去重集合；若遍历带大量重复起点的原数组，可能退化为 O(n²)。','平均时间 O(n)，空间 O(n)。','''
def longestConsecutive(nums):
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 not in values:
            y = x
            while y in values:
                y += 1
            best = max(best, y - x)
    return best
''','[100,4,200,1,3,2] → 4；只从 1 开始扫描 1,2,3,4。')

group('pointers','02 · 双指针：利用顺序排除候选','相向指针依赖一个能证明的排除规则，而不是“两个指针看起来快”。同向指针维护已处理区间。排序常把三数问题降为两数问题；但排序会改变原下标，不能无条件用于返回下标的题。')
q(283,'移动零','move-zeroes','pointers','原地把 0 移到末尾，非零元素相对顺序不变。','写指针 w 之前恰好是已经扫描到的全部非零元素。','扫描每个 x，非零就写到 nums[w] 并推进 w；扫描后把 [w,n) 填 0','不要边遍历边删除；本实现逐元素赋值，额外空间 O(1)。','时间 O(n)，额外空间 O(1)。','''
def moveZeroes(nums):
    w = 0
    for x in nums:
        if x != 0:
            nums[w] = x
            w += 1
    for i in range(w, len(nums)):
        nums[i] = 0
''','[0,1,0,3,12] → 原数组变成 [1,3,12,0,0]。')
q(11,'盛最多水的容器','container-with-most-water','pointers','选两条竖线，与横轴组成容器，求最大容量；中间的线不影响容量。','面积由较短边和距离决定。固定短边、缩短距离不可能变好，所以舍弃短边是安全的。','左右端初始化；计算 min(height[l],height[r])*(r-l)；移动较短的一端并重复','不能移动高边来赌更优解；盛水容器与接雨水的目标不同。','时间 O(n)，空间 O(1)。','''
def maxArea(height):
    l, r, best = 0, len(height) - 1, 0
    while l < r:
        best = max(best, min(height[l], height[r]) * (r - l))
        if height[l] <= height[r]:
            l += 1
        else:
            r -= 1
    return best
''','[1,8,6,2,5,4,8,3,7] → 49，由下标 1 和 8 的线组成。')
q(15,'三数之和','3sum','pointers','返回和为 0 的不重复三元组，三元组内部顺序不限。','排序后固定第一个数，剩余两数和可用相向指针，数值过小左移大、过大右移小。','排序并枚举 i，跳过重复首数；在 i+1 到末尾双指针求 -nums[i]；命中时记录并越过两端重复值','去重按数值，不是按下标；同一三元组中的两个 0 仍可以来自不同位置。','时间 O(n²)，排序空间 O(n)（Python 排序最坏），结果另计。','''
def threeSum(nums):
    nums = sorted(nums)
    ans = []
    for i in range(len(nums) - 2):
        if i and nums[i] == nums[i - 1]:
            continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            total = nums[i] + nums[l] + nums[r]
            if total < 0:
                l += 1
            elif total > 0:
                r -= 1
            else:
                ans.append([nums[i], nums[l], nums[r]])
                a, b = nums[l], nums[r]
                while l < r and nums[l] == a:
                    l += 1
                while l < r and nums[r] == b:
                    r -= 1
    return ans
''','[-1,0,1,2,-1,-4] → [[-1,-1,2],[-1,0,1]]。')
q(42,'接雨水','trapping-rain-water','pointers','每根柱宽为 1，下雨后所有凹槽共能积多少水。','某位置水量是两侧最高墙较小者减自身高度；维护两端已见最高墙，较小的最高墙一侧可以立刻结算。','初始化左右指针和最高墙；更新左右最高墙；较小墙那侧累加墙高减柱高，并向内推进','当前柱高度与历史最高墙不是一个变量；高度差应在更新最高墙后计算，不产生负水量。','时间 O(n)，空间 O(1)。','''
def trap(height):
    l, r = 0, len(height) - 1
    left = right = ans = 0
    while l <= r:
        left = max(left, height[l])
        right = max(right, height[r])
        if left <= right:
            ans += left - height[l]
            l += 1
        else:
            ans += right - height[r]
            r -= 1
    return ans
''','[4,2,0,3,2,5] → 9；各内部位置水量为 2,4,1,2。')

group('window','03 · 窗口、前缀和与单调队列','窗口用于连续区间，但能否收缩取决于可维护的条件。含负数的和不单调，不能照搬正数窗口；改用前缀和差。固定窗维护增删，覆盖窗在满足条件后尽量缩短，极值窗删除永远不可能再最优的候选。')
q(3,'无重复字符的最长子串','longest-substring-without-repeating-characters','window','求字符串中不含重复字符的最长连续子串长度。','窗口 [left,right] 始终无重复；新字符重复时把 left 跳到其上次位置后一位。','记录每字符最后下标；令 left=max(left,last[c]+1)；更新长度和 last[c]','left 不能倒退：abba 读到最后的 a，不能把 left 从 2 改成 1。','时间 O(n)，空间 O(min(n,字符集大小))。','''
def lengthOfLongestSubstring(s):
    last = {}
    left = best = 0
    for right, c in enumerate(s):
        left = max(left, last.get(c, -1) + 1)
        last[c] = right
        best = max(best, right - left + 1)
    return best
''','"abba" → 2；窗口先 ab，再 ba。')
q(438,'找到字符串中所有字母异位词','find-all-anagrams-in-a-string','window','在小写字母字符串 s 中，返回所有长度为 len(p)、且字符计数等于 p 的窗口起点。','固定窗口长度后，只需维护 26 个计数，无需每个窗口重新排序。','建立目标计数；右端加入新字符，窗口过长时删左侧字符；窗口足长且计数相等时记录起点','右端为 i 时起点 i-m+1；当 s 比 p 短时不记录。','时间 O(26n)=O(n)，空间 O(26)。','''
def findAnagrams(s, p):
    need, window = [0] * 26, [0] * 26
    m = len(p)
    for c in p:
        need[ord(c) - 97] += 1
    ans = []
    for i, c in enumerate(s):
        window[ord(c) - 97] += 1
        if i >= m:
            window[ord(s[i - m]) - 97] -= 1
        if i >= m - 1 and window == need:
            ans.append(i - m + 1)
    return ans
''','s="cbaebabacd", p="abc" → [0,6]。')
q(560,'和为 K 的子数组','subarray-sum-equals-k','window','整数数组中，统计和为 k 的非空连续子数组数量；允许负数。','若当前前缀和为 total，要找的旧前缀和就是 total-k；存出现次数而非单一位置。','设空前缀和 0 出现 1 次；每读一个数更新 total；先累加 freq[total-k]，再记录 total','先记录当前前缀会在 k=0 时计入空子数组；负数使普通滑动窗口失效。','平均时间 O(n)，空间 O(n)。','''
def subarraySum(nums, k):
    freq = {0: 1}
    total = ans = 0
    for x in nums:
        total += x
        ans += freq.get(total - k, 0)
        freq[total] = freq.get(total, 0) + 1
    return ans
''','[1,1,1], k=2 → 2；两个位置不同的 [1,1]。')
q(239,'滑动窗口最大值','sliding-window-maximum','window','返回每个长度为 k 的连续窗口的最大值。','双端队列存下标，数值从队首到队尾递减；新数更大时，旧的小数更早过期且永远不会再是最大值。','先删除过期队首；弹出小于等于新值的队尾；压入当前下标，窗口成形后读队首','必须存下标才能判断过期；每个下标最多入队出队各一次，嵌套 while 仍为线性。','时间 O(n)，空间 O(k)。','''
def maxSlidingWindow(nums, k):
    from collections import deque
    candidates, ans = deque(), []
    for i, x in enumerate(nums):
        while candidates and candidates[0] <= i - k:
            candidates.popleft()
        while candidates and nums[candidates[-1]] <= x:
            candidates.pop()
        candidates.append(i)
        if i >= k - 1:
            ans.append(nums[candidates[0]])
    return ans
''','[1,3,-1,-3,5,3,6,7], k=3 → [3,3,5,5,6,7]。')
q(76,'最小覆盖子串','minimum-window-substring','window','在 s 中找包含 t 全部字符及其重复次数的最短子串，不存在返回空串。','need 保存尚缺数量，missing 保存尚缺的字符总数；右端扩张到覆盖后，左端尽可能收缩。','右端加入字符，若尚缺则 missing 减一；当 missing=0 时记录当前窗口；移出左字符，若使某字符重新短缺则停止收缩','t="AA" 需要两个 A；覆盖种类数与覆盖字符总数不是一回事。','时间 O(len(s)+len(t))，空间 O(字符集大小)。','''
def minWindow(s, t):
    from collections import Counter
    if not t:
        return ''
    need = Counter(t)
    missing, left = len(t), 0
    start, best = 0, len(s) + 1
    for right, c in enumerate(s):
        if need[c] > 0:
            missing -= 1
        need[c] -= 1
        while missing == 0:
            if right - left + 1 < best:
                start, best = left, right - left + 1
            old = s[left]
            need[old] += 1
            if need[old] > 0:
                missing += 1
            left += 1
    return '' if best > len(s) else s[start:start + best]
''','s="ADOBECODEBANC", t="ABC" → "BANC"。')

group('array','04 · 数组与矩阵：状态、原地标记、几何变换','数组题先区分是否必须原地、能否排序、输出是否包含自身。前后缀可把“排除自身”分成两部分。原地哈希把值 x 放到下标 x-1；矩阵题用边界或坐标变换，不能把行列写反。')
q(53,'最大子数组和','maximum-subarray','array','非空整数数组中，求非空连续子数组的最大和。','end 表示必须以当前位置结尾的最优和；前面的 end 为负时，接上它只会更差。','首元素初始化 end 和 best；对新 x 取 end=max(x,end+x)；用 end 更新全局 best','不能把 best 初始化为 0，否则全负数组会错误地选择空子数组。','时间 O(n)，空间 O(1)。','''
def maxSubArray(nums):
    end = best = nums[0]
    for i in range(1, len(nums)):
        x = nums[i]
        end = max(x, end + x)
        best = max(best, end)
    return best
''','[-2,1,-3,4,-1,2,1,-5,4] → 6，对应 [4,-1,2,1]。')
q(56,'合并区间','merge-intervals','array','把所有有交集的闭区间合并，返回互不重叠的区间。','按左端点排序，当前区间只可能与最后一个已合并区间相交。','按起点排序；若新起点大于末区间终点则另开一段；否则更新末区间终点为两者较大值','[1,4] 与 [4,5] 在闭区间语义下应合并；更新终点要取 max，不能直接覆盖。','时间 O(n log n)，空间 O(n) 含结果和排序。','''
def merge(intervals):
    ans = []
    for a, b in sorted(intervals):
        if not ans or a > ans[-1][1]:
            ans.append([a, b])
        else:
            ans[-1][1] = max(ans[-1][1], b)
    return ans
''','[[1,3],[2,6],[8,10]] → [[1,6],[8,10]]。')
q(189,'轮转数组','rotate-array','array','原地把数组向右移动 k 位。','整体反转会交换两段的位置，再分别反转两段恢复各自顺序。','令 k 对 n 取模；反转整个数组；反转前 k 个和剩余 n-k 个元素','右移与左移方向不同；空数组先返回，避免模 0。','时间 O(n)，额外空间 O(1)。','''
def rotate(nums, k):
    if not nums:
        return
    def reverse(l, r):
        while l < r:
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1
    k %= len(nums)
    reverse(0, len(nums) - 1)
    reverse(0, k - 1)
    reverse(k, len(nums) - 1)
''','[1,2,3,4,5,6,7], k=3 → [5,6,7,1,2,3,4]。')
q(238,'除了自身以外数组的乘积','product-of-array-except-self','array','不用除法，返回每个位置之外所有元素的乘积。','答案等于左侧全部乘积乘右侧全部乘积；输出数组先存左积，再用一个变量乘入右积。','左到右把前缀积写入 ans[i]；右到左维护 suffix；令 ans[i] 乘 suffix 后再把 nums[i] 乘入 suffix','不能先乘自身；有一个或多个 0 的输入也应自然处理，无需除法特判。','时间 O(n)，除输出外空间 O(1)。','''
def productExceptSelf(nums):
    ans, prefix = [], 1
    for x in nums:
        ans.append(prefix)
        prefix *= x
    suffix = 1
    for i in range(len(nums) - 1, -1, -1):
        ans[i] *= suffix
        suffix *= nums[i]
    return ans
''','[1,2,3,4] → [24,12,8,6]；[0,2,3] → [6,0,0]。')
q(41,'缺失的第一个正数','first-missing-positive','array','在 O(n) 时间、O(1) 额外空间内找未出现的最小正整数。','长度 n 的数组答案只可能在 1..n+1；将值 x 放到槽位 x-1，数组自己充当哈希表。','扫描 i，只要 nums[i] 在 1..n 且目标槽不是相同值就交换；交换后继续检查当前位置；最后找首个 nums[i]≠i+1 的位置','重复数字必须检测目标槽已相等，否则无限交换；0 和负数无需归位。','时间 O(n)，额外空间 O(1)。','''
def firstMissingPositive(nums):
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]
    for i, x in enumerate(nums):
        if x != i + 1:
            return i + 1
    return n + 1
''','[3,4,-1,1] 归位后 [1,-1,3,4] → 2。')
q(73,'矩阵置零','set-matrix-zeroes','array','若某元素为 0，将其整行整列原地置 0。','第一行和第一列作标记，另用两个布尔值记下它们原本是否含 0。','先记录首行首列原始状态；扫描内部，把需要清零的行列写入首列首行；根据标记清内部，最后处理首行首列','边发现 0 边清整行会把新写的 0 当作原始 0 扩散；标记阶段与修改阶段分开。','时间 O(mn)，额外空间 O(1)。','''
def setZeroes(matrix):
    m, n = len(matrix), len(matrix[0])
    row0 = any(x == 0 for x in matrix[0])
    col0 = any(matrix[i][0] == 0 for i in range(m))
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][j] == 0:
                matrix[i][0] = matrix[0][j] = 0
    for i in range(1, m):
        for j in range(1, n):
            if matrix[i][0] == 0 or matrix[0][j] == 0:
                matrix[i][j] = 0
    if row0:
        for j in range(n):
            matrix[0][j] = 0
    if col0:
        for i in range(m):
            matrix[i][0] = 0
''','[[1,1,1],[1,0,1],[1,1,1]] → [[1,0,1],[0,0,0],[1,0,1]]。')
q(54,'螺旋矩阵','spiral-matrix','array','按顺时针由外向内输出矩阵元素。','维护尚未访问的上、下、左、右四条边，每走完一条就收缩对应边界。','依次走上边、右边；确认仍有行后走下边；确认仍有列后走左边，再循环','单行或单列时，后两条边必须检查边界，避免重复访问。','时间 O(mn)，除输出空间 O(1)。','''
def spiralOrder(matrix):
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    ans = []
    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            ans.append(matrix[top][j])
        top += 1
        for i in range(top, bottom + 1):
            ans.append(matrix[i][right])
        right -= 1
        if top <= bottom:
            for j in range(right, left - 1, -1):
                ans.append(matrix[bottom][j])
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1):
                ans.append(matrix[i][left])
            left += 1
    return ans
''','[[1,2,3],[4,5,6],[7,8,9]] → [1,2,3,6,9,8,7,4,5]。')
q(48,'旋转图像','rotate-image','array','将 n×n 矩阵顺时针旋转 90°，要求原地修改。','顺时针坐标变换 (i,j)→(j,n-1-i)，可分解为主对角线转置后逐行反转。','只交换主对角线上方元素与其对称点；逐行原地 reverse','不要把矩阵行列都遍历后交换，那会交换两次回到原状；本题必须是方阵。','时间 O(n²)，额外空间 O(1)。','''
def rotateImage(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()
''','[[1,2],[3,4]] → [[3,1],[4,2]]。')
q(240,'搜索二维矩阵 II','search-a-2d-matrix-ii','array','每行从左到右、每列从上到下递增，判断 target 是否存在。','右上角同时具有本行最大、本列最小的性质，一次比较可以排除一整行或一整列。','从右上角开始；当前值大于目标则左移；当前值小于目标则下移','不能把整个矩阵直接展平成有序数组；题目没有保证上一行末尾小于下一行开头。','时间 O(m+n)，空间 O(1)。','''
def searchMatrixII(matrix, target):
    if not matrix or not matrix[0]:
        return False
    i, j = 0, len(matrix[0]) - 1
    while i < len(matrix) and j >= 0:
        x = matrix[i][j]
        if x == target:
            return True
        if x > target:
            j -= 1
        else:
            i += 1
    return False
''','[[1,4,7],[2,5,8],[3,6,9]], target=6 → True。')
group('linked','05 · 链表：先保存后断链，虚拟头统一边界','链表操作的单位是结点身份，不是数值。dummy 虚拟头可统一删除首结点与中间结点。修改 next 前先保存还要访问的结点；快慢指针解决中点和环，归并把有序链拆成能复用的原语。下面 Node、ListNode、TreeNode 由评测平台提供，离线测试中有等价定义。')
q(160,'相交链表','intersection-of-two-linked-lists','linked','两条无环单链表若共享同一个尾部结点，返回第一个共享结点，否则返回 None。','各走完 A+B 与 B+A，总路程相同，较长链的长度差自动抵消。','两个指针各从一条链出发；到尾后转到另一条链头；当两个指针身份相同时返回','相交指同一个对象，数值相等不算；两条链无交点时会一起变为 None。','时间 O(m+n)，空间 O(1)。','''
def getIntersectionNode(headA, headB):
    a, b = headA, headB
    while a is not b:
        a = a.next if a else headB
        b = b.next if b else headA
    return a
''','A=1→共享结点 8→9，B=2→3→同一个 8→9 → 返回共享的 8 结点。')
q(206,'反转链表','reverse-linked-list','linked','原地反转单链表并返回新的头结点。','prev 是已反转前缀的头，cur 是还未处理的后缀头。','先保存 cur.next；令 cur.next 指向 prev；将 prev、cur 向前推进','先改 next 再读取 cur.next 会丢失后续链；最后返回 prev 而非 cur。','时间 O(n)，空间 O(1)。','''
def reverseList(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    return prev
''','1→2→3→None → 3→2→1→None。')
q(234,'回文链表','palindrome-linked-list','linked','判断单链表的结点值序列是否为回文。','快慢指针定位后半段；反转后半段后，两端即可同时向中间比较。','快指针每次两步、慢指针一步；原地反转慢指针后的半段；比较，最后再反转回来恢复链表','只比较后半段长度；奇数长度的中点不影响；不要提前 return 而忘记恢复原链。','时间 O(n)，额外空间 O(1)。','''
def isPalindrome(head):
    if not head or not head.next:
        return True
    def rev(node):
        prev = None
        while node:
            nxt = node.next
            node.next = prev
            prev, node = node, nxt
        return prev
    slow = fast = head
    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next
    half = rev(slow.next)
    a, b, ok = head, half, True
    while b:
        if a.val != b.val:
            ok = False
        a, b = a.next, b.next
    slow.next = rev(half)
    return ok
''','1→2→2→1 → True；比较后仍保持原链。')
q(141,'环形链表','linked-list-cycle','linked','判断单链表中是否存在环。','有环时快指针每轮比慢指针多走一步，相对距离会模环长循环，必然相遇。','两个指针从头出发；每轮慢一步快两步；相遇返回 True，快指针遇到 None 则无环','先移动再比较，否则刚初始化就在头结点相遇；访问 fast.next 前检查 fast。','时间 O(n)，空间 O(1)。','''
def hasCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False
''','1→2→3→2（回到第二结点）→ True；普通 1→2→None → False。')
q(142,'环形链表 II','linked-list-cycle-ii','linked','有环则返回入环的第一个结点，无环返回 None。','相遇时若入环前长 a、慢指针在环内走 b，则 a+b 是环长的整数倍；一个从头、一个从相遇点同步走会在入口相遇。','先按快慢指针找到相遇点；一个指针重置 head；两者每次走一步直到再次相遇','返回的是入口结点对象；不可用修改链表标记的办法破坏输入。','时间 O(n)，空间 O(1)。','''
def detectCycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            entry = head
            while entry is not slow:
                entry, slow = entry.next, slow.next
            return entry
    return None
''','3→2→0→-4→回到结点 2 → 返回 2 所在结点。')
q(21,'合并两个有序链表','merge-two-sorted-lists','linked','把两个非降序链表合并为一个非降序链表。','当前最小值一定在两个头结点之一；不断把较小头接到答案尾部。','建 dummy 与 tail；比较两头并接上较小者；一边耗尽后直接接剩余后缀','tail 每次必须推进；返回 dummy.next，不能返回虚拟结点。','时间 O(m+n)，额外空间 O(1)。','''
def mergeTwoLists(list1, list2):
    dummy = tail = ListNode(0)
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next, list1 = list1, list1.next
        else:
            tail.next, list2 = list2, list2.next
        tail = tail.next
    tail.next = list1 or list2
    return dummy.next
''','1→2→4 与 1→3→4 → 1→1→2→3→4→4。')
q(2,'两数相加','add-two-numbers','linked','两个非负整数以逆序链表存储，每结点一位；返回和的逆序链表。','逐位相加并保留进位，长短不同的链用 0 补齐。','循环条件包含任一链非空或 carry 非零；计算本位总和并 divmod 10；追加余数位并推进指针','末尾进位必须生成新结点；不能把整条链直接转成整数来绕过题目。','时间 O(max(m,n))，输出 O(max(m,n))，额外状态 O(1)。','''
def addTwoNumbers(l1, l2):
    dummy = tail = ListNode(0)
    carry = 0
    while l1 or l2 or carry:
        total = carry + (l1.val if l1 else 0) + (l2.val if l2 else 0)
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    return dummy.next
''','2→4→3 表示 342，5→6→4 表示 465；输出 7→0→8 表示 807。')
q(19,'删除链表的倒数第 N 个结点','remove-nth-node-from-end-of-list','linked','删除倒数第 n 个结点并返回头；保证 n 有效。','前后指针相隔 n 个结点；前指针到尾时，后指针恰好在待删除结点前。','从 dummy 出发让 fast 先走 n 步；当 fast.next 非空时两指针同步前进；令 slow.next 跳过一个结点','从 dummy 起步可覆盖删头；循环用 fast.next 与先走 n 步必须配套。','时间 O(n)，空间 O(1)。','''
def removeNthFromEnd(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        slow, fast = slow.next, fast.next
    slow.next = slow.next.next
    return dummy.next
''','1→2→3→4→5, n=2 → 1→2→3→5。')
q(24,'两两交换链表中的节点','swap-nodes-in-pairs','linked','交换每一对相邻结点，不能仅交换数值。','保存一对结点 a、b，重连 prev→b→a→后缀，再将 prev 移到 a。','使用 dummy；只要后面至少有两结点就交换；不足两个时保持剩余后缀','重连 a.next 前要记住 b；修改的是链接，不是 val。','时间 O(n)，空间 O(1)。','''
def swapPairs(head):
    dummy = ListNode(0, head)
    prev = dummy
    while prev.next and prev.next.next:
        a, b = prev.next, prev.next.next
        a.next = b.next
        b.next = a
        prev.next = b
        prev = a
    return dummy.next
''','1→2→3→4→5 → 2→1→4→3→5。')
q(25,'K 个一组翻转链表','reverse-nodes-in-k-group','linked','每 k 个结点原地翻转，不满 k 个的尾段保留。','每轮先确认整组存在，再以组后结点为 prev 反转这一组，最后连接组前结点。','从组前结点向后走 k 步定位 kth；保存 after=kth.next；反转到 after，再把组前 next 指向 kth，下一轮组前变为旧组头','不能先翻转后才发现不足 k 个；反转期间 cur 与 after 比较身份。','时间 O(n)，空间 O(1)。','''
def reverseKGroup(head, k):
    dummy = ListNode(0, head)
    before = dummy
    while True:
        kth = before
        for _ in range(k):
            kth = kth.next
            if kth is None:
                return dummy.next
        after, cur = kth.next, before.next
        prev = after
        while cur is not after:
            nxt = cur.next
            cur.next = prev
            prev, cur = cur, nxt
        old_head = before.next
        before.next = kth
        before = old_head
''','1→2→3→4→5, k=3 → 3→2→1→4→5。')
q(138,'随机链表的复制','copy-list-with-random-pointer','linked','深拷贝带 next 和 random 指针的链表；新旧结点不能共享。','先建立原结点→新结点的映射，第二遍才能同时正确连接向前或向后的 random。','第一遍创建所有新结点；映射 None 到 None；第二遍按映射填 next 与 random','不能以值作映射键，因为值可重复；random 可以指向自身或任意先前结点。','时间 O(n)，额外空间 O(n)。','''
def copyRandomList(head):
    copies = {None: None}
    cur = head
    while cur:
        copies[cur] = Node(cur.val)
        cur = cur.next
    cur = head
    while cur:
        copies[cur].next = copies[cur.next]
        copies[cur].random = copies[cur.random]
        cur = cur.next
    return copies[head]
''','两结点 7→13，13.random 指向 7；复制后新 13 指向新 7，不能指回旧 7。')
q(148,'排序链表','sort-list','linked','将链表升序排序。','链表没有随机访问，用快慢指针分半、递归排序、线性归并，得到 O(n log n)。','长度 0 或 1 时返回；快慢指针找左半尾并断开；递归两半，双指针合并','必须断开 slow.next，否则递归区间不缩小；此教学版递归栈 O(log n)，不是严格 O(1) 空间。','时间 O(n log n)，额外空间 O(log n) 递归栈。','''
def sortList(head):
    if not head or not head.next:
        return head
    slow, fast = head, head.next
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    second = slow.next
    slow.next = None
    a, b = sortList(head), sortList(second)
    dummy = tail = ListNode(0)
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next
''','4→2→1→3 → 1→2→3→4。')
q(23,'合并 K 个升序链表','merge-k-sorted-lists','linked','合并 k 条有序链，设所有结点总数为 N。','最小堆只保存每条链的当前头，堆顶就是全局下一个最小结点。','将各非空头入堆；弹出最小结点接入输出；把它的 next 放入堆，直到堆空','Python 的结点不能直接比较；堆元组增加唯一递增序号，避免相等 val 时比较结点。','时间 O(N log k)，额外空间 O(k)。','''
def mergeKLists(lists):
    import heapq
    from itertools import count
    serial, heap = count(), []
    for node in lists:
        if node:
            heapq.heappush(heap, (node.val, next(serial), node))
    dummy = tail = ListNode(0)
    while heap:
        _, _, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(heap, (node.next.val, next(serial), node.next))
    return dummy.next
''','[1→4→5, 1→3→4, 2→6] → 1→1→2→3→4→4→5→6。')
q(146,'LRU 缓存','lru-cache','linked','实现容量固定的缓存，get/put 平均 O(1)；满时淘汰最久未被访问的键。','字典把 key 映射到双向链表结点，可 O(1) 定位与删除；循环哨兵 root 的 next 为最旧、prev 为最新，省掉空链和头尾特判。','get 命中后摘下结点并接到末尾；put 新写或更新都移到末尾；超容量时删除 root.next，同时删除其字典项','更新已有键也算使用；双向连接要成对修改；淘汰时字典与链表必须同时移除，否则会保留失效结点。','get/put 平均 O(1)，空间 O(capacity)。','''
class LRUCache:
    class _Link:
        def __init__(self, key=None, value=None):
            self.key, self.value = key, value
            self.prev = self.next = self

    def __init__(self, capacity):
        self.capacity = capacity
        self.data = {}
        self.root = self._Link()

    def _remove(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _recent(self, node):
        tail = self.root.prev
        tail.next = node
        node.prev = tail
        node.next = self.root
        self.root.prev = node

    def get(self, key):
        if key not in self.data:
            return -1
        node = self.data[key]
        self._remove(node)
        self._recent(node)
        return node.value

    def put(self, key, value):
        if key in self.data:
            node = self.data[key]
            node.value = value
            self._remove(node)
        else:
            node = self._Link(key, value)
            self.data[key] = node
        self._recent(node)
        if len(self.data) > self.capacity:
            oldest = self.root.next
            self._remove(oldest)
            del self.data[oldest.key]
''','容量 2；put(1,1),put(2,2),get(1),put(3,3) 后 get(2)=-1。')
group('tree','06 · 树：递归返回值与全局答案分开','每道树题先写出递归函数“返回什么”。深度返回一条向下路径，直径/最大路径和却在当前结点把左右贡献合并；合并结果更新全局答案，不能继续向父结点返回分叉路径。层序遍历用队列按层处理；BST 的中序是递增序列。h 表示树高，最坏可等于 n。')
q(94,'二叉树的中序遍历','binary-tree-inorder-traversal','tree','按左子树、根、右子树输出结点值。','显式栈模拟递归：先把所有左子孙压栈，弹出的结点就是下一个中序结点。','沿 left 一直入栈；弹栈访问；转向其 right 再重复','循环条件是 cur 非空或栈非空；遍历到空左孩子并不意味着结束。','时间 O(n)，额外空间 O(h)，输出 O(n)。','''
def inorderTraversal(root):
    stack, ans, cur = [], [], root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        ans.append(cur.val)
        cur = cur.right
    return ans
''','根 1、右子 2、2 的左子 3 → [1,3,2]。')
q(104,'二叉树的最大深度','maximum-depth-of-binary-tree','tree','求从根到最远叶结点路径上的结点数。','空树深度 0；非空树深度等于左右最大深度加 1。','空结点返回 0；递归计算左右深度；取最大并加 1','深度按结点数；只有根时返回 1。偏斜树很深时 Python 递归可能达栈限制，可改层序。','时间 O(n)，空间 O(h)。','''
def maxDepth(root):
    if root is None:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))
''','根 3，左子 9，右子 20 且 20 有两孩子 → 3。')
q(226,'翻转二叉树','invert-binary-tree','tree','交换每个结点的左右子树。','每个子树都执行同一交换，递归结构与问题一致。','空结点返回 None；递归翻转原左右子树并交换赋值；返回 root','交换的是整棵子树引用；不能只交换孩子的数值。','时间 O(n)，空间 O(h)。','''
def invertTree(root):
    if root:
        root.left, root.right = invertTree(root.right), invertTree(root.left)
    return root
''','[4,2,7,1,3,6,9] → [4,7,2,9,6,3,1]（层序）。')
q(101,'对称二叉树','symmetric-tree','tree','判断二叉树是否以根为中心镜像对称。','比较两个结点时，需要 a.left 对 b.right、a.right 对 b.left，而非同方向。','两者都空则真；恰一个空或值不同则假；递归比较两组镜像孩子','仅比较每一层数值集合不够，空结点的位置也决定结构。','时间 O(n)，空间 O(h)。','''
def isSymmetric(root):
    def mirror(a, b):
        if not a or not b:
            return a is b
        return (a.val == b.val and mirror(a.left, b.right)
                and mirror(a.right, b.left))
    return root is None or mirror(root.left, root.right)
''','[1,2,2,3,4,4,3] → True；[1,2,2,None,3,None,3] → False。')
q(543,'二叉树的直径','diameter-of-binary-tree','tree','求任意两个结点之间最长路径的边数，路径可以不经过根。','左右子树高度之和就是经过当前结点的最长路径边数；递归返回值只保留一边高度。','后序取得 left/right 高度；更新 best=max(best,left+right)；返回 1+max(left,right)','直径按边数、高度按结点数，这里 left+right 已是边数，不再加 1。','时间 O(n)，空间 O(h)。','''
def diameterOfBinaryTree(root):
    best = 0
    def height(node):
        nonlocal best
        if not node:
            return 0
        left, right = height(node.left), height(node.right)
        best = max(best, left + right)
        return 1 + max(left, right)
    height(root)
    return best
''','[1,2,3,4,5] → 3，路径 4→2→1→3。')
q(102,'二叉树的层序遍历','binary-tree-level-order-traversal','tree','逐层从左到右输出结点值，每层单独一个列表。','处理本层前固定队列长度，新加入孩子留给下一层。','根入队；每轮读取 len(queue) 次；出队记录值并按左右顺序入队孩子','不能在本层循环中动态改变终止长度；list.pop(0) 会产生线性搬移，改用 deque。','时间 O(n)，空间 O(w)，w 为最大层宽，输出另计。','''
def levelOrder(root):
    from collections import deque
    queue = deque([root]) if root else deque()
    ans = []
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        ans.append(level)
    return ans
''','[3,9,20,None,None,15,7] → [[3],[9,20],[15,7]]。')
q(108,'将有序数组转换为二叉搜索树','convert-sorted-array-to-binary-search-tree','tree','把严格递增数组转为高度平衡 BST。','中点作根，将左右半区分别转为左右子树，保证排序性质和高度平衡。','递归区间 [l,r)；空区间返回 None；取中点建根并递归两个半区','用区间下标而非切片，避免不必要复制；偶数长度可以选两个中点中的任一个。','时间 O(n)，额外栈 O(log n)，树输出 O(n)。','''
def sortedArrayToBST(nums):
    def build(l, r):
        if l >= r:
            return None
        mid = (l + r) // 2
        root = TreeNode(nums[mid])
        root.left = build(l, mid)
        root.right = build(mid + 1, r)
        return root
    return build(0, len(nums))
''','[-10,-3,0,5,9] → 根可为 0，左右分别由两个半区构建。')
q(98,'验证二叉搜索树','validate-binary-search-tree','tree','判断每个结点的左子树全部小于它、右子树全部大于它。','祖先传下来的上下界必须同时满足，不能只比较直接孩子。','从 (-∞,+∞) 开始；检查 low<val<high；左子树收紧 high，右子树收紧 low','重复值不合法；[5,1,4,None,None,3,6] 的 4 虽局部孩子正确但小于祖先 5。','时间 O(n)，空间 O(h)。','''
def isValidBST(root):
    def valid(node, low, high):
        if not node:
            return True
        return (low < node.val < high
                and valid(node.left, low, node.val)
                and valid(node.right, node.val, high))
    return valid(root, float('-inf'), float('inf'))
''','[2,1,3] → True；[2,2,3] → False。')
q(230,'二叉搜索树中第 K 小的元素','kth-smallest-element-in-a-bst','tree','合法 BST 中返回第 k 小的值，k 从 1 开始且有效。','BST 的中序遍历是升序，第 k 次弹栈即答案，无需遍历全部结点。','按中序栈模板压左链；每次访问令 k 减一；k=0 时返回值','若题目变成频繁更新和查询，需要维护子树大小；这里只解决静态单次查询。','时间 O(h+k)，空间 O(h)。','''
def kthSmallest(root, k):
    stack, cur = [], root
    while cur or stack:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        k -= 1
        if k == 0:
            return cur.val
        cur = cur.right
''','[3,1,4,None,2], k=2 → 2。')
q(199,'二叉树的右视图','binary-tree-right-side-view','tree','从右侧能看到的每层最右结点值。','层序遍历每层最后一个结点就是可见结点，右侧没有孩子时也可能由左子树贡献。','每层固定长度；按左再右入队；记录每层最后一次出队的值','不能只沿 right 指针走；右子树较浅时，更深层可能来自左边。','时间 O(n)，空间 O(w)，输出另计。','''
def rightSideView(root):
    from collections import deque
    queue = deque([root]) if root else deque()
    ans = []
    while queue:
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        ans.append(node.val)
    return ans
''','[1,2,3,None,5,None,4] → [1,3,4]。')
q(114,'二叉树展开为链表','flatten-binary-tree-to-linked-list','tree','原地把树按前序顺序展开，所有 left 置空，right 指向下一结点。','存在左子树时，把原右子树接到左子树最右结点，再把左子树搬到右边。','从根沿 right 扫描；找左子树最右结点；接上旧 right，再将 left 搬到 right 并清空 left','最终必须清空每个 left；不能新建结点替代原树。所有前驱查找的右边合计线性。','时间 O(n)，额外空间 O(1)。','''
def flatten(root):
    cur = root
    while cur:
        if cur.left:
            tail = cur.left
            while tail.right:
                tail = tail.right
            tail.right = cur.right
            cur.right = cur.left
            cur.left = None
        cur = cur.right
''','[1,2,5,3,4,None,6] → right 链 1→2→3→4→5→6。')
q(105,'从前序与中序遍历序列构造二叉树','construct-binary-tree-from-preorder-and-inorder-traversal','tree','给定值互不重复的前序和中序序列，重建原树。','前序下一个元素是根；它在中序的位置将左右子树分开，按左后右消费前序。','建立中序值到下标映射；递归维护中序半开区间；取前序下一个根并先构左子树再构右子树','前序迭代器是共享状态，构造左右顺序不能颠倒；重复值不适用这张位置映射。','时间 O(n)，额外空间 O(n) 含映射与栈。','''
def buildTree(preorder, inorder):
    positions = {x: i for i, x in enumerate(inorder)}
    values = iter(preorder)
    def build(l, r):
        if l >= r:
            return None
        value = next(values)
        mid = positions[value]
        node = TreeNode(value)
        node.left = build(l, mid)
        node.right = build(mid + 1, r)
        return node
    return build(0, len(inorder))
''','前序 [3,9,20,15,7]、中序 [9,3,15,20,7] → 根 3，左 9，右 20。')
q(437,'路径总和 III','path-sum-iii','tree','统计所有从某结点向下延伸、和值为 targetSum 的非空路径，不要求从根开始。','根到当前结点的前缀和减某祖先前缀和等于目标，复用一维前缀和计数。','维护当前递归路径的前缀计数，初始 {0:1}；到结点先查询 total-target；加入当前前缀，递归左右，退出时减回','回溯减计数必不可少，否则会把另一分支的前缀当作祖先；先查后加避免空路径。','平均时间 O(n)，空间 O(h)。','''
def pathSum(root, targetSum):
    counts = {0: 1}
    def visit(node, total):
        if not node:
            return 0
        total += node.val
        ans = counts.get(total - targetSum, 0)
        counts[total] = counts.get(total, 0) + 1
        ans += visit(node.left, total) + visit(node.right, total)
        counts[total] -= 1
        return ans
    return visit(root, 0)
''','[10,5,-3,3,2,None,11,3,-2,None,1], target=8 → 3。')
q(236,'二叉树的最近公共祖先','lowest-common-ancestor-of-a-binary-tree','tree','给定两个确实存在且不同的结点 p、q，返回最近公共祖先。','递归返回当前子树找到的目标或公共祖先；若左右各找到一个，当前根就是交汇点。','空结点或根等于 p/q 时返回它；递归左右；两边非空返回根，否则返回非空一边','比较结点身份；一个目标可能是另一个的祖先，此时应返回祖先目标本身。','时间 O(n)，空间 O(h)。','''
def lowestCommonAncestor(root, p, q):
    if root is None or root is p or root is q:
        return root
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)
    if left and right:
        return root
    return left or right
''','根 3，左右子树分别含 5、1；p=5,q=1 → 3。')
q(124,'二叉树中的最大路径和','binary-tree-maximum-path-sum','tree','求任意非空简单路径的最大结点和值，路径不必经过根。','负贡献可以舍弃；经过当前根的答案可连接左右两边，但向父亲返回时只能选一边。','递归得到左右非负贡献；用 val+left+right 更新 best；返回 val+max(left,right)','best 初始化为 -∞，才能处理全负树；不能把左右都返回给父结点，路径不能分叉。','时间 O(n)，空间 O(h)。','''
def maxPathSum(root):
    best = float('-inf')
    def gain(node):
        nonlocal best
        if not node:
            return 0
        left = max(0, gain(node.left))
        right = max(0, gain(node.right))
        best = max(best, node.val + left + right)
        return node.val + max(left, right)
    gain(root)
    return best
''','[-10,9,20,None,None,15,7] → 42，路径 15→20→7。')
group('graph','07 · 图与前缀树：可达、最短层数、依赖','DFS/栈找连通块；多源 BFS 把所有起点同时入队，层数就是最短传播时间；有向依赖用入度消除，剩余结点意味着环。访问标记在入队时设置，避免重复入队。Trie 则把共享字符串前缀压成路径，末尾标记区分完整单词与前缀。')
q(200,'岛屿数量','number-of-islands','graph','字符网格中 1 为陆地、0 为水，四方向相连算一座岛，求岛数。','每遇到尚未标记的陆地就新开一个连通块，用栈把整座岛淹掉。','枚举格子，遇 1 则计数加一并改 0 入栈；不断处理四邻居；邻居入栈时立刻标记','对角线不相连；本实现会修改输入；迭代栈避免巨大岛屿导致 Python 递归溢出。','时间 O(mn)，最坏额外空间 O(mn)。','''
def numIslands(grid):
    if not grid:
        return 0
    m, n, ans = len(grid), len(grid[0]), 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] != '1':
                continue
            ans += 1
            grid[i][j] = '0'
            stack = [(i, j)]
            while stack:
                r, c = stack.pop()
                for a, b in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)):
                    if 0 <= a < m and 0 <= b < n and grid[a][b] == '1':
                        grid[a][b] = '0'
                        stack.append((a, b))
    return ans
''','[["1","1","0"],["0","1","0"],["0","0","1"]] → 2。')
q(994,'腐烂的橘子','rotting-oranges','graph','每分钟腐烂橘子使四邻新鲜橘子腐烂；返回全部腐烂的最少分钟，无法全部腐烂则 -1。','所有初始腐烂点同时做 BFS，传播层数等于最近腐烂源距离。','初始所有 2 入队并统计 1；每轮处理当前层并感染邻居、减少 fresh；fresh 归零时停止，队列空仍有 fresh 则 -1','没有新鲜橘子直接 0；不能从每个腐烂点分开 DFS 求时间。','时间 O(mn)，空间 O(mn)。','''
def orangesRotting(grid):
    from collections import deque
    m, n = len(grid), len(grid[0])
    queue = deque()
    fresh = minutes = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 2:
                queue.append((i, j))
            elif grid[i][j] == 1:
                fresh += 1
    while queue and fresh:
        minutes += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for a, b in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)):
                if 0 <= a < m and 0 <= b < n and grid[a][b] == 1:
                    grid[a][b] = 2
                    fresh -= 1
                    queue.append((a, b))
    return minutes if fresh == 0 else -1
''','[[2,1,1],[1,1,0],[0,1,1]] → 4。')
q(207,'课程表','course-schedule','graph','[a,b] 表示上 a 前必须先上 b，判断是否能完成全部课程。','有向图存在拓扑序等价于无环；反复删除入度 0 的结点，模拟选课。','建 b→a 边与 a 的入度；所有入度 0 的课程入队；删除课程并减少后继入度，统计被处理数量','边方向要与入度一致；无依赖的孤立课程也应入队，不能只枚举边里出现的课程。','时间 O(V+E)，空间 O(V+E)。','''
def canFinish(numCourses, prerequisites):
    from collections import deque
    graph = [[] for _ in range(numCourses)]
    degree = [0] * numCourses
    for a, b in prerequisites:
        graph[b].append(a)
        degree[a] += 1
    queue = deque(i for i, d in enumerate(degree) if d == 0)
    done = 0
    while queue:
        cur = queue.popleft()
        done += 1
        for nxt in graph[cur]:
            degree[nxt] -= 1
            if degree[nxt] == 0:
                queue.append(nxt)
    return done == numCourses
''','2 门课，[[1,0]] → True；[[1,0],[0,1]] → False。')
q(208,'实现 Trie（前缀树）','implement-trie-prefix-tree','graph','支持 insert(word)、search(word) 与 startsWith(prefix)。','每条边表示一个字符；字典嵌套存孩子，特殊结束键表示某条路径也是完整单词。','insert 逐字符创建子字典并标记结束；查询逐字符走边；完整查找检查结束标记，前缀查找只要路径存在','插入 apple 后 search(app) 应为 False，startsWith(app) 为 True；结束标记不应与合法字符冲突。','每操作时间 O(L)，空间与所有不同前缀总长度成正比。','''
class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for c in word:
            node = node.setdefault(c, {})
        node['#'] = True

    def _walk(self, text):
        node = self.root
        for c in text:
            if c not in node:
                return None
            node = node[c]
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and '#' in node

    def startsWith(self, prefix):
        return self._walk(prefix) is not None
''','insert("apple") 后 search("apple")=True，search("app")=False。')

group('backtrack','08 · 回溯：选择、约束、撤销','回溯是在一棵隐含决策树中枚举合法结果。排列维护“哪些位置已用”；组合维护起点避免不同顺序重复；路径每次修改后都要恢复。先用状态定义解释为什么不漏不重，再谈剪枝。输出规模常为指数，复杂度必须计入复制答案的代价。')
q(46,'全排列','permutations','backtrack','对值互不相同的数组，返回所有排列。','每一层决定下一个位置选哪个尚未使用的原下标。','维护 path 和 used；枚举没用过的下标并标记、追加；递归后撤销，长度 n 时复制答案','append(path) 会引用同一个可变列表，必须 path.copy()；本题不处理重复输入去重。','时间 O(n·n!)，额外搜索栈与标记 O(n)，输出 O(n·n!)。','''
def permute(nums):
    ans, path, used = [], [], [False] * len(nums)
    def dfs():
        if len(path) == len(nums):
            ans.append(path.copy())
            return
        for i, x in enumerate(nums):
            if not used[i]:
                used[i] = True
                path.append(x)
                dfs()
                path.pop()
                used[i] = False
    dfs()
    return ans
''','[1,2,3] → 6 种排列；固定首位 1 后递归排列 [2,3]。')
q(78,'子集','subsets','backtrack','返回互不相同元素数组的所有子集，包括空集。','每个元素只有选与不选两种决定；逐轮将已有子集各复制一份并加上新元素。','初始 [[]]；枚举 x；将当前每个子集加 x 后追加','遍历 ans 时不能同时无界追加；列表推导先计算新增结果再扩展。','时间 O(n·2^n)，含输出空间 O(n·2^n)。','''
def subsets(nums):
    ans = [[]]
    for x in nums:
        ans += [part + [x] for part in ans]
    return ans
''','[1,2]：先 [[]]，加入 1 得 [[],[1]]，加入 2 得 [[],[1],[2],[1,2]]。')
q(17,'电话号码的字母组合','letter-combinations-of-a-phone-number','backtrack','输入仅含 2..9 的数字串，返回电话按键可能对应的全部字母串；空输入返回空列表。','每一层对一个数字选择一个字母，结果是各按键候选集合的笛卡尔积。','建立数字到字母映射；初始前缀为一个空串；逐位把每个前缀扩展为所有候选字母','空输入的输出是 []，不是 [""]；7 和 9 有四个字母。','长度 d：最坏时间 O(d·4^d)，含输出空间 O(d·4^d)。','''
def letterCombinations(digits):
    if not digits:
        return []
    letters = dict(zip('23456789', ['abc','def','ghi','jkl','mno','pqrs','tuv','wxyz']))
    ans = ['']
    for digit in digits:
        ans = [prefix + c for prefix in ans for c in letters[digit]]
    return ans
''','"23" → ["ad","ae","af","bd","be","bf","cd","ce","cf"]。')
q(39,'组合总和','combination-sum','backtrack','给定互不相同的正整数候选，每个可用无限次，返回和为 target 的不重复组合。','只选择下标不小于 start 的元素保证组合顺序固定；重复使用允许递归仍从 i 开始。','候选排序；枚举 i≥start，x 超过剩余目标即可 break；加入 x 递归 dfs(i,remain-x)，回来撤销','如果传 i+1 就错误地变为每数只能用一次；剪枝依赖候选全为正数。','设最小候选 a、深度 D=target/a，最坏 O(k^D·D)，输出相关；栈 O(D)。','''
def combinationSum(candidates, target):
    values = sorted(candidates)
    ans, path = [], []
    def dfs(start, remain):
        if remain == 0:
            ans.append(path.copy())
            return
        for i in range(start, len(values)):
            x = values[i]
            if x > remain:
                break
            path.append(x)
            dfs(i, remain - x)
            path.pop()
    dfs(0, target)
    return ans
''','[2,3,6,7], target=7 → [[2,2,3],[7]]。')
q(22,'括号生成','generate-parentheses','backtrack','生成 n 对括号构成的所有合法字符串。','任意前缀中，右括号数不能多于左括号数；左括号总数不能超过 n。','left<n 时可以加左括号；right<left 时可以加右括号；长度 2n 时收集','只检查最终左右数量相等不够，例如 )( 在中途已经非法。','结果数为 Catalan 数 Cn，时间 O(n·Cn)，额外栈 O(n)，输出另计。','''
def generateParenthesis(n):
    ans = []
    def dfs(text, left, right):
        if len(text) == 2 * n:
            ans.append(text)
            return
        if left < n:
            dfs(text + '(', left + 1, right)
        if right < left:
            dfs(text + ')', left, right + 1)
    dfs('', 0, 0)
    return ans
''','n=3 → ["((()))","(()())","(())()","()(())","()()()"]。')
q(79,'单词搜索','word-search','backtrack','在字符网格四方向相邻走出 word，同一格在一条路径中不可重复。','状态为当前位置和已匹配长度；临时标记当前格防止路径重用，返回前必须恢复。','从每个格尝试；字符不符或越界失败；匹配后标记，递归四邻，恢复原字符后返回结果','不能用全局 visited 永久屏蔽格子，不同起点和不同路径可重用；即使成功也要恢复。','字长 L，时间上界 O(mn·4^L)，更紧可为 O(mn·3^L)，栈 O(L)。','''
def exist(board, word):
    m, n = len(board), len(board[0])
    def dfs(r, c, k):
        if not (0 <= r < m and 0 <= c < n) or board[r][c] != word[k]:
            return False
        if k == len(word) - 1:
            return True
        old = board[r][c]
        board[r][c] = None
        ok = any(dfs(a, b, k + 1) for a, b in
                 ((r-1,c),(r+1,c),(r,c-1),(r,c+1)))
        board[r][c] = old
        return ok
    return any(dfs(r, c, 0) for r in range(m) for c in range(n))
''','[["A","B"],["C","D"]], "ABD" → True；"ABA" → False。')
q(131,'分割回文串','palindrome-partitioning','backtrack','把字符串切成若干非空段，返回每段均为回文的全部切分方案。','先用区间 DP 预计算 s[i:j+1] 是否回文，回溯时只枚举合法切割终点。','i 倒序、j 正序计算 pal[i][j]；从 start 枚举 pal 为真的终点；切到 n 时收集路径','单字符都是回文；pal 计算必须先有内部区间；切片终点 j+1 才包含 j。','时间 O(n²+n·2^n)，空间 O(n²) 预处理，输出另计。','''
def partition(s):
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        for j in range(i, n):
            pal[i][j] = s[i] == s[j] and (j - i < 2 or pal[i+1][j-1])
    ans, path = [], []
    def dfs(start):
        if start == n:
            ans.append(path.copy())
            return
        for end in range(start, n):
            if pal[start][end]:
                path.append(s[start:end+1])
                dfs(end + 1)
                path.pop()
    dfs(0)
    return ans
''','"aab" → [["a","a","b"],["aa","b"]]。')
q(51,'N 皇后','n-queens','backtrack','在 n×n 棋盘放 n 个皇后，任意两个不同行、同列、同对角线；返回全部棋盘。','逐行放一个，自然保证不同行；列 c、主对角 r-c、副对角 r+c 三个集合判断冲突。','每层枚举列；未占用就加入三个集合并记录列号；递归下一行后撤销，放满 n 行时构造棋盘','对角线的编码是 r-c 与 r+c；所有集合都必须撤销。','候选搜索上界 O(n·n!)，每个输出棋盘 O(n²)，额外搜索空间 O(n)。','''
def solveNQueens(n):
    cols, diag1, diag2 = set(), set(), set()
    path, ans = [], []
    def dfs(r):
        if r == n:
            ans.append(['.' * c + 'Q' + '.' * (n-c-1) for c in path])
            return
        for c in range(n):
            if c in cols or r-c in diag1 or r+c in diag2:
                continue
            cols.add(c); diag1.add(r-c); diag2.add(r+c)
            path.append(c)
            dfs(r + 1)
            path.pop()
            cols.remove(c); diag1.remove(r-c); diag2.remove(r+c)
    dfs(0)
    return ans
''','n=4 → 两种棋盘，列号序列 [1,3,0,2] 与 [2,0,3,1]。')
group('binary','09 · 二分：明确要找的边界','二分压缩的是答案区间，不只是“数组有序”。lower_bound 找第一个大于等于目标的位置，答案可等于 n。旋转数组要先判断哪一半有序；中位数则在较短数组上二分分割点，使左右数量平衡且左最大不超过右最小。')
q(35,'搜索插入位置','search-insert-position','binary','有序无重复数组中，返回 target 所在位置，不存在则返回保持有序的插入位置。','寻找第一个 nums[i]≥target 的下标，使用半开区间 [l,r)。','设 l=0,r=n；若 nums[mid]<target 则 l=mid+1，否则 r=mid；结束返回 l','r 初始为 n，允许答案插到数组末尾；不要混用闭区间的更新规则。','时间 O(log n)，空间 O(1)。','''
def searchInsert(nums, target):
    l, r = 0, len(nums)
    while l < r:
        mid = (l + r) // 2
        if nums[mid] < target:
            l = mid + 1
        else:
            r = mid
    return l
''','[1,3,5,6], target=2 → 1；target=7 → 4。')
q(74,'搜索二维矩阵','search-a-2d-matrix','binary','每行递增，且下一行第一个数大于上一行最后一个数，判断目标是否存在。','矩阵按行展开后整体有序；逻辑下标 mid 对应行 mid//n、列 mid%n。','在 0..mn-1 上常规闭区间二分；计算矩阵值；按与 target 比较排除半边','与第 240 题不同，本题有跨行有序保证；行列映射用列数 n。','时间 O(log(mn))，空间 O(1)。','''
def searchMatrix(matrix, target):
    if not matrix or not matrix[0]:
        return False
    m, n = len(matrix), len(matrix[0])
    l, r = 0, m * n - 1
    while l <= r:
        mid = (l + r) // 2
        value = matrix[mid // n][mid % n]
        if value == target:
            return True
        if value < target:
            l = mid + 1
        else:
            r = mid - 1
    return False
''','[[1,3,5],[7,9,11]], target=9 → True。')
q(34,'在排序数组中查找元素的第一个和最后一个位置','find-first-and-last-position-of-element-in-sorted-array','binary','非降序数组中返回 target 首末下标，不存在则 [-1,-1]；要求 O(log n)。','首位置是第一个 ≥target，末位置是第一个 >target 再减 1。','写 boundary(strict)；strict=False 时找 ≥target，True 时找 >target；检查首位置是否越界或不相等','先验证存在性；不能用线性向两边扩展，否则全重复时退化 O(n)。','时间 O(log n)，空间 O(1)。','''
def searchRange(nums, target):
    def boundary(strict):
        l, r = 0, len(nums)
        while l < r:
            mid = (l + r) // 2
            if nums[mid] < target or (strict and nums[mid] == target):
                l = mid + 1
            else:
                r = mid
        return l
    first = boundary(False)
    if first == len(nums) or nums[first] != target:
        return [-1, -1]
    return [first, boundary(True) - 1]
''','[5,7,7,8,8,10], target=8 → [3,4]。')
q(33,'搜索旋转排序数组','search-in-rotated-sorted-array','binary','严格递增数组经一次旋转，返回 target 下标或 -1。','每轮左半或右半至少有一半有序；先识别有序半，再判断目标是否落在其数值范围。','闭区间二分并先查相等；若 nums[l]≤nums[mid] 则左半有序；目标落左半则缩右，否则移左，右半同理','区间端点不等号要与 mid 已排除相配套；本题无重复，有重复时不能直接保证二分效率。','时间 O(log n)，空间 O(1)。','''
def search(nums, target):
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = (l + r) // 2
        if nums[mid] == target:
            return mid
        if nums[l] <= nums[mid]:
            if nums[l] <= target < nums[mid]:
                r = mid - 1
            else:
                l = mid + 1
        else:
            if nums[mid] < target <= nums[r]:
                l = mid + 1
            else:
                r = mid - 1
    return -1
''','[4,5,6,7,0,1,2], target=0 → 4。')
q(153,'寻找旋转排序数组中的最小值','find-minimum-in-rotated-sorted-array','binary','无重复递增数组旋转后，找最小值。','与右端点比较：mid 更大则最小值一定在右边；否则 mid 仍可能是最小值。','l=0,r=n-1；若 nums[mid]>nums[r] 则 l=mid+1；否则 r=mid，结束取 nums[l]','保留 mid 的分支用 r=mid，不能 mid-1；未经旋转的数组也适用。','时间 O(log n)，空间 O(1)。','''
def findMin(nums):
    l, r = 0, len(nums) - 1
    while l < r:
        mid = (l + r) // 2
        if nums[mid] > nums[r]:
            l = mid + 1
        else:
            r = mid
    return nums[l]
''','[3,4,5,1,2] → 1；[1,2,3] → 1。')
q(4,'寻找两个正序数组的中位数','median-of-two-sorted-arrays','binary','两个有序数组总长非零，求合并后中位数，要求对数时间。','二分短数组切点 i，长数组切点 j 由左半应有的元素数决定；合法切分满足两侧左最大≤右最小。','确保 a 较短，左边总量 (m+n+1)//2；越界用 ±∞；若 a 左过大则 i 左移，若 b 左过大则 i 右移；奇数取左最大，偶数取左右中值平均','空数组可处理；偶数时必须除以 2；比较的是跨数组相邻边界，不是两数组各自中位数。','时间 O(log(min(m,n)+1))，空间 O(1)。','''
def findMedianSortedArrays(a, b):
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    l, r = 0, m
    while l <= r:
        i = (l + r) // 2
        j = (m + n + 1) // 2 - i
        al = a[i-1] if i else float('-inf')
        ar = a[i] if i < m else float('inf')
        bl = b[j-1] if j else float('-inf')
        br = b[j] if j < n else float('inf')
        if al > br:
            r = i - 1
        elif bl > ar:
            l = i + 1
        elif (m + n) % 2:
            return max(al, bl)
        else:
            return (max(al, bl) + min(ar, br)) / 2
''','[1,3] 与 [2] → 2；[1,2] 与 [3,4] → 2.5。')

group('stack','10 · 栈：嵌套结构与最近更优者','普通栈保存尚未闭合的语法或上下文；单调栈保存尚未找到答案的候选。温度题中弹出结点时确定“右侧第一个更高”；柱状图中弹出高度时确定其最远横向范围。栈存下标通常比只存数值更有用。')
q(20,'有效的括号','valid-parentheses','stack','只含 ()[]{} 的字符串，判断是否正确嵌套且全部闭合。','每个右括号必须匹配最近的未闭合左括号，后进先出正好用栈。','左括号入栈；右括号检查栈非空且栈顶匹配；最后栈必须为空','数量相等不代表有效，如 ([)]；遇空栈右括号立即失败。','时间 O(n)，空间 O(n)。','''
def isValid(s):
    pair = {')': '(', ']': '[', '}': '{'}
    stack = []
    for c in s:
        if c in pair:
            if not stack or stack.pop() != pair[c]:
                return False
        else:
            stack.append(c)
    return not stack
''','"()[]{}" → True；"([)]" → False。')
q(155,'最小栈','min-stack','stack','支持 push、pop、top、getMin，全部 O(1)，查询和弹出时栈非空。','每个栈元素同时存当前值与加入后栈的最小值；删除时历史最小值自动恢复。','push 时取新值与上一个最小值较小者；pop 直接移除元组；top/getMin 分别读取两个字段','重复最小值也要正确保留；只存一个全局最小值无法在 pop 后恢复。','每操作时间 O(1)，空间 O(n)。','''
class MinStack:
    def __init__(self):
        self.stack = []

    def push(self, val):
        minimum = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, minimum))

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1][0]

    def getMin(self):
        return self.stack[-1][1]
''','push(-2),push(0),push(-3) 后最小 -3；pop 后最小恢复 -2。')
q(394,'字符串解码','decode-string','stack','将 k[内容] 展开为重复 k 次的内容，允许嵌套和多位数字，输入合法。','遇 [ 保存外层已解码前缀和重复次数，转入新层；遇 ] 把内层结果乘次数再接回外层。','连续数字累积 count=count*10+digit；遇 [ 入栈并清空局部状态；遇 ] 弹出并组合，普通字母追加','次数不只一位；不能在嵌套层覆盖外层前缀。输出很大时本身就需要对应时间内存。','最终输出长 L、最大嵌套 d，本字符串版本保守时间 O(L²)，空间 O(L+d)。','''
def decodeString(s):
    stack, text, number = [], '', 0
    for c in s:
        if c.isdigit():
            number = number * 10 + int(c)
        elif c == '[':
            stack.append((text, number))
            text, number = '', 0
        elif c == ']':
            prefix, repeat = stack.pop()
            text = prefix + text * repeat
        else:
            text += c
    return text
''','"3[a2[c]]" → "accaccacc"。')
q(739,'每日温度','daily-temperatures','stack','对每一天，返回要等待几天才能遇到更高温度，没有则为 0。','单调递减栈保存尚未找到更高日的下标；新温度更高时，弹出日的答案已确定。','从左到右遍历；当当前温度大于栈顶日时弹出并记 i-j；当前日入栈','相等不是更高，不弹相等温度；剩余栈元素保持答案 0。','时间 O(n)，空间 O(n)。','''
def dailyTemperatures(temperatures):
    ans = [0] * len(temperatures)
    stack = []
    for i, x in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < x:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans
''','[73,74,75,71,69,72,76,73] → [1,1,4,2,1,1,0,0]。')
q(84,'柱状图中最大的矩形','largest-rectangle-in-histogram','stack','柱子宽为 1，求全部柱子围成区域内最大的矩形面积。','单调递增高度栈中，遇到更矮柱时，弹出柱的右边界确定；新栈顶给左侧更矮边界。','给末尾加高度 0 清栈；栈初始 -1 作为左边界；弹出高度 h 时宽为 i-stack[-1]-1','宽度要减 1；栈顶弹出后再读取左边界；相等高度可保留，最终仍会算到完整宽度。','时间 O(n)，空间 O(n)。','''
def largestRectangleArea(heights):
    values = heights + [0]
    stack, best = [-1], 0
    for i, x in enumerate(values):
        while stack[-1] != -1 and values[stack[-1]] > x:
            h = values[stack.pop()]
            best = max(best, h * (i - stack[-1] - 1))
        stack.append(i)
    return best
''','[2,1,5,6,2,3] → 10，来自高度 5、宽度 2。')

group('heap','11 · 堆：只维护需要的极值边界','前 k 大用大小 k 的最小堆，堆顶是入选集合最弱的一项；中位数用两个堆把数据分成较小一半和较大一半。堆并不保证整体有序，只保证堆顶是极值。Python heapq 是最小堆，最大堆可存负数。')
q(215,'数组中的第 K 个最大元素','kth-largest-element-in-an-array','heap','找排序意义下第 k 大元素，重复值分别计数。','保留当前最大的 k 个数，最小堆堆顶就是第 k 大。','先用前 k 项 heapify；扫描余下元素，比堆顶大才 heapreplace；最后返回堆顶','不是第 k 个不同值；本版优先易记和稳定性，时间 O(n log k)，不是平均线性快选。','时间 O(n log k)，空间 O(k)。','''
def findKthLargest(nums, k):
    import heapq
    heap = nums[:k]
    heapq.heapify(heap)
    for i in range(k, len(nums)):
        if nums[i] > heap[0]:
            heapq.heapreplace(heap, nums[i])
    return heap[0]
''','[3,2,1,5,6,4], k=2 → 5。')
q(347,'前 K 个高频元素','top-k-frequent-elements','heap','返回出现次数最高的 k 个不同元素，保证答案唯一，顺序不限。','先计频，再按频次用大小 k 的堆选取。','Counter 得到 value→count；nlargest 以 counts.get 为排序键；返回 k 个键','不要按数值大小选；频次统计后只有 u 个候选。桶排序可进一步做到 O(n)。','时间 O(n+u log k)，空间 O(u+k)，u 为不同元素数。','''
def topKFrequent(nums, k):
    from collections import Counter
    from heapq import nlargest
    counts = Counter(nums)
    return nlargest(k, counts, key=counts.get)
''','[1,1,1,2,2,3], k=2 → [1,2]。')
q(295,'数据流的中位数','find-median-from-data-stream','heap','支持持续插入整数和随时查询中位数。','小半区用最大堆 low，大半区用最小堆 high；保持 low 元素数等于 high 或多 1，且 low 最大≤high 最小。','新数先入 low，再将 low 最大转入 high；若 high 更大，再把 high 最小转回 low；奇数读 low，偶数取两顶平均','low 存负数，取值要取反；空流不查询，避免未定义中位数。','插入 O(log n)，查询 O(1)，空间 O(n)。','''
class MedianFinder:
    def __init__(self):
        self.low, self.high = [], []

    def addNum(self, num):
        import heapq
        heapq.heappush(self.low, -num)
        heapq.heappush(self.high, -heapq.heappop(self.low))
        if len(self.high) > len(self.low):
            heapq.heappush(self.low, -heapq.heappop(self.high))

    def findMedian(self):
        if len(self.low) > len(self.high):
            return -self.low[0]
        return (-self.low[0] + self.high[0]) / 2
''','插入 1,2 → 1.5；再插入 3 → 2。')

group('greedy','12 · 贪心：证明局部选择不损失未来','贪心能省掉 DP 状态，但必须有支配或交换论证。股票只需此前最低价；跳跃只需最远可达范围；最少跳跃按可达区间分层；字母区间只有收集完当前出现字母的最后位置才可切分。')
q(121,'买卖股票的最佳时机','best-time-to-buy-and-sell-stock','greedy','最多完成一次先买后卖交易，返回最大利润，允许不交易。','固定卖出日，最优买入价是此前的最低价。','遍历时更新最低价格；计算当前价格减最低价；更新从 0 开始的最优利润','不能用未来最低价配过去卖价；价格单调下降时返回 0。','时间 O(n)，空间 O(1)。','''
def maxProfit(prices):
    low, best = float('inf'), 0
    for price in prices:
        low = min(low, price)
        best = max(best, price - low)
    return best
''','[7,1,5,3,6,4] → 5，在 1 买、6 卖。')
q(55,'跳跃游戏','jump-game','greedy','nums[i] 是从 i 最远可跳的步数，判断从 0 能否到末尾。','在已可达区域内，维护能扩展的最远位置；若当前下标已超过最远位置则不可达。','reach=0；枚举 i，先判断 i>reach；可达则更新 reach=max(reach,i+nums[i])','不能用最后一步恰好落在末尾作条件，可以选择小于最大步数的跳跃。','时间 O(n)，空间 O(1)。','''
def canJump(nums):
    reach = 0
    for i, step in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + step)
    return True
''','[2,3,1,1,4] → True；[3,2,1,0,4] → False。')
q(45,'跳跃游戏 II','jump-game-ii','greedy','保证能到末尾，求最少跳跃次数。','当前跳数可到达的区间是一层，扫描整层后选择下一层最远边界，相当于压缩后的 BFS。','end 表示当前层右边界、farthest 表示下一层最远；扫描除末尾外的下标；走到 end 时 jump 加一并扩展 end','不要扫描末尾后再多加一次；不能每步只跳到 nums[i] 最大的位置，要比较 i+nums[i]。','时间 O(n)，空间 O(1)。','''
def jump(nums):
    end = farthest = jumps = 0
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == end:
            jumps += 1
            end = farthest
    return jumps
''','[2,3,1,1,4] → 2，可按 0→1→4 跳。')
q(763,'划分字母区间','partition-labels','greedy','把字符串切成尽可能多段，使每个字符只出现在一段中，返回每段长度。','段内任意字符最后出现的位置都必须包含；不断扩展当前段终点，扫描点到达终点时才能切。','预先记录每字符最后位置；遍历更新 end=max(end,last[c])；i=end 时记录段长并开启下一段','不能遇到字符第一次重复就切；只有所有段内字符均不再出现时才安全。','时间 O(n)，空间 O(字符集大小)。','''
def partitionLabels(s):
    last = {c: i for i, c in enumerate(s)}
    start = end = 0
    ans = []
    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:
            ans.append(end - start + 1)
            start = i + 1
    return ans
''','"ababcbacadefegdehijhklij" → [9,7,8]。')
group('dp-linear','13 · DP 一：线性递推与有限状态','动态规划先写状态的中文含义，再列最后一步的互斥选择，最后写初始化和计算顺序。爬楼梯按最后一步分解；打家劫舍按最后一家是否偷分解；乘积最大子数组需要最大和最小两个状态，因为乘负数会交换大小。滚动数组只在理解完整状态依赖后使用。')
q(70,'爬楼梯','climbing-stairs','dp-linear','每次可走 1 或 2 阶，问到达第 n 阶有多少种不同走法。','到第 i 阶的最后一步要么从 i-1 走 1 阶，要么从 i-2 走 2 阶，两类不重叠，所以 f[i]=f[i-1]+f[i-2]。','定义 f[0]=1 表示不走也是一种完整前缀，f[1]=1；按 i 从 2 到 n 递推；只依赖前两项，可用 a,b 滚动','f[0]=1 是计数的单位元；若误设为 0，会少算从起点一次走 2 阶的路径。','时间 O(n)，额外空间 O(1)。','''
def climbStairs(n):
    a, b = 1, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
''','n=4：f0=1,f1=1,f2=2,f3=3,f4=5；最后一步分成 3+2 种。')
q(118,'杨辉三角','pascals-triangle','dp-linear','返回杨辉三角前 numRows 行，每行两端为 1，中间等于上一行相邻两项之和。','状态 row[i][j] 表示第 i 行第 j 项，转移只依赖上一行 j-1 与 j。','每行先初始化为全 1；内部位置填上一行相邻两项之和；将整行加入结果','边界不能访问上一行越界位置；每行要新建列表，避免多行共享同一对象。','时间 O(r²)，输出空间 O(r²)，r=numRows。','''
def generate(numRows):
    ans = []
    for i in range(numRows):
        row = [1] * (i + 1)
        for j in range(1, i):
            row[j] = ans[-1][j-1] + ans[-1][j]
        ans.append(row)
    return ans
''','5 行 → [[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]]。')
q(198,'打家劫舍','house-robber','dp-linear','一排房屋各有非负金额，不能偷相邻两家，求最多金额。','设 f[i] 为前 i 家最优。最后一家不偷得 f[i-1]；偷则前一家不能偷，得 f[i-2]+nums[i-1]。','空前缀收益 0；逐家计算 new=max(prev1,prev2+x)；滚动更新前两项','选择“偷第 i 家”时接的是前 i-2 家最优，不是简单把奇数或偶数位置相加。','时间 O(n)，空间 O(1)。','''
def rob(nums):
    prev2 = prev1 = 0
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1
''','[2,7,9,3,1]：逐步最优 2,7,11,11,12，最终选 2+9+1。')
q(152,'乘积最大子数组','maximum-product-subarray','dp-linear','非空整数数组中求非空连续子数组的最大乘积。','必须以当前数结尾的最大积 hi 与最小积 lo 同时维护；负数乘 lo 可变成最大正数。','以首数初始化 hi,lo,best；对新数 x，同步比较 x、旧 hi*x、旧 lo*x；更新全局最大','不能先改 hi 再用新 hi 算 lo；0 会自然重启，不需要删除 0。','时间 O(n)，空间 O(1)。','''
def maxProduct(nums):
    hi = lo = best = nums[0]
    for i in range(1, len(nums)):
        x = nums[i]
        hi, lo = max(x, hi*x, lo*x), min(x, hi*x, lo*x)
        best = max(best, hi)
    return best
''','[-2,3,-4]：读 3 后 hi=3,lo=-6；再乘 -4 得 hi=24。')
q(32,'最长有效括号','longest-valid-parentheses','dp-linear','只含左右括号的字符串，求最长合法连续子串长度。','dp[i] 为以 i 结尾的最长合法段。仅 s[i] 为右括号才可能非零；跳过紧邻合法段后，检查前一个字符能否与当前配对。','令 j=i-dp[i-1]-1；若 j≥0 且 s[j] 为左括号，则 dp[i]=dp[i-1]+2；再加 j 左侧紧接的合法段 dp[j-1]','必须把相邻合法段接上，例如 ()()；j<0 要先判断，避免 Python 负下标误读尾部。','时间 O(n)，空间 O(n)。','''
def longestValidParentheses(s):
    dp = [0] * len(s)
    best = 0
    for i in range(1, len(s)):
        if s[i] == ')':
            j = i - dp[i-1] - 1
            if j >= 0 and s[j] == '(':
                dp[i] = dp[i-1] + 2 + (dp[j-1] if j > 0 else 0)
                best = max(best, dp[i])
    return best
''','")()())" → 4；"()(())" 末位跨过内部 () 后匹配，再接左边 ()，得 6。')

group('dp-bag','14 · DP 二：容量、完全背包、0/1 背包与切分','容量 DP 问“恰好达到状态 i 时，最少几步/是否可行”。完全背包允许重复选择，金额从小到大；0/1 背包每项最多一次，压缩后容量倒序。单词拆分把每个可匹配单词视为一条从前缀 j 到 i 的边。区分求最小值、求可行性和求方案数，初始化与聚合运算不同。')
q(279,'完全平方数','perfect-squares','dp-bag','正整数 n，求和为 n 的完全平方数的最少数量，平方数可重复使用。','dp[i] 为凑成 i 的最少数量；最后选 j²，则来自 dp[i-j²]+1，对所有平方数取最小。','dp[0]=0，其余设无穷；金额 i 从 1 到 n；枚举 j²≤i 更新','允许平方数重复，例如 12=4+4+4；不是贪心地每次取最大平方数。','时间 O(n√n)，空间 O(n)。','''
def numSquares(n):
    dp = [0] + [float('inf')] * n
    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j*j] + 1)
            j += 1
    return dp[n]
''','n=12：最大平方贪心 9+1+1+1 共 4 个，DP 找到 4+4+4 共 3 个。')
q(322,'零钱兑换','coin-change','dp-bag','每种正面额硬币无限枚，求凑成 amount 的最少硬币数，无法凑成返回 -1。','dp[x] 表示恰好凑成 x 的最少枚数；最后一枚面额 c，则候选 dp[x-c]+1。','dp[0]=0，其余 amount+1 作不可达上界；金额升序，对 c≤x 尝试转移；末项仍大于 amount 则 -1','这是最少枚数，不是组合数；[2],amount=3 必须 -1；金额 0 需要 0 枚。','时间 O(amount·k)，空间 O(amount)。','''
def coinChange(coins, amount):
    dp = [0] + [amount + 1] * amount
    for total in range(1, amount + 1):
        for c in coins:
            if c <= total:
                dp[total] = min(dp[total], dp[total-c] + 1)
    return dp[amount] if dp[amount] <= amount else -1
''','[1,2,5], amount=11 → 3，最后一枚可选 1/2/5，最优为 5+5+1。')
q(416,'分割等和子集','partition-equal-subset-sum','dp-bag','正整数数组能否分成两个元素和相等的子集，每元素恰用一次。','总和必须为偶数；问题化为 0/1 背包能否恰好装满 total/2。dp[s] 表示使用已扫描元素能否凑出 s。','奇数总和直接 False；dp[0]=True；每个 x 让容量 s 从 target 倒序到 x，dp[s] |= dp[s-x]','容量必须倒序，保证 dp[s-x] 来自加入 x 之前；正序会把同一元素重复使用。','时间 O(n·S)，空间 O(S)，S=总和/2。','''
def canPartition(nums):
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for s in range(target, x - 1, -1):
            dp[s] = dp[s] or dp[s-x]
    return dp[target]
''','[1,5,11,5] → True；一组 [11]，另一组 [1,5,5]。')
q(139,'单词拆分','word-break','dp-bag','判断 s 能否由字典中若干非空单词连接而成，单词可重复。','dp[i] 表示前 i 个字符可被完全拆分；若某词 w 是以 i 结尾的后缀，且 dp[i-len(w)] 成立，就能转移到 i。','dp[0]=True；i 从 1 到 n；枚举单词，检查长度、此前可达状态、对应后缀是否匹配','“出现过字典里的词”不等于整个字符串能覆盖；不能漏掉 dp[0]。','字典 k 词、最大词长 L：时间 O(nkL)，空间 O(n)。','''
def wordBreak(s, wordDict):
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for word in wordDict:
            length = len(word)
            if i >= length and dp[i-length] and s[i-length:i] == word:
                dp[i] = True
                break
    return dp[-1]
''','"leetcode", ["leet","code"]：dp[4] 由 dp[0] 转移，dp[8] 由 dp[4] 转移。')

group('dp-sequence','15 · DP 三：序列、区间与二维对齐','连续子串不能跳字符，子序列允许跳。LIS 用“长度相同，末尾越小越容易续接”的支配关系压缩状态；最长回文子串按内部区间递推；LCS 和编辑距离按两个前缀对齐。二维 DP 先明确 dp[i][j] 对应前 i 个/前 j 个元素，避免状态下标和字符下标混淆。')
q(300,'最长递增子序列','longest-increasing-subsequence','dp-sequence','求严格递增子序列的最长长度，不要求连续。','基础 DP：f[i]=1+max(f[j])，其中 j<i 且 nums[j]<nums[i]。优化保存 tails[len-1] 为该长度递增序列的最小结尾；新 x 替换第一个≥x 的结尾。','建立空 tails；用 lower_bound 找第一个≥x 的位置；在末尾就追加，否则替换；最终 tails 长度即答案','严格递增应找 ≥x，重复数不能增加长度；tails 的值序列不一定是原数组中的同一条实际子序列。','时间 O(n log n)，空间 O(n)；基础 DP 为 O(n²)。','''
def lengthOfLIS(nums):
    from bisect import bisect_left
    tails = []
    for x in nums:
        i = bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
''','[10,9,2,5,3,7,101,18]：tails 最终 [2,3,7,18]，长度 4。')
q(5,'最长回文子串','longest-palindromic-substring','dp-sequence','求最长的连续回文子串，若并列可返回任意一个。','区间 DP 定义 pal[l][r]=(s[l]=s[r]) 且（长度≤2 或 pal[l+1][r-1]）。等价的中心扩展从单字符和字符间隙出发，省去整张表。','枚举每个位置的奇数中心 (i,i) 与偶数中心 (i,i+1)；只要两端相等就扩展；更新最长合法区间','退出循环时 l、r 已越出合法回文，正确区间是 [l+1,r)，长度 r-l-1。','时间 O(n²)，额外空间 O(1)（不计返回字符串）。','''
def longestPalindrome(s):
    start = length = 0
    for i in range(len(s)):
        for l, r in ((i, i), (i, i+1)):
            while l >= 0 and r < len(s) and s[l] == s[r]:
                l -= 1
                r += 1
            if r - l - 1 > length:
                start, length = l + 1, r - l - 1
    return s[start:start+length]
''','"babad" → "bab" 或 "aba"；"cbbd" → "bb"，必须考虑偶数中心。')
q(1143,'最长公共子序列','longest-common-subsequence','dp-sequence','两个字符串中找最长的公共子序列长度，字符可不连续但相对顺序不变。','dp[i][j] 表示两个前缀的 LCS。末字符相同则 dp[i-1][j-1]+1；不同则舍弃一边末字符取 max(dp[i-1][j],dp[i][j-1])。','建立多一行一列的零表，空前缀 LCS=0；i,j 均从 1 开始；按相等与否转移','不是最长公共子串，不同时不能直接清零；字符访问用 i-1,j-1。','时间 O(mn)，空间 O(mn)，可滚动压成 O(min(m,n))。','''
def longestCommonSubsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
''','"abcde" 与 "ace" → 3；ace 可以跳过 b、d。')
q(72,'编辑距离','edit-distance','dp-sequence','用插入、删除、替换，每步代价 1，把 word1 变成 word2 的最少操作数。','dp[i][j] 是两个前缀的转换代价。末字符相等时沿对角；否则在删除 dp[i-1][j]、插入 dp[i][j-1]、替换 dp[i-1][j-1] 中取最小再加 1。','空串到长度 j 的串需 j 次插入，反向需 i 次删除；按 i,j 升序填表；返回 dp[m][n]','不同字符时三种操作不能漏；相同字符直接沿对角，不额外加 1。','时间 O(mn)，空间 O(mn)，可滚动压缩。','''
def minDistance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n+1) for _ in range(m+1)]
    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]
''','"horse"→"ros"：替换 h→r、删掉第三位 r、删 e，共 3 步。')

group('dp-grid','16 · DP 四：网格上的路径计数与最优值','网格只能向右或向下时，依赖图无环，每格只由上方和左方转移。计数题用加法，最短代价用 min 后加当前权重。滚动行中 dp[j] 更新前是上方，dp[j-1] 更新后是左方；循环方向就是状态语义的一部分。')
q(62,'不同路径','unique-paths','dp-grid','m×n 网格从左上走到右下，每步只能向右或向下，求路径条数。','到 (i,j) 的最后一步只有从上或从左两种，故 ways[i][j]=ways[i-1][j]+ways[i][j-1]。首行首列各只有 1 条路。','用全 1 一维数组表示第一行；从第二行开始，j 从 1 到 n-1；令 dp[j]+=dp[j-1]','不能把 dp[0] 改成 0，第一列仍只有一种走法；m,n 的 1×n 边界应返回 1。','时间 O(mn)，空间 O(n)。','''
def uniquePaths(m, n):
    dp = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]
    return dp[-1]
''','m=3,n=3：首行 [1,1,1]，第二行 [1,2,3]，第三行 [1,3,6]。')
q(64,'最小路径和','minimum-path-sum','dp-grid','非负权重网格，只能右移或下移，求左上到右下的最小权重和，含起终点。','dp[i][j]=grid[i][j]+min(上方最优,左方最优)，最优子结构来自最后一步只有两个来源。','dp 初始化无穷；起点设为自身；每格以旧 dp[j] 为上方、新 dp[j-1] 为左方更新','边界不存在的来源应设无穷，而非 0；起点不能重复累加。','时间 O(mn)，空间 O(n)，不修改输入。','''
def minPathSum(grid):
    n = len(grid[0])
    dp = [float('inf')] * n
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            if i == 0 and j == 0:
                dp[j] = value
            else:
                left = dp[j-1] if j else float('inf')
                dp[j] = value + min(dp[j], left)
    return dp[-1]
''','[[1,3,1],[1,5,1],[4,2,1]] → 7，路径 1→3→1→1→1。')

group('tricks','17 · 技巧：异或、投票、原地分区、置换与函数图','技巧不是背口令：异或抵消要求成对出现；投票要求多数元素确实存在；荷兰旗维护三个已分类区间；下一个排列只改变尽可能靠右的后缀；找重复数把数组下标看作函数图结点，重复值对应环入口。')
q(136,'只出现一次的数字','single-number','tricks','除一个元素只出现一次外，其余均恰出现两次，找单个元素。','异或满足 x^x=0、x^0=x、结合交换律，成对元素全部抵消。','ans=0；依次异或所有数；返回 ans','如果其他元素出现三次，这个方法不成立；负整数在 Python 中也可用异或抵消。','时间 O(n)，空间 O(1)。','''
def singleNumber(nums):
    ans = 0
    for x in nums:
        ans ^= x
    return ans
''','[4,1,2,1,2] → 4，因为 1 与 2 各抵消一次。')
q(169,'多数元素','majority-element','tricks','保证有一个元素出现次数大于 n/2，返回它。','Boyer–Moore 投票每次抵消一对不同元素，多数元素的剩余票不可能被全部抵消。','count=0 时选当前值为候选；同候选加一、不同减一；最终候选就是多数元素','如果题目不保证多数存在，必须再扫描计数验证；不要把“众数”与超过一半的多数混同。','时间 O(n)，空间 O(1)。','''
def majorityElement(nums):
    candidate, count = None, 0
    for x in nums:
        if count == 0:
            candidate = x
        count += 1 if x == candidate else -1
    return candidate
''','[2,2,1,1,1,2,2] → 2，票数抵消后候选仍为 2。')
q(75,'颜色分类','sort-colors','tricks','只含 0、1、2 的数组，一趟原地排成 0 区、1 区、2 区。','维护 [0,low) 为 0，[low,i) 为 1，(high,n) 为 2，[i,high] 未知。','遇 0 与 low 交换，low 和 i 前进；遇 1 仅 i 前进；遇 2 与 high 交换，high 后退但 i 不动','交换过来的末尾元素尚未分类，遇 2 后不能立刻 i++；这是最常见漏元素原因。','时间 O(n)，空间 O(1)。','''
def sortColors(nums):
    low = i = 0
    high = len(nums) - 1
    while i <= high:
        if nums[i] == 0:
            nums[low], nums[i] = nums[i], nums[low]
            low += 1
            i += 1
        elif nums[i] == 2:
            nums[i], nums[high] = nums[high], nums[i]
            high -= 1
        else:
            i += 1
''','[2,0,2,1,1,0] → [0,0,1,1,2,2]。')
q(31,'下一个排列','next-permutation','tricks','原地改为字典序紧邻的下一个排列；若已最大则变为最小。','尽量保持左侧不变：从右找到首个上升对的左元素 pivot，以右侧刚好更大的数替换，再把降序后缀反转成最小。','从右找 nums[i]<nums[i+1]；若存在，从右找首个 nums[j]>nums[i] 并交换；反转 i+1..n-1','比较必须严格；全降序时 i=-1，反转整个数组；重复值也能正确处理。','时间 O(n)，空间 O(1)。','''
def nextPermutation(nums):
    i = len(nums) - 2
    while i >= 0 and nums[i] >= nums[i+1]:
        i -= 1
    if i >= 0:
        j = len(nums) - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    l, r = i + 1, len(nums) - 1
    while l < r:
        nums[l], nums[r] = nums[r], nums[l]
        l += 1
        r -= 1
''','[1,3,2] → [2,1,3]；[3,2,1] → [1,2,3]。')
q(287,'寻找重复数','find-the-duplicate-number','tricks','长度 n+1 的数组，每项在 1..n，只有一个重复值但可多次出现；不改数组、O(1) 空间找它。','把 i→nums[i] 看成函数图。从 0 出发必入环；0 无入边，重复值对应路径进入环的结点，使用 Floyd 找入口。','slow=fast=0，先移动至相遇；一个指针重回 0；两者同步一步直到相遇，返回下标值','这是数值作为下一结点下标，不是对数组排序；值域 1..n 和 n+1 长度是论证关键。','时间 O(n)，空间 O(1)，不修改输入。','''
def findDuplicate(nums):
    slow = fast = 0
    while True:
        slow, fast = nums[slow], nums[nums[fast]]
        if slow == fast:
            break
    entry = 0
    while entry != slow:
        entry, slow = nums[entry], nums[slow]
    return entry
''','[1,3,4,2,2] → 函数路径 0→1→3→2→4→2，入口 2 即重复数。')
FOUNDATIONS = '''<section class="intro" id="basics"><h2>先补最少的基础：能看懂代码，再学解题模式</h2>
<p>这一节从零约定本书的语言。先看数组 <code>[2,7,11]</code>：它有3个元素，下标从0开始，<code>nums[0]</code> 是2、<code>nums[1]</code> 是7。问题说“返回下标”，答案便是0和1；说“返回数值”，才是2和7。下标是位置，值是位置里装的内容，两者不能混用。</p>
<h3>1. 变量、条件与循环：程序怎样一步步执行</h3>
<p><code>total = 0</code> 是把变量total设为0，<code>total += 2</code> 等同于 <code>total = total + 2</code>。<code>if x &gt; 0:</code> 后缩进的代码只在条件成立时执行；<code>==</code> 判断相等，单个 <code>=</code> 则是赋值。<code>and</code> 要求两条件都真，<code>or</code> 要求至少一个真，<code>not</code> 取反。</p>
<pre><code>nums = [2, 7, 11]
total = 0
for i, x in enumerate(nums):
    total += x
# 三轮分别是 (i,x,total)=(0,2,2)、(1,7,9)、(2,11,20)</code></pre>
<p><code>enumerate</code> 同时给下标i和元素x；<code>range(1,4)</code> 依次给1、2、3，右端4不包含。<code>while 条件:</code> 只要条件仍真就重复，因此循环体必须让状态朝结束方向改变。<code>break</code> 退出当前循环，<code>continue</code> 跳过本轮剩余代码，<code>return</code> 则立即结束整个函数并交回答案。<code>a,b=b,a+b</code> 的右边先用旧值计算，再同时赋值，不会先改a再算b。</p>
<h3>2. 列表、字典和集合：分别解决什么问题</h3>
<p><b>列表 list</b> 是有顺序的一排元素，<code>a=[3,1,3]</code> 保留两个3。<code>a.append(5)</code> 尾部追加，<code>a.pop()</code> 删除并返回末项；<code>len(a)</code> 求长度。<code>a[l:r]</code> 复制下标l到r之前的元素，故 <code>a[0:2]</code> 得到 <code>[3,1]</code>，复制多少项就花多少时间和空间。写成区间[l,r)同样表示含左端l、不含右端r，称“半开区间”；[l,r]则两端都含。<code>sorted(a)</code> 返回新排序列表，<code>a.sort()</code> 则修改原列表。</p>
<p><b>字典 dict</b> 是“键→值”的查询表。<code>seen={2:0,7:1}</code> 表示值2曾在下标0、值7曾在下标1；<code>seen[7]</code> 得1，<code>7 in seen</code> 判断是否有键7，<code>seen.get(11,0)</code> 在键不存在时给默认0。这种默认值常用于计数：<code>count[x]=count.get(x,0)+1</code>。键必须能稳定散列，列表不能直接作键，可改用不允许修改的 <code>tuple</code>（元组）。</p>
<p><b>集合 set</b> 只回答“在不在”，不记录重复次数。<code>set([3,1,3])</code> 只有1和3两个成员；<code>add</code> 加成员、<code>remove</code> 删成员。哈希指把键计算成存储位置的办法，字典与集合借它跳到少量候选处，所以平均查询近似一步；若只用列表逐项找，则可能检查整排。需要“出现几次”用字典，需要“出现过没有”才用集合。</p>
<p>字符串可像列表一样按下标读取或切片，但不能执行 <code>s[0]='a'</code> 原地改字符。<code>''.join(parts)</code> 把若干字符串连接起来；<code>ord('a')</code> 为97，所以小写字母c用 <code>ord(c)-97</code> 映射到0至25的计数槽位。<code>Counter</code> 是标准库提供的计数字典，未出现的键读取为0；<code>bisect_left</code> 用二分找第一个大于等于目标的位置；<code>heapq</code> 提供堆，含义在堆章节说明。<code>from collections import Counter</code> 是取用库中已有工具，不是本题另藏一段推导。</p>
<p>列表推导 <code>[x*2 for x in [1,3]]</code> 是“对每项算一次再收集”，得 <code>[2,6]</code>；<code>[0]*3</code> 得三个0。二维表用 <code>[[0]*3 for _ in range(2)]</code> 新建两行，变量 <code>_</code> 表示本轮序号用不上；不要写 <code>[[0]*3]*2</code>，后者让两行指向同一列表，改第一行会连第二行一起改。<code>a[-1]</code> 读末项；某下标可能是-1时要先判断边界，不能误把不存在的前驱当末项。</p>
<h3>3. 引用、链表与树：为什么值一样不等于同一个结点</h3>
<p>列表变量指向一个对象：<code>a=[1,2]; b=a</code> 后两变量指向同一列表，改 <code>b[0]=9</code> 会让a也变成 <code>[9,2]</code>；<code>b=a.copy()</code> 才新建外层列表。回溯记录答案用 <code>path.copy()</code>，是为了留下当前内容，而非一直指向正在变化的同一条path。</p>
<p>链表是一串结点对象，每个有 <code>val</code> 存数、<code>next</code> 指向下一个，末尾指向 <code>None</code>（没有对象）。对 <code>1→2→3</code>，变量cur若指着2，则 <code>cur.next</code> 指着3；把 <code>cur.next=None</code> 会断开通往3的链接。反转前先用nxt保存原后继，就不会找不到剩余链。<code>a is b</code> 问是否同一对象；两个分别新建的值8结点并不相交。</p>
<p>树把每个结点的后继改为 <code>left</code> 与 <code>right</code> 两个孩子；root是起点“根”，没有孩子的结点叫叶结点。parent是某结点的直接上层，祖先则包括更远上层。子树是某结点连同其所有后代。BST指二叉搜索树：左子树所有值比根小，右子树所有值比根大，后面的验证题会解释为何仅比较直接孩子还不够。</p>
<p><code>class</code> 定义一类对象，把一份数据与操作它的函数放在一起。<code>cache = LRUCache(2)</code> 建立一个容量2的实例，初始化函数 <code>__init__</code> 会运行；<code>self.data</code> 表示“这一个缓存自己的data”，另一个缓存有另一份。<code>cache.get(1)</code> 调用方法时，Python自动把cache作为self传进去；普通函数不用self。<code>node.next</code> 同样只是读取这个对象里名为next的字段。</p>
<h3>4. 函数、递归、栈与队列：暂存的到底是什么</h3>
<p><code>def f(x):</code> 定义函数，参数是本次输入，<code>return y</code> 把结果交给调用者。递归是函数把更小的同类问题交给自己，例如树高 <code>height(node)=1+max(height(left),height(right))</code>。到空结点时必须返回0，这个不再继续调用的条件叫“递归出口”。执行父结点时，程序会先等孩子返回，不能凭空同时知道所有子树答案。</p>
<p><b>栈</b> 像叠盘子，最后放的最先取。求只有根2、左孩子1的树高时，根的调用先暂存“等左边答案”，孩子又暂存自己的现场；空孩子返回0后，孩子算出1交给根，根再算出2。程序保存这些未完成调用的地方是调用栈。<code>nonlocal best</code> 允许内部函数更新外层变量best，常用于“递归返回一条路径，同时更新整棵树答案”。</p>
<p><b>队列</b> 像排队买票，最先进入的最先出去。<code>deque.append(x)</code> 加到尾部，<code>deque.popleft()</code> 从头取出，适合一层层处理树或图；<b>双端队列</b> 还允许从尾部 <code>pop()</code> 删除。不要把栈、队列与递归当成三个新算法，它们首先是不同的待办顺序：最新的先做，或最早的先做。</p>
<h3>5. 状态、不变量与动态规划：把术语换成可以检查的话</h3>
<p><b>状态</b> 是“此刻记住哪些信息，就足以继续计算”。例如当前读到第3项、此前总和5，便可用5继续加下一项；不必把前三项反复重加。<b>不变量</b> 是“每轮开始或结束都保证成立的事实”。移动零时可说“写指针w之前恰好存着已读到的全部非零数”，每写入一项就检查它仍成立；它用来解释代码为什么不会漏、乱或重复。</p>
<p><b>动态规划（DP）</b> 把相同的小问题答案存起来，让大问题直接复用。比如到第4阶的最后一步，要么从第3阶走1步，要么从第2阶走2步，因此 <code>f[4]=f[3]+f[2]</code>。这里“状态”是到第i阶的方案数f[i]，“转移”是由旧答案算新答案的规则；“初始化”给最小问题答案。<b>滚动数组</b> 只是当新答案仅依赖前两项时，只保留那两项而不保存整张表，并非另一种推导。</p>
<h3>6. 大 O：看输入扩大后，操作次数怎样增长</h3>
<p>n表示输入规模，例如数组长度。读 <code>nums[3]</code> 不必扫描前3项，访问次数不随n增长，记 <b>O(1)</b>。从头扫描一次需约n步，记 <b>O(n)</b>；两层各枚举n项共约n²对，记 <b>O(n²)</b>。输入从100变1000，一次扫描约放大10倍，枚举所有数对约放大100倍；这比纠结某一步多一次加法更重要。</p>
<p>每次排除一半候选：1024→512→…→1，仅10轮，这种增长记 <b>O(log n)</b>，本书对数可按以2为底理解。排序通常约 <b>O(n log n)</b>；枚举每项选/不选共有 <b>2^n</b> 种；排列n个不同数共有 <b>n!</b> 种（例如4!=4×3×2×1=24）。若输出本来就有这些数量，算法无法凭空省掉写出答案的代价。</p>
<p><b>额外空间</b> 看除输入与返回结果外，运行时还保留多少东西。两个指针用常量空间，复制n项的列表要O(n)，递归同时挂起h层调用要O(h)。两次顺序扫描是2n，仍记O(n)；嵌套while也未必O(n²)，如果每项总共只进栈一次、出栈一次，合计仍只有约2n次。字典的O(1)通常是平均情形；Python大整数的位数变长后，算术本身也会更贵。</p>
</section>'''

GROUP_START = {
    'hash': '先把名字译成操作：哈希表就是按键快速查询的字典；“补数”是使和达到目标还缺的那一个数，如目标9、当前7，补数就是2。“规范键”是为同类对象生成同一个表示，例如eat与tea都排序成aet。',
    'pointers': '这里“指针”通常只是一个下标变量，不是必须掌握的底层内存地址。相向指针从两端向中间走，例如l=0、r=5；同向指针都朝右，一个负责读取、一个负责写入。一次移动必须能说明：被丢掉的候选为什么不会更好。',
    'window': '窗口是一段连续位置，例如s[2:5]含下标2、3、4；滑动是每次增删两端少量元素。前缀和是从开头累加的和，例如[2,-1,3]的前缀为0、2、1、4，整段之外的一段可用两个前缀相减。单调队列是让候选值按一个方向排好、两端均可删除的队列。',
    'array': '数组在本书中用Python列表表示，矩阵是“列表里再放每一行”。m行n列中的matrix[i][j]先取第i行，再取第j列。原地修改是直接改变输入对象；前缀是当前位置前面的部分，后缀是后面的部分；几何变换则是把旧坐标算成新坐标。',
    'linked': '链表没有列表那样按下标直接跳到第i项的能力，只能顺着next走。虚拟头dummy是在真正头结点前临时放一个空结点，使“删第一个”也能写成“改前一个的next”。快慢指针是每轮分别走两步与一步的两个结点引用；归并是反复取两条有序链较小的头。',
    'tree': '树高是根到最远叶结点的结点数；直径则是任意两结点间最长路径的边数。“遍历”指按某种顺序访问每个结点：中序是左子树→根→右子树，前序是根→左→右，后序是左→右→根；层序则先根，再其孩子，再孙子。BST即前文的二叉搜索树。',
    'graph': '图由“点”和“边”组成，边表示可走通道或先后依赖。DFS（深度优先）沿一条路尽量走到底再回头；BFS（广度优先）先走完一步可达点，再两步可达点。连通块是一组能互相走到的点；入度是指向某点的依赖边数量；拓扑序是让所有先修任务都排在后修任务之前的顺序。Trie叫前缀树，单词共享的开头只存一份路径。',
    'backtrack': '回溯就是试一个选择，继续往下试，再撤销这个选择试另一条路。全排列问不同的摆放顺序；组合只问选了哪些数，不区分[2,3]与[3,2]；剪枝是发现这条路已不可能合法后立即停止，而不是把所有结果生成后再删。',
    'binary': '二分查找是在有序或能判断答案落在哪半边的候选中，每轮排除一半。区间[l,r)含l、不含r；[l,r]两端都含。lower_bound是“第一个大于等于目标的位置”，没有这样元素时返回n。旋转排序数组如[4,5,1,2,3]，来自把递增数组前面一段挪到末尾。',
    'stack': '栈是后进先出的待办列表，append入栈、pop出栈。单调栈额外要求栈内对应数值总是递增或递减，例如待解温度[75,71,69]递减；遇到72便可处理并弹出69和71。保存的是下标时，还可算两天距离或矩形宽度。',
    'heap': '堆是一种能快速拿出当前最小或最大元素的结构，只保证顶端极值，不保证整个列表已排序。最小堆顶是最小值；每次插入或取出后用约log n步恢复这一性质。前k大若保留[4,5,6]，最小堆顶4正是这三名里最弱的一名，新来7才值得替换它。',
    'greedy': '贪心是每步立即作一个局部选择，不回头枚举所有组合；正确前提是这个选择不会挡住某个更优答案。“支配”指一个候选在所有后续情况下都不差于另一个；“交换论证”是把最优方案的第一步换成贪心这一步，证明总结果不变差。',
    'dp-linear': 'DP是前文的动态规划；线性指按一排位置从前向后计算。有限状态指每个位置只需几种含义明确的数字，例如“以这里结尾的最大乘积/最小乘积”，而非记住此前所有子数组。“互斥选择”就是每个答案只属于一种分支，不重复相加。',
    'dp-bag': '背包只是把限制想成容量：有目标金额6，每选一个值2便占去2容量。完全背包允许同一个元素用多次，0/1背包只允许每个输入元素选或不选一次。可行性只问能否做到，用True/False；最优化问最少几次，用min；计数则把所有不同方案相加。',
    'dp-sequence': '子串必须连续，例如abcde中的bcd；子序列可以跳字符但不能换顺序，例如ace。LIS是“最长严格递增子序列”，LCS是“两串的最长公共子序列”。区间DP把一段起终点作为状态；二维前缀DP用“第一串前i项、第二串前j项”作状态，依赖较短前缀的答案。',
    'dp-grid': '网格DP把每格的答案写在同尺寸表里。只能右走或下走意味着不会走回已处理行列，依赖不会形成环。二维表可逐行压成一行，更新前的dp[j]还是上面格子的值，更新后的dp[j-1]则是左边格子的值；计数相加，路径代价则先取min再加本格。',
    'tricks': '异或^逐二进制位计算，同位相同为0、不同为1，所以x^x=0。投票通过配对抵消不同数，找数量超过一半的元素。分区是把数组划成几段、每段只放某类数；荷兰旗是0/1/2三段。字典序像查字典，从左找到第一个不同位置决定大小；函数图则把“下标i连到nums[i]”当成一条有向边。',
}

WALKTHROUGHS = {
    560: [
        '对[1,1,1]、k=2，初始freq={0:1}、total=0、ans=0。读第一项后total=1，要找旧前缀-1，没有；把前缀1记一次。读第二项后total=2，要找旧前缀0，有1次，所以ans=1；再记前缀2。读第三项后total=3，找前缀1，有1次，所以ans=2。',
        '为何存“次数”而非仅存在性？[0,0]、k=0中，读第一项前旧前缀0有1次，产生1条；读第二项前旧前缀0已有2次，产生2条，共3条。当前前缀必须在查询后才加入，否则会把“当前减当前”的空区间也算进去。'
    ],
    239: [
        '对[1,3,-1,-3,5]、k=3，队列存下标。读下标0的1得到[0]；读下标1的3，1更小且比3更早离窗，以后不可能赢过3，所以弹0，队列变[1]；读下标2的-1得到[1,2]，窗口[1,3,-1]最大值取nums[1]=3。',
        '读下标3的-3得到[1,2,3]，最大仍3。读下标4时，下标1已经不在窗口[2,4]，先从队首删除；新5又使尾部-3、-1都失去竞争力，全部弹出，再加4，队列只剩[4]，答案变5。队列里不是整个窗口，只是仍可能当最大值的候选。'
    ],
    76: [
        '用较短的s="AABBC"、t="ABC"亲手走：初始need={A:1,B:1,C:1}、missing=3。读第一个A后need[A]=0、missing=2；再读A后need[A]=-1、missing仍2，这个负数的意思是“多了一个A”，并非缺少负一个字符。',
        '接着读B，missing变1；第二个B只是多余；读到C时missing=0，窗口AABBC已覆盖。先记长度5。移出第一个多余A，need[A]由-1变0，仍然覆盖，所以继续缩，记录ABBC长度4。再移出A，need[A]由0变1，missing变1，说明再缩就缺A；停止收缩，最终返回ABBC。',
        'while missing==0不是“多跑几次碰运气”，而是在右端固定时找最靠右的合法左端。内层看似嵌套，但left最多从0走到n，每个字符最多入窗和出窗一次，总时间仍线性。'
    ],
    41: [
        '对[3,4,-1,1]，下标0读到3：3应放下标2，交换得[-1,4,3,1]；当前位置现在是-1，不在1..4，无需再处理。下标1读到4，与下标3交换得[-1,1,3,4]。',
        '仍停在下标1，因为交换过来的1还没放对；再与下标0交换得[1,-1,3,4]。最后从左检查，1在槽0正确，槽1本应是2却为-1，所以缺2。条件nums[nums[i]-1]!=nums[i]避免[1,1]把两个相同值交换到永远。',
        '虽然每个i里有while，每一次真正交换至少把一个数送到它自己的最终槽位，最多n个这样的槽，所以交换总量O(n)，不是每个i都各交换n次。'
    ],
    146: [
        '把循环哨兵记为R。容量2时初始R↔R；put(1,10)后R↔1↔R；put(2,20)后R↔1↔2↔R，左端1最久没用、右端2最新。字典data[1]直接指向结点1，所以get(1)不必从链头搜索。',
        'get(1)先_remove：把1的前驱R的next改到2，把2的prev改到R；再_recent把1接在末尾，得到R↔2↔1↔R。现在put(3,30)得到R↔2↔1↔3↔R，超过容量便删除R.next，也就是2，同时del data[2]。再get(2)才会正确返回-1。',
        'R的值不属于缓存，存在意义是统一首尾操作。删除/移动一个已知结点只改固定几个引用，所以O(1)；若用列表remove(1)，必须先找位置再搬移后续元素，就会随容量增长。'
    ],
    124: [
        '对根-10、左9、右20，且20的孩子为15与7这棵树，叶子15向父结点返回15，叶子7返回7。处理20时，完整路径15→20→7得到42，更新best=42；但向-10只能返回20+max(15,7)=35。',
        '为什么不能向父结点返回42？因为42已用了20的左右两条边；再连到-10，会在20出现三条岔路，已经不是一条简单路径。处理-10时完整候选为-10+9+35=34，向上返回25，但全树最大仍是之前的42。',
        '若只一个结点-3，左右贡献都是0，完整候选是-3，结果必须-3；这就是best从负无穷开始，而不是允许选一条得0的空路径。'
    ],
    437: [
        '沿10→5→3这一支，前缀和依次10、15、18。目标8时，到结点3便查询18-8=10；祖先前缀10出现过一次，减掉它，留下5→3这一条和8的路径。counts={0:1}中的空前缀使“从根就开始”的路径也能被同样规则统计。',
        '退出结点3时把counts[18]减回去，再去兄弟分支。字典应只记录“当前结点的祖先链”，不是此前访问过的所有结点；否则另一支某个前缀恰好差8，会被错误地拼成跨树枝路径。递归返回的是该子树中合格路径的条数，不是前缀和本身。'
    ],
    207: [
        '3门课，prerequisites=[[1,0],[2,1]]表示0先于1、1先于2。边建成0→1→2，入度degree=[0,1,1]；队列初始[0]。取出0表示已完成它，把1入度减到0并入队；再取1，把2减到0；最后done=3，能全部完成。',
        '若是0→1与1→0，degree=[1,1]，没有一门可先上，队列一开始就空，done=0小于2。因此“有向环”就是几门课互相等待，不是看到任何连线闭起来都能不分方向地判错。'
    ],
    208: [
        '先insert("app")：从空根逐字走a→p→p，在最后一个p的字典放结束键#。再insert("apple")时前三步都复用已有a→p→p，只新建l→e，并在e上放#；保存的是共享开头，不是把每个完整词作为一个字典键。',
        'search("ap")走完a、p后确有路径，但当前位置无#，所以不是完整词；startsWith("ap")只要求这段路径存在，因此为True。search("app")则在第二个p处找到#，即使还有l孩子也照样成立。“末尾标记”用于区分“走得到”与“恰有这个词”。'
    ],
    79: [
        '棋盘第一行AB、第二行CD，找ABD：从(0,0)的A开始，k=0匹配；临时把A格标None，再走到右邻(0,1)的B，k=1；把B也标None，再走下邻(1,1)的D，k=2恰为最后一字，于是返回True。',
        '这个True逐层返回时，B格、A格各恢复原字符；换成找ABA，B回头看原A格时那里是None，所以不能重复用。某次尝试失败后也恢复，下一条路线仍可合法使用该格。这就是“当前路径不能重复”与“所有搜索永远不能重复”的区别。'
    ],
    33: [
        '数组[4,5,6,7,0,1,2]找0：l=0,r=6，mid=3、值7。左半[4,5,6,7]递增，但0不在[4,7)内，所以丢掉含mid的左半，令l=4。',
        '现在mid=5、值1，左半[0,1]递增且0在[0,1)内，所以r=4。接着mid=4恰好为0，返回4。每步先检查相等，才把mid排除；如果省掉这一顺序或把边界不等号抄错，就会漏掉恰位于中点或端点的目标。'
    ],
    4: [
        '取a=[1,3]、b=[2,4]，两边共4项，左半需要2项。假设a切在i=1（左边取1项），那么b必须切在j=2-1=1。四个边界为al=1、ar=3、bl=2、br=4，左边[1,2]、右边[3,4]。',
        '只要al≤br且bl≤ar，左半任何数都不超过右半任何数，切分就成立。总数偶数，中间两数是左半最大2与右半最小3，中位数(2+3)/2=2.5。若总长奇数，左边预留多1项，直接取左半最大。',
        '为看懂二分方向，再试a=[1,2]、b=[3,4]的i=1：al=1、ar=2、bl=3、br=4，bl>ar表示a左边取少了，所以增大i；i=2、j=0后边界为2、+∞、-∞、3，切分正确。空侧用无穷表示“没有约束”，不是数组里真的存了无穷。'
    ],
    84: [
        '在[2,1,5,6,2,3]中，栈起始[-1]，-1是不存在的左边界。读下标0高度2入栈；下标1高度1使2出栈，弹后左界-1，宽1-(-1)-1=1，面积2。继续入1，然后下标2的5、下标3的6依次入栈。',
        '下标4高度2比6矮：弹下标3，左界为2，宽4-2-1=1，面积6；还比5矮，再弹下标2，左界变1，宽4-1-1=2，面积5×2=10。正是弹完后剩余的栈顶告诉我们，向左还能延伸到哪里。',
        '末尾补0会把仍在等“右边更矮柱子”的高度全部结算；否则单调上升输入[1,2,3]会一直压栈、漏算答案。一次弹出就确定一个高度的最大宽度，不必枚举所有左右端点。'
    ],
    322: [
        '先用coins=[2]、amount=4看重复使用：dp=[0,5,5,5,5]中的5表示不可能的上界；total=1仍不可达，total=2由dp[0]+1变1，total=4再用dp[2]+1变2。这里dp[2]已经用了2元，但允许再用同面额，所以复用是正确的。',
        '对[1,2,5]凑11，最后一枚若为5，需要先凑6（最少2枚：5+1），所以候选3枚；最后为1或2也各取此前最小值比较。程序按金额升序，因为所有coin正数，total-coin总是更小、已经算完。'
    ],
    416: [
        '用[2,3,3]，总和8、目标4看“每个位置只用一次”。初始只有dp[0]=True。处理第一个2，容量从4向2倒着看：s=4时dp[2]仍是False，所以dp[4]不变；到s=2才把dp[2]设True，表示用了这个唯一的2。',
        '若错误地正序，先在s=2设True，再在s=4读到刚改的dp[2]，就会误判2+2可达，等于把同一元素偷用了两次。[2,3,3]实际无法凑4，应False；它与完全背包中[2]凑4可重复使用形成直接对照。',
        '外层每处理一个x，就表示“现在允许使用的输入位置多了一个”；倒序只是让这一层在原地写入时仍读取上一层答案。两枚数值相同但位置不同的3仍可各用一次，不是按数值全局去重。'
    ],
    300: [
        '把[10,9,2,5,3,7,101,18]逐项读入，tails依次为[10]→[9]→[2]→[2,5]→[2,3]→[2,3,7]→[2,3,7,101]→[2,3,7,18]。数组第j格表示“已见过的长度j+1递增子序列中，最小的末尾值”。',
        '读3时替换5：同为长度2，[2,3]比[2,5]更容易接上未来4，所以保留较小结尾不会损失最佳长度。读18替换101同理。最后长度4，不表示必须输出tails本身这条序列；本题只问长度。重复数[2,2]必须替换第一个≥2的位置，不能追加，答案才仍为1。'
    ],
    1143: [
        '用text1="ab"、text2="acb"建前缀表。第0行[0,0,0,0]表示空串与任意前缀没有公共字符。处理a后，第1行成为[0,1,1,1]：与a相等时对角+1，接着遇c或b不等便保留已有的1。',
        '处理b时，第2行是[0,1,1,2]。最后一格对应ab与acb，末字符b相等，所以取上一行上一列（a与ac）的1再加1，得2；若末字符不同，则分别尝试“不要第一串末字”或“不要第二串末字”，取上格与左格较大者。',
        'dp行列比原串多1，是为了把“空前缀”存为第0行/列；因此dp[i][j]的末字符位置是i-1与j-1。子序列允许跳过c，若问连续公共子串则不能沿用这个“不等也保留”的转移。'
    ],
    72: [
        '先走最小例子word1="ab"、word2="ac"。空串一行是[0,1,2]，表示插入0、1、2个字符；处理a后为[1,0,1]：a→a不用改，a→ac加一个c。',
        '处理b的最后一格，对应ab→ac，末字不同。删b后a→ac的代价为dp[1][2]+1=2；给ab增加末字c，则先要ab→a，代价dp[2][1]+1=2；把b替换为c，只要此前a→a，代价dp[1][1]+1=1。所以本格选1。',
        '三个相邻格不是任意凑出来的：上格少了第一串末字，对应删除；左格少了目标末字，对应插入；左上两边各少一字，对应替换或相同字符直接沿用。空串边界填长度，保证这些操作在第一行第一列也有正确含义。'
    ],
    32: [
        '以"()(())"的下标0..5走到i=4时，子串s[3:5]是()，所以dp[4]=2。到i=5又见右括号，先跨过这段已配好的2项，j=5-dp[4]-1=2；s[2]恰为左括号，可以包成(())。',
        '先得内部2+新一对2=4；而j前面下标1已有一段()，dp[1]=2，继续接上，最终dp[5]=2+2+2=6。若只加新括号不接dp[j-1]，会误得4；若j<0不先判断，Python负下标会从尾部读字符，制造不存在的配对。',
        '这里dp[i]一定要求有效段“恰在i结尾”，不能存前i项见过的最大长度；全局最大由best单独记录。正因为结尾条件严格，才能用dp[i-1]知道要向左跳过多少个已经配好的字符。'
    ],
    139: [
        's="leetcode"、词表[leet,code]，dp[0]=True表示空前缀已经完整覆盖。i=1,2,3都没词匹配；i=4检查长度4的leet，s[0:4]相等且dp[0]为True，所以dp[4]=True。到i=8，code匹配s[4:8]且dp[4]为True，故dp[8]=True。',
        '若s="leetcodes"，前8项虽然可拆，末尾s没有对应字典词，dp[9]仍False；“找到过一个词”不等于“全部覆盖”。本题返回布尔可行性，不是最少词数；所以成功找到任一前缀分法就能break。'
    ],
}

def render():
    assert len(BANK) == 100 and len({q['id'] for q in BANK}) == 100
    nav = ''.join(f'<a href="#{key}">{escape(title)}</a>' for key, (title, _) in GROUPS.items())
    blocks = []
    for key, (title, lesson) in GROUPS.items():
        questions = [item for item in BANK if item['kind'] == key]
        links = ' · '.join(f'<a href="#lc-{item["id"]}">{item["id"]} {escape(item["title"])}</a>' for item in questions)
        blocks.append(f'<section class="category" id="{key}"><h2>{escape(title)}</h2><p class="category-foundation"><b>先把这类话说懂：</b>{escape(GROUP_START[key])}</p><p class="lesson">{escape(lesson)}</p><p class="question-links">{links}</p>')
        for item in questions:
            steps = ''.join(f'<li>{escape(step)}</li>' for step in item['steps'])
            walk = ''
            if item['id'] in WALKTHROUGHS:
                paragraphs = ''.join(f'<li>{escape(line)}</li>' for line in WALKTHROUGHS[item['id']])
                walk = f'<div class="state-walkthrough"><h4>把关键状态走完</h4><ol>{paragraphs}</ol></div>'
            blocks.append(f'''<article class="problem" id="lc-{item['id']}" data-search="{escape(str(item['id'])+' '+item['title']+' '+item['idea']+' '+title, quote=True)}">
<h3><span class="number">LC {item['id']}</span> {escape(item['title'])}</h3>
<p><b>题意：</b>{escape(item['task'])}</p>
<p><b>推导与核心思路：</b>{escape(item['idea'])}</p>
<p class="example"><b>走一遍：</b>{escape(item['example'])}</p>
{walk}
<h4>具体步骤</h4><ol>{steps}</ol>
<h4>Python 实现</h4><pre><code>{escape(item['code'])}</code></pre>
<p><b>复杂度：</b>{escape(item['cost'])}</p>
<p class="pitfall"><b>易错点与适用边界：</b>{escape(item['pitfall'])}</p>
<p class="source-link"><a href="https://leetcode.cn/problems/{item['slug']}/">官方题面 · LC {item['id']}</a> <a href="#top">返回导读 ↑</a></p>
</article>''')
        blocks.append('</section>')
    body = '\n'.join(blocks)
    page = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>LeetCode Hot 100：按解题模式学习的 Python 面试手册</title>
<meta name="description" content="100 道 Hot 100 原创中文讲解，17 个模式类别，动态规划细分为线性、背包、序列与网格；每题含推导、例子、步骤、Python、复杂度与易错点。">
<link rel="stylesheet" href="../assets/notes-shell.css?v=20261018"><link rel="stylesheet" href="book.css"></head>
<body class="notes-shell-page">
<nav class="notes-sitebar" aria-label="站点导航"><a class="notes-sitebar__brand" href="../"><span class="notes-sitebar__mark" aria-hidden="true"></span><span>Notes</span></a><span class="notes-sitebar__links"><a class="notes-sitebar__link" href="../">All Notes</a><a class="notes-sitebar__link" href="../../">Home</a></span></nav>
<header id="top"><p class="kicker">Interview Practice · Python 3</p><h1>LeetCode Hot 100<br>用模式压缩记忆，用不变量解释代码</h1><p class="lede">100 道题、17 个模式类别。先学每类为何能缩小搜索，再看同一思路怎样适应不同约束。每题都给出题意、推导、具体步骤、可实现的 Python 代码、复杂度与失败边界。</p><p><a href="../interview-offline/">面试学习总入口</a></p></header>
<div class="book-layout"><aside class="book-toc"><h2>模式目录</h2><nav aria-label="模式目录"><a href="#basics">00 · 从零补基础</a>NAV</nav></aside><main>
BASICS
<section class="intro" id="how-to"><h2>如何最快建立可迁移的解题能力</h2><p>例如 LC 1 的暴力解要为每个数在其余数里寻找补数，哈希将这段重复搜索压成一次查询。LC 560 表面换成“连续区间和”，本质仍是找补数，只是被查询对象变成旧的前缀和，而且需要记录次数。学习时把这个映射讲出来，比记两段代码更有用。</p>
<p><b>建议顺序：</b>先学习哈希、双指针、窗口、二分与线性 DP，再学链表、树、图；最后攻克回溯、单调栈、堆和困难题。每类先默写 1 道代表题，再用同类变体检查边界。目录按模式分组，题号保留官方编号，便于对照练习。</p>
<ol><li><b>第一轮：</b>只读“题意→推导→走一遍”，遮住代码，口头说明状态与不变量。</li><li><b>第二轮：</b>按步骤独立写代码，拿空/单元素、重复值、全负数、最短边界检查。</li><li><b>第三轮：</b>改变约束：能否含负数？能否重复选？要求连续还是子序列？根据失效条件切换模式。</li></ol>
<h3>学完后回来看：五组可以一起记的题</h3><ul><li>两数之和 → 前缀和计数 → 树上的路径总和：都是“当前累积值减目标，再查询此前出现过的值”；树题退出某条分支时还需撤销该分支的记录。</li><li>二叉树深度 → 直径 → 最大路径和：向父结点返回一条向下路线的贡献，整棵树的最佳答案则可以在某结点处连接左右两条。</li><li>每日温度 → 柱状图矩形 → 窗口最大值：删去以后再也不必保留的候选，分别在等到更高温、遇到更矮柱、或离开窗口时处理它。</li><li>爬楼梯 → 零钱兑换 → 分割等和：都按最后一步拆问题，计算规则分别是相加、取最少、判断能否做到；允许同一项重复使用与否，决定能否读本轮刚更新的状态。</li><li>最长公共子序列（LCS）→ 编辑距离：都比较“第一串前i字与第二串前j字”，一个求最多保留多少共同字，一个求最少改动多少次。</li></ul>
<h3>代码约定与复杂度记法</h3><p>代码使用 Python 3 标准库，采用普通函数便于离线练习。提交平台时将函数放进 <code>class Solution</code> 并添加首参数 <code>self</code>；LC 48 的 <code>rotateImage</code>、LC 240 的 <code>searchMatrixII</code> 应分别改回题目要求的 <code>rotate</code>、<code>searchMatrix</code>。内部递归函数引用外层函数时也要相应改成 <code>self.method(...)</code>；辅助局部函数不变。四道设计题直接提供类。</p><p><code>ListNode(val=0,next=None)</code>、<code>TreeNode(val=0,left=None,right=None)</code> 和随机链表的 <code>Node(val,next=None,random=None)</code> 使用平台定义；所有结点比较都指对象身份。复杂度默认按整数运算 O(1) 的面试模型；Python 大整数、字符串复制、排序和输出开销在相关题中单独说明。递归树题的栈深度是树高，极深输入可改迭代，不能用“理论正确”忽略运行时限制。</p>
<p>本书正文默认全部展开，可直接连续阅读与打印。搜索只帮助定位；打印会自动恢复全部题目。PDF 适合离线通读，在线版方便按锚点跳转。</p>
<div class="search-tools"><label for="problem-search">定位题号、题名或思路</label><input type="search" id="problem-search" placeholder="例如：416、背包、回溯、前缀和"><output id="match-count" aria-live="polite">100 道题</output><button type="button" id="show-all">显示全部</button></div></section>
BODY
<section id="sources" data-note-role="evidence-appendix"><h2>证据边界与资料索引</h2><p>题目范围对应力扣“LeetCode 热题 100”学习计划，100 个题号与类别覆盖该计划的当前公开清单；为帮助迁移学习，本书将动态规划重新细分为四类，并保留每题官方题面链接。题意是必要条件的原创自述，代码与教学步骤为独立编写，并非官方题解逐字转录。平台可能调整题单、限制或函数签名，练习时以对应官方题面为准。题目测试通过代表用例与小规模交叉检查，不能替代完整平台隐藏用例评测。</p><ul><li><a href="https://leetcode.cn/studyplan/top-100-liked/?isDark=false&amp;rawContent=false">力扣官方：LeetCode 热题 100</a></li><li><a href="https://leetcode.com/studyplan/top-100-liked/">LeetCode 官方：Top 100 Liked</a></li><li><a href="https://docs.python.org/3/library/collections.html">Python 标准库：collections</a></li><li><a href="https://docs.python.org/3/library/heapq.html">Python 标准库：heapq</a></li><li><a href="https://docs.python.org/3/library/bisect.html">Python 标准库：bisect</a></li></ul></section>
</main></div><script src="book.js" defer></script></body></html>'''
    Path(__file__).with_name('index.html').write_text(page.replace('NAV', nav).replace('BODY', body).replace('BASICS', FOUNDATIONS), encoding='utf-8')

if __name__ == '__main__':
    render()
