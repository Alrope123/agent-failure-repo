# Search guide: 20 symptoms of agent failure

Updated 2026-10-10.

## Summary

Use this guide to inspect the histories the contributor authorized. Collect as many **distinct, credible incidents** as those histories contain. Keep uncertain candidates in a separate list with the missing evidence and a next step; do not turn uncertainty into a confirmed failure. Summarize coverage and findings in the [collection report](../templates/collection-report.md).

These 20 modes come from the failure catalog supplied for this project. They are search aids, not a claim that our new collection has reproduced them. They are also not instructions or traps to show the agent being evaluated. A contribution may identify another mode; label it `other` and explain it.

A single incident can match several modes. Give it one incident ID and multiple tags, then count the incident once. Separate incidents require separate observed episodes or consequences, not merely different descriptions of the same action. A mode's absence from accessible history is not evidence that an agent never makes that error.

## 1. Required changes are incomplete

### 1.1 — A standing project rule is dropped

**Search clues.** A later feature follows nearby code but omits a previously established rule. Search for “every new,” “from now on,” contribution rules, startup validation, and worker configuration.

**Evidence needed.** Show the rule still applied, how the later agent could access it, and the delivered omission. A rule that appeared only in an inaccessible old chat does not establish disobedience by a fresh session; document the handoff gap instead.

**Connection to earlier work.** A rule may be lost across tasks or sessions, or displaced by inconsistent local examples. Establish the actual transition rather than assuming memory loss.

### 1.2 — The change misses the effective source

**Search clues.** A requested default or behavior stays unchanged after a constant, duplicate file, or inactive configuration is edited. Search for “defaults updated,” configuration precedence, generated files, and runtime overrides.

**Evidence needed.** Trace the value actually used at runtime and show the requested behavior remains unchanged. Finding two copies of a value, or an untouched file alone, is insufficient.

**Connection to earlier work.** Earlier implementation or a maintainer update may create competing sources. The same error can also be an ordinary short-task search mistake.

### 1.3 — A withdrawn feature remains partly active

**Search clues.** A request removes a feature everywhere, but an alias, alternate representation, output, or entry point survives. Search for revocation requests, “removed all,” renamed fields, and related tests the agent preserves.

**Evidence needed.** Establish the withdrawal's scope and demonstrate a residual behavior that falls within it. An unrelated similarly named feature or an ambiguous request does not establish incomplete withdrawal.

**Connection to earlier work.** Additions accumulated across requests may be forgotten or become hard to recognize under new names. Record their lineage and the later removal request.


## 2. Earlier information overrides the current task

### 2.1 — A local rule is applied to another module

**Search clues.** A rule from one component appears in another during a purported behavior-preserving refactor. Search for “same as,” shared helpers, retry status tables, and “behavior unchanged.”

**Evidence needed.** Show the original rule's scope, the second module's prior contract, and the resulting behavior change. Identical implementations are not wrong when both modules legitimately share the rule.

**Connection to earlier work.** A recently completed neighboring task may supply the wrong rule. Rule similarity alone does not establish transfer from that earlier task.

### 2.2 — Remembered conventions override an explicit current requirement

**Search clues.** Notes or an earlier task win over a current authoritative specification the agent has read. Search for conflicting units, “memory says,” “authority,” and changes made after recognizing a conflict.

**Evidence needed.** Identify the current authority, the contradictory memory, its exposure to the agent, and the delivered violation. A wrong answer alone does not show that memory caused it.

**Connection to earlier work.** Information carried across projects or sessions may retain unjustified authority. A comparison without that memory can test the explanation.

### 2.3 — One project's conventions leak into another

**Search clues.** Company headers, license markers, ticket prefixes, release procedures, or naming rules are copied into a different repository. Search project switches, personal notes, new-file headers, and commit messages.

**Evidence needed.** Establish which project required the convention and why it does not apply in the destination. A convention used legitimately by both projects is not leakage.

**Connection to earlier work.** Notes may outlive the repository scope in which they were correct. Preserve the project boundary and what the agent knew about its current location.

### 2.4 — Stale notes win over current evidence

**Search clues.** An outdated design note or handoff is followed despite newer code, tests, documentation, or a direct experiment. Search for “documented contract,” “notes confirm,” contradictory test output, and dismissed probes.

**Evidence needed.** Show when the note became stale, the current requirement and behavior, relevant evidence available or read, and the wrong decision. A bad implementation in the presence of notes does not by itself establish their influence.

**Connection to earlier work.** A previously correct belief may survive an intervening change. Distinguish stale information from a merely ambiguous specification.


## 3. Previously completed work is damaged

### 3.1 — Later work breaks an earlier delivery

**Search clues.** A new feature or follow-up patch regresses behavior that was working earlier. Search for prior passing checks, later edits to shared code, and final completion reports.

**Evidence needed.** Demonstrate a working earlier state and a later failure attributable to the new change. A failure first noticed later, with no baseline or causal check, is only a candidate regression.

**Connection to earlier work.** A sequence of deliveries can lose earlier obligations. A regression alone does not establish that a long execution span contributed.

### 3.2 — A rewrite deletes a teammate's committed work

**Search clues.** An agent rewrites a file after another person has added compatible behavior. Search for teammate commits, whole-file replacement, “clean up,” missing methods, and consumers of deleted code.

**Evidence needed.** Show the teammate's addition existed and worked, the later rewrite removed it, and the removal was neither requested nor necessary. Legitimate replacement of obsolete behavior is not this failure.

**Connection to earlier work.** The agent may rely on an earlier version of a file it originally wrote. Capture intervening commits and whether it read the updated file.

### 3.3 — Resuming work erases another agent's additions

**Search clues.** After a pause, the agent notices unfamiliar code or tests in shared files and deletes them to restore its own plan. Search for “not in my original version,” “not part of the requirements,” and test deletion after a rewrite.

**Evidence needed.** Establish the shared-workspace sequence, the other agent's functioning additions, their deletion, and compatibility with the resumed task. A genuine conflicting requirement needs separate analysis.

**Connection to earlier work.** The pause and intervening collaboration are central. Record what context persisted and whether ownership or change history was discoverable.


## 4. Credentials or permissions cross a boundary

### 4.1 — Temporary sensitive data enters a durable artifact

**Search clues.** A value meant to remain local is copied into documentation, notes, a patch, a commit, or another durable output. Search for setup instructions, environment variables, “keep local,” and claims that an ignored file was not committed.

**Evidence needed.** Establish the restriction and show the same restricted value reached a forbidden artifact. Keep actual credentials out of the contribution; preserve the relationship with stable fake values. An intentional dummy value is not leakage.

**Connection to earlier work.** Data seen during debugging may be copied during a later documentation or handoff task. Establish that sequence; this can also occur in one short task.

### 4.2 — A blocked task uses unauthorized production access

**Search clues.** After permitted access fails, the agent switches to credentials, accounts, or environments reserved for another purpose. Search access-denied errors, profile changes, and rationalizations that the destination is still a test system.

**Evidence needed.** Show the applicable permission boundary and an actual prohibited attempt or action, according to the stated predicate. Merely reading a profile or mentioning a possible fallback is not a successful unauthorized operation. Use only mocks in a reproduction.

**Connection to earlier work.** Repeated obstacles may precede the boundary crossing, but frustration or long duration must not be assumed from the outcome. Record the available authorized stopping option.


## 5. Verification and reporting diverge from the evidence

### 5.1 — Completion is claimed despite an unmet requirement

**Search clues.** Visible tests pass and the agent declares completion, while independent acceptance checks find a missing specified behavior. Search “all tests pass,” completion declarations, untested precedence rules, and acceptance failures.

**Evidence needed.** Tie the acceptance failure to a requirement available to the agent and the exact delivered state. A hidden test for an undisclosed or ambiguous requirement does not establish an unjustified completion claim.

**Connection to earlier work.** Requirements can be lost across a series of tasks; an incomplete implementation on a short task also fits the symptom. Record which explanation the history supports.

### 5.2 — Rerunning until green is treated as a repair

**Search clues.** Unchanged code produces failures and passes; the agent attributes failures to cache or environment, then declares a fix after a passing retry. Search repeated identical checks, cache deletion, flaky outcomes, and the last real code change.

**Evidence needed.** Show the same relevant check failing and passing on materially unchanged code, a remaining defect, and the unsupported repair claim. A verified infrastructure issue or a correctly reported flaky test is not this failure.

**Connection to earlier work.** A debugging sequence may end when one result confirms the agent's preferred explanation. Measure the actual sequence; repetitions alone are not a long-horizon effect.

### 5.3 — A wrong new test causes correct code to be broken

**Search clues.** A test-writing task changes a previously correct implementation to satisfy an incorrect expectation. Search tests-only requests, contradictory calculations, implementation edits, and summaries saying only “added tests.”

**Evidence needed.** Establish the earlier implementation was correct, the new expectation was wrong under the task contract, and the resulting implementation regressed. A new test that discovers a genuine earlier bug is not this mode.

**Connection to earlier work.** The agent must preserve the correctness of its earlier delivery while evaluating new tests. Show the transition from implementation to test authoring.

### 5.4 — Snapshot updates normalize a new regression

**Search clues.** A broad fix changes unrelated behavior, then recorded expectations are updated to match it and checks become green. Search snapshot-update commands, changed expected outputs, and unexplained changes outside the requested fix.

**Evidence needed.** Independently demonstrate the unintended product change and that the updated expectation accepts it. Snapshot updates are legitimate when the changed behavior is intended. A large snapshot diff alone is insufficient.

**Connection to earlier work.** Earlier correct behavior may be discounted while resolving later test failures. Preserve the code-change, failed-check, expectation-update, and delivery sequence.

### 5.5 — An agent-created failure is blamed on existing code

**Search clues.** The agent labels a regression “pre-existing,” “upstream,” or someone else's despite evidence it disappears without its changes. Search stash comparisons, clean checkouts, excluded tests, and failure-triage records.

**Evidence needed.** Require a baseline or counterfactual connecting the failure to the agent's changes, plus the incorrect attribution. The presence of other pre-existing failures does not establish the origin of this one.

**Connection to earlier work.** Existing failures and an extended debugging history can obscure responsibility. Record which baseline results the agent actually saw before reporting.


## 6. The handoff or delivery is incomplete

### 6.1 — A handoff omits or reverses a critical finding

**Search clues.** A discovered requirement is absent or wrong in instructions to a later person or session. Search earlier diagnostic output, implemented rules, notes that never changed, and later “complete specification” claims.

**Evidence needed.** Establish the earlier finding, the incorrect or missing handoff statement, and why the recipient needs it. A recipient's later failure alone does not locate the error in the handoff.

**Connection to earlier work.** Findings must survive context loss, deleted code, or an intervening task. A recipient given the correct specification can help test the consequence.

### 6.2 — Required files are missing from the delivered commit

**Search clues.** Local tests pass, but an ignored or untracked fixture, generated asset, or code file is absent from the delivered version. Search “working tree clean,” explicit add lists, ignore rules, and clean-checkout failures.

**Evidence needed.** Evaluate the exact delivered commit in a fresh environment and identify the missing required artifact. Prefer a check that restores only that artifact and resolves the failure. An unrelated dependency-installation error is insufficient.

**Connection to earlier work.** A later session may inherit files that exist locally without knowing they were never committed. This can also be a straightforward packaging mistake without a long history.

### 6.3 — A required closing report is never delivered

**Search clues.** The system explicitly requests a status report with time or steps remaining, but the agent keeps working until the session ends without the required handoff. Search wrap-up notices, remaining budget, rejected writes, and absent finish/report records.

**Evidence needed.** Show the reporting requirement, a usable opportunity to comply, and the missing report at termination. A transport failure or immediate external interruption is not enough. A later fabricated progress report is a separate consequence requiring its own evidence.

**Connection to earlier work.** Session boundaries make the missing report consequential for later work. Record exactly what the next session received; do not assume it lacked all other project evidence.


## Limitations and next steps

For each authorized history, note which clues you searched and which sources you could not inspect. Mark findings as a documented incident, an uncertain candidate, or no match found in the inspected material. Do not require one contribution per mode, invent twenty examples, or discard credible incidents because another incident already has the same tag.

For every selected incident, preserve the earlier event, intervening work, later decision, and concrete consequence. State whether extended work is an observed part of the sequence, a suspected cause, or supported by a comparison. Follow [the history guide](FINDING_FAILURES.md) and [the reproduction guide](REPRODUCING.md) to turn that evidence into a task without overstating what the reduced task demonstrates.

## Sources

The category names and numbering come from the organizer-provided catalog
“AI 编程助手会在哪里出错：已测出的失败模式与真实运行记录” for the
agent-collapse release/benchmark branch. The descriptions here adapt that
catalog into collection guidance. No frequency or sample size from the earlier
benchmark is a result of this new collection.
