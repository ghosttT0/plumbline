# Anonymous review artifact

Artifact for **Flagging Is Not Naming: Mention, Attribution, and Verdicts in LLM Code Review**.

## Quick start

Python 3.11+; no API keys, third-party packages, network access or Docker required for the default checks:

```sh
python reproduce.py
python -m unittest discover -s tests -v
python verify.py
```

`reproduce.py` recomputes the archived summary from the included review/annotation records and compares 93 summary values with the frozen expectations. Results are written to `outputs/summary.json` and `outputs/verification.json`.

## Included experiments

- Main grid: 33 items, three core reviewers, four conditions — 396 responses.
- GPT-track replication: the same 33 items and four conditions — 132 responses.
- Expansion: 33 additional items — 308 responses, including three repetitions per condition for 22 leak items.
- Main total: **66 items, 836 responses, 660 distinct cells**.
- Final issue-level annotations: **686 reviews**. The remaining 150 reviews are outside this final issue-level annotation dataset.
- Paired-burial pilot: **18 items and 72 responses**, stored and analyzed separately.

The formal annotation protocol follows the paper: two independent human coders received metadata-blinded review packets, followed by human adjudication. Anonymous review IDs and the analysis metadata needed for reproduction are included; participant identities and internal working records are not.

## Contents

- `data/`: full item diffs, verbatim reviewer text, final annotations, pilot data, and item-status definitions.
- `prompts/`, `render_prompt.py`: architecture statements, system-prompt templates and user-message rendering.
- `reproduce.py`, `tests/`, `expected/`: offline recomputation and frozen expectations.
- `materials/`: upstream URLs/commits and compact frozen before/after source snapshots for the six agent-control items.
- `licenses/`: upstream license notices.
- `DATA_DICTIONARY.md`: population definitions and joins.
- `MANIFEST.json`, `verify.py`: release-file integrity and anonymity checks.

Example prompt rendering (no API call): `python render_prompt.py D2-a bare`.

The package contains the analysis populations and final research materials, not a dump of the collection workspace. Earlier/superseded runs, chat/curation notes, budgets, temporary outputs, debugging scripts, Git history and environment folders are excluded. The paper is submitted separately and is not duplicated here. Verbatim main review text and issue-label values are unchanged.

## Source reconstruction

`materials/upstream_sources.json` pins the three upstream base commits. Historical human PRs also carry their own parent/head provenance in the item records. `materials/clean_source_snapshots.zip` contains fixed before/after input states, without Git metadata or local environments. Extract these only when inspecting source-level evidence; the default offline statistics do not require extraction.

Prompt rendering displays the archived template definitions; it is not represented as a wire capture for every historical request. Historical validation descriptions remain in item metadata. This package reproduces the archived evaluation rather than starting a new model collection.

## Review use

Provided for anonymous peer review. Included upstream code/excerpts retain the notices in `licenses/`. No additional public redistribution license is asserted for the original research materials.
