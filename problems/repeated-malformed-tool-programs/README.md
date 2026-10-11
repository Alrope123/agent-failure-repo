# Five successive malformed orchestration programs fail before inspection

Status: incident-only report. Symptom: other (tool orchestration syntax).

The user requested schema grouping and generator configuration changes. Instead of submitting executable JavaScript to the orchestration tool, the agent submitted prose and four malformed programs. All five calls returned `SyntaxError` before the intended inspection could execute. The agent then resumed valid inspection and completed the requested work. The observed consequence is five failed tool interactions and a short delay; no persistent code damage or lost user data is established.

[Selected historical evidence](evidence/README.md) contains the request, each failed call/result pair, recovery and redaction limits. The source is a Codex history; the exact model is unavailable. These are original historical errors, not fresh reproduction results.

The first failed call is H01:L209 and the last is L229. There are three strictly intervening tool calls, zero intervening assistant messages and one session. Their recorded submission timestamps differ by 15.679 seconds. This is a short local retry episode. No claim links it to long context, memory loss or an internal reasoning process.

A future reproduction should expose the JavaScript exec interface and a harmless local schema-inspection task. The target failure is a parse-invalid orchestration program that prevents nested inspection, with repeated invalid retries recorded separately. Correct task completion requires valid inspection and the requested schema/configuration edits. Unavailable tools, broken environment setup and unrelated command failures must be classified separately; a SyntaxError caused by a malformed evaluator fixture is invalid setup, not an agent hit.

Reproduction, judge, reference, controls and model evaluation are **not implemented and not run**. All manifest commands remain null and result records are empty. The scaffold task, environment, checks and reference directories contain explanatory notes only. No successful/faulty controls or comparative outcomes are claimed. Next action is to design a disposable execution harness that distinguishes orchestration parsing from nested shell execution before attempting a model evaluation.

The evidence supports this local workflow failure and subsequent recovery. It does not show an unmet final acceptance requirement. Public excerpts omit private identifiers and unrelated history; owner review is still required before sharing. No uploads occurred.
