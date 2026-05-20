# Erdős 287 Finite N=65 Demo

This folder is a compact, MathOverflow-facing verification demo. It does not prove Erdős #287. It verifies a finite N=65 candidate-level anomaly pattern in one exported dataset.

The live heavy workflows remain in the main `RexHannes/Math-demo` repository under `.github/workflows`. The workflow files copied into `erdosdemo/workflows/` are provenance references only; GitHub Actions does not run workflows from this folder.

## Scope

- Denominator cutoff: `N = 65`
- Prime cutoff used by the run: `P = 65`
- Candidate window for this CSV: `[0.99, 1.01]`
- Total anomaly rows: `137`
- Backbone split: `2+31 = 68`, `19+37 = 69`
- Classification residual: `0` unclassified rows under the four finite templates below

The tighter `[0.999, 1.001]` mask-level certificate is a separate artifact in the main work. This folder packages the complete candidate-level CSV currently available, which is the `[0.99, 1.01]` finite pattern.

## Fast Check

```bash
python3 erdosdemo/scripts/verify_n65_templates.py
```

Expected output:

```text
rows: 137
backbone counts:
  19+37: 69
  2+31: 68
template counts:
  2+31 + {8,24}: 63
  2+31 + {12,20}: 5
  19+37 + {22}: 58
  19+37 + {21,23}: 11
unclassified rows: 0
PASS
```

## Other Checks

```bash
python3 erdosdemo/scripts/verify_dataset_basic.py
python3 erdosdemo/scripts/verify_residue_blocks.py
```

These scripts recompute exact reciprocal sums, check denominator bounds, print the CSV SHA256, and verify the small residue-block arithmetic used in the notes.

## Files

- `data/anomalies_N65_candidates.csv`: the finite N=65 candidate anomaly dataset.
- `data/anomalies_N65_candidates.sha256`: SHA256 checksum for the CSV.
- `scripts/verify_n65_templates.py`: verifies row counts, forced cores, and four-template classification.
- `scripts/verify_dataset_basic.py`: verifies dataset integrity and basic arithmetic bounds.
- `scripts/verify_residue_blocks.py`: verifies the small p-adic residue blocks.
- `notes/top_layer_obstruction.md`: short statement of the top-layer obstruction lemma.
- `notes/n65_finite_pattern.md`: finite-pattern summary.
- `workflows/`: copied provenance YAMLs, not live workflows.

