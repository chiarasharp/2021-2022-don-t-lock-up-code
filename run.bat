@echo off
title OpenCitations-pipeline

cd run

python -m 1_divide_dois_by_journals_DOAJ
python -m 2_filter_OC
python -m 3_groupBy_OC
python -m 4_concat_groupBy_OC
python -m 5_make_ratio
python -m 6_add_useful_metrics

cd ..


