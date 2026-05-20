# N=65 Finite Pattern

This note summarizes only the finite candidate-level CSV in `erdosdemo/data/`.

Scope:

```text
N = 65
P = 65
window = [0.99, 1.01]
rows = 137
```

Backbone split:

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

N=70 is not summarized here. It is pending / separate, and should be discussed from its own `anomalies_N70_candidates.csv` artifact once that run is complete.

