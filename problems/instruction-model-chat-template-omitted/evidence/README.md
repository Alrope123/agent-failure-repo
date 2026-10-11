# Historical evidence: The vLLM rendering adapter sends instruction prompts as raw completions

This is a minimal selected historical excerpt, not a full transcript. H01 and H07 are stable aliases for the two reviewed histories; L numbers refer to original archive lines.

- H01:L752 user asks one message per natural-language call, with only necessary context; L803 requests vLLM, HF and API inference backends.
- H01:L893, exact relevant implementation excerpt (other code omitted):

```python
requests = self._engine.generate(
    list(prompts),
    self._sampling_params_factory(**options),
    use_tqdm=False,
)
```

- H01:L1394, verbatim generated excerpt: “The student uses complete sentences. The student uses correct grammar and spelling.” This is returned as a student transcript message, continuing the description rather than naturalizing the student's answer.
- H01:L1408 changes the instruction-model path to conversations containing user-role messages and `self._engine.chat(...)`.
- H01:L1420, verbatim student output after the change: “11 is bigger than 9, so 11/17 is bigger.” Teacher solution leakage remains and is a separate incident.

Observed horizon: 9 substantive visible user/assistant messages from requirement to selected action, inclusive; line aliases are archive positions, not causal measures.

Evidence limit: Initial implementation explicitly disclosed lack of accelerator verification. The controlled change supports adapter mismatch but not universal causation for all generation defects; teacher leakage remained a separate issue after chat templating.

Redactions and omissions: private filesystem roots, job/session/event identifiers, hostnames, unrelated messages, tool boilerplate, duplicate patch echoes and hidden reasoning are omitted. No credential values are included. Quoted prose is verbatim unless marked transformed; transformed snippets preserve the relevant operation and ordering. Owner sharing approval has not been requested or assumed.
