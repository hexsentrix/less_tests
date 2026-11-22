
===========================================================================
OVERALL
===========================================================================
Compared commits : 30
Missing commits  : 0
Unknown commits  : 0
TP               : 3
FP               : 351
FN               : 70
Precision        : 0.85%
Recall           : 4.11%
F1-score         : 1.41%

Commits with missed tests: 17: ['bvw2', 'f4bn', '3utz', '6vvp', 'j6uz', 'ary6', 'egys', 'st8f', 'gbhk', '6ze8', 'mthh', 'bj7g', '535z', '2vdj', '986c', '2jrq', 'nwnx']
details
######### bvw2 #########
expected: {1302} ,got: set()
######### f4bn #########
expected: {1375} ,got: set()
######### 3utz #########
expected: {1417, 139, 1420, 909, 914, 1558, 919, 1559, 921, 1434, 1560, 1561, 1562, 927, 1440, 1185, 1313, 1314, 1441, 1324, 1325, 1454, 1327, 1335, 1343, 1352, 1353, 1355, 1106, 1107, 1362, 1375, 1377, 1378, 1382, 1384, 1397} ,got: set()
######### 6vvp #########
expected: {1383} ,got: set()
######### j6uz #########
expected: {27, 1295} ,got: set()
######### ary6 #########
expected: {64, 1189, 1382, 1417, 42, 1355, 1420, 1519, 54, 27} ,got: set()
######### egys #########
expected: {1434} ,got: set()
######### st8f #########
expected: {1335} ,got: set()
######### gbhk #########
expected: {1302} ,got: set()
######### 6ze8 #########
expected: {302} ,got: set()
######### mthh #########
expected: {1343} ,got: set()
######### bj7g #########
expected: {94} ,got: set()
######### 535z #########
expected: {1434} ,got: set()
######### 2vdj #########
expected: {1377} ,got: set()
######### 986c #########
expected: {1454} ,got: set()
######### 2jrq #########
expected: {1440, 1441, 1381, 1355, 1325, 1104, 1106, 1369} ,got: set()
######### nwnx #########
expected: {1378} ,got: set()

2jrq.patch edited_elements [EditedElement(file_path='sqlglot/optimizer/eliminate_joins.py', py_import_name='sqlglot.optimizer.eliminate_joins')]
files edited: [<PatchedFile: sqlglot/optimizer/eliminate_joins.py>]
2vdj.patch edited_elements []
files edited: [<PatchedFile: tests/fixtures/optimizer/pushdown_predicates.sql>]
3utz.patch edited_elements [EditedElement(file_path='sqlglot/serde.py', py_import_name='sqlglot.serde')]
files edited: [<PatchedFile: sqlglot/serde.py>]
rare sqlglot/dialects/snowflake.py pranet sqlglot/dialects
535z.patch edited_elements [EditedElement(file_path='sqlglot/dialects/tsql.py', py_import_name='sqlglot.dialects.tsql')]
files edited: [<PatchedFile: sqlglot/dialects/tsql.py>]
6vvp.patch edited_elements []
files edited: [<PatchedFile: tests/fixtures/optimizer/qualify_columns__invalid.sql>]
6ze8.patch edited_elements [EditedElement(file_path='sqlglot/parsers/dremio.py', py_import_name='sqlglot.parsers.dremio')]
files edited: [<PatchedFile: sqlglot/parsers/dremio.py>]
rare sqlglot/dialects/singlestore.py pranet sqlglot/dialects
986c.patch edited_elements [EditedElement(file_path='sqlglot/dialects/singlestore.py', py_import_name='sqlglot.dialects.singlestore'), EditedElement(file_path='sqlglot/typing/snowflake.py', py_import_name='sqlglot.typing.snowflake')]
files edited: [<PatchedFile: sqlglot/dialects/singlestore.py>, <PatchedFile: sqlglot/typing/snowflake.py>, <PatchedFile: tests/fixtures/optimizer/unnest_subqueries.sql>]
ary6.patch edited_elements [EditedElement(file_path='sqlglot/parsers/bigquery.py', py_import_name='sqlglot.parsers.bigquery')]
files edited: [<PatchedFile: sqlglot/parsers/bigquery.py>]
bj7g.patch edited_elements [EditedElement(file_path='sqlglot/generators/clickhouse.py', py_import_name='sqlglot.generators.clickhouse')]
files edited: [<PatchedFile: sqlglot/generators/clickhouse.py>]
rare sqlglot/dialects/materialize.py pranet sqlglot/dialects
bvw2.patch edited_elements [EditedElement(file_path='sqlglot/dialects/materialize.py', py_import_name='sqlglot.dialects.materialize')]
files edited: [<PatchedFile: sqlglot/dialects/materialize.py>, <PatchedFile: tests/fixtures/optimizer/annotate_types.sql>]
egys.patch edited_elements []
files edited: [<PatchedFile: tests/fixtures/optimizer/simplify.sql>]
f4bn.patch edited_elements []
files edited: [<PatchedFile: tests/fixtures/optimizer/pushdown_cte_alias_columns.sql>]
gbhk.patch edited_elements []
files edited: [<PatchedFile: tests/fixtures/optimizer/annotate_types.sql>]
j6uz.patch edited_elements [EditedElement(file_path='sqlglot/parsers/bigquery.py', py_import_name='sqlglot.parsers.bigquery')]
files edited: [<PatchedFile: sqlglot/parsers/bigquery.py>]
mthh.patch edited_elements []
files edited: [<PatchedFile: tests/fixtures/optimizer/merge_subqueries.sql>]
nwnx.patch edited_elements []
files edited: [<PatchedFile: tests/fixtures/optimizer/pushdown_projections.sql>]
st8f.patch edited_elements []
files edited: [<PatchedFile: tests/fixtures/optimizer/isolate_table_selects.sql>]