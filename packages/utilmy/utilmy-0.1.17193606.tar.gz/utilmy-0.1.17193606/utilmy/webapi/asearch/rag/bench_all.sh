#!/bin/bash
export PYTHONPATH="$(pwd)"

echo "PYTHONPATH: $PYTHONPATH"


dirquery=${1:-ztmp/bench/ag_news/kg_questions/common_test_questions_all.parquet}
echo $dirquery

shopt -s expand_aliases
#source ~/.bash_aliases

alias pybench="python rag/bench.py "
alias pykg="python rag/engine_kg.py "



echo "# All benchmarks - `date -I`" >> rag/zlogs.md
echo "\`\`\`" >> rag/zlogs.md

echo "## dense run" >> rag/zlogs.md
pybench bench_v1_dense_run --dirquery "$dirquery" --topk 5 | grep -v 'HTTP Request:'>> rag/zlogs.md
echo -e "\n\n" >> rag/zlogs.md

echo "## sparse run" >> rag/zlogs.md
pybench bench_v1_sparse_run --dirquery "$dirquery" --topk 5 | grep -v 'HTTP Request:'>> rag/zlogs.md
echo -e "\n\n" >> rag/zlogs.md

echo "## tantivy run" >> rag/zlogs.md
pybench bench_v1_tantivy_run --dirquery "$dirquery" --topk 5 >> rag/zlogs.md
echo -e "\n\n" >> rag/zlogs.md


echo "## neo4j run" >> rag/zlogs.md
pybench bench_v1_neo4j_run --dirquery "$dirquery" --topk 5 >> rag/zlogs.md
echo -e "\n\n" >> rag/zlogs.md

echo "## sparse+ neo4j run" >> rag/zlogs.md
pybench bench_v1_fusion_run --engine "sparse_neo4j" --dirquery "$dirquery" --topk 5 | grep -v 'HTTP Request:' >> rag/zlogs.md
echo -e "\n\n" >> rag/zlogs.md

echo "## dense+ neo4j run" >> rag/zlogs.md
pybench bench_v1_fusion_run --engine "dense_neo4j" --dirquery "$dirquery" --topk 5 | grep -v 'HTTP Request:' >> rag/zlogs.md
echo -e "\n\n" >> rag/zlogs.md

echo "## tantivy+ neo4j run" >> rag/zlogs.md
pybench bench_v1_fusion_run --engine "tantivy_neo4j" --dirquery "$dirquery" --topk 5  >> rag/zlogs.md
echo -e "\n\n" >> rag/zlogs.md

# generate text from metrics
pybench report_create_textsample --dirquery "$dirquery"
echo "\`\`\`" >> rag/zlogs.md
