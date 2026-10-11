# Historical evidence: endpoint-logit-control

Local draft for owner sharing review; privacy approval pending. Source aliases and physical line anchors identify original records privately. Excerpts below are quotations with explicit replacements, not recreated model outputs. Long text and unrelated intervening work are omitted. No hidden reasoning was inspected.

## Observed behavior and limits

To distinguish output softmax geometry from bending in the weight-to-logit path, the agent first proposed interpolating endpoint logits. It subsequently corrected this to extending the initial logit slope, because the endpoint line generally has a different initial Fisher.

Meaning: The first proposed control would not hold the quantity under investigation fixed. It was corrected before the requested control experiment ran.

Contrary evidence and recovery: This was a research-design proposal, not an executed invalid experiment. Other hypothesis language remained explicitly tentative; do not infer a fabricated result.

## Observed horizon

```json
{
  "source_range": "S0813:9089\u20139477",
  "visible_message_counts": {
    "user": 4,
    "assistant": 7
  },
  "logged_top_level_tool_calls": 30,
  "first_visible_timestamp": "2026-10-08T22:20:52.838Z",
  "last_visible_timestamp": "2026-10-08T23:18:04.178Z",
  "counting_rule": "Counts cover incident evidence window, not full task. Each visible response_item message counts once, and each logged top-level tool call once; nested commands and guardian copies are not independent turns.",
  "long_horizon_assessment": "Observed window length alone does not establish long-horizon dependence or causal memory loss. Context actually retained at decision is unknown."
}
```

The measured window includes diagnosis/recovery; it is not necessarily time before the erroneous decision. Earlier acceptance and actual retained context can be unknown. An ordinary local mistake remains an alternative explanation.

## Selected historical excerpts

### S0813:9089 — user

```text
Ok I am glad we've finally reached this conclusion. Now any just high-level ideas (needs to be based) or hypotheses about why this is the case? Also given this, we don't have a better analysis tool for our purpose? Also it seems like we are treating KL divergence as the ground truth here, is it much more explansive than fisher so people don't use it directly for analysis?
```

### S0813:9288 — assistant

```text
Yes. The strongest clue is that this is a **vision-path pattern**, not an attention-only pattern: from 25% to the full averaging move, vision-attention KL grows only 3–5× and vision-FFN KL 4–9×, while decoder-attention KL grows about 16–18×—close to quadratic growth. Our component curves (<private-path>)

There are two grounded explanations. For logits \(z_\alpha\) and \(K(\alpha)=\mathrm{KL}(p_0\|p_\alpha)\), the exact curvature is

\[
K''(\alpha)=\underbrace{\operatorname{Var}_{p_\alpha}(z'_\alpha)}_{\text{current output sensitivity}}
+\underbrace{(p_\alpha-p_0)^\top z''_\alpha}_{\text{bend in the logit path}}.
\]

At \(\alpha=0\), the second term vanishes and the first is our directional Fisher. Farther along:

- **Output probabilities may become less responsive.** The softmax changes how it weights the same logit movement as probabilities shift. This alone can turn initially quadratic KL growth into slower growth.
- **The visual signal may bend or be attenuated before reaching the output.** Both vision attention and FFN feed through Qwen2.5-VL’s visual patch merger before the decoder. Its normalization and compression make this a plausible shared point of attenuation; decoder attention does not traverse that route. This is an inference from the architecture and our shared vision-component pattern, not an identified cause. [Qwen2.5-VL report](https://arxiv.org/pdf/2502.13923), [RMSNorm paper](https://arxiv.org/abs/1910.07467)

A clean way to separate the explanations is to compare the real KL curve with one made by **linearly interpolating the endpoint logits**, \(z_0+\
```

Remaining text omitted for brevity; no claim it was absent.

### S0813:9295 — user

```text
1. "Output probabilities may become less responsive": this is not specific to vison attention, is it?
2. What does "a finite-move, per-component KL" exactly measure? Do people use KL as an similar analysis tool like we do? My thinking is just that, say in our paper we report "we conduct an analysis on the importance of each components using some tool, then we decide which components are worth moe and which components that are not based the insights we get from the analysis," we want want to make sure that this analysis in inspiring and interesting in the sense that it can let the reader learn something they didn't expect.
```

### S0813:9477 — assistant

```text
The control holds **the starting point and initial direction fixed**, then asks what happens if the model’s logits keep moving in that direction. :codex-annotation{index="1"}

Let \(z(\alpha)\) be the model’s output logits as we average a component, and let \(v=z'(0)\) be their initial rate of change. We compare two curves:

- **Actual:** \(p_{\mathrm{actual}}(\alpha)=\operatorname{softmax}(z(\alpha))\).
- **Imaginary straight path:** \(p_{\mathrm{straight}}(\alpha)=\operatorname{softmax}(z(0)+\alpha v)\).

Both begin with the **same logits and the same initial slope**, so they have the same starting Fisher prediction. Both also use softmax. The imaginary path removes just one possibility: its logits cannot slow down or turn as the weights move.

That makes the comparison informative:

- If the imaginary KL also flattens about as much as actual KL, **softmax acting on the initial vision logit movement is enough to account for the curve**. It would not prove the network stays linear; it would mean its bending is unnecessary to explain this measurement.
- If imaginary KL remains much larger than actual KL, **softmax alone cannot account for the gap**. The real model’s output-relevant logit movement must slow or change direction somewhere along the weight path. This test would establish that change, then we could examine where it happens—vision tower, merger, or decoder.

A simple two-token example shows the distinction. Suppose the logit gap initially changes at rate \(4\). A straight path keeps changing at that rate; its KL becomes less than Fisher’s quadratic extrapolation 
```

Remaining text omitted for brevity; no claim it was absent.

## Reproduction target

Declared reduced-task failure rule: `d.get('direction')=='endpoint_difference' and d.get('preserves_initial_fisher') is True`. Correct completion and target failure have separate checks; the fixtures expose explicit local observations and can be easier than the original. A checker/infrastructure crash is invalid unless it is the declared application failure. Correct/faulty scripted controls are recorded in the package's result_records. Fresh agent/model evaluation: **not run**; no authorized model runner was available.

## Redaction and evidence omissions

Private filesystem paths, scheduler/session/node/account/contact identifiers, private repository/model names and event IDs are replaced with angle-bracket aliases. Quoted excerpts can omit suffixes; tool excerpts can preserve only a relevant substring. Substitution can remove relationships between paths; the private original retains those details. The public reproduction uses independent mock names. Full transcripts, unrelated code/logs and identifying metadata are withheld. These derivatives permit assessment of the selected claims, not authentication of originals or a claim that all original evidence is public. Owner approval remains required before sharing.
