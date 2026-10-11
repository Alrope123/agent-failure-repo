# Historical evidence: nested-vl-checkpoint

Local draft for owner sharing review; privacy approval pending. Source aliases and physical line anchors identify original records privately. Excerpts below are quotations with explicit replacements, not recreated model outputs. Long text and unrelated intervening work are omitted. No hidden reasoning was inspected.

## Observed behavior and limits

A failed loader was reported as requiring a replacement text-only checkpoint, but inspecting the nested final/config.json showed the model was vision-language; the agent corrected its conclusion.

Meaning: An actionable diagnosis incorrectly required a different model or loader changes instead of resolving the existing checkpoint path.

Contrary evidence and recovery: The supplied parent path was ambiguous. The loader really failed; no evidence establishes that the corrected full merge subsequently completed.

## Observed horizon

```json
{
  "source_range": "S0527:1132\u20131227",
  "visible_message_counts": {
    "assistant": 7,
    "user": 2
  },
  "logged_top_level_tool_calls": 10,
  "first_visible_timestamp": "2026-09-19T01:21:26.358Z",
  "last_visible_timestamp": "2026-09-19T05:55:23.342Z",
  "counting_rule": "Counts cover incident evidence window, not full task. Each visible response_item message counts once, and each logged top-level tool call once; nested commands and guardian copies are not independent turns.",
  "long_horizon_assessment": "Observed window length alone does not establish long-horizon dependence or causal memory loss. Context actually retained at decision is unknown."
}
```

The measured window includes diagnosis/recovery; it is not necessarily time before the erroneous decision. Earlier acceptance and actual retained context can be unknown. An ordinary local mistake remains an alternative explanation.

## Selected historical excerpts

### S0527:1165 — assistant

```text
The replacement also failed on job `<scheduler-host>`.

- The first two checkpoints loaded successfully.
- The revised third checkpoint uses `Qwen2Config`, but `merge_vl_parameters.py` expects a vision-language model configuration for `AutoModelForImageTextToText`.
- No output directory was created.
- The debug job was released and is completing deletion (`E`).

A compatible vision-language checkpoint is needed as the third input, or the merge script must be adapted for this text-only checkpoint.
```

### S0527:1174 — user

```text
How is <private-path>   not a VL model?
```

### S0527:1205 — tool result

```text
",
  "hidden_size": 2048,
  "image_token_id": 151655,
  "initializer_range": 0.02,
  "intermediate_size": 11008,
  "max_position_embeddings": 128000,
  "max_window_layers": 70,
  "model_type": "qwen2_5_vl",
  "num_attention_heads": 16,
  "num_hidden_layers": 36,
  "num_key_value_heads": 2,
  "rms_norm_eps": 1e-06,
  "rope_scaling": {
    "mrope_section": [
      16,
      24,
      24
    ],
    "rope_type": "default",
    "type": "default"
  },
  "rope_theta": 1000000.0,
  "sliding_window": 32768,
  "text_config": {
    "architectures": [
      "Qwen2_5_VLForConditionalGeneration"
    ],
    "attention_dropout": 0.0,
    "dtype": "bfloat16",
    "eos_token_id": 151645,
    "hidden_act": "silu",
    "hidden_size": 2048,
    "initializer_range": 0.02,
    "intermediate_size": 1100
```

Relevant substring of recorded tool result; surrounding output omitted.

### S0527:1227 — assistant

```text
You’re right—it is a VL model. My earlier conclusion was wrong.

The actual checkpoint is:

`<private-path>`

Its metadata confirms:

- `model_type: "qwen2_5_vl"`
- `architectures: ["Qwen2_5_VLForConditionalGeneration"]`
- vision configuration with 32 layers and image/video token IDs
- `Qwen2_5_VLProcessor`, image processor, and video processor

The mistake was passing the parent directory without `/final`. The correct third argument is:

```text
<private-path>
```

The earlier `flex_qwen2_5_vl_moe` error came from the wrong Flex-MoE checkpoint path used in that run.
```

## Reproduction target

Declared reduced-task failure rule: `d.get('model_type')=='text_only' and d.get('action')=='replace-model'`. Correct completion and target failure have separate checks; the fixtures expose explicit local observations and can be easier than the original. A checker/infrastructure crash is invalid unless it is the declared application failure. Correct/faulty scripted controls are recorded in the package's result_records. Fresh agent/model evaluation: **not run**; no authorized model runner was available.

## Redaction and evidence omissions

Private filesystem paths, scheduler/session/node/account/contact identifiers, private repository/model names and event IDs are replaced with angle-bracket aliases. Quoted excerpts can omit suffixes; tool excerpts can preserve only a relevant substring. Substitution can remove relationships between paths; the private original retains those details. The public reproduction uses independent mock names. Full transcripts, unrelated code/logs and identifying metadata are withheld. These derivatives permit assessment of the selected claims, not authentication of originals or a claim that all original evidence is public. Owner approval remains required before sharing.
