# Copy these forms, then replace uncertainty with evidence

`problem/` is copied by the scaffolder. `result.json` describes one attempted
run and is copied manually into `results/<problem-id>/<run-id>/summary.json`.
Null values mean unknown or not yet available. They are not measured zeros.

The problem status is one of `incident`, `packaged`, `model_reproduced`, or
`temporal_supported`. These mark progressively stronger evidence, not a score.
The guides explain their meaning. A package does not need to reach the final
status to be a useful contribution.

`privacy_reviewed` starts false. Only change it after the owner reviews the
exact files intended for sharing. The validator cannot perform that review.
Do not copy private originals into these templates.

Start a private collection ledger by copying `collection-report.md` and
`incident-index.csv` into `.local/` or another private directory. Inspect all
authorized sources and all symptom categories, then log every distinct candidate.
Use semicolons between multiple symptom IDs in the CSV cell. Each source label
must refer to the collection report; event references stay local until reviewed.
Do not equate several labels with several independent incidents.

Use `symptoms` in each problem manifest to record the existing IDs or `other`.
Unknown categories can remain empty in a draft. The metadata checker does not
check the completeness of your search; the collection report makes its limits
reviewable.
