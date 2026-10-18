"""对教材展示的原始代码执行代表用例、结点身份检查与小规模穷举交叉检查。"""
import ast
import copy
import itertools
import random
from collections import deque
from build import BANK, GROUPS, render

class ListNode:
    def __init__(self, val=0, next=None):
        self.val, self.next = val, next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right

class Node:
    def __init__(self, val=0, next=None, random=None):
        self.val, self.next, self.random = val, next, random

def linked(values):
    dummy = tail = ListNode()
    for x in values:
        tail.next = ListNode(x)
        tail = tail.next
    return dummy.next

def values(node):
    ans, seen = [], set()
    while node:
        assert node not in seen, '输出链表不能存在意外环'
        seen.add(node)
        ans.append(node.val)
        node = node.next
    return ans

def tree(data):
    if not data or data[0] is None:
        return None
    root = TreeNode(data[0])
    queue, source = deque([root]), iter(data[1:])
    for node in iter(queue.popleft, None):
        for side in ('left', 'right'):
            try:
                val = next(source)
            except StopIteration:
                return root
            if val is not None:
                child = TreeNode(val)
                setattr(node, side, child)
                queue.append(child)
        if not queue:
            break
    return root

NAMESPACE = dict(ListNode=ListNode, TreeNode=TreeNode, Node=Node)
FUNCS = {}
for item in BANK:
    syntax = ast.parse(item['code'])
    name = syntax.body[0].name
    exec(compile(syntax, f'LC {item["id"]}', 'exec'), NAMESPACE)
    FUNCS[item['id']] = NAMESPACE[name]

CHECKED = set()
ASSERTIONS = 0

def check(n, args, expected, normalize=lambda x: x, mutate=False):
    global ASSERTIONS
    args = copy.deepcopy(args)
    result = FUNCS[n](*args)
    actual = args[0] if mutate else result
    assert normalize(actual) == normalize(expected), (n, args, actual, expected)
    CHECKED.add(n)
    ASSERTIONS += 1

def nested_sorted(x):
    return sorted(tuple(sorted(row)) for row in x)

def tests():
    global ASSERTIONS
    check(1, ([2,7,11,15],9), [0,1]); check(1, ([3,3],6), [0,1])
    check(49, (['eat','tea','tan','ate'],), [['eat','tea','ate'],['tan']], nested_sorted)
    check(128, ([100,4,200,1,3,2,1],), 4); check(128, ([],), 0)
    check(283, ([0,1,0,3,12],), [1,3,12,0,0], mutate=True)
    check(11, ([1,8,6,2,5,4,8,3,7],),49)
    check(15, ([-1,0,1,2,-1,-4],), [[-1,-1,2],[-1,0,1]], nested_sorted)
    check(42, ([4,2,0,3,2,5],),9); check(42, ([],),0)
    check(3, ('abba',),2); check(3, ('',),0)
    check(438, ('cbaebabacd','abc'),[0,6])
    check(560, ([1,1,1],2),2); check(560, ([0,0],0),3)
    check(239, ([1,3,-1,-3,5,3,6,7],3),[3,3,5,5,6,7])
    check(76, ('ADOBECODEBANC','ABC'),'BANC'); check(76, ('a','aa'),'')
    check(53, ([-2,1,-3,4,-1,2,1,-5,4],),6); check(53, ([-3,-1],),-1)
    check(56, ([[1,3],[2,6],[8,10]],),[[1,6],[8,10]])
    check(189, ([1,2,3,4,5,6,7],3),[5,6,7,1,2,3,4],mutate=True)
    check(238, ([1,2,3,4],),[24,12,8,6]); check(238, ([0,2,3],),[6,0,0])
    check(41, ([3,4,-1,1],),2); check(41, ([1,1],),2)
    check(73, ([[1,1,1],[1,0,1],[1,1,1]],),[[1,0,1],[0,0,0],[1,0,1]],mutate=True)
    check(73, ([[0,1],[1,1]],),[[0,0],[0,1]],mutate=True)
    check(54, ([[1,2,3],[4,5,6],[7,8,9]],),[1,2,3,6,9,8,7,4,5])
    check(54, ([[1],[2],[3]],),[1,2,3])
    check(48, ([[1,2],[3,4]],),[[3,1],[4,2]],mutate=True)
    check(240, ([[1,4,7],[2,5,8],[3,6,9]],6),True)

    shared = linked([8,9]); a = ListNode(1,shared); b = ListNode(2,ListNode(3,shared))
    assert FUNCS[160](a,b) is shared; assert FUNCS[160](linked([1]),linked([1])) is None
    CHECKED.add(160); ASSERTIONS += 2
    check(206,(linked([1,2,3]),),[3,2,1],lambda x: values(x) if isinstance(x,ListNode) else x)
    head = linked([1,2,2,1]); before = values(head)
    assert FUNCS[234](head) and values(head) == before
    assert not FUNCS[234](linked([1,2])); CHECKED.add(234); ASSERTIONS += 2
    cyclic = linked([1,2,3]); cyclic.next.next.next = cyclic.next
    assert FUNCS[141](cyclic); assert not FUNCS[141](linked([1,2]))
    assert FUNCS[142](cyclic) is cyclic.next; assert FUNCS[142](linked([1])) is None
    CHECKED.update([141,142]); ASSERTIONS += 4
    for n,args,expected in [(21,(linked([1,2,4]),linked([1,3,4])),[1,1,2,3,4,4]),
        (2,(linked([9,9]),linked([1])),[0,0,1]),(19,(linked([1,2,3,4,5]),2),[1,2,3,5]),
        (24,(linked([1,2,3,4,5]),),[2,1,4,3,5]),(25,(linked([1,2,3,4,5]),3),[3,2,1,4,5]),
        (148,(linked([4,2,1,3]),),[1,2,3,4]),(23,([linked([1,4,5]),linked([1,3,4]),linked([2,6])],),[1,1,2,3,4,4,5,6])]:
        check(n,args,expected,lambda x: values(x) if isinstance(x,ListNode) else x)
    old = Node(7); old.next = Node(13); old.random = old; old.next.random = old
    new = FUNCS[138](old)
    assert new is not old and new.val == 7 and new.random is new
    assert new.next is not old.next and new.next.random is new
    CHECKED.add(138); ASSERTIONS += 2
    cache = FUNCS[146](2); cache.put(1,1); cache.put(2,2)
    assert cache.get(1) == 1; cache.put(3,3); assert cache.get(2) == -1
    cache.put(1,7); cache.put(4,4); assert cache.get(1) == 7 and cache.get(3) == -1
    CHECKED.add(146); ASSERTIONS += 3

    check(94,(tree([1,None,2,3]),),[1,3,2])
    check(104,(tree([3,9,20,None,None,15,7]),),3)
    flipped = FUNCS[226](tree([4,2,7,1,3,6,9]))
    assert FUNCS[94](flipped) == [9,7,6,4,3,2,1]; CHECKED.add(226); ASSERTIONS += 1
    check(101,(tree([1,2,2,3,4,4,3]),),True)
    check(543,(tree([1,2,3,4,5]),),3)
    check(102,(tree([3,9,20,None,None,15,7]),),[[3],[9,20],[15,7]])
    bst = FUNCS[108]([-10,-3,0,5,9]); assert FUNCS[94](bst)==[-10,-3,0,5,9] and FUNCS[98](bst)
    CHECKED.add(108); ASSERTIONS += 1
    check(98,(tree([2,1,3]),),True); check(98,(tree([5,1,4,None,None,3,6]),),False)
    check(230,(tree([3,1,4,None,2]),2),2)
    check(199,(tree([1,2,3,None,5,None,4]),),[1,3,4])
    flat = tree([1,2,5,3,4,None,6]); FUNCS[114](flat); chain=[]
    while flat:
        assert flat.left is None
        chain.append(flat.val); flat=flat.right
    assert chain==[1,2,3,4,5,6]; CHECKED.add(114); ASSERTIONS += 1
    rebuilt=FUNCS[105]([3,9,20,15,7],[9,3,15,20,7])
    assert FUNCS[102](rebuilt)==[[3],[9,20],[15,7]]; CHECKED.add(105); ASSERTIONS += 1
    check(437,(tree([10,5,-3,3,2,None,11,3,-2,None,1]),8),3)
    root=tree([3,5,1,6,2,0,8,None,None,7,4])
    assert FUNCS[236](root,root.left,root.left.right.right) is root.left
    CHECKED.add(236); ASSERTIONS += 1
    check(124,(tree([-10,9,20,None,None,15,7]),),42); check(124,(tree([-3]),),-3)
    check(200,([list('110'),list('010'),list('001')],),2)
    check(994,([[2,1,1],[1,1,0],[0,1,1]],),4)
    check(207,(2,[[1,0]]),True);check(207,(2,[[1,0],[0,1]]),False)
    trie=FUNCS[208]();trie.insert('apple')
    assert trie.search('apple') and not trie.search('app') and trie.startsWith('app')
    trie.insert('app'); assert trie.search('app');CHECKED.add(208);ASSERTIONS += 2
    check(46,([1,2,3],),list(itertools.permutations([1,2,3])),lambda a: sorted(tuple(x) for x in a))
    check(78,([1,2],),[[],[1],[2],[1,2]],nested_sorted)
    check(17,('23',),['ad','ae','af','bd','be','bf','cd','ce','cf'],sorted)
    check(39,([2,3,6,7],7),[[2,2,3],[7]],nested_sorted)
    check(22,(3,),['((()))','(()())','(())()','()(())','()()()'],sorted)
    board=[list('AB'),list('CD')]; check(79,(board,'ABD'),True);check(79,(board,'ABA'),False)
    check(131,('aab',),[['a','a','b'],['aa','b']],nested_sorted)
    queens=FUNCS[51](4);assert len(queens)==2
    for board in queens:
        coords=[(r,row.index('Q')) for r,row in enumerate(board)]
        assert len({c for r,c in coords})==4 and len({r-c for r,c in coords})==4 and len({r+c for r,c in coords})==4
    CHECKED.add(51);ASSERTIONS += 3

    check(35,([1,3,5,6],2),1);check(35,([],3),0)
    check(74,([[1,3,5],[7,9,11]],9),True)
    check(34,([5,7,7,8,8,10],8),[3,4]);check(34,([],8),[-1,-1])
    check(33,([4,5,6,7,0,1,2],0),4)
    check(153,([3,4,5,1,2],),1)
    check(4,([1,3],[2]),2);check(4,([1,2],[3,4]),2.5);check(4,([],[1]),1)
    check(20,('()[]{}',),True);check(20,('([)]',),False)
    stack=FUNCS[155]();stack.push(-2);stack.push(0);stack.push(-3)
    assert stack.getMin()==-3;stack.pop();assert stack.top()==0 and stack.getMin()==-2
    CHECKED.add(155);ASSERTIONS += 2
    check(394,('3[a2[c]]',),'accaccacc');check(394,('10[a]',),'a'*10)
    check(739,([73,74,75,71,69,72,76,73],),[1,1,4,2,1,1,0,0])
    check(84,([2,1,5,6,2,3],),10)
    check(215,([3,2,1,5,6,4],2),5)
    check(347,([1,1,1,2,2,3],2),[1,2],sorted)
    finder=FUNCS[295]();finder.addNum(1);finder.addNum(2);assert finder.findMedian()==1.5
    finder.addNum(3);assert finder.findMedian()==2;CHECKED.add(295);ASSERTIONS += 2
    check(121,([7,1,5,3,6,4],),5)
    check(55,([2,3,1,1,4],),True);check(55,([3,2,1,0,4],),False)
    check(45,([2,3,1,1,4],),2);check(45,([0],),0)
    check(763,('ababcbacadefegdehijhklij',),[9,7,8])
    check(70,(4,),5);check(118,(5,),[[1],[1,1],[1,2,1],[1,3,3,1],[1,4,6,4,1]])
    check(198,([2,7,9,3,1],),12);check(152,([-2,3,-4],),24)
    check(32,(')()())',),4);check(32,('()(())',),6)
    check(279,(12,),3);check(322,([1,2,5],11),3);check(322,([2],3),-1)
    check(416,([1,5,11,5],),True);check(416,([1,2,5],),False)
    check(139,('leetcode',['leet','code']),True)
    check(300,([10,9,2,5,3,7,101,18],),4)
    assert FUNCS[5]('babad') in ('bab','aba');CHECKED.add(5);ASSERTIONS += 1
    check(5,('cbbd',),'bb');check(1143,('abcde','ace'),3);check(72,('horse','ros'),3)
    check(62,(3,3),6);check(64,([[1,3,1],[1,5,1],[4,2,1]],),7)
    check(136,([4,1,2,1,2],),4);check(169,([2,2,1,1,1,2,2],),2)
    check(75,([2,0,2,1,1,0],),[0,0,1,1,2,2],mutate=True)
    check(31,([1,3,2],),[2,1,3],mutate=True);check(31,([3,2,1],),[1,2,3],mutate=True)
    check(287,([1,3,4,2,2],),2)
    assert len(CHECKED)==100, sorted({x['id'] for x in BANK}-CHECKED)

def crosschecks():
    rng=random.Random(100)
    for _ in range(150):
        n=rng.randint(1,8);a=[rng.randint(-3,3) for _ in range(n)]
        k=rng.randint(-4,4)
        segments=[a[i:j] for i in range(n) for j in range(i+1,n+1)]
        check(560,(a,k),sum(sum(s)==k for s in segments))
        check(53,(a,),max(map(sum,segments)))
        def product(seq):
            out=1
            for x in seq:out*=x
            return out
        check(152,(a,),max(map(product,segments)))
        check(238,(a,),[product(a[:i]+a[i+1:]) for i in range(n)])
        check(41,(a,),next(x for x in range(1,n+2) if x not in a))
        check(15,(a,),[list(s) for s in {tuple(sorted(c)) for c in itertools.combinations(a,3) if sum(c)==0}],nested_sorted)
        positives=[abs(x) for x in a]
        check(42,(positives,),sum(min(max(positives[:i+1]),max(positives[i:]))-x for i,x in enumerate(positives)))
        check(84,(positives,),max(min(positives[i:j])*(j-i) for i in range(n) for j in range(i+1,n+1)))
        window=rng.randint(1,n)
        check(239,(a,window),[max(a[i:i+window]) for i in range(n-window+1)])
        check(739,(a,),[next((j-i for j in range(i+1,n) if a[j]>x),0) for i,x in enumerate(a)])
        all_subsets=[c for length in range(n+1) for c in itertools.combinations(range(n),length)]
        check(198,(positives,),max(sum(positives[i] for i in c) for c in all_subsets if all(c[j+1]>c[j]+1 for j in range(len(c)-1))))
        check(300,(a,),max(len(c) for c in all_subsets if all(a[c[j]]<a[c[j+1]] for j in range(len(c)-1))))
        vals=[x+1 for x in positives];total=sum(vals)
        check(416,(vals,),total%2==0 and any(sum(vals[i] for i in c)==total//2 for c in all_subsets))
        ordered=sorted(a);target=rng.randint(-4,4)
        check(35,(ordered,target),sum(x<target for x in ordered))
        hits=[i for i,x in enumerate(ordered) if x==target]
        check(34,(ordered,target),[hits[0],hits[-1]] if hits else [-1,-1])
        split=rng.randint(0,n);left=sorted(a[:split]);right=sorted(a[split:])
        expected=ordered[n//2] if n%2 else (ordered[n//2-1]+ordered[n//2])/2
        check(4,(left,right),expected)
        permutations=sorted(set(itertools.permutations(a)))
        idx=permutations.index(tuple(a));expected=list(permutations[(idx+1)%len(permutations)])
        check(31,(a,),expected,mutate=True)
    for size in range(0,9):
        for chars in itertools.product('()',repeat=size):
            s=''.join(chars);best=0
            for i in range(size):
                balance=0
                for j in range(i,size):
                    balance+=1 if s[j]=='(' else -1
                    if balance<0:break
                    if balance==0:best=max(best,j-i+1)
            check(32,(s,),best)

if __name__=='__main__':
    tests();crosschecks();render()
    print(f'PASS: {len(CHECKED)}/100 题覆盖，{ASSERTIONS} 次断言；17 个模式；HTML 已重建。')
