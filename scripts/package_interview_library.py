#!/usr/bin/env python3
"""Package thematic PDFs with an offline, actual-page-number topic search."""
from pathlib import Path
import hashlib
import html
import json
import re
import shutil
import subprocess
from urllib.parse import quote
from zipfile import ZipFile, ZIP_DEFLATED

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
CATALOG = json.loads((ROOT / "scripts/interview_books.json").read_text())["books"]
DEST = ROOT / "output/pdf/量化面试分册"
DEST.mkdir(parents=True, exist_ok=True)
books, topics = [], []


def walk_outline(items, reader, book, trail=()):
    parent_trail = trail
    for item in items:
        if isinstance(item, list):
            walk_outline(item, reader, book, parent_trail)
            continue
        title = re.sub(r"\s+", " ", str(item.get("/Title", ""))).strip("# ")
        page = reader.get_destination_page_number(item) + 1
        if not 1 <= page <= len(reader.pages):
            raise ValueError(f"Bad bookmark {book['title']}: {title}")
        if len(title) >= 4 and page > 2 and not title.startswith(("复习目标", "证据边界")):
            topics.append({"title": title, "book": book["title"],
                           "key": book["key"], "context": " / ".join(trail),
                           "href": book["href"] + f"#page={page}", "page": page})
        parent_trail = (*trail, title)


for key, entry in sorted(CATALOG.items(), key=lambda x: (x[1].get("group", ""), x[0])):
    if entry.get("archive"):
        continue
    source = ROOT / "notes/downloads" / entry["file"]
    if not source.exists():
        raise FileNotFoundError(f"Export {key} before packaging: {source}")
    reader = PdfReader(source)
    name = re.sub(r'[<>:"/\\|?*]', "-", entry["title"]) + ".pdf"
    relative = Path(entry["group"]) / name
    target = DEST / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    book = {"key": key, "title": entry["title"], "group": entry["group"],
            "file": relative.as_posix(), "href": quote(relative.as_posix()),
            "pages": len(reader.pages), "bytes": source.stat().st_size,
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest()}
    books.append(book)
    walk_outline(reader.outline, reader, book)

payload = json.dumps(topics, ensure_ascii=False).replace("</", "<\\/")
cards = []
for group in sorted({b["group"] for b in books}):
    cards.append("<h2>" + html.escape(group.replace("_", " · ")) + "</h2><div class=books>")
    for b in books:
        if b["group"] == group:
            cards.append(f'<a class=book href="{b["href"]}"><strong>{html.escape(b["title"])}</strong>'
                         f'<span>{b["pages"]}页 · {b["bytes"]/1048576:.1f} MB</span></a>')
    cards.append("</div>")
page = """<!doctype html><html lang=zh-CN><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>量化面试分册检索</title>
<style>body{max-width:1000px;margin:auto;padding:24px;font:17px/1.7 system-ui,sans-serif;color:#242b30;background:#faf9f6}
h1{font-size:30px}h2{font-size:23px;margin-top:32px}a{color:#873e25}input{box-sizing:border-box;width:100%;padding:12px;font:inherit}
.books{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:12px}.book{display:block;padding:14px;border:1px solid #ddd;background:white;border-radius:6px;text-decoration:none}
.book span{display:block;color:#666;font-size:14px}.result,.book{overflow-wrap:anywhere}.result{padding:10px 0;border-bottom:1px solid #ddd}.muted{font-size:14px;color:#666}.route{padding:14px;border-left:4px solid #b3663e;background:#f1e9dd}
button{font:inherit;margin:4px;padding:4px 9px;cursor:pointer}mark{background:#f7e4b6}</style>
<h1>量化面试：按问题找分册</h1>
<p>先解压整个压缩包，再打开本文件。页面、搜索和PDF均不需要联网；书中外部参考链接需要联网。</p>
<div class=route><strong>从零学习：</strong>数学起步 → 回归与正则化 → 概率统计基础 → 估计与推断 → 机器学习 → 深度学习。
<br>基础课慢讲；方法题按原题号练习；专项题按目标岗位选读。旧全量合集仅保留归档，不必继续从中翻找。
<br><strong>查题：</strong>输入关键词，点击结果会打开对应PDF及实际页码。PDF自带目录页码、章节和题目书签。</div>
<h2>关键词检索</h2><input id=q placeholder="例如：最小二乘、岭回归、PCA、最大似然、标准误">
<div id=quick></div><p id=status class=muted>输入关键词，最多展示80个匹配书签。</p><div id=results></div>
""" + "".join(cards) + """
<script>
const topics=PAYLOAD;
const q=document.getElementById('q'),out=document.getElementById('results'),status=document.getElementById('status');
const aliases={'最小二乘':['最小二乘','ols'],'岭回归':['岭回归','ridge'],'lasso':['lasso','套索'],'pca':['pca','主成分'],'最大似然':['最大似然','mle'],'标准误':['标准误','置信区间']};
function search(){const value=q.value.trim().toLowerCase();out.replaceChildren();if(!value){status.textContent='输入关键词，最多展示80个匹配书签。';return;}
 const keys=aliases[value]||[value];const hits=topics.filter(t=>keys.some(k=>(t.title+' '+t.book+' '+t.context).toLowerCase().includes(k)));
 const preferred={'最小二乘':'regression','ols':'regression','岭回归':'regression','ridge':'regression','lasso':'regression','最大似然':'statistics','mle':'statistics','pca':'ml','adam':'dl'};
 hits.sort((a,b)=>Number(b.key===preferred[value])-Number(a.key===preferred[value]));
 status.textContent='匹配 '+hits.length+' 条；显示前 '+Math.min(80,hits.length)+' 条。';
 for(const t of hits.slice(0,80)){const div=document.createElement('div');div.className='result';const a=document.createElement('a');a.href=t.href;a.textContent=t.title;
 const meta=document.createElement('div');meta.className='muted';meta.textContent=t.book+' · 第'+t.page+'页';div.append(a,meta);out.append(div);}}
q.addEventListener('input',search);
for(const word of ['最小二乘','岭回归','Lasso','PCA','最大似然','标准误','条件概率','Adam']){const b=document.createElement('button');b.textContent=word;b.onclick=()=>{q.value=word;search();};document.getElementById('quick').append(b);}
</script></html>""".replace("PAYLOAD", payload)
(DEST / "先打开这个-分册检索.html").write_text(page)
(DEST / "分册清单.json").write_text(json.dumps({"books": books, "topics": topics}, ensure_ascii=False, indent=2))
queries = [
    ("下标、平方和", "math", "下标"), ("配方与1.5", "math", "配方"),
    ("导数与链式法则", "math", "导数"), ("矩阵乘法与转置", "math", "矩阵"),
    ("逆矩阵与投影", "math", "解方程"), ("最小二乘从头算", "regression", "慢速起步：先用"),
    ("Ridge与Lasso", "regression", "把误差平方"), ("SVD与收缩", "regression", "谱视角"),
    ("估计与似然", "statistics", "MLE"), ("条件高斯与相关", "statistics", "多元高斯"),
    ("条件概率", "probability", "条件概率"), ("等待与递推", "expectation", "期望递推"),
    ("置信区间", "probability", "置信区间"), ("假设检验", "probability", "假设检验"),
    ("逻辑回归", "ml", "逻辑回归"), ("偏差与方差", "ml", "偏差与方差"),
    ("PCA", "ml", "PCA"), ("树与集成", "ml", "决策树"),
    ("时间验证", "ml", "时间验证"), ("RNN与LSTM", "dl", "RNN"),
    ("Transformer注意力", "dl", "注意力"), ("Adam与AdamW", "dl", "AdamW"),
    ("MoE", "dl", "MoE："), ("MTP", "dl", "MTP："), ("循环Transformer", "dl", "Looped"),
    ("动态规划", "leetcode", "动态规划"), ("窗口与前缀和", "programming", "滑动窗口"),
    ("风险与回测", "finance", "回测"),
]
rows = []
for label, key, needle in queries:
    matches = [t for t in topics if t["key"] == key and needle.lower() in t["title"].lower()]
    if not matches:
        raise ValueError(f"Missing quick-lookup topic: {label} / {key} / {needle}")
    t = matches[0]
    rows.append(f"<tr><td>{html.escape(label)}</td><td>{html.escape(t['book'])}</td><td>{t['page']}</td></tr>")
guide = """<!doctype html><html lang=zh-CN><meta charset=utf-8><title>分册书目与页码速查</title>
<style>@page{size:A4;margin:15mm}body{font:11pt/1.55 system-ui,sans-serif;color:#222}
h1{font-size:22pt}h2{font-size:15pt;break-after:avoid}table{border-collapse:collapse;width:100%;font-size:9pt}
th,td{padding:3px 7px;border-bottom:1px solid #ddd;text-align:left}tr{break-inside:avoid}thead{display:table-header-group}
.volumes{break-before:page}p{orphans:2;widows:2}</style><h1>量化面试分册：先按问题找书</h1>
<p>数字是对应分册的实际PDF页码，不是旧合编页码。手机不便打开HTML时，直接按下表找册、输入页码。
更多题目请展开该册书签栏；电脑解压后打开“先打开这个-分册检索.html”可全文搜索书签。</p>
<p>从零路线：数学起步 → 回归与正则化 → 概率统计基础 → 估计与推断 → 机器学习 → 深度学习。
先逐步跟算，再看后读的密集汇总；专项题按目标岗位选读。</p><table><thead><tr><th>想复习什么</th><th>打开哪册</th><th>页码</th></tr></thead><tbody>""" + "".join(rows) + "</tbody></table><section class=volumes><h2>全部分册</h2><table><thead><tr><th>分组</th><th>书名</th><th>页数</th></tr></thead><tbody>" + "".join(
    f"<tr><td>{html.escape(b['group'])}</td><td>{html.escape(b['title'])}</td><td>{b['pages']}</td></tr>"
    for b in books) + "</tbody></table><p>全量合集仅归档，不在本分册包中重复放置。每个PDF均保留公式与原题内容。</p></section></html>"
(DEST / "书目页码速查.html").write_text(guide)
subprocess.run(["node", str(ROOT / "scripts/render_library_guide.cjs"),
                str(DEST / "书目页码速查.html"), str(DEST / "先看-书目与页码速查.pdf")], check=True)
(DEST / "使用说明.txt").write_text(
    "先解压，再打开“先打开这个-分册检索.html”。所有PDF均本地可读。\n"
    "输入关键词可跳到对应册实际页码；也可在PDF阅读器中打开书签栏。\n"
    "部分阅读器不支持网页#page跳转时，请按结果显示的页码手动输入。\n"
    "全量合编不作为默认阅读入口；原题与更紧凑的旧解答仍在相应册的后读部分保留。\n")
archive = ROOT / "output/pdf/量化面试-分册与检索.zip"
with ZipFile(archive, "w", ZIP_DEFLATED, compresslevel=6) as zipped:
    allowed = {b["file"] for b in books} | {"先打开这个-分册检索.html", "分册清单.json", "使用说明.txt",
                                             "先看-书目与页码速查.pdf"}
    for name in sorted(allowed):
        zipped.write(DEST / name, name)
with ZipFile(archive) as zipped:
    assert zipped.testzip() is None
print(json.dumps({"books": len(books), "searchable_bookmarks": len(topics),
                  "archive": str(archive), "bytes": archive.stat().st_size}, ensure_ascii=False))
