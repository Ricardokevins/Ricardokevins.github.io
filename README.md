# Ricardokevins.github.io

个人学术网站与公开研究笔记，基于 Jekyll / AcademicPages。网站配置在 `_config.yml`，笔记索引在 `_data/notes.yml`；维护约束见 `AGENTS.md`。以下“上游模板说明”仅保留历史来源，不作为当前项目的维护流程。

## 本地运行与验证

需要 Ruby / Bundler、Python 3.10+；传统主题 JavaScript 打包还需要 Node.js / npm。CI 的 Ruby 版本见 `.github/workflows/deploy.yml`。

```sh
bundle install
bundle exec jekyll serve --config _config.yml,_config.dev.yml
```

```sh
ruby scripts/validate_notes_index.rb
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 -m unittest discover -s notes/llm-interview-question-bank/code -p 'test_*.py'
bundle exec jekyll build --destination _site
python3 scripts/validate_site.py _site
git diff --check
```

保留 `Gemfile.lock`；删除锁文件不是安全修复。`.bundle/config` 是忽略的本机配置，如果指向失效的临时 gem 目录，先检查 `bundle config`，不要清理其他项目的依赖。隔离构建时将 `_site` 替换为独立临时目录，避免覆盖其他任务的预览。

笔记索引检查验证结构、资源和本地保留路径；站点检查验证构建产物的 HTML / CSS 链接、锚点、重复 ID 与排除路径，不联网检查外部链接，也不代替内容审读或浏览器版面检查。

## 维护入口与隔离

- 量化、算法题库和原 unlisted 内容须同时由 `.gitignore` 与 `_config.yml` 隔离；Git 忽略不等于 Jekyll 排除。
- JavaScript 使用 `npm ci --ignore-scripts` 安装锁定依赖，`npm test` 运行导航回归，`npm run build:js` 重建实际加载的 `assets/js/main.min.js`。当前 jQuery 为兼容旧插件的 3.7.1；MathJax 使用已有本地 3.2.2 运行时。
- `scripts/check_site_frontend.cjs <隔离构建目录> <截图目录>` 验证首页、零宽导航恢复、公式和旧论文 URL；需当前 Node 环境能解析 Playwright 并有 Chromium。检查会启动独立无头浏览器，不附加用户的 Chrome；外部资源被替代，仅证明本地资源与交互行为。
- GitHub Pages 当前使用 `main` 分支根目录的 legacy 构建（2026-11-10 只读核实）。`.github/workflows/deploy.yml` 仅验证，不启用 Actions 部署；引用刷新先于验证构建，刷新后的源文件存为 Actions artifact，不自动提交回分支，因此不会凭空更新 legacy 站点。要自动刷新线上引用，需要另行授权回写源文件或切换部署方式。本地修改与验证不自动授权提交、推送或启用部署。
- 历史 TSV/BibTeX 导入器现在按脚本目录定位输入与输出，并转义元数据；运行仍会生成目标目录文件，不作为自动同步入口。`talkmap.py` 只有显式运行才访问地理编码服务，必须指定 `--output-dir`，不会导入时覆盖现有地图。

## 上游模板说明（历史）

A Github Pages template for academic websites. This was forked (then detached) by [Stuart Geiger](https://github.com/staeiou) from the [Minimal Mistakes Jekyll Theme](https://mmistakes.github.io/minimal-mistakes/), which is © 2016 Michael Rose and released under the MIT License. See LICENSE.

I think I've got things running smoothly and fixed some major bugs, but feel free to file issues or make pull requests if you want to improve the generic template / theme.

### Dependency security

Investigate the affected dependency, update it deliberately and retain the lockfile for reproducible builds.

# Instructions

1. Register a GitHub account if you don't have one and confirm your e-mail (required!)
1. Fork [this repository](https://github.com/academicpages/academicpages.github.io) by clicking the "fork" button in the top right. 
1. Go to the repository's settings (rightmost item in the tabs that start with "Code", should be below "Unwatch"). Rename the repository "[your GitHub username].github.io", which will also be your website's URL.
1. Set site-wide configuration and create content & metadata (see below -- also see [this set of diffs](http://archive.is/3TPas) showing what files were changed to set up [an example site](https://getorg-testacct.github.io) for a user with the username "getorg-testacct")
1. Upload any files (like PDFs, .zip files, etc.) to the files/ directory. They will appear at https://[your GitHub username].github.io/files/example.pdf.  
1. Check status by going to the repository settings, in the "GitHub pages" section
1. (Optional) Use the Jupyter notebooks or python scripts in the `markdown_generator` folder to generate markdown files for publications and talks from a TSV file.

See more info at https://academicpages.github.io/

## To run locally (not on GitHub Pages, to serve on your own computer)

1. Clone the repository and made updates as detailed above
1. Make sure you have ruby-dev, bundler, and nodejs installed: `sudo apt install ruby-dev ruby-bundler nodejs`
1. Run `bundle clean` to clean up the directory (no need to run `--force`)
1. Run `bundle install` to install Ruby dependencies. Diagnose installation errors without deleting `Gemfile.lock`.
1. Run `bundle exec jekyll liveserve` to generate the HTML and serve it from `localhost:4000` the local server will automatically rebuild and refresh the pages on change.

# Changelog -- bugfixes and enhancements

There is one logistical issue with a ready-to-fork template theme like academic pages that makes it a little tricky to get bug fixes and updates to the core theme. If you fork this repository, customize it, then pull again, you'll probably get merge conflicts. If you want to save your various .yml configuration files and markdown files, you can delete the repository and fork it again. Or you can manually patch. 

To support this, all changes to the underlying code appear as a closed issue with the tag 'code change' -- get the list [here](https://github.com/academicpages/academicpages.github.io/issues?q=is%3Aclosed%20is%3Aissue%20label%3A%22code%20change%22%20). Each issue thread includes a comment linking to the single commit or a diff across multiple commits, so those with forked repositories can easily identify what they need to patch.



bundle exec jekyll serve
