"""Package contracts; run with unittest discover after assembling the plugin."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILLS = {"deliberate-dev", "clarify-request", "plan-tasks", "test-first", "isolated-worktrees", "review-delivery"}


class PackageTests(unittest.TestCase):
    def test_six_discoverable_skills(self):
        self.assertEqual({p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md")}, SKILLS)
        for name in SKILLS:
            body = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(body.startswith("---\n"))
            front = body.split("---", 2)[1]
            self.assertIn(f"name: {name}\n", front)
            self.assertRegex(front, r"description: .+\n")

    def test_manifest_is_self_contained(self):
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "deliberate-dev")
        self.assertEqual(manifest["skills"], "./skills/")
        prompts = manifest["interface"]["defaultPrompt"]
        self.assertIsInstance(prompts, list)
        self.assertTrue(1 <= len(prompts) <= 3)
        self.assertTrue(all(isinstance(p, str) and 0 < len(p) <= 128 for p in prompts))
        self.assertNotIn("mcpServers", manifest)
        self.assertNotIn("apps", manifest)
        self.assertNotIn("hooks", manifest)

    def test_bundled_markdown_references_resolve_inside_plugin(self):
        self.assertTrue((ROOT / "skills/deliberate-dev/SKILL.md").is_file())
        for path in (ROOT / "skills").rglob("*.md"):
            for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if "://" in target or target.startswith("#"):
                    continue
                destination = (path.parent / target.split("#", 1)[0]).resolve()
                self.assertTrue(destination.is_relative_to(ROOT.resolve()), f"Outside package: {target}")
                self.assertTrue(destination.is_file(), f"Broken reference: {path}: {target}")

    def test_templates_and_example_are_usable(self):
        for name in ("brief.md", "task.md", "review.md"):
            self.assertTrue((ROOT / "skills/deliberate-dev/assets" / name).is_file())
        example = json.loads((ROOT / "examples/plan.json").read_text(encoding="utf-8"))
        self.assertEqual(example["schema_version"], 1)
        ids = {criterion["id"] for criterion in example["acceptance_criteria"]}
        self.assertTrue(ids)
        self.assertEqual(ids, {ac for task in example["tasks"] for ac in task["acceptance_criteria"]})
        self.assertTrue(all("tdd" not in task or not task["tdd"] for task in example["tasks"]))
        self.assertFalse(example.get("integration"))


if __name__ == "__main__":
    unittest.main()
