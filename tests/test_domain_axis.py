"""Focused checks for the domain axis tracer bullet (WO 2026-08-22-031).

Covers Decision 1 (domain as a controlled-vocabulary frontmatter field,
a second axis independent of `type`) and Decision 3 (list-shaped, not
scalar; mirror mechanism is a generated index file, not a symlink/junction
-- both of which were tested and ruled out in this environment).

  1. schema.validate_domain rejects unknown values, requires non-empty.
  2. schema.format_domain_field / parse_domain_field round-trip an
     ordered list, including the multi-domain case the scalar
     assumption failed on (WO 2026-08-22-026: business + architecture).
  3. `ws create --domain` (repeatable) writes a bracketed list; the field
     is genuinely optional -- omitting it produces no `domain:` line at
     all (no retro-migration forced on legacy objects).
  4. `ws domain sync` builds one generated index file per domain value,
     each listing every object whose domain list includes it -- so a
     multi-domain object appears under more than one file, which is the
     entire point of Decision 3 over the original scalar design.
  5. The domain field does not touch `type`; both are independently
     readable frontmatter values on the same object.
"""

import os
import tempfile
import unittest
from argparse import Namespace
from contextlib import contextmanager
from pathlib import Path

from tools.ws.schema import validate_domain, format_domain_field, parse_domain_field
from tools.ws.__main__ import cmd_create
from tools.ws.domain import cmd_domain_sync, collect_domain_index, cmd_list, collect_object_rows

REPO_ROOT = Path(__file__).resolve().parents[1]


def _wo_content(obj_id: str, title: str, domains=None, obj_type: str = "change") -> str:
    lines = [
        "---",
        f"id: {obj_id}",
        f"title: {title}",
        f"type: {obj_type}",
        "status: active",
        "state: build",
        "consequence: meaningful",
        "sensitivity: ordinary",
    ]
    if domains:
        lines.append(f"domain: {format_domain_field(domains)}")
    lines += [
        "created_at: 2026-08-22T00:00:00Z",
        "updated_at: 2026-08-22T00:00:00Z",
        "---",
        "## Intent\n\nFixture.\n",
    ]
    return "\n".join(lines)


@contextmanager
def workspace_with_wos(objects: dict):
    """Tempdir workspace with fixture Work Objects (mirrors relation/graph tests).

    ``objects`` maps obj_id -> (title, domains_list_or_None).
    """
    previous = Path.cwd()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        month_dir = root / ".work-studio" / "objects" / "2026" / "08"
        month_dir.mkdir(parents=True)
        for obj_id, (title, domains) in objects.items():
            content = _wo_content(obj_id, title, domains)
            (month_dir / f"{obj_id}-fixture.md").write_text(content, encoding="utf-8")
        os.chdir(root)
        try:
            yield root
        finally:
            os.chdir(previous)


@contextmanager
def empty_workspace():
    previous = Path.cwd()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / ".work-studio" / "objects").mkdir(parents=True)
        os.chdir(root)
        try:
            yield root
        finally:
            os.chdir(previous)


class TestDomainValidation(unittest.TestCase):
    def test_rejects_unknown_domain_value(self):
        err = validate_domain(["not_a_real_domain"])
        self.assertIsNotNone(err)
        self.assertIn("not_a_real_domain", err)

    def test_rejects_empty_list(self):
        err = validate_domain([])
        self.assertIsNotNone(err)

    def test_accepts_known_values(self):
        self.assertIsNone(validate_domain(["business", "architecture"]))

    def test_format_parse_round_trip_preserves_order(self):
        """Order matters -- primary domain first, per Decision 3."""
        values = ["engineering", "business", "architecture"]
        formatted = format_domain_field(values)
        self.assertEqual(formatted, "[engineering, business, architecture]")
        self.assertEqual(parse_domain_field(formatted), values)

    def test_parse_handles_single_value_and_empty(self):
        self.assertEqual(parse_domain_field("[business]"), ["business"])
        self.assertEqual(parse_domain_field(""), [])


class TestCreateWithDomain(unittest.TestCase):
    def test_create_with_domain_writes_bracketed_list(self):
        with empty_workspace():
            args = Namespace(
                title="Test multi-domain object", type="change",
                consequence="meaningful", sensitivity="ordinary",
                domain=["business", "architecture"],
            )
            rc = cmd_create(args)
            self.assertEqual(rc, 0)

            month_dir = Path.cwd() / ".work-studio" / "objects"
            created = list(month_dir.rglob("*.md"))
            self.assertEqual(len(created), 1)
            content = created[0].read_text(encoding="utf-8")
            self.assertIn("domain: [business, architecture]", content)
            # type is untouched -- domain is a second, independent axis
            self.assertIn("type: change", content)

    def test_create_without_domain_omits_field_entirely(self):
        """No retro-migration forced: omitting --domain writes no domain: line."""
        with empty_workspace():
            args = Namespace(
                title="Test unclassified object", type="inquiry",
                consequence="low", sensitivity="ordinary", domain=None,
            )
            rc = cmd_create(args)
            self.assertEqual(rc, 0)

            month_dir = Path.cwd() / ".work-studio" / "objects"
            created = list(month_dir.rglob("*.md"))
            content = created[0].read_text(encoding="utf-8")
            self.assertNotIn("domain:", content)

    def test_create_rejects_invalid_domain_value(self):
        with empty_workspace():
            args = Namespace(
                title="Bad domain object", type="change",
                consequence="meaningful", sensitivity="ordinary",
                domain=["not_a_real_domain"],
            )
            rc = cmd_create(args)
            self.assertEqual(rc, 1)
            month_dir = Path.cwd() / ".work-studio" / "objects"
            self.assertEqual(list(month_dir.rglob("*.md")), [])


class TestDomainSync(unittest.TestCase):
    def test_multi_domain_object_appears_under_every_declared_domain(self):
        """The entire point of Decision 3: a scalar would force one label;
        a list-shaped field lets one real object (like the studio's own
        WO 2026-08-22-026) appear under both business and architecture.
        """
        objects = {
            "2026-08-22-100": ("Connect business pipeline into the graph system",
                                ["business", "architecture"]),
            "2026-08-22-101": ("Manage liquidity and cash runway", ["business"]),
            "2026-08-22-102": ("Design engineering operating pipeline graph capabilities",
                                ["design", "engineering", "architecture"]),
            "2026-08-22-103": ("Unclassified legacy object", None),
        }
        with workspace_with_wos(objects) as root:
            index = collect_domain_index(root / ".work-studio" / "objects")
            business_ids = {row[0] for row in index["business"]}
            architecture_ids = {row[0] for row in index["architecture"]}
            design_ids = {row[0] for row in index["design"]}
            engineering_ids = {row[0] for row in index["engineering"]}

            self.assertEqual(business_ids, {"2026-08-22-100", "2026-08-22-101"})
            self.assertEqual(architecture_ids, {"2026-08-22-100", "2026-08-22-102"})
            self.assertEqual(design_ids, {"2026-08-22-102"})
            self.assertEqual(engineering_ids, {"2026-08-22-102"})
            # unclassified object appears nowhere -- absence, not exclusion
            self.assertNotIn("2026-08-22-103", business_ids | architecture_ids)

    def test_sync_writes_generated_marked_index_files(self):
        objects = {
            "2026-08-22-200": ("Solo business decision", ["business"]),
        }
        with workspace_with_wos(objects) as root:
            rc = cmd_domain_sync(Namespace())
            self.assertEqual(rc, 0)

            domain_dir = root / ".work-studio" / "domain"
            business_file = domain_dir / "business.md"
            self.assertTrue(business_file.exists())
            content = business_file.read_text(encoding="utf-8")
            self.assertIn("GENERATED", content)
            self.assertIn("2026-08-22-200", content)

            # every controlled-vocabulary domain gets a file, even if empty --
            # a missing edge/entry means "not recorded", never "false"
            self.assertTrue((domain_dir / "engineering.md").exists())
            empty_content = (domain_dir / "engineering.md").read_text(encoding="utf-8")
            self.assertIn("No Work Objects currently declare this domain", empty_content)

    def test_sync_is_idempotent_and_fully_regenerates(self):
        """Regeneration must fully overwrite stale entries, not merge with them --
        otherwise the mirror could drift from frontmatter, which Decision 2/3
        explicitly rule out.
        """
        objects = {"2026-08-22-300": ("First pass object", ["research"])}
        with workspace_with_wos(objects) as root:
            cmd_domain_sync(Namespace())
            research_file = root / ".work-studio" / "domain" / "research.md"
            self.assertIn("2026-08-22-300", research_file.read_text(encoding="utf-8"))

            # Simulate the object's domain changing (e.g. reclassified) --
            # a stale sync must not leave the old entry behind.
            obj_path = root / ".work-studio" / "objects" / "2026" / "08" / "2026-08-22-300-fixture.md"
            content = obj_path.read_text(encoding="utf-8")
            obj_path.write_text(content.replace("domain: [research]", "domain: [ideation]"), encoding="utf-8")

            cmd_domain_sync(Namespace())
            research_content = research_file.read_text(encoding="utf-8")
            ideation_content = (root / ".work-studio" / "domain" / "ideation.md").read_text(encoding="utf-8")
            self.assertNotIn("2026-08-22-300", research_content)
            self.assertIn("2026-08-22-300", ideation_content)


class TestWsList(unittest.TestCase):
    """Covers WO 2026-08-22-036: `ws list --domain` as a live query, separate
    from the generated `ws domain sync` mirror -- both must agree on
    membership since they share the same scan/filter semantics.
    """

    def _objects(self):
        return {
            "2026-08-22-400": ("Multi-domain object", ["business", "architecture"]),
            "2026-08-22-401": ("Business-only object", ["business"]),
            "2026-08-22-402": ("Unclassified object", None),
        }

    def test_domain_filter_matches_any_of_given_values(self):
        with workspace_with_wos(self._objects()) as root:
            rc = cmd_list(Namespace(domain=["business"]))
            self.assertEqual(rc, 0)
            rows = collect_object_rows(root / ".work-studio" / "objects")
            business_ids = {r["id"] for r in rows if set(r["domain"]) & {"business"}}
            self.assertEqual(business_ids, {"2026-08-22-400", "2026-08-22-401"})

    def test_multi_domain_object_matches_every_declared_domain(self):
        """The same object must appear under both filters -- mirrors the
        collect_domain_index guarantee so `ws list` and `ws domain sync`
        never disagree about membership.
        """
        with workspace_with_wos(self._objects()) as root:
            rows = collect_object_rows(root / ".work-studio" / "objects")
            business_ids = {r["id"] for r in rows if "business" in r["domain"]}
            architecture_ids = {r["id"] for r in rows if "architecture" in r["domain"]}
            self.assertIn("2026-08-22-400", business_ids)
            self.assertIn("2026-08-22-400", architecture_ids)

    def test_unclassified_object_has_empty_domain_not_excluded_from_full_list(self):
        with workspace_with_wos(self._objects()) as root:
            rows = collect_object_rows(root / ".work-studio" / "objects")
            unclassified = next(r for r in rows if r["id"] == "2026-08-22-402")
            self.assertEqual(unclassified["domain"], [])
            # no --domain filter -> full corpus, unclassified included
            self.assertEqual(len(rows), 3)

    def test_rejects_invalid_domain_filter_value(self):
        with workspace_with_wos(self._objects()):
            rc = cmd_list(Namespace(domain=["not_a_real_domain"]))
            self.assertEqual(rc, 1)

    def test_no_filter_returns_full_corpus_sorted_by_id(self):
        with workspace_with_wos(self._objects()) as root:
            rows = collect_object_rows(root / ".work-studio" / "objects")
            self.assertEqual([r["id"] for r in rows],
                              ["2026-08-22-400", "2026-08-22-401", "2026-08-22-402"])


if __name__ == "__main__":
    unittest.main()
