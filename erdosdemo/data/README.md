# Data

This folder contains the finite candidate-level anomaly CSVs used by the demo.

Included files:

- `anomalies_N65_candidates.csv`
- `anomalies_N70_candidates.csv`
- `sentinel/anomalies_N35_candidates.csv`
- `sentinel/anomalies_N36_candidates.csv`

N65 provenance:

- Source repository: `RexHannes/Math-demo`
- GitHub Actions artifact: `erdos287-anomaly-dump-N65-P65-merged`
- Workflow run id: `26154176653`
- Artifact id: `7106752331`
- Source commit prefix: `b40bf42`

N70 provenance:

- Source repository: `RexHannes/Math-demo`
- GitHub Actions artifact: `erdos287-anomaly-dump-N70-P70-merged`
- Workflow run id: `26170405455`
- Artifact id: `7113496334`
- Source commit: `3f3a12afd2ed469d4ce4e2747af245fe8d2dd4be`
- Artifact ZIP digest: `006713a5a531a779b50fe8cda27b7352c252b35d1d42fa11e17bfa1f39f71f20`

Sentinel provenance:

- Generated locally from `RexHannes/Math-demo` commit `3f3a12afd2ed469d4ce4e2747af245fe8d2dd4be`.
- Command family: `N=35` and `N=36`, `P=70`, window `[0.99, 1.01]`, `--dump-anomalies`.
- `src/erdos287_cover_hyb.cpp` SHA256: `e7b4a7fe0a50aaae0868b11442635f12934325a6552ca801c1d0e1eca327c08e`

Integrity:

```text
1525364f0dd280f5fb5b1cc153ef87ad0523c51628823cc7e0e4e9ff1e1b2f3c  erdosdemo/data/anomalies_N65_candidates.csv
96d6578fb48096692807bca6dc0c1495b68f9caa63557a2e7d8080c5cbfb859f  erdosdemo/data/anomalies_N70_candidates.csv
3490103f1cce601e9abd920f8ca686a016ef65ba2935d9b6206e51ddf6adcdbf  erdosdemo/data/sentinel/anomalies_N35_candidates.csv
c04fe76d9bc07c46579f0a5b87bbac6566940f861e56e08b80595534090d7a22  erdosdemo/data/sentinel/anomalies_N36_candidates.csv
```

Important scope note:

These CSVs are wide-window `[0.99, 1.01]` candidate anomaly files. They should not be described as complete `[0.999, 1.001]` candidate dumps.

The N70 artifact has the correct N70/P70 labels and N70-specific `p67` residue columns, but its workflow summary reported incomplete chunk-status sidecar coverage. The demo therefore relies on the independent denominator-only audit and the N35/N36 sentinel comparison for the narrow public claim.
