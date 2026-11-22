# Less tests

Test selection uses Python import relationships from `assets/tests_deps.json` and
explicit fixture-to-test relationships from `assets/fixtures_deps.json`. Keep the
fixture graph aligned with the test methods that load each fixture; matching is
by exact fixture path and test node ID, not directory or filename similarity.
