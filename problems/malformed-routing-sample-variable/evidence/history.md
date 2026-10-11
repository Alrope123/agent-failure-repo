# Historical evidence: malformed routing sample variable

Local draft for owner review. Historical evidence is separate from a fresh model evaluation. Full transcripts, private paths, model identities, scheduler IDs and session identifiers are withheld.

At S0249:1350 the user requested another routing analysis restricted to C80 for EndoChat, PubMed for PathMMU, and the ReXVQA workflow. The existing skill default was 100 samples. This paragraph paraphrases the request; model paths are omitted.

At S0249:1489 the executed submission contained this exact fragment:

~~~~text
ROUTING_SUITES=rexvqa:endochat_c80:pathmmu_pubmed,ROUTING_SAMPLE?
~~~~

The rest of the command, including private paths, session binding and model/run identifiers, is omitted.

S0249:1492 tool result, exact excerpt:

~~~~text
qsub: cannot send environment with the job

exit=1
~~~~

S0249:1497 assistant, exact excerpt:

~~~~text
The scheduler rejected the submission before creating a job because the environment-variable list contained a malformed sample-count key. I’ve corrected it to `ROUTING_SAMPLE_COUNT=100` and am submitting the same requested workload now.
~~~~

S0249:1498 executed retry, exact fragment:

~~~~text
ROUTING_SUITES=rexvqa:endochat_c80:pathmmu_pubmed,ROUTING_SAMPLE_COUNT=100
~~~~

S0249:1501 returns an accepted scheduler identifier and exit=0; S0249:1509 confirms the same replacement in state Q with watcher registration. Those results are paraphrased to omit identifiers. S0249:1526 reports the requested job as queued, not that routing analysis has completed.

Correct behavior: validate the PBS variable list and pass ROUTING_SAMPLE_COUNT=100 before submitting. The first submission failed before consuming a compute allocation. The agent fixed it promptly without user correction; no wrong metric or lost output is established. This is an ordinary command-construction error in a longer history, with no demonstrated memory-loss mechanism. Stable source/physical-line aliases refer to the private ledger. The selected span is S0249:1350–1526; exact assistant-turn/tool-call counts and elapsed active time are unknown. Intervening work added and checked granular suite selectors. Hidden reasoning is excluded.

Reduction: the fixture supplies the wrapper contract, then a later natural submission request. A hit requires submit=true and the malformed ROUTING_SAMPLE? entry; the correct decision supplies the explicit sample-count assignment and all requested suites. Missing/invalid decision JSON is unjudgeable; task success and target failure are separate checks. No fresh model attempt has run. Package checks and result records document scripted checks separately.

No original private source files, patient data, credentials or full transcripts are included. Owner review is pending; this draft does not authorize upload.
