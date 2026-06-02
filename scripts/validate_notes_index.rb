#!/usr/bin/env ruby
# frozen_string_literal: true

require "set"
require "yaml"

ROOT = File.expand_path("..", __dir__)
NOTES_ROOT = File.join(ROOT, "notes")
NOTES_YAML = File.join(ROOT, "_data", "notes.yml")
NOTE_TEMPLATE = File.join(NOTES_ROOT, "NOTE_TEMPLATE.md")

BOOK_INDEX_URLS = {
  "/notes/llm-interview-question-bank/index.html" => "/notes/llm-interview-question-bank/",
  "/notes/math-interview-question-bank/index.html" => "/notes/math-interview-question-bank/"
}.freeze

ASSET_EXTENSIONS = /\.(?:css|js|png|jpe?g|gif|webp|svg|pdf|txt|md|json|woff2?|ttf|eot)\z/i
REFERENCE_ATTRIBUTES = /\b(?:src|href)=["']([^"']+)["']/i
CSS_URL_REFERENCES = /url\(\s*["']?([^"')]+)["']?\s*\)/i
IMAGE_TAG = /<img\b[^>]*>/i
ALT_ATTRIBUTE = /\balt=["']([^"']*)["']/i
BODY_CLASS = /<body\b[^>]*class=["'][^"']*\bnotes-shell-page\b[^"']*["'][^>]*>/i
BODY_TAG = /<body\b/i
NOTES_SITEBAR = /<nav\b[^>]*class=["'][^"']*\bnotes-sitebar\b[^"']*["'][^>]*>(.*?)<\/nav>/im
MAIN_TAG = /<main\b/i
MAIN_CLOSE_TAG = /<\/main>/i
SHELL_STYLESHEET = "notes-shell.css"
MATHJAX_MARKERS = [
  /\\\(/,
  /\\\[/,
  /\$\$/,
  /class=["'][^"']*\bmath-display\b/i
].freeze
IGNORED_FOR_MATH_SCAN = %r{<(script|style|pre|code)\b[^>]*>.*?</\1>}im
QUALITY_WARNING_PATTERNS = {
  "generation artifact" => /Generated locally|HTML generated|本地 HTML 生成|本地 HTML 报告生成|本 HTML 报告|本报告生成|报告生成日期|生成日期：20\d{2}-\d{2}-\d{2}|\d{4}-\d{2}-\d{2}\s*生成/i,
  "local temporary path" => %r{/Users/xxx|/tmp/|/Users/bytedance/Downloads}i,
  "download artifact wording" => /最终 HTML 路径|最终文件路径|文件位置：|报告文件：/i
}.freeze
CONTENT_SOURCE_TOP_PATTERNS = /(?:HTML 报告|材料来源|资料来源|来源[:：]|报告日期[:：]|生成日期[:：]|原始链接|下载 PDF|OpenCLI|抓取|本地路径|文件位置|single HTML note)/i
CONTENT_TERM_HEADING = /术语|概念|名词|关键词|词先对齐|什么叫|是什么意思|Terms|Glossary|符号|定义/i
CONTENT_EVIDENCE_HEADING = /证据|来源|资料|Source|References|边界|核验|参考/i
CONTENT_TERM_TEXT = /这里的.{0,30}(?:指|表示|意思是|是指)|所谓.{0,30}(?:是|指)|(?:什么叫|是什么意思|指的是|定义为|词先对齐)|\b[A-Z][A-Za-z0-9-]{1,}\b.{0,32}(?:指|表示|意思是|是指|是|代表)/
CONTENT_TEXT_TAG_STRIP = %r{<(script|style|nav|aside)\b[^>]*>.*?</\1>}im
CONTENT_TEXT_TAGS = /<[^>]+>/m
CONTENT_WARNING_MIN_CHARS = 4_500
CONTENT_WARNING_MIN_HEADINGS = 5
LLM_BANK_CHAPTER_PATH = %r{\Anotes/llm-interview-question-bank/chapters/[^/]+\.html\z}
MATH_BANK_CHAPTER_PATH = %r{\Anotes/math-interview-question-bank/chapters/[^/]+\.html\z}
BANK_CHAPTER_PATH = %r{\Anotes/(?:llm-interview-question-bank|math-interview-question-bank)/chapters/[^/]+\.html\z}
BOOK_CHAPTER_INDEXES = {
  "notes/llm-interview-question-bank" => File.join(NOTES_ROOT, "llm-interview-question-bank", "index.html"),
  "notes/math-interview-question-bank" => File.join(NOTES_ROOT, "math-interview-question-bank", "index.html")
}.freeze
CHAPTER_SECTION = /<section\b[^>]*class=["'][^"']*\bchapter\b[^"']*["'][^>]*>/i
CHAPTER_ORIENTATION = /class=["'][^"']*\bchapter-orientation\b[^"']*["']/i
CHAPTER_NAV = %r{<nav\b[^>]*class=["'][^"']*\bchapter-nav\b[^"']*["'][^>]*>.*?</nav>}im
HTML_ID_ATTRIBUTE = /\bid=["']([^"']+)["']/i
LLM_CHAPTER_MIN_CHARS = 1_200
LLM_CHAPTER_MIN_HEADINGS = 2
MATH_CHAPTER_MIN_CHARS = 5_000
MATH_CHAPTER_MIN_HEADINGS = 8
LLM_CHAPTER_SIGNAL_TEXT = /核心术语|术语|知识点|详细解答|标准答案|就地速答|代表笔试题|代表面试题|作答抓手|题型|追问|模板|速查|复盘|检查清单|验收|阅读顺序|参考入口|下一步/i
MATH_CHAPTER_SIGNAL_TEXT = /学习目标|概念起点|公式|符号|例题|详细解答|常见误区|反例|边界|检查清单|验收/i

def fail_with(messages)
  warn messages.join("\n")
  exit 1
end

def note_entry_files
  Dir.glob(File.join(NOTES_ROOT, "*", "*.html")).map do |path|
    relative = path.delete_prefix("#{ROOT}/")
    "/#{relative}"
  end.sort
end

def note_html_files
  Dir.glob(File.join(NOTES_ROOT, "**", "*.html")).sort
end

def document_head(content)
  content.match(%r{<head\b[^>]*>(.*?)</head>}im)&.captures&.first.to_s
end

def visible_text(content)
  content.gsub(CONTENT_TEXT_TAG_STRIP, " ")
         .gsub(CONTENT_TEXT_TAGS, " ")
         .gsub(/\s+/, " ")
         .strip
end

def heading_texts(content)
  content.scan(%r{<h[23]\b[^>]*>(.*?)</h[23]>}im).flatten.map do |heading|
    visible_text(heading)
  end
end

def article_content(content)
  content.match(%r{<article\b[^>]*>(.*?)</article>}im)&.captures&.first || content
end

def chapter_heading_texts(content)
  article_content(content).scan(%r{<h[2-4]\b[^>]*>(.*?)</h[2-4]>}im).flatten.map do |heading|
    visible_text(heading)
  end
end

def book_chapter_orders
  BOOK_CHAPTER_INDEXES.transform_values do |index_path|
    File.read(index_path).scan(%r{href=["']chapters/([^"']+\.html)["']}i).flatten.uniq
  end
end

def book_root_for(relative_path)
  BOOK_CHAPTER_INDEXES.keys.find { |book_root| relative_path.start_with?("#{book_root}/chapters/") }
end

def chapter_nav_hrefs(nav_html)
  nav_html.scan(/\bhref=["']([^"']+)["']/i).flatten.map do |href|
    File.basename(href.split("#", 2).first.split("?", 2).first)
  end
end

def external_reference?(reference)
  reference.start_with?("#", "mailto:", "tel:", "javascript:", "data:") ||
    reference.match?(%r{\A[a-z][a-z0-9+.-]*://}i) ||
    reference.start_with?("//")
end

def referenced_asset_path(html_path, reference)
  clean_reference = reference.split("#", 2).first.split("?", 2).first
  return nil if clean_reference.empty?
  return nil unless clean_reference.match?(ASSET_EXTENSIONS)

  if clean_reference.start_with?("/")
    File.join(ROOT, clean_reference.delete_prefix("/"))
  else
    File.expand_path(clean_reference, File.dirname(html_path))
  end
end

errors = []
warnings = []
notes = YAML.load_file(NOTES_YAML)
chapter_orders = book_chapter_orders
errors << "#{NOTES_YAML} must contain a YAML list" unless notes.is_a?(Array)
fail_with(errors) unless errors.empty?

errors << "Missing notes template: #{NOTE_TEMPLATE.delete_prefix("#{ROOT}/")}" unless File.file?(NOTE_TEMPLATE)

urls = notes.map { |note| note["url"] }
duplicate_urls = urls.group_by(&:itself).select { |_url, values| values.size > 1 }.keys
errors << "Duplicate notes.yml urls: #{duplicate_urls.join(', ')}" unless duplicate_urls.empty?

urls.each do |url|
  next if url.nil? || url.empty?

  candidate = File.join(ROOT, url.delete_prefix("/"))
  candidate = File.join(candidate, "index.html") if url.end_with?("/")
  errors << "notes.yml url has no file: #{url}" unless File.file?(candidate)
end

indexed_urls = urls.to_set
missing_index_entries = note_entry_files.reject do |url|
  indexed_urls.include?(url) || indexed_urls.include?(BOOK_INDEX_URLS.fetch(url, nil))
end
errors << "Notes HTML files missing from _data/notes.yml:\n  #{missing_index_entries.join("\n  ")}" unless missing_index_entries.empty?

missing_assets = []
note_html_files.each do |html_path|
  content = File.read(html_path)
  references = content.scan(REFERENCE_ATTRIBUTES).flatten + content.scan(CSS_URL_REFERENCES).flatten
  references.each do |reference|
    next if external_reference?(reference)

    asset_path = referenced_asset_path(html_path, reference)
    next if asset_path.nil?

    missing_assets << "#{html_path.delete_prefix("#{ROOT}/")} -> #{reference}" unless File.file?(asset_path)
  end
end
errors << "Missing local note assets:\n  #{missing_assets.join("\n  ")}" unless missing_assets.empty?

note_html_files.each do |html_path|
  relative = html_path.delete_prefix("#{ROOT}/")
  content = File.read(html_path)
  head = document_head(content)

  errors << "#{relative} contains Unicode replacement characters" if content.include?("\uFFFD") || content.include?("�")
  errors << "#{relative} must contain exactly one document <title> in <head>" unless head.scan(/<title\b/i).size == 1
  errors << "#{relative} must include viewport meta" unless head.match?(/<meta\b[^>]*name=["']viewport["']/i)

  shell_count = content.scan(SHELL_STYLESHEET).size
  errors << "#{relative} must include #{SHELL_STYLESHEET} exactly once, found #{shell_count}" unless shell_count == 1
  errors << "#{relative} body must include notes-shell-page class" if content.match?(BODY_TAG) && !content.match?(BODY_CLASS)

  content.scan(IMAGE_TAG).each do |tag|
    alt = tag.match(ALT_ATTRIBUTE)&.captures&.first
    errors << "#{relative} has <img> without non-empty alt: #{tag[0, 120]}" if alt.nil? || alt.strip.empty?
  end

  math_scan_content = content.gsub(IGNORED_FOR_MATH_SCAN, "")
  needs_mathjax = MATHJAX_MARKERS.any? { |pattern| math_scan_content.match?(pattern) }
  errors << "#{relative} appears to contain TeX/math markup but does not load MathJax" if needs_mathjax && !content.include?("MathJax")

  QUALITY_WARNING_PATTERNS.each do |label, pattern|
    next unless content.match?(pattern)

    warnings << "#{relative}: #{label}"
  end

  if relative.match?(BANK_CHAPTER_PATH)
    section_count = content.scan(CHAPTER_SECTION).size
    errors << "#{relative} must contain exactly one .chapter section, found #{section_count}" unless section_count == 1
    errors << "#{relative} chapter must include chapter-orientation" unless content.match?(CHAPTER_ORIENTATION)

    duplicate_ids = content.scan(HTML_ID_ATTRIBUTE).flatten.group_by(&:itself).select { |_id, values| values.size > 1 }.keys
    errors << "#{relative} has duplicate HTML ids: #{duplicate_ids.join(', ')}" unless duplicate_ids.empty?

    chapter_navs = content.scan(CHAPTER_NAV)
    errors << "#{relative} must contain exactly one chapter-nav, found #{chapter_navs.size}" unless chapter_navs.size == 1

    book_root = book_root_for(relative)
    if book_root
      order = chapter_orders.fetch(book_root)
      chapter_file = File.basename(relative)
      chapter_index = order.index(chapter_file)
      if chapter_index.nil?
        errors << "#{relative} is missing from #{book_root}/index.html chapter order"
      elsif chapter_navs.size == 1
        expected_hrefs = []
        expected_hrefs << order[chapter_index - 1] if chapter_index.positive?
        expected_hrefs << order[chapter_index + 1] if chapter_index < order.size - 1
        actual_hrefs = chapter_nav_hrefs(chapter_navs.first)
        unless actual_hrefs == expected_hrefs
          errors << "#{relative} chapter-nav links #{actual_hrefs.inspect} do not match index order #{expected_hrefs.inspect}"
        end
      end
    end

    chapter_text = visible_text(article_content(content))
    chapter_headings = chapter_heading_texts(content)

    if relative.match?(MATH_BANK_CHAPTER_PATH)
      warnings << "#{relative}: math chapter audit short article text (#{chapter_text.length} chars)" if chapter_text.length < MATH_CHAPTER_MIN_CHARS
      warnings << "#{relative}: math chapter audit few h2/h3/h4 sections (#{chapter_headings.size})" if chapter_headings.size < MATH_CHAPTER_MIN_HEADINGS
      warnings << "#{relative}: math chapter audit missing formula/example/boundary signals" unless chapter_text.match?(MATH_CHAPTER_SIGNAL_TEXT) || chapter_headings.any? { |heading| heading.match?(MATH_CHAPTER_SIGNAL_TEXT) }
    elsif relative.match?(LLM_BANK_CHAPTER_PATH)
      warnings << "#{relative}: llm chapter audit short article text (#{chapter_text.length} chars)" if chapter_text.length < LLM_CHAPTER_MIN_CHARS
      warnings << "#{relative}: llm chapter audit few h2/h3/h4 sections (#{chapter_headings.size})" if chapter_headings.size < LLM_CHAPTER_MIN_HEADINGS
      warnings << "#{relative}: llm chapter audit missing study/term/answer signals" unless chapter_text.match?(LLM_CHAPTER_SIGNAL_TEXT) || chapter_headings.any? { |heading| heading.match?(LLM_CHAPTER_SIGNAL_TEXT) }
    end
  end

  public_path = "/#{relative}"
  next if BOOK_INDEX_URLS.key?(public_path)
  next unless html_path.match?(%r{/notes/[^/]+/[^/]+\.html\z})

  nav_html = content.match(NOTES_SITEBAR)&.captures&.first.to_s
  nav_text = visible_text(nav_html)
  errors << "#{relative} notes navigation must show Notes / All Notes / Home" unless nav_text.include?("Notes") && nav_text.include?("All Notes") && nav_text.include?("Home")
  errors << "#{relative} must include a semantic <main> wrapper" unless content.match?(MAIN_TAG) && content.match?(MAIN_CLOSE_TAG)

  text = visible_text(content)
  headings = heading_texts(content)
  main_text = content.match(%r{<main\b[^>]*>(.*?)</main>}im)&.captures&.first || content
  first_main_text = visible_text(main_text)[0, 700].to_s
  has_terms = headings.any? { |heading| heading.match?(CONTENT_TERM_HEADING) } || text.match?(CONTENT_TERM_TEXT)
  has_evidence = content.include?('data-note-role="evidence-appendix"') ||
                 headings.any? { |heading| heading.match?(CONTENT_EVIDENCE_HEADING) }

  warnings << "#{relative}: content audit missing explicit term/concept explanations" unless has_terms
  warnings << "#{relative}: content audit missing evidence/source boundary section" unless has_evidence
  warnings << "#{relative}: content audit source/process wording appears near top" if first_main_text.match?(CONTENT_SOURCE_TOP_PATTERNS)
  warnings << "#{relative}: content audit short visible text (#{text.length} chars)" if text.length < CONTENT_WARNING_MIN_CHARS
  warnings << "#{relative}: content audit few h2/h3 sections (#{headings.size})" if headings.size < CONTENT_WARNING_MIN_HEADINGS
end

fail_with(errors) unless errors.empty?

puts "notes index ok: #{notes.size} entries, #{note_entry_files.size} top-level note html files"
unless warnings.empty?
  puts "notes quality warnings: #{warnings.size}"
  warnings.each { |warning| puts "  #{warning}" }
end
