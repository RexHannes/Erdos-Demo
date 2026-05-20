# N65/N70 Finite Pattern

This note summarizes only the finite candidate-level CSV in `erdosdemo/data/`.

Scope:

```text
N = 65, P = 65
N = 70, P = 70
window = [0.99, 1.01]
rows = 137 in each main CSV
```

The denominator-normalized N65 and N70 row sets are identical:

```text
N65 not in N70: 0
N70 not in N65: 0
max denominator: 36
```

The N35/N36 sentinel check gives:

```text
N35 rows: 116
N36 rows: 137
N70 rows: 137
N36 vs N70 difference count: 0
```

Backbone split in both main CSVs, recomputed from denominators by `verify_n65_n70_audit.py`:

```text
2+31: 68
19+37: 69
```

Forced cores verified by `verify_n65_templates.py`:

```text
Every 2+31 row contains {15,17}.
Every 19+37 row contains {18,20}.
```

Four-template classification:

```text
2+31 + {8,24}:      63
2+31 + {12,20}:      5
19+37 + {22}:       58
19+37 + {21,23}:    11
unclassified:        0
```

The template checks are priority checks. For example, a `2+31` row containing `{8,24}` is assigned to that template even if it also contains `{12,20}`.

This is a finite saturation observation, not a proof of an infinite phenomenon.
