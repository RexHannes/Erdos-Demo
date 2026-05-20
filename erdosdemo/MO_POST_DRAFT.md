# MathOverflow Draft: A finite p-adic anomaly pattern in an Erdős #287 computation

I am looking for conceptual explanations for a finite pattern that appeared in a computational experiment related to Erdős #287. I am not claiming a proof of the problem.

For a finite search with denominator cutoff `N = 65`, I enumerated candidate denominator sets `S` in a near-sum window around 1 and recorded which prime-modulus top-layer obstructions eliminate each candidate. The candidate-level dataset packaged here uses the window `[0.99, 1.01]`.

Two prime-pair backbones are especially close to covering all candidates:

```text
{2,31}: 68 exceptions
{19,37}: 69 exceptions
```

The 137 exception rows have a surprisingly simple finite classification:

```text
2+31 + {8,24}:      63
2+31 + {12,20}:      5
19+37 + {22}:       58
19+37 + {21,23}:    11
unclassified:        0
```

There are also forced small cores:

```text
Every 2+31 exception contains {15,17}.
Every 19+37 exception contains {18,20}.
```

The question is not whether this finite computation proves Erdős #287. It does not. The question is:

> Is there a known p-adic or Egyptian-fraction mechanism that would naturally force small cores such as `{15,17}` and `{18,20}` in the exceptions to these near-covering prime pairs?

The repository contains:

```text
erdosdemo/data/anomalies_N65_candidates.csv
erdosdemo/scripts/verify_n65_templates.py
erdosdemo/scripts/verify_residue_blocks.py
erdosdemo/notes/top_layer_obstruction.md
erdosdemo/notes/n65_finite_pattern.md
```

The intended minimal verification command is:

```bash
python3 erdosdemo/scripts/verify_n65_templates.py
```

I would especially appreciate pointers to comparable finite p-adic obstruction phenomena, or reasons this kind of small-core split should be expected rather than exceptional.

