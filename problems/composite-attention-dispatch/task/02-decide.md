Configure upstream Qwen so its text attention actually uses xpu_sdpa; retain Flex sdpa. Write decision.json with attention_implementation, effective_text_backend, and flex_backend.
Do not contact a real scheduler, download a model, or submit a job.
