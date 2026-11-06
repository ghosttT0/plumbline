# Data dictionary

## Files and joins

- `items.jsonl`: 66 main item records with `id`, `campaign`, `cat`, title, complete diff and supplied validation/provenance metadata.
- `reviews.jsonl`: 836 main records. `release_id` is unique. `campaign` distinguishes `core`, `gpt_replication`, and `expansion`; `item`, `model`, `mode`, `rep` identify the response. `text` is the verbatim archived output and `verdict` is the parsed blocking decision.
- `annotations.jsonl`: 686 final issue-coded review records, joined to reviews by `release_id`. Original blinded `review_id` values and issue checking evidence are retained. `track` is a historical analysis field; `campaign` is the release-level population field.
- `pilot_items.jsonl`, `pilot_reviews.jsonl`, `pilot_annotations.jsonl`: the separate 18-item/72-response paired pilot. Pilot attribution labels join directly to pilot responses by original `review_id`; the annotation `case_id` matches the response `item`. Original case/item IDs and model aliases are retained.
- `item_status.json`: adjudicated non-violations, the pilot X family, out-of-view expansion items, validated bugs and title-congruent changes.

Curation-only source filenames, local source-line references, chunk names and packaging/author-confirmation metadata are omitted from the review release. Review text, scientific item metadata, checking evidence and label values are preserved.

## Conditions

- `bare`: diff, without the architecture statement.
- `generic`: architecture statement with the standard reviewer persona.
- `design`: architecture statement with a design-review persona.
- `linter`: architecture statement with detector/mutation evidence.

The raw key `generic` names the architecture condition. Model aliases are retained as recorded, including `deepseek-chat`; aliases are not silently converted into backend/version claims.

## Labels and denominators

`T` denotes a verified substantive issue, `P` a verified minor/conditional issue, `I` a refuted premise and `U` an undetermined issue. At review level, `tpi=T` means at least one verified substantive issue. Review-level yields and issue-level precision use different denominators.

The main 836 responses include one invalid verdict. Approval fractions exclude invalid verdicts, so agent-control approvals can use 71 as the denominator. Sampling stability uses 88 leak cells with three repetitions each. The 72 pilot responses are not part of 836. The pilot X family is an adjudicated non-violation and is kept separate from R/C violation attribution.

A `clean` category is a control provenance label, not a guarantee that every issue in that code is absent. Historical human PR source provenance refers to upstream project authors, not submission authors.
