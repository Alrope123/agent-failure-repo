# Historical evidence: An answer parser accepts a lowercase ambiguous choice as a valid MC answer

This is a minimal selected historical excerpt, not a full transcript. H01 and H07 are stable aliases for the two reviewed histories; L numbers refer to original archive lines.

- H07:L312 agent states that ambiguous/unparseable responses will be invalid; H07:L377 reports implementation completed and says ambiguous responses are invalid.
- H07:L327 historical implementation uses case-insensitive leading-answer detection and case-sensitive uppercase standalone-option collection:

```python
_STANDALONE_UPPERCASE_OPTION = re.compile(r"(?<![A-Za-z])[ABC](?![A-Za-z])")
```

It collects the leading match and explicit-answer matches, adds the standalone uppercase matches, and accepts a singleton candidate set. The leading detector uses `re.IGNORECASE`.
- Reviewer counterexample against those exact regexes: `a or b` returns `A`; `A or B` returns `None`; `(b)` returns `B`.
- H07:L606 and L637 show four ordinary Llama answers parsed correctly and scored4/4. No historical lowercase ambiguous answer or actual historical mis-score appears. The lowercase ambiguity is a newly exercised static counterexample to the archived implementation contract.

Observed horizon: 3 substantive visible user/assistant messages from requirement to selected action, inclusive; line aliases are archive positions, not causal measures.

Evidence limit: Counterexample is reviewer-reproduced against archived code, not a historical recorded mis-score. No user explicitly enumerated lowercase ambiguity; the parser supports lowercase forms and agent stated an ambiguity-invalid contract at 312/377. No claim that the four observed Llama answers were incorrectly graded.

Redactions and omissions: private filesystem roots, job/session/event identifiers, hostnames, unrelated messages, tool boilerplate, duplicate patch echoes and hidden reasoning are omitted. No credential values are included. Quoted prose is verbatim unless marked transformed; transformed snippets preserve the relevant operation and ordering. Owner sharing approval has not been requested or assumed.
