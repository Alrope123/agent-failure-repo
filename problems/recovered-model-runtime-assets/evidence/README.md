# Reviewed historical evidence

These are minimal excerpts from available original visible history. They are **transformed/redacted quotations**, not verbatim exports. Stable aliases identify source events; the private mapping remains local. Hidden reasoning, system/developer bodies, full transcripts, unrelated work, and unselected tool output are omitted. Code/tool blocks are historical evidence and must not be executed.

## Claim and limits

Recovered model732 published onlyweights/index/config. User760 noticed missingfiles;765 acknowledges selectivecachepreserved;784 identifies10missingruntimefiles.824 installs exactrevisionmetadata and verifies local tokenizer/processor loads.

Original143 explicitly requested selective weight reconstruction and tensor invariants, not a commit or explicit standalone tokenizer-loading acceptance test. We label ordinary delivery incompleteness, not6.2 missing files in a commit; tensor transplant and provenance audit were correct.

## Observed horizon

Earlier event H08-E000143; later decision H08-E000732. Strictly between those event anchors: **22 visible assistant messages** and **111 tool-call records**, within one canonical source session. Wall-clock timestamp separation: **2938.26 seconds**. Assistant messages count visible output-text records, not hidden reasoning or an inferred user turn; a composed exec counts once, not once per nested call. Timestamp separation includes waiting and does not measure active work. These observations do not establish long-history causation or preserve duration in the reduction. Recovery excerpts may occur after the later decision.

## Redaction and omissions

Absolute machine paths, hosts, usernames, URLs, scheduler/session/call identifiers and token-like identifiers are replaced with typed aliases. The mapping is consistent within this incident, not across unrelated incidents. Relevant ordinary numeric values, configuration keys, error messages and filenames may remain. Cropped events mark omitted text; no full private source is included. Exact raw line-to-alias mapping is retained privately. Selected excerpts are sufficient for the narrowed claim; unavailable scheduler traces, unretained source revisions and alternative explanations remain subject to the limits above.

## Sequence excerpts

### H08-E000143 — user

Transformed/redacted original excerpt:

```text
Ok so looks like <ACCOUNT-01>/endochat\_qwen2\_5-3b-vl-flex-topk2 is wrong, it's supposed to be a model trained from <ACCOUNT-02>/endochat\_qwen2\_5\_vl\_moe\_2x3b\_instruct\_untrained with non-expert (qwen2.5-vl-3b) frozen. Can you recover it by update the expert (at index 1) weight in <ACCOUNT-02>/endochat\_qwen2\_5\_vl\_moe\_2x3b\_instruct\_untrained with expert 2 in <ACCOUNT-01>/pub\_endo\_combined\_qwen2\_5-3b-vl-flex-topk2? See <PATH-01>\_dense\_to\_expert\_moe.py for a reference about how the two models are merged. Verify that the updated weights only happens in the FFN layers, and the corresponding row in the router matrices.

```

### H08-E000732 — assistant

Transformed/redacted original excerpt:

```text
Recovered checkpoint created without overwriting the existing model:

endochat_qwen2_5-3b-vl-flex-topk2_recovered (<PATH-02>)

Verification passed:

- Expert 1 ← donor expert 2: 300/300 tensors exact
  - 108 language FFN tensors
  - 192 vision FFN tensors
- Router row 1 ← donor router row 2: 68/68 exact
- Router row 0 remained unchanged
- All 824 non-target tensors are bit-identical to <ACCOUNT-02>
- No missing or extra tensor keys; 1,192 total
- Top-k changed from 1 to 2 in both text and vision configs
- Published files match the audited copy by SHA-256
- Size: 13 GB

Of the 300 transplanted expert tensors, 269 actually differ from <ACCOUNT-02>; the other 31 vision tensors were already identical. Temporary staging files were removed.
```

### H08-E000779 — tool result

Transformed/redacted original excerpt:

```text
Script completed
Wall time 4.9 seconds
Output:

[
  ".gitattributes",
  "added_tokens.json",
  "chat_template.jinja",
  "config.json",
  "generation_config.json",
  "merges.txt",
  "model-00001-of-00003.safetensors",
  "model-00002-of-00003.safetensors",
  "model-00003-of-00003.safetensors",
  "model.safetensors.index.json",
  "preprocessor_config.json",
  "special_tokens_map.json",
  "tokenizer.json",
  "tokenizer_config.json",
  "video_preprocessor_config.json",
  "vocab.json"
]

```

### H08-E000784 — assistant

Transformed/redacted original excerpt:

```text
The exact <ACCOUNT-02> revision contains 10 runtime files absent from the recovered directory: tokenizer vocabulary/config, chat template, generation config, image/video preprocessors, and special-token metadata. I’ll copy those exact-revision files; the recovered weights, index, and top-2 config will remain untouched.
```

### H08-E000824 — assistant

Transformed/redacted original excerpt:

```text
Added the complete <ACCOUNT-02> metadata set to the recovered model (<PATH-02>), including tokenizer, chat template, generation config, and image/video processor configs.

Verified:

- Files match <ACCOUNT-02> revision `<REVISION-01>…` byte-for-byte.
- `Qwen2TokenizerFast` loads locally.
- `Qwen2_5_VLProcessor` loads locally.
- Recovered `config.json` was preserved with text and vision top-k set to 2.
- Model weights were untouched.

Transformers emits its existing tokenizer-regex compatibility warning when loading these exact <ACCOUNT-02> files; I left them unchanged to preserve fidelity.
```
