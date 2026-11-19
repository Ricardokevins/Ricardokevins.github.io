import json
import importlib.util
import runpy
import shutil
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
from pathlib import Path

import build_scripod_transcript as scripod
import build_youtube_transcript as youtube
from validate_site import validate_site


ROOT = Path(__file__).resolve().parents[1]


class CitationTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("citation_refresh", ROOT / "cite.py")
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)
        self.paper = "a" * 40
        self.badge = f"[![citation](https://img.shields.io/badge/citation-12-grey.svg)](https://example.test/{self.paper})\n"

    def test_only_matching_badge_counts_change(self):
        content = "citation-12\n" + self.badge
        self.assertEqual(self.module.refresh_badges(content, {self.paper: 23}),
                         "citation-12\n" + self.badge.replace("citation-12", "citation-23"))

    def test_missing_and_invalid_counts_preserve_content(self):
        for counts in ({}, {self.paper: None}, {self.paper: -1}, {self.paper: True}):
            self.assertEqual(self.module.refresh_badges(self.badge, counts), self.badge)

    def test_about_page_is_independent_of_working_directory(self):
        self.assertEqual(self.module.ABOUT_PAGE, ROOT / "_pages/about.md")


class LegacyImporterTests(unittest.TestCase):
    def import_fixture(self, script, fields):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            generator = root / "markdown_generator"
            generator.mkdir()
            (root / "_talks").mkdir()
            (root / "_publications").mkdir()
            target = generator / script
            shutil.copyfile(ROOT / "markdown_generator" / script, target)
            input_paths = []
            dataframe = types.SimpleNamespace(iterrows=lambda: [(0, types.SimpleNamespace(**fields))])
            def read_csv(filename, **options):
                input_paths.append(filename)
                return dataframe
            pandas = types.SimpleNamespace(read_csv=read_csv)
            with patch.dict(sys.modules, {"pandas": pandas}):
                runpy.run_path(str(target))
            generated = list((root / "_talks").glob("*.md")) + list((root / "_publications").glob("*.md"))
            self.assertEqual(len(generated), 1)
            self.assertTrue(all(filename.parent == generator.resolve() for filename in input_paths))
            return generated[0].read_text(encoding="utf-8")

    def test_talk_importer_escapes_title_and_keeps_date_without_location(self):
        content = self.import_fixture("talks.py", {"title": 'A "quoted" talk', "type": "Talk",
            "url_slug": "fixture", "venue": 'Venue "quoted"', "date": "2024-01-02",
            "location": "", "talk_url": "", "description": "description"})
        self.assertIn('title: "A &quot;quoted&quot; talk"', content)
        self.assertIn('venue: "Venue &quot;quoted&quot;"', content)
        self.assertIn("date: 2024-01-02", content)

    def test_publication_importer_escapes_title_and_url(self):
        content = self.import_fixture("publications.py", {"title": 'A "quoted" paper',
            "url_slug": "fixture", "pub_date": "2024-01-02", "venue": "Conference",
            "excerpt": "description", "paper_url": "https://example.test/paper?name='a'",
            "citation": "Author's citation"})
        self.assertIn('title: "A &quot;quoted&quot; paper"', content)
        self.assertIn("name=&apos;a&apos;", content)

    def test_map_import_does_not_start_network_or_generate_files(self):
        spec = importlib.util.spec_from_file_location("talkmap", ROOT / "talkmap.py")
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {"getorg": None, "geopy": None}):
            spec.loader.exec_module(module)
        self.assertTrue(callable(module.talk_locations))


class TranscriptTests(unittest.TestCase):
    def test_millisecond_rounding_carries_minutes_and_hours(self):
        for seconds, expected in ((59.9996, "00:01:00.000"), (3599.9996, "01:00:00.000"),
                                  (0.0006, "00:00:00.001"), (3.125, "00:00:03.125")):
            with self.subTest(seconds=seconds):
                self.assertEqual(youtube.stamp(seconds, True), expected)
                cue = scripod.SpeakerCue(seconds, seconds + 1, "example")
                self.assertIn(expected.replace(".", ","), scripod.render_srt([cue], False))

    def test_whole_second_display_still_truncates(self):
        self.assertEqual(youtube.stamp(59.9996), "00:00:59")

    def test_encoded_comparisons_survive_markup_removal(self):
        self.assertEqual(youtube.clean_cue_text(["2 &lt; 3 &gt; 1; <b>hello</b>"]), "2 < 3 > 1; hello")
        self.assertEqual(youtube.clean_cue_text(["&lt;literal&gt; &amp; <v Guest>text</v>"]), "<literal> & text")

    def test_vtt_notes_are_not_timing_lines(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "captions.vtt"
            source.write_text("WEBVTT\n\nNOTE example --> explanation\nignored\n\n"
                              "00:00.000 --> 00:01.000\n2 &lt; 3\n", encoding="utf-8")
            cues, _ = youtube.parse_vtt(source)
        self.assertEqual(cues, [youtube.Cue(0, 1, "2 < 3")])

    def test_invalid_scripod_times_are_rejected(self):
        for start, end in (("NaN", 1), (0, "Infinity"), (-1, 1), (2, 1)):
            with self.subTest(start=start, end=end):
                source = {"segments": [{"sentences": [{"start": start, "end": end, "text": "text"}]}]}
                with self.assertRaises(youtube.TranscriptError):
                    scripod.flatten_sentences(source)

    def test_nonfinite_repair_is_rejected(self):
        for repair in ("1,0,1,nan,2", "1,0,1,0,inf", "1,-1,1,0,2"):
            with self.subTest(repair=repair), self.assertRaises(youtube.TranscriptError):
                youtube.parse_timing_repairs([repair])

    def test_out_of_range_timestamp_is_rejected(self):
        for value in ("00:60.000", "01:60:00.000", "01:00:nan", "not:a:time"):
            with self.subTest(value=value), self.assertRaises(youtube.TranscriptError):
                youtube.parse_timestamp(value)

    def test_cli_preserves_transcript_text(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            metadata = directory / "metadata.json"
            source = directory / "source.json"
            metadata.write_text(json.dumps({"title": "Example", "duration": 61}), encoding="utf-8")
            source.write_text(json.dumps({"speakers": {"a": "Guest"}, "segments": [{"speaker": "a",
                "sentences": [{"start": 59.9996, "end": 60.5, "text": "2 < 3"},
                              {"start": 60.5, "end": 61, "text": "42"}]}]}), encoding="utf-8")
            result = subprocess.run(["python3", str(ROOT / "scripts/build_scripod_transcript.py"),
                "--source-json", str(source), "--metadata", str(metadata), "--output-dir", str(directory / "out")],
                text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)["ok"])
            self.assertIn("00:01:00,000", (directory / "out/complete-transcript.srt").read_text())
            self.assertIn("2 < 3", (directory / "out/complete-transcript-readable.md").read_text())


class SiteValidationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "source"
        self.site = Path(self.temporary.name) / "site"
        self.root.mkdir()
        self.site.mkdir()
        self.config = {"url": "https://example.test", "baseurl": "", "exclude": []}
        self.write("index.html", '<a href="/article#section">read</a>')
        self.write("article.html", '<h1 id="section">Section</h1>')

    def write(self, relative, content):
        path = self.site / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_extensionless_page_and_anchor_resolve(self):
        errors, counts = validate_site(self.site, self.root, self.config)
        self.assertEqual(errors, [])
        self.assertEqual(counts["html_pages"], 2)

    def test_missing_asset_and_anchor_fail(self):
        self.write("index.html", '<a href="article#missing">read</a><img src="missing.png">')
        errors, _ = validate_site(self.site, self.root, self.config)
        self.assertTrue(any("missing anchor" in error for error in errors))
        self.assertTrue(any("missing target" in error for error in errors))

    def test_duplicate_ids_fail(self):
        self.write("article.html", '<h1 id="section">A</h1><h2 id="section">B</h2>')
        errors, _ = validate_site(self.site, self.root, self.config)
        self.assertTrue(any("duplicate ids" in error for error in errors))

    def test_excluded_directory_leak_fails(self):
        (self.root / "private").mkdir()
        self.write("private/data.txt", "local")
        self.config["exclude"] = ["private"]
        errors, _ = validate_site(self.site, self.root, self.config)
        self.assertTrue(any("excluded source leaked" in error for error in errors))

    def test_css_resources_and_encoded_names(self):
        self.write("assets/theme.css", 'body { background: url("%E5%9B%BE.png") }')
        self.write("assets/图.png", "fixture")
        errors, _ = validate_site(self.site, self.root, self.config)
        self.assertEqual(errors, [])

    def test_manifest_icon_references_are_validated(self):
        self.write("images/manifest.json", json.dumps({"icons": [{"src": "missing.png"}]}))
        errors, _ = validate_site(self.site, self.root, self.config)
        self.assertTrue(any("missing target missing.png" in error for error in errors))

    def test_external_urls_are_not_fetched(self):
        self.write("index.html", '<a href="https://elsewhere.test/missing">outside</a><img src="data:image/png,fixture">')
        errors, _ = validate_site(self.site, self.root, self.config)
        self.assertEqual(errors, [])

    def test_baseurl_and_same_host_absolute_url(self):
        self.config["baseurl"] = "/blog"
        self.write("index.html", '<a href="https://example.test/blog/article#section">read</a>')
        errors, _ = validate_site(self.site, self.root, self.config)
        self.assertEqual(errors, [])

    def test_reference_cannot_escape_build(self):
        self.write("index.html", '<a href="../outside.txt">outside</a>')
        errors, _ = validate_site(self.site, self.root, self.config)
        self.assertTrue(any("escapes the build" in error for error in errors))


class NotesValidationTests(unittest.TestCase):
    def run_validator(self, notes, config):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for folder in ("scripts", "_data", "notes"):
                (root / folder).mkdir()
            shutil.copyfile(ROOT / "scripts/validate_notes_index.rb", root / "scripts/validate_notes_index.rb")
            (root / "notes/NOTE_TEMPLATE.md").write_text("template")
            (root / "_data/notes.yml").write_text(json.dumps(notes))
            (root / "_config.yml").write_text(json.dumps(config))
            return subprocess.run(["ruby", str(root / "scripts/validate_notes_index.rb")], text=True, capture_output=True)

    def test_empty_index_is_valid(self):
        result = self.run_validator([], {"exclude": ["notes/math-interview-question-bank", "notes/quant-interview-question-bank", "notes/llm-interview-question-bank"]})
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_entry_has_diagnostic_not_traceback(self):
        for entry, diagnostic in (("text", "must be a mapping"), ({"title": "Title"}, "requires non-empty url")):
            result = self.run_validator([entry], {})
            self.assertNotEqual(result.returncode, 0)
            self.assertIn(diagnostic, result.stderr)
            self.assertNotIn("NoMethodError", result.stderr)

    def test_local_only_scope_must_be_excluded(self):
        config = {"defaults": [{"scope": {"path": "notes/local"}, "values": {"unlisted": True, "sitemap": False}}]}
        result = self.run_validator([], config)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Local-only scope must be excluded", result.stderr)

    def test_missing_book_index_has_clear_diagnostic(self):
        result = self.run_validator([], {})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing book index", result.stderr)
        self.assertNotIn("Errno::ENOENT", result.stderr)


if __name__ == "__main__":
    unittest.main()
