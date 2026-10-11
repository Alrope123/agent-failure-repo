# Historical evidence: directional-checkpoint-key-mismatch

Local draft for owner sharing review; privacy approval pending. Source aliases and physical line anchors identify original records privately. Excerpts below are quotations with explicit replacements, not recreated model outputs. Long text and unrelated intervening work are omitted. No hidden reasoning was inspected.

## Observed behavior and limits

The new directional Fisher script used loaded-model names directly in the donor safetensors index. The smoke job failed after1m37s; its dependent full job never ran. A reversible mapping fixed all824 keys without shape mismatches.

Meaning: The smoke gate caught a real implementation error before the full10k calculation.

Contrary evidence and recovery: This is an ordinary local implementation mistake; no long-history cause established. The main KL interpolation loader normalized both checkpoints already and was unaffected.

## Observed horizon

```json
{
  "source_range": "S0813:3752\u20134722",
  "visible_message_counts": {
    "user": 4,
    "assistant": 18
  },
  "logged_top_level_tool_calls": 106,
  "first_visible_timestamp": "2026-10-08T04:07:32.477Z",
  "last_visible_timestamp": "2026-10-08T05:34:36.040Z",
  "counting_rule": "Counts cover incident evidence window, not full task. Each visible response_item message counts once, and each logged top-level tool call once; nested commands and guardian copies are not independent turns.",
  "long_horizon_assessment": "Observed window length alone does not establish long-horizon dependence or causal memory loss. Context actually retained at decision is unknown."
}
```

The measured window includes diagnosis/recovery; it is not necessarily time before the erroneous decision. Earlier acceptance and actual retained context can be unknown. An ordinary local mistake remains an alternative explanation.

## Selected historical excerpts

### S0813:3752 — user

```text
Ok, but even we set alpha to be 1, 2 with attention still looks more reasonable than 600+ with FFN. So I agree with you intial point vision attention's Fisher prediction is roughly the right order of magnitude.&#x20;



Ok I want you to do this:

1. I want to calculate the component-wise Fisher score over the same 10k examples as before. Components should be broken down as before.
2. I also want to do the experiment you proposed.

Do the implementation under <private-path>, and propose what jobs needs to be submit.

```

### S0813:4163 — tool result

```text
Script completed
Wall time 1.8 seconds
Output:

keys 824
model.visual.patch_embed.proj.weight False
model.language_model.embed_tokens.weight False
lm_head.weight False
model.lm_head.weight False
examples ['model.embed_tokens.weight', 'model.layers.0.input_layernorm.weight', 'model.layers.0.mlp.down_proj.weight', 'model.layers.0.mlp.gate_proj.weight', 'model.layers.0.mlp.up_proj.weight', 'model.layers.0.post_attention_layernorm.weight', 'model.layers.0.self_attn.k_proj.bias', 'model.layers.0.self_attn.k_proj.weight']
```

Relevant substring of recorded tool result; surrounding output omitted.

### S0813:4247 — assistant

```text
The nine-group Fisher output and the four-component interpolation path are both implemented. I’ve also added a join script that puts the same-run diagonal score, full directional score, and KL at each \(\alpha\) in one table. I’m checking the code and run instructions now; no jobs have been submitted.
```

### S0813:4405 — user

```text
Ok proceed with the jobs, use capacity queue. And remember only 5 jobs can be queued at once. One job is queued currently, so I guess we won't exceed that.
```

### S0813:4722 — assistant

```text
The two missing jobs were the **Fisher smoke job** and its dependent full run. The smoke job (`<job-id>`) failed after 1 minute 37 seconds because the script looked up loaded-model parameter names directly in a donor checkpoint that uses different prefixes. PBS then ended the dependent full job (`<job-id>`) without running it. The smoke log (<private-path>) has the traceback.

I fixed the lookup, verified all **824 parameter names** map correctly for Endo, ReX, and PathGen, and passed five focused tests. A new Fisher smoke job (`<job-id>`) is queued, with a replacement full run (`<job-id>`) held until it succeeds.

The KL smoke job (`<job-id>`) is running; its full run (`<job-id>`) remains held. Including your unrelated job, there are **five active PBS entries**. No new analysis results are ready yet.
```

## Reproduction target

Declared reduced-task failure rule: `any(k==v for k,v in d.get('lookup',{}).items())`. Correct completion and target failure have separate checks; the fixtures expose explicit local observations and can be easier than the original. A checker/infrastructure crash is invalid unless it is the declared application failure. Correct/faulty scripted controls are recorded in the package's result_records. Fresh agent/model evaluation: **not run**; no authorized model runner was available.

## Redaction and evidence omissions

Private filesystem paths, scheduler/session/node/account/contact identifiers, private repository/model names and event IDs are replaced with angle-bracket aliases. Quoted excerpts can omit suffixes; tool excerpts can preserve only a relevant substring. Substitution can remove relationships between paths; the private original retains those details. The public reproduction uses independent mock names. Full transcripts, unrelated code/logs and identifying metadata are withheld. These derivatives permit assessment of the selected claims, not authentication of originals or a claim that all original evidence is public. Owner approval remains required before sharing.
