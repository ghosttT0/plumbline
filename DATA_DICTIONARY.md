# Data dictionary

## Main dataset

### Items — `data/items.jsonl`

Contains 66 benchmark items. Each record includes an `id`, `campaign`, `cat`, title, full code-change diff, and available validation/provenance metadata. Item status and analysis groups are defined in `data/item_status.json`.

### Reviews — `data/reviews.jsonl`

Contains 836 model responses. `release_id` uniquely identifies each response. The fields `campaign`, `item`, `model`, `mode`, and `rep` identify its experimental setting. `text` contains the model response; `verdict` contains the parsed approve/reject decision.

Campaigns are `core`, `gpt_replication`, and `expansion`. Model identifiers use the strings recorded during collection, including `deepseek-chat`.

### Annotations — `data/annotations.jsonl`

Contains 686 final issue-coded review records. Join to reviews through `release_id`. Records preserve the blinded `review_id`, issue labels, and checking evidence. `track` is the original-grid analysis field; `campaign` identifies the population across the full dataset.

Human coders independently assessed metadata-blinded review packets, followed by adjudication, as described in the paper. Analysis metadata is included with the released records to support reproduction.

## Paired-burial pilot

The pilot comprises 18 items and 72 responses:

- `data/pilot_items.jsonl` — the minimal, buried, and carrier-only item variants.
- `data/pilot_reviews.jsonl` — model responses and their item/model identifiers.
- `data/pilot_annotations.jsonl` — supplied attribution judgments.

Join pilot responses and annotations through `review_id`. The annotation `case_id` corresponds to the response `item`.

## Conditions

- `bare`: PR title and diff.
- `generic`: architecture context with the standard reviewer persona.
- `design`: architecture context with a design-review persona.
- `linter`: architecture context with detector/mutation evidence.

The stored key `generic` denotes the architecture condition. Prompt templates and architecture statements are in `prompts/`.

## Labels

Issue-level labels are:

- `T`: verified substantive issue.
- `P`: verified minor or conditional issue.
- `I`: refuted premise.
- `U`: undetermined issue.

At review level, `tpi=T` means that the review contains at least one verified substantive issue. Construct-level `Y`/`N` labels describe whether the reviewer names the target construct or rule. `item_status.json` supplies the corresponding item classifications, including adjudicated non-violations and out-of-view items.

The `clean` category identifies a control population. Findings on control items retain their source-checked labels.

## Analysis units

The main dataset has 836 responses across 660 distinct `(campaign, item, model, mode)` cells. Expansion leak cells contain three repetitions each. The 88 repeated leak cells are the sampling-stability population.

Approval rates use valid verdicts. The dataset retains one invalid verdict, which gives 71 valid verdicts in the relevant agent-control denominator. Review-level yields and issue-level precision use their respective review and issue counts.

The 72 pilot responses form a separate population. Pilot family X is an adjudicated non-violation; the R/C families are used for violation-attribution comparisons.

## Source materials

`materials/upstream_sources.json` records frozen upstream commits. Historical human PR items also include their own upstream source provenance. `materials/clean_source_snapshots.zip` contains fixed before/after states for the six agent-control items. Project authors named in upstream PR metadata are the authors of those source changes.
