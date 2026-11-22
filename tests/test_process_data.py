import unittest
from unittest.mock import patch

from src.input.edited_element import EditedElement, patch_set_to_edited_elements
from src.process.process_data import process_data
from src.process.tests_depenancies import get_tests_fixture_dependencies
from src.process.tests_list import Test
from unidiff import PatchSet


def edited_elements_from_patch(patch_text):
    return patch_set_to_edited_elements(PatchSet.from_string(patch_text))


class ProcessDataFixtureTests(unittest.TestCase):
    def test_explicit_fixture_edge_selects_only_its_test(self):
        dependency_graph = get_tests_fixture_dependencies()
        fixture_path = "tests/fixtures/optimizer/isolate_table_selects.sql"
        test_id = "tests/test_optimizer.py::TestOptimizer::test_isolate_table_selects"
        self.assertEqual(dependency_graph[fixture_path], [test_id])

        tests = [
            Test("tests/test_optimizer.py", 1, 0.1, test_id),
            Test(
                "tests/test_optimizer.py",
                2,
                0.1,
                "tests/test_optimizer.py::TestOptimizer::test_simplify",
            ),
        ]
        with (
            patch(
                "src.process.process_data.get_tests_depenancies",
                return_value={"tests/test_optimizer.py": []},
            ),
            patch(
                "src.process.process_data.get_tests_fixture_dependencies",
                return_value=dependency_graph,
            ),
            patch("src.process.process_data.get_all_tests", return_value=tests),
        ):
            result = process_data("fixture.patch", [EditedElement(fixture_path)])

        self.assertEqual(result.failing, [tests[0]])

    def test_python_import_dependency_behavior_is_preserved(self):
        test = Test(
            "tests/test_optimizer.py",
            1,
            0.1,
            "tests/test_optimizer.py::TestOptimizer::test_simplify",
        )
        with (
            patch(
                "src.process.process_data.get_tests_depenancies",
                return_value={"tests/test_optimizer.py": ["sqlglot.optimizer.simplify"]},
            ),
            patch("src.process.process_data.get_tests_fixture_dependencies", return_value={}),
            patch("src.process.process_data.get_all_tests", return_value=[test]),
        ):
            result = process_data(
                "code.patch",
                [EditedElement("sqlglot/optimizer/simplify.py", "sqlglot.optimizer.simplify")],
            )

        self.assertEqual(result.failing, [test])

    def test_multiple_changed_files_select_a_test_once(self):
        test = Test(
            "tests/test_optimizer.py",
            1,
            0.1,
            "tests/test_optimizer.py::TestOptimizer::test_simplify",
        )
        with (
            patch(
                "src.process.process_data.get_tests_depenancies",
                return_value={
                    "tests/test_optimizer.py": [
                        "sqlglot.optimizer.simplify",
                        "sqlglot.optimizer.qualify",
                    ]
                },
            ),
            patch("src.process.process_data.get_tests_fixture_dependencies", return_value={}),
            patch("src.process.process_data.get_all_tests", return_value=[test]),
        ):
            result = process_data(
                "multi.patch",
                [
                    EditedElement("sqlglot/optimizer/simplify.py", "sqlglot.optimizer.simplify"),
                    EditedElement("sqlglot/optimizer/qualify.py", "sqlglot.optimizer.qualify"),
                ],
            )

        self.assertEqual(result.failing, [test])

    def test_non_python_patch_does_not_create_import_evidence(self):
        [edited_file] = edited_elements_from_patch(
            """\
diff --git a/tests/fixtures/optimizer/sample.sql b/tests/fixtures/optimizer/sample.sql
--- a/tests/fixtures/optimizer/sample.sql
+++ b/tests/fixtures/optimizer/sample.sql
@@ -1 +1 @@
-SELECT 1;
+SELECT 2;
"""
        )

        self.assertIsNone(edited_file.py_import_name)
        self.assertEqual(edited_file.file_path, "tests/fixtures/optimizer/sample.sql")

    def test_comment_only_python_patch_does_not_select_import_dependents(self):
        [edited_file] = edited_elements_from_patch(
            '''\
diff --git a/pkg/module.py b/pkg/module.py
--- a/pkg/module.py
+++ b/pkg/module.py
@@ -1,3 +1,4 @@
 def function():
+    # Documents the behavior
     """Description
     More context
'''
        )
        test = Test("tests/test_module.py", 1, 0.1, "tests/test_module.py::test_case")

        with (
            patch(
                "src.process.process_data.get_tests_depenancies",
                return_value={"tests/test_module.py": ["pkg.module"]},
            ),
            patch("src.process.process_data.get_tests_fixture_dependencies", return_value={}),
            patch("src.process.process_data.get_all_tests", return_value=[test]),
        ):
            result = process_data("comment.patch", [edited_file])

        self.assertFalse(edited_file.has_executable_changes)
        self.assertEqual(result.failing, [])

    def test_executable_ast_change_remains_a_candidate(self):
        [edited_file] = edited_elements_from_patch(
            """\
diff --git a/pkg/module.py b/pkg/module.py
--- a/pkg/module.py
+++ b/pkg/module.py
@@ -1,2 +1,2 @@
 def function():
-    return 1
+    return 2
"""
        )

        self.assertTrue(edited_file.has_executable_changes)

    def test_tool_directive_comment_remains_a_candidate(self):
        [edited_file] = edited_elements_from_patch(
            """\
diff --git a/pkg/module.py b/pkg/module.py
--- a/pkg/module.py
+++ b/pkg/module.py
@@ -1,3 +1,3 @@
 def function():
-    # noqa: F401
+    # noqa: F402
     return 1
"""
        )

        self.assertTrue(edited_file.has_executable_changes)

    def test_inline_tool_directive_comment_remains_a_candidate(self):
        [edited_file] = edited_elements_from_patch(
            """\
diff --git a/pkg/module.py b/pkg/module.py
--- a/pkg/module.py
+++ b/pkg/module.py
@@ -1,2 +1,2 @@
 def function():
-    return 1  # noqa: F401
+    return 1  # noqa: F402
"""
        )

        self.assertTrue(edited_file.has_executable_changes)

    def test_comment_like_text_inside_a_string_remains_a_candidate(self):
        [edited_file] = edited_elements_from_patch(
            '''\
diff --git a/pkg/module.py b/pkg/module.py
--- a/pkg/module.py
+++ b/pkg/module.py
@@ -1,5 +1,5 @@
 def function():
     value = """literal
-# old value
+# new value
     """
     return value
'''
        )

        self.assertTrue(edited_file.has_executable_changes)

    def test_comment_only_new_file_remains_a_candidate(self):
        [edited_file] = edited_elements_from_patch(
            """\
diff --git a/pkg/new_module.py b/pkg/new_module.py
new file mode 100644
--- /dev/null
+++ b/pkg/new_module.py
@@ -0,0 +1 @@
+# Module documentation
"""
        )

        self.assertTrue(edited_file.has_executable_changes)

    def test_comment_only_deleted_file_remains_a_candidate(self):
        [edited_file] = edited_elements_from_patch(
            """\
diff --git a/pkg/removed_module.py b/pkg/removed_module.py
deleted file mode 100644
--- a/pkg/removed_module.py
+++ /dev/null
@@ -1 +0,0 @@
-# Removed module documentation
"""
        )

        self.assertTrue(edited_file.has_executable_changes)

    def test_non_code_file_does_not_override_code_change_evidence(self):
        test = Test("tests/test_module.py", 1, 0.1, "tests/test_module.py::test_case")
        with (
            patch(
                "src.process.process_data.get_tests_depenancies",
                return_value={"tests/test_module.py": ["pkg.comment"]},
            ),
            patch("src.process.process_data.get_tests_fixture_dependencies", return_value={}),
            patch("src.process.process_data.get_all_tests", return_value=[test]),
        ):
            result = process_data(
                "mixed.patch",
                [
                    EditedElement("pkg/comment.py", "pkg.comment", False),
                    EditedElement("pkg/changed.py", "pkg.changed", True),
                ],
            )

        self.assertEqual(result.failing, [test])


if __name__ == "__main__":
    unittest.main()
