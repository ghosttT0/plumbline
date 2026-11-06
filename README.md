# Plumbline

**A benchmark and analysis toolkit for LLM code review.**

[中文说明](README.zh-CN.md)

Plumbline studies how language-model reviewers identify code issues, attribute findings to architectural rules, and make approval decisions. It brings together code-change diffs, reviewer responses, source-grounded annotations, prompt templates, and scripts for reproducing the evaluation.

This repository accompanies **Flagging Is Not Naming: Mention, Attribution, and Verdicts in LLM Code Review**.

## Quick start

Requires **Python 3.11+**. The analysis uses the Python standard library and runs locally on the included data.

```sh
git clone https://github.com/ghosttt0/plumbline.git
cd plumbline
python reproduce.py
```

The command recomputes the results, checks 93 values against the reference summary, and writes:

- `outputs/summary.json` — experiment counts, approval rates, issue precision, rule attribution, and sampling stability.
- `outputs/verification.json` — the verification results.

Run the tests and check file integrity:

```sh
python -m unittest discover -s tests -v
python verify.py
```

## Benchmark

The benchmark covers three Python codebases: **rentomatic**, **full-stack-fastapi-template**, and **Saleor**.

- **66 main items**: 33 original-grid items and 33 expansion items.
- **836 reviewer responses**: 396 core responses, 132 GPT-track responses, and 308 expansion responses.
- **660 distinct review cells**, with repeated sampling on expansion leak items.
- **686 reviews with final issue-level annotations**.
- **72 additional responses** from an 18-item paired-burial pilot, analyzed separately.

The evaluation separates construct mention, design-rule attribution, issue validity, and the reviewer's approve/reject verdict. Review annotations follow the paper's human double-blind coding and adjudication protocol.

See [DATA_DICTIONARY.md](DATA_DICTIONARY.md) for record fields, joins, labels, and analysis units.

## Review conditions

The data uses four condition keys:

- `bare` — PR title and diff.
- `generic` — architecture context and the standard reviewer persona.
- `design` — architecture context and a design-review persona.
- `linter` — architecture context and detector/mutation evidence.

Render a prompt for a benchmark item:

```sh
python render_prompt.py D2-a bare
python render_prompt.py D2-a design
```

Architecture statements and system-prompt templates are stored in [`prompts/`](prompts/).

## Repository layout

```text
data/                 Benchmark items, model responses, annotations, and pilot data
prompts/              Architecture context and reviewer prompt templates
materials/            Frozen upstream commits and source snapshots
expected/             Reference results used by the verification checks
outputs/              Recomputed summaries and verification reports
tests/                Data, metric, and prompt-rendering tests
licenses/             Upstream source license notices
reproduce.py          Recompute and check experiment statistics
render_prompt.py      Render the prompt for an item and condition
verify.py             Check repository files, hashes, and data hygiene
```

## Working with the data

Main review records are in [`data/reviews.jsonl`](data/reviews.jsonl). Join their `release_id` to [`data/annotations.jsonl`](data/annotations.jsonl) to inspect the corresponding judgments and checking evidence. Full code-change diffs are in [`data/items.jsonl`](data/items.jsonl).

The pilot has separate item, response, and annotation files. Pilot annotations join to responses through `review_id`.

[`materials/upstream_sources.json`](materials/upstream_sources.json) records upstream URLs and frozen commits. [`materials/clean_source_snapshots.zip`](materials/clean_source_snapshots.zip) provides before/after source states for the six agent-control items.

## Integrity and source licenses

`MANIFEST.json` records SHA-256 hashes for the repository materials. After an intentional file update, regenerate and check the manifest:

```sh
python verify.py --build-manifest
python verify.py
```

Upstream source code and excerpts retain the license notices in [`licenses/`](licenses/).
