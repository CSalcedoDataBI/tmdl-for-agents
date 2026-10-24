"""Tests for scripts/check_repo.py: the catalogue is well-formed, valid cards pass, invented
names fail."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from scripts import check_repo as cr  # noqa: E402


class TestCatalogShape(unittest.TestCase):
    def setUp(self):
        self.cat = cr.load_catalog()

    def test_catalog_present_and_consistent(self):
        self.assertEqual(cr.check_catalog_shape(self.cat), [])

    def test_known_types_and_props(self):
        self.assertIn("Measure", self.cat["types"])
        self.assertIn("SingleColumnRelationship", self.cat["types"])
        self.assertIn("FormatString", self.cat["type_props"]["Measure"])
        # a property of one type is not silently allowed on another
        self.assertNotIn("CrossFilteringBehavior", self.cat["type_props"]["Measure"])

    def test_shape_errors_surface(self):
        broken = {"raw": {"objectTypes": 99, "propertyNamesTotal": 1},
                  "entries": [{"type": "Measure", "properties": ["Name"]}],
                  "types": {"Measure"}, "type_props": {"Measure": {"Name"}},
                  "all_props": {"Name"}, "all_props_ci": {"name"}}
        errs = cr.check_catalog_shape(broken)
        self.assertTrue(any("objectTypes says 99" in e for e in errs))


class TestCardCheck(unittest.TestCase):
    def setUp(self):
        self.cat = cr.load_catalog()

    def card(self, type_line, props, body=""):
        prop_lines = "\n".join(f"  - {p}" for p in props)
        return f"---\ntype: {type_line}\nproperties:\n{prop_lines}\n---\n\n{body}"

    def test_valid_card(self):
        text = self.card("Measure", ["Name", "Expression", "FormatString"])
        self.assertEqual(cr.check_card(text, "T", self.cat), [])

    def test_invented_type(self):
        text = self.card("Measurr", ["Name"])
        errs = cr.check_card(text, "T", self.cat)
        self.assertTrue(any("object type 'Measurr'" in e for e in errs))

    def test_invented_property(self):
        text = self.card("Measure", ["Name", "FormatStrng"])
        errs = cr.check_card(text, "T", self.cat)
        self.assertTrue(any("property 'FormatStrng'" in e for e in errs))

    def test_property_on_wrong_type(self):
        # CrossFilteringBehavior is a relationship property, not a measure property.
        text = self.card("Measure", ["CrossFilteringBehavior"])
        errs = cr.check_card(text, "T", self.cat)
        self.assertTrue(any("'CrossFilteringBehavior' is not on type 'Measure'" in e for e in errs))

    def test_missing_frontmatter(self):
        errs = cr.check_card("no frontmatter here", "T", self.cat)
        self.assertTrue(any("missing frontmatter" in e for e in errs))

    def test_flow_list_properties_validated(self):
        # A YAML flow list must be validated too, not silently skipped.
        text = "---\ntype: Measure\nproperties: [Name, FormatStrng]\n---\n"
        errs = cr.check_card(text, "T", self.cat)
        self.assertTrue(any("property 'FormatStrng'" in e for e in errs))

    def test_missing_properties_is_error(self):
        text = "---\ntype: Measure\n---\n\nbody"
        errs = cr.check_card(text, "T", self.cat)
        self.assertTrue(any("`properties` must be a non-empty list" in e for e in errs))

    # --- tmdl example blocks ---

    def test_valid_tmdl_example(self):
        body = (
            "```tmdl\n"
            "measure 'Total Sales' = SUM(Sales[Amount])\n"
            "\tformatString: \"\\$#,0\"\n"
            "\tdisplayFolder: Key Measures\n"
            "\tisHidden\n"
            "\tlineageTag: 8a1-abc\n"
            "```\n"
        )
        text = self.card("Measure", ["Name"], body)
        self.assertEqual(cr.check_card(text, "T", self.cat), [])

    def test_invented_keyword_in_tmdl_example(self):
        body = (
            "```tmdl\n"
            "measure 'Total Sales' = SUM(Sales[Amount])\n"
            "\tformatStrng: \"#,0\"\n"
            "```\n"
        )
        text = self.card("Measure", ["Name"], body)
        errs = cr.check_card(text, "T", self.cat)
        self.assertTrue(any("property keyword 'formatStrng'" in e for e in errs))

    def test_declaration_and_dax_lines_not_flagged(self):
        # A multi-line expression body is indented one level deeper than the properties, as real
        # TMDL writes it. The DAX tokens are skipped; the property one level shallower is checked.
        body = (
            "```tmdl\n"
            "measure 'Total' =\n"
            "\t\tSUMX(\n"
            "\t\t\tSales,\n"
            "\t\t\tSales[Qty] * Sales[Price]\n"
            "\t\t)\n"
            "\tformatString: \"#,0\"\n"
            "```\n"
        )
        text = self.card("Measure", ["Name"], body)
        self.assertEqual(cr.check_card(text, "T", self.cat), [])

    def test_invented_keyword_after_multiline_expression(self):
        # The property that follows a multi-line expression must still be name-checked (the core
        # 'no invented name' promise must survive a multi-line DAX / M body).
        body = (
            "```tmdl\n"
            "measure 'Total' =\n"
            "\t\tSUMX(\n"
            "\t\t\tSales,\n"
            "\t\t\tSales[Qty]\n"
            "\t\t)\n"
            "\tformatStrng: \"#,0\"\n"
            "```\n"
        )
        text = self.card("Measure", ["Name"], body)
        errs = cr.check_card(text, "T", self.cat)
        self.assertTrue(any("property keyword 'formatStrng'" in e for e in errs))

    def test_multiline_m_expression_body_not_flagged(self):
        # `source =` opens an M block; `let`/`in` must not be read as property keywords.
        body = (
            "```tmdl\n"
            "partition Sales = m\n"
            "\tmode: import\n"
            "\tsource =\n"
            "\t\t\tlet\n"
            "\t\t\t\tSource = Sql.Database(\"s\", \"db\")\n"
            "\t\t\tin\n"
            "\t\t\t\tSource\n"
            "```\n"
        )
        text = self.card("Partition", ["Name"], body)
        self.assertEqual(cr.check_card(text, "T", self.cat), [])


class TestRepoShape(unittest.TestCase):
    def test_catalog_file_exists(self):
        self.assertTrue((cr.ROOT / "exports" / "tmdl-tom.catalog.json").exists())

    def test_readme_numbers_match_catalogue(self):
        self.assertEqual(cr.check_readme_numbers(cr.load_catalog()), [])

    def test_full_repo_check_passes(self):
        """The repository as committed passes every check."""
        cat = cr.load_catalog()
        result = (cr.check_catalog_shape(cat) + cr.check_readme_numbers(cat) + cr.check_skills()
                  + cr.check_workflows() + cr.check_names(cat))
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
