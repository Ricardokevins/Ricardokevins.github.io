#!/usr/bin/env ruby
# frozen_string_literal: true

require "set"
require "yaml"

ROOT = File.expand_path("..", __dir__)
NOTES_ROOT = File.join(ROOT, "notes")
NOTES_YAML = File.join(ROOT, "_data", "notes.yml")

BOOK_INDEX_URLS = {
  "/notes/llm-interview-question-bank/index.html" => "/notes/llm-interview-question-bank/",
  "/notes/math-interview-question-bank/index.html" => "/notes/math-interview-question-bank/"
}.freeze

ASSET_EXTENSIONS = /\.(?:css|js|png|jpe?g|gif|webp|svg|pdf|txt|md|json|woff2?|ttf|eot)\z/i
REFERENCE_ATTRIBUTES = /\b(?:src|href)=["']([^"']+)["']/i
CSS_URL_REFERENCES = /url\(\s*["']?([^"')]+)["']?\s*\)/i

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
notes = YAML.load_file(NOTES_YAML)
errors << "#{NOTES_YAML} must contain a YAML list" unless notes.is_a?(Array)
fail_with(errors) unless errors.empty?

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
Dir.glob(File.join(NOTES_ROOT, "**", "*.html")).sort.each do |html_path|
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

fail_with(errors) unless errors.empty?

puts "notes index ok: #{notes.size} entries, #{note_entry_files.size} top-level note html files"
