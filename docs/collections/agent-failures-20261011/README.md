# Agent failure collection

Unified authorized workspace and one-to-many project collection. Project provenance is retained in one index. **426 candidate/reference rows, 79 checker-tested reductions, and 1 incident-only report.** Duplicate rows are references, not additional failures.

[Complete sanitized index](incidents.csv) · [Provider and project coverage](coverage.md)

Disposition counts: {'packaged': 79, 'uncertain': 30, 'not-a-failure': 29, 'duplicate': 183, 'needs-more-evidence': 22, 'rejected': 57, 'rejected-ambiguous-requirement': 2, 'rejected-as-4.1': 13, 'infrastructure-blocked-not-supported-agent-failure': 9, 'incident-only': 1, 'rejected-as-separate': 1}.

All **319 actual scripted checker attempts** remain recorded: 318 valid and 1 invalid development attempt. Correct and deliberately faulty controls test deterministic decision reductions. Superseded controls, clean-copy reruns and the invalid attempt are retained. No fresh model runs or historical job replays. The incident-only report explicitly records reproduction/evaluation not run. Consolidation copied package and result contents unchanged and introduced no new checker runs.

Problem documentation and historical evidence explain observed errors, horizon, meaning, recovery, contrary evidence, intended failure and fidelity limits. Local mock tasks expose stronger explicit information than some original tasks and omit unrelated work; passing controls do not establish historical causation or model reproduction.

Proposed sharing contains this summary/index/coverage, problem documentation and historical evidence, mock task/environment/check/reference files, and recorded result evidence. Raw histories, private indexes, private reports, and the attribution-uncertain draft controls are excluded. Nothing uploaded; owner authorized publication to DylanZSZ/agent-failure-repo.
