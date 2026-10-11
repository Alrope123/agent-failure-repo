# Original incident excerpts: learning carryover

Sanitized historical excerpts, preserving the development failure and repair ordering. No fresh model run.

N11:3502 patch introducing absent attribute
```diff
-    blocks = tuple(simulate_classroom_block(
-        topic, students, concept_id, seed=rng.getrandbits(64), block_id=f\"B{index + 1}\",
-        teacher_config=teacher_config, student_config=student_config,
-    ) for index, concept_id in enumerate(concept_ids))
-    return ClassroomScenario(seed, topic, students, blocks)
+    current = students
+    blocks = []
+    for index, concept_id in enumerate(concept_ids):
+        block = simulate_classroom_block(
+            topic, current, concept_id, seed=rng.getrandbits(64), block_id=f\"B{index + 1}\",
+            teacher_config=teacher_config, student_config=student_config,
+        )
+        blocks.append(block)
+        current = tuple(replace(student, latent_state_parameters=ParticipantKnowledgeState(tuple(
+            block.final_knowledge[state.topic.topic_id] if False else
+            block.final_knowledge[student.participant_id] if state.topic.topic_id == topic.topic_id else state
+            for state in student.latent_state_parameters.topics
+        ))) for student in current)
+    return ClassroomScenario(seed, topic, students, tuple(blocks))

```

N11:3513 actual record definition (bounded excerpt)
```python
Script completed
Wall time 1.5 seconds
Output:

class ParticipantKnowledgeState:
    """Topic-specific concept substates, with no categorical label or level."""

    topic_states: tuple[TopicKnowledgeState, ...]


```

N11:3532 failure from test process started before correction (bounded excerpt)
```text
lace(student, latent_state_parameters=ParticipantKnowledgeState(tuple(
        block.final_knowledge[state.topic.topic_id] if False else
        block.final_knowledge[student.participant_id] if state.topic.topic_id == topic.topic_id else state
>       for state in student.latent_state_parameters.topics
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ))) for student in current)
E   AttributeError: 'ParticipantKnowledgeState' object has no attribute 'topics'

src/one_to_many/classroom_simulation.py:428: AttributeError
_ test_teacher_questions_omit_definitions_and_open_invitations_keep_selection_internal _

    def test_teacher_questions_omit_definitions_and_open_invitations_kee
```

N11:3528 actual repair, performed before the pending old-version test output was collected
```diff
text(await tools.apply_patch("*** Begin Patch
*** Update File: /workspace/classroom/src/one_to_many/classroom_simulation.py
@@
-            block.final_knowledge[state.topic.topic_id] if False else
             block.final_knowledge[student.participant_id] if state.topic.topic_id == topic.topic_id else state
-            for state in student.latent_state_parameters.topics
+            for state in student.latent_state_parameters.topic_states

```

N11:3582 final repaired completion
```text
已实现：

- 新问题的 prompt 会看到同一概念下已问的问题，并要求避免重复；同题转交其他学生不受影响。
- 默认最多追加 **1 次同伴回复**，上限仍可配置。
- 学生新增 `ability_to_understand=0.5`、`ability_to_correct=1.0`，按确认的规则更新状态：

| 教学内容 | 当前状态 | 掌握概率 |
|---|---|---|
| Concept | not_mastered | understand |
| Concept | misconception | understand × correct |
| 对应 misconception | 该 misconception | correct |

更新遵守先修约束，并记录前后状态；后续回答和下一个 block 使用更新后的状态。完整测试通过。问题去重目前是 prompt 约束，不能保证模型完全遵守。
```
