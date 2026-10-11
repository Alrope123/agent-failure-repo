"""Exercise the history CLI using synthetic, disposable provider homes only.

The subprocess receives a fresh HOME and both provider roots on every call.
No test opens an actual transcript, authentication file, or user configuration.
"""

import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


REPOSITORY = Path(__file__).resolve().parents[1]


class HistoryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name).resolve()
        self.home = self.base / "home"
        self.home.mkdir()
        self.project = self.base / "chosen-project"
        self.project.mkdir()
        self.other_project = self.base / "chosen-project-sibling"
        self.other_project.mkdir()
        self.claude_home = self.base / "claude-fixture"
        self.codex_home = self.base / "codex-fixture"
        self.claude_home.mkdir()
        self.codex_home.mkdir()
        self.command = self.base / "commands/history.py"
        self.command.parent.mkdir()
        shutil.copyfile(REPOSITORY / "commands/history.py", self.command)
        self.environment = {
            "HOME": str(self.home),
            "PATH": os.defpath,
            "CLAUDE_CONFIG_DIR": str(self.claude_home),
            "CODEX_HOME": str(self.codex_home),
            "PYTHONIOENCODING": "utf-8",
        }
        self.index_number = 0

    def call(self, *args, environment=None):
        return subprocess.run(
            [sys.executable, "-B", str(self.command), *map(str, args)],
            cwd=self.base,
            env=self.environment if environment is None else environment,
            capture_output=True,
            text=True,
            check=False,
        )

    @staticmethod
    def write_lines(path, records):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "".join((record if isinstance(record, str) else json.dumps(record, ensure_ascii=False)) + "\n"
                    for record in records),
            encoding="utf-8",
        )
        return path

    def claude(self, session="claude-main", records=None, home=None):
        if records is None:
            records = [self.claude_message(session=session)]
        return self.write_lines(
            (home or self.claude_home) / "projects/encoded-project" / (session + ".jsonl"),
            records,
        )

    def claude_message(self, text="Synthetic user request.", session="claude-main",
                       cwd=True, role="user", **extra):
        record = {
            "type": role,
            "sessionId": session,
            "timestamp": "2026-10-01T12:00:00Z",
            "message": {"role": role, "content": text},
        }
        if cwd is not False:
            record["cwd"] = str(self.project if cwd is True else cwd)
        record.update(extra)
        return record

    def codex(self, session="codex-main", records=None, archived=False, home=None):
        if records is None:
            records = [self.codex_meta(session), self.codex_message("Synthetic final answer.")]
        root = "archived_sessions" if archived else "sessions/2026/10/01"
        return self.write_lines(
            (home or self.codex_home) / root / ("rollout-" + session + ".jsonl"), records,
        )

    def codex_meta(self, session="codex-main", cwd=None, **extra):
        return {
            "timestamp": "2026-10-01T12:00:00Z",
            "type": "session_meta",
            "payload": {"id": session, "cwd": str(cwd or self.project), **extra},
        }

    @staticmethod
    def codex_message(text, role="assistant", channel="final"):
        return {
            "timestamp": "2026-10-01T12:00:01Z",
            "type": "response_item",
            "payload": {"type": "message", "role": role, "channel": channel,
                        "content": [{"type": "output_text", "text": text}]},
        }

    def inventory(self, *args, projects=None, explicit_roots=True, environment=None):
        self.index_number += 1
        index = self.base / f"index-{self.index_number}.json"
        options = []
        for project in projects or [self.project]:
            options += ["--project", str(project)]
        if explicit_roots:
            options += ["--claude-home", str(self.claude_home),
                        "--codex-home", str(self.codex_home)]
        result = self.call("inventory", *options, "--output", index, *args,
                           environment=environment)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return index, json.loads(index.read_text(encoding="utf-8"))

    def read(self, index, source, start=1, maximum=100):
        source_id = source["id"] if isinstance(source, dict) else source
        result = self.call("read", "--index", index, "--source", source_id,
                           "--start-line", start, "--max-lines", maximum)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def source_for(self, inventory, path):
        matches = [source for source in inventory["sources"] if source["path"] == str(path)]
        self.assertEqual(len(matches), 1, inventory)
        return matches[0]

    @staticmethod
    def snapshot(root):
        return {path.relative_to(root).as_posix(): (path.read_bytes(), path.stat().st_mtime_ns)
                for path in root.rglob("*") if path.is_file() and not path.is_symlink()}

    def test_inventory_checks_both_providers_and_codex_archive(self):
        claude = self.claude(records=[self.claude_message("CLAUDE_BODY_SENTINEL")])
        codex = self.codex()
        archived = self.codex("codex-archive", archived=True)
        before = (self.snapshot(self.claude_home), self.snapshot(self.codex_home))
        index, inventory = self.inventory()
        self.assertEqual(inventory["format_version"], 1)
        self.assertIn(str(self.project), inventory["projects"])
        self.assertEqual(set(inventory["providers"]), {"claude", "codex"})
        self.assertEqual(index.stat().st_mode & 0o777, 0o600)
        self.assertNotIn("CLAUDE_BODY_SENTINEL", index.read_text())
        required = {"id", "provider", "path", "root", "status", "eligible", "session_id",
                    "thread_id", "parent_id", "line_count", "malformed_lines", "fingerprint",
                    "scope", "timestamps", "metadata_notes"}
        for path, provider, session in ((claude, "claude", "claude-main"),
                                        (codex, "codex", "codex-main"),
                                        (archived, "codex", "codex-archive")):
            with self.subTest(path=path):
                source = self.source_for(inventory, path)
                self.assertTrue(required.issubset(source))
                self.assertEqual(source["provider"], provider)
                self.assertEqual(source["session_id"], session)
                self.assertEqual(source["status"], "matched")
                self.assertTrue(source["eligible"])
                self.assertTrue(source["fingerprint"])
        self.assertEqual(inventory["providers"]["claude"]["counts"]["matched"], 1)
        self.assertEqual(inventory["providers"]["codex"]["counts"]["matched"], 2)
        for provider in inventory["providers"].values():
            self.assertTrue({"home", "roots", "counts"}.issubset(provider))
            self.assertTrue({"matched", "excluded", "unknown", "unreadable"}
                            .issubset(provider["counts"]))
        self.assertEqual(before, (self.snapshot(self.claude_home), self.snapshot(self.codex_home)))

    def test_project_descendants_and_explicit_aliases_match_but_siblings_do_not(self):
        alias = self.base / "project-on-old-machine"
        alias.mkdir()
        descendant = self.claude("descendant", [
            self.claude_message(session="descendant", cwd=self.project / "package")])
        alias_source = self.codex("alias", [self.codex_meta("alias", cwd=alias)])
        excluded = self.claude("excluded", [
            self.claude_message("EXCLUDED_BODY_SENTINEL", session="excluded", cwd=self.other_project)])
        _, inventory = self.inventory(projects=[self.project, alias])
        self.assertTrue(self.source_for(inventory, descendant)["eligible"])
        self.assertTrue(self.source_for(inventory, alias_source)["eligible"])
        self.assertNotIn(str(excluded), json.dumps(inventory))
        self.assertNotIn("EXCLUDED_BODY_SENTINEL", json.dumps(inventory))
        self.assertEqual(inventory["providers"]["claude"]["counts"]["excluded"], 1)

    def test_mixed_scope_source_is_never_eligible_for_reading(self):
        mixed = self.claude("mixed", [
            self.claude_message("AUTHORIZED_BODY", session="mixed"),
            self.claude_message("OUTSIDE_SCOPE_BODY", session="mixed", cwd=self.other_project),
        ])
        index, inventory = self.inventory()
        source = self.source_for(inventory, mixed)
        self.assertEqual(source["status"], "unknown")
        self.assertEqual(source["scope"]["reason"], "mixed_project_cwds")
        self.assertFalse(source["eligible"])
        result = self.call("read", "--index", index, "--source", source["id"],
                           "--start-line", 1, "--max-lines", 10)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("OUTSIDE_SCOPE_BODY", result.stdout + result.stderr)
        self.assertNotIn("OUTSIDE_SCOPE_BODY", json.dumps(inventory))

    def test_missing_scope_is_recorded_unknown_and_cannot_be_read(self):
        unknown = self.claude("unknown", [
            self.claude_message("UNSCOPED_BODY_SENTINEL", session="unknown", cwd=False)])
        index, inventory = self.inventory()
        source = self.source_for(inventory, unknown)
        self.assertEqual(source["status"], "unknown")
        self.assertFalse(source["eligible"])
        self.assertEqual(inventory["providers"]["claude"]["counts"]["unknown"], 1)
        result = self.call("read", "--index", index, "--source", source["id"],
                           "--start-line", 1, "--max-lines", 10)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("UNSCOPED_BODY_SENTINEL", result.stdout + result.stderr)

    def test_claude_child_inherits_scope_only_from_a_verified_parent(self):
        parent = self.claude("parent-session", [self.claude_message(session="parent-session")])
        child = self.write_lines(parent.with_suffix("") / "subagents/agent-child-a.jsonl", [
            self.claude_message("CHILD_VISIBLE_TEXT", session="parent-session", cwd=False,
                                agentId="child-a", isSidechain=True),
        ])
        orphan = self.write_lines(parent.parent / "missing-parent/subagents/agent-orphan.jsonl", [
            self.claude_message("ORPHAN_TEXT", session="missing-parent", cwd=False,
                                agentId="orphan", isSidechain=True),
        ])
        index, inventory = self.inventory()
        child_source = self.source_for(inventory, child)
        self.assertEqual(child_source["status"], "matched")
        self.assertTrue(child_source["eligible"])
        self.assertEqual(child_source["parent_id"], "parent-session")
        self.assertIn("CHILD_VISIBLE_TEXT", json.dumps(self.read(index, child_source)))
        orphan_source = self.source_for(inventory, orphan)
        self.assertEqual(orphan_source["status"], "unknown")
        self.assertFalse(orphan_source["eligible"])

    def test_claude_projection_keeps_messages_and_tools_but_omits_thinking(self):
        path = self.claude(records=[
            self.claude_message("VISIBLE_USER_TEXT"),
            self.claude_message(role="assistant", text=[
                {"type": "thinking", "thinking": "PRIVATE_THINKING_SENTINEL", "signature": "HIDDEN_SIGNATURE"},
                {"type": "redacted_thinking", "data": "PRIVATE_REDACTED_SENTINEL"},
                {"type": "text", "text": "VISIBLE_ASSISTANT_TEXT"},
                {"type": "tool_use", "id": "call-one", "name": "Read", "input": {"file_path": "visible.txt"}},
            ]),
            self.claude_message(text=[
                {"type": "tool_result", "tool_use_id": "call-one", "content": [
                    {"type": "text", "text": "VISIBLE_TOOL_OUTPUT"},
                ]},
            ]),
        ])
        before = self.snapshot(self.claude_home)
        index, inventory = self.inventory()
        page = self.read(index, self.source_for(inventory, path))
        serialized = json.dumps(page)
        for visible in ("VISIBLE_USER_TEXT", "VISIBLE_ASSISTANT_TEXT", "visible.txt", "VISIBLE_TOOL_OUTPUT"):
            self.assertIn(visible, serialized)
        for hidden in ("PRIVATE_THINKING_SENTINEL", "HIDDEN_SIGNATURE", "PRIVATE_REDACTED_SENTINEL"):
            self.assertNotIn(hidden, serialized)
        self.assertTrue(page["omissions"])
        self.assertEqual({anchor["line"] for anchor in page["omission_anchors"]}, {2})
        self.assertEqual(before, self.snapshot(self.claude_home))

    def test_ordinary_tool_arguments_named_file_are_not_treated_as_attachments(self):
        arguments = {"type": "file", "source": "a", "destination": "b",
                     "encrypted_content": "ordinary task data"}
        path = self.claude(records=[self.claude_message(role="assistant", text=[
            {"type": "tool_use", "id": "file-call", "name": "inspect", "input": arguments},
        ])])
        index, inventory = self.inventory()
        page = self.read(index, self.source_for(inventory, path))
        self.assertEqual(page["events"][0]["content"][0]["input"], arguments)

    def test_codex_projection_keeps_tools_and_final_messages_but_omits_analysis(self):
        path = self.codex(records=[
            self.codex_meta(),
            self.codex_message("PRIVATE_ANALYSIS_SENTINEL", channel="analysis"),
            {"type": "response_item", "payload": {"type": "reasoning", "summary": [
                {"type": "summary_text", "text": "PRIVATE_REASONING_SENTINEL"}],
                "encrypted_content": "PRIVATE_ENCRYPTED_SENTINEL"}},
            {"type": "response_item", "payload": {"type": "function_call", "name": "exec_command",
                "call_id": "call-one", "arguments": '{"cmd":"echo VISIBLE_COMMAND"}'}},
            {"type": "response_item", "payload": {"type": "function_call_output",
                "call_id": "call-one", "output": "VISIBLE_CODEX_TOOL_OUTPUT"}},
            self.codex_message("VISIBLE_CODEX_FINAL"),
        ])
        index, inventory = self.inventory()
        page = self.read(index, self.source_for(inventory, path))
        serialized = json.dumps(page)
        for visible in ("VISIBLE_COMMAND", "VISIBLE_CODEX_TOOL_OUTPUT", "VISIBLE_CODEX_FINAL"):
            self.assertIn(visible, serialized)
        for hidden in ("PRIVATE_ANALYSIS_SENTINEL", "PRIVATE_REASONING_SENTINEL", "PRIVATE_ENCRYPTED_SENTINEL"):
            self.assertNotIn(hidden, serialized)
        self.assertTrue(page["omissions"])
        self.assertEqual({anchor["line"] for anchor in page["omission_anchors"]}, {2, 3})

    def test_codex_standing_instructions_provenance_and_sandbox_are_preserved(self):
        sandbox = {"type": "workspace-write", "writable_roots": [str(self.project)],
                   "network_access": False, "exclude_slash_tmp": True}
        path = self.codex(records=[
            self.codex_meta(
                base_instructions={"text": "VISIBLE_BASE_INSTRUCTION"},
                originator="synthetic-cli", cli_version="1.2.3", model_provider="synthetic-provider",
                git={"branch": "fixture-branch", "commit_hash": "fixture-commit"},
            ),
            {"type": "turn_context", "payload": {
                "cwd": str(self.project), "turn_id": "turn-one", "model": "fixture-model",
                "approval_policy": "never", "sandbox_policy": sandbox,
                "developer_instructions": "VISIBLE_DEVELOPER_INSTRUCTION",
                "user_instructions": "VISIBLE_USER_INSTRUCTION",
            }},
        ])
        index, inventory = self.inventory()
        page = self.read(index, self.source_for(inventory, path))
        session, turn = page["events"]
        self.assertEqual(session["base_instructions"], {"text": "VISIBLE_BASE_INSTRUCTION"})
        self.assertEqual(session["originator"], "synthetic-cli")
        self.assertEqual(session["cli_version"], "1.2.3")
        self.assertEqual(session["model_provider"], "synthetic-provider")
        self.assertEqual(session["git"]["branch"], "fixture-branch")
        self.assertEqual(turn["sandbox_policy"], sandbox)
        self.assertEqual(turn["approval_policy"], "never")
        self.assertEqual(turn["developer_instructions"], "VISIBLE_DEVELOPER_INSTRUCTION")
        self.assertEqual(turn["user_instructions"], "VISIBLE_USER_INSTRUCTION")

    def test_native_codex_exec_patch_and_web_events_keep_visible_results(self):
        events = [
            {"type": "exec_command_begin", "call_id": "exec-one",
             "command": ["echo", "VISIBLE_NATIVE_COMMAND"], "cwd": str(self.project)},
            {"type": "exec_command_end", "call_id": "exec-one", "exit_code": 0,
             "stdout": "VISIBLE_NATIVE_STDOUT", "stderr": "VISIBLE_NATIVE_STDERR"},
            {"type": "patch_apply_begin", "call_id": "patch-one", "changes": {
                "example.txt": {"type": "add", "content": "VISIBLE_PATCH_CONTENT"}}},
            {"type": "patch_apply_end", "call_id": "patch-one", "success": True,
             "stdout": "VISIBLE_PATCH_RESULT"},
            {"type": "web_search_begin", "call_id": "web-one", "query": "VISIBLE_WEB_QUERY"},
            {"type": "web_search_end", "call_id": "web-one", "result": "VISIBLE_WEB_RESULT"},
        ]
        path = self.codex(records=[self.codex_meta()] + [
            {"type": "event_msg", "payload": event} for event in events
        ])
        index, inventory = self.inventory()
        page = self.read(index, self.source_for(inventory, path))
        self.assertEqual([event["type"] for event in page["events"]],
                         ["session_meta"] + [event["type"] for event in events])
        for sentinel in ("VISIBLE_NATIVE_COMMAND", "VISIBLE_NATIVE_STDOUT", "VISIBLE_NATIVE_STDERR",
                         "VISIBLE_PATCH_CONTENT", "VISIBLE_PATCH_RESULT", "VISIBLE_WEB_QUERY", "VISIBLE_WEB_RESULT"):
            self.assertIn(sentinel, json.dumps(page))

    def test_pagination_uses_original_lines_and_can_start_in_the_middle(self):
        path = self.codex(records=[
            self.codex_meta(), self.codex_message("FIRST_VISIBLE"),
            self.codex_message("OMITTED_ANALYSIS", channel="analysis"),
            self.codex_message("SECOND_VISIBLE"), self.codex_message("LAST_VISIBLE"),
        ])
        index, inventory = self.inventory()
        source = self.source_for(inventory, path)
        first = self.read(index, source, start=1, maximum=2)
        middle = self.read(index, source, start=3, maximum=2)
        last = self.read(index, source, start=5, maximum=2)
        for page, start, end, next_start, eof in (
            (first, 1, 2, 3, False), (middle, 3, 4, 5, False), (last, 5, 5, None, True),
        ):
            with self.subTest(start=start):
                self.assertEqual(page["source_id"], source["id"])
                self.assertEqual(page["start_line"], start)
                self.assertEqual(page["end_line"], end)
                self.assertEqual(page["next_start_line"], next_start)
                self.assertEqual(page["eof"], eof)
                for event in page["events"]:
                    self.assertIn("type", event)
                    self.assertGreaterEqual(event["line"], start)
                    self.assertLessEqual(event["line"], end)
        self.assertNotIn("FIRST_VISIBLE", json.dumps(middle))
        self.assertNotIn("OMITTED_ANALYSIS", json.dumps(middle))
        self.assertIn("SECOND_VISIBLE", json.dumps(middle))
        self.assertIn("LAST_VISIBLE", json.dumps(last))

    def test_multibyte_pagination_crosses_byte_checkpoints_without_losing_lines(self):
        path = self.codex(records=[self.codex_meta()] + [
            self.codex_message(f"VISIBLE_LINE_{line:04d}_é_東京") for line in range(2, 307)
        ])
        index, inventory = self.inventory()
        source = self.source_for(inventory, path)
        self.assertEqual(source["line_count"], 306)
        for start in (255, 300):
            with self.subTest(start=start):
                page = self.read(index, source, start=start, maximum=4)
                self.assertEqual([event["line"] for event in page["events"]], list(range(start, start + 4)))
                for line in range(start, start + 4):
                    self.assertIn(f"VISIBLE_LINE_{line:04d}_é_東京", json.dumps(page, ensure_ascii=False))
                self.assertNotIn(f"VISIBLE_LINE_{start - 1:04d}", json.dumps(page))
                self.assertEqual(page["next_start_line"], start + 4)
                self.assertFalse(page["eof"])

    def test_superseded_claude_transcript_remains_discoverable(self):
        original = self.claude("superseded-session", [
            self.claude_message("VISIBLE_SUPERSEDED_TEXT", session="superseded-session"),
        ])
        superseded = original.with_name(original.name + ".superseded-20261001")
        original.rename(superseded)
        index, inventory = self.inventory()
        source = self.source_for(inventory, superseded)
        self.assertTrue(source["eligible"])
        self.assertIn("VISIBLE_SUPERSEDED_TEXT", json.dumps(self.read(index, source)))

    def test_malformed_lines_and_unknown_schema_remain_explicit_coverage_gaps(self):
        path = self.codex(records=[
            self.codex_meta(), self.codex_message("VISIBLE_BEFORE_GAP"),
            '{"type": "broken", INVALID_PRIVATE_SENTINEL',
            {"type": "future_record_type", "payload": {"private": "UNKNOWN_PRIVATE_SENTINEL"}},
            self.codex_message("VISIBLE_AFTER_GAP"),
        ])
        index, inventory = self.inventory()
        source = self.source_for(inventory, path)
        self.assertEqual(source["line_count"], 5)
        self.assertTrue(source["malformed_lines"])
        page = self.read(index, source, start=3, maximum=3)
        self.assertTrue(page["errors"])
        self.assertTrue(page["schema_gaps"])
        self.assertIn(4, [gap["line"] for gap in page["schema_gaps"]])
        self.assertTrue(page["eof"])
        self.assertIn("VISIBLE_AFTER_GAP", json.dumps(page))
        self.assertNotIn("INVALID_PRIVATE_SENTINEL", json.dumps(page))
        self.assertNotIn("UNKNOWN_PRIVATE_SENTINEL", json.dumps(page))

    def test_later_codex_metadata_does_not_replace_primary_identity_or_hide_replay(self):
        path = self.codex(records=[
            self.codex_meta("primary-session"),
            self.codex_message("BEFORE_REPLAY"),
            self.codex_meta("replayed-session"),
            self.codex_message("AFTER_REPLAY"),
        ])
        index, inventory = self.inventory()
        source = self.source_for(inventory, path)
        self.assertEqual(source["session_id"], "primary-session")
        self.assertEqual(source["thread_id"], "primary-session")
        self.assertTrue(source["metadata_notes"])
        self.assertEqual(source["line_count"], 4)
        page = self.read(index, source)
        self.assertIn("BEFORE_REPLAY", json.dumps(page))
        self.assertIn("AFTER_REPLAY", json.dumps(page))
        self.assertEqual(page["end_line"], 4)

    def test_codex_session_thread_and_parent_identities_are_distinct(self):
        path = self.codex(records=[self.codex_meta(
            "rollout-identity", session_id="thread-identity", parent_thread_id="parent-identity",
        ), self.codex_message("VISIBLE_CHILD_ANSWER")])
        index, inventory = self.inventory()
        source = self.source_for(inventory, path)
        self.assertEqual(source["session_id"], "rollout-identity")
        self.assertEqual(source["thread_id"], "thread-identity")
        self.assertEqual(source["parent_id"], "parent-identity")
        self.assertIn("VISIBLE_CHILD_ANSWER", json.dumps(self.read(index, source)))

    def test_codex_mirrored_messages_and_large_tool_output_are_preserved(self):
        output = "TOOL_OUTPUT_START " + "x" * 25000 + " TOOL_OUTPUT_END"
        path = self.codex(records=[
            self.codex_meta(), self.codex_message("MIRRORED_VISIBLE_MESSAGE"),
            {"type": "event_msg", "payload": {"type": "agent_message",
                "message": "MIRRORED_VISIBLE_MESSAGE"}},
            {"type": "response_item", "payload": {"type": "function_call_output",
                "call_id": "large-tool", "output": output}},
        ])
        index, inventory = self.inventory()
        page = self.read(index, self.source_for(inventory, path))
        self.assertEqual(json.dumps(page["events"]).count("MIRRORED_VISIBLE_MESSAGE"), 2)
        self.assertIn(output, json.dumps(page))
        self.assertEqual([event["line"] for event in page["events"]], [1, 2, 3, 4])

    def test_environment_roots_and_home_defaults_are_isolated_and_honored(self):
        env_claude = self.claude("from-environment")
        env_codex = self.codex("from-environment")
        _, inventory = self.inventory(explicit_roots=False)
        self.source_for(inventory, env_claude)
        self.source_for(inventory, env_codex)
        default_claude = self.claude("from-home", home=self.home / ".claude")
        default_codex = self.codex("from-home", home=self.home / ".codex")
        environment = {key: value for key, value in self.environment.items()
                       if key not in {"CLAUDE_CONFIG_DIR", "CODEX_HOME"}}
        _, inventory = self.inventory(explicit_roots=False, environment=environment)
        self.source_for(inventory, default_claude)
        self.source_for(inventory, default_codex)
        self.assertEqual(len(inventory["sources"]), 2)

    def test_provider_root_gaps_distinguish_missing_and_unreadable(self):
        (self.claude_home / "projects").write_text("NOT_A_DIRECTORY", encoding="utf-8")
        _, inventory = self.inventory()
        self.assertEqual(inventory["sources"], [])
        claude = inventory["providers"]["claude"]
        codex = inventory["providers"]["codex"]
        self.assertEqual(claude["roots"][0]["status"], "unreadable")
        self.assertTrue(claude["roots"][0]["errors"])
        self.assertEqual([root["status"] for root in codex["roots"]], ["missing", "missing"])

    def test_history_symlinks_are_reported_but_not_followed(self):
        regular = self.claude()
        outside = self.write_lines(self.base / "outside.jsonl", [
            self.claude_message("OUTSIDE_LINK_TARGET_SENTINEL", session="outside")])
        link = regular.parent / "linked-transcript.jsonl"
        link.symlink_to(outside)
        directory_link = self.codex_home / "sessions"
        directory_link.symlink_to(outside.parent, target_is_directory=True)
        before = outside.read_bytes()
        _, inventory = self.inventory()
        self.assertEqual(len(inventory["sources"]), 1)
        self.source_for(inventory, regular)
        self.assertIn(str(link), inventory["providers"]["claude"]["roots"][0]["skipped_symlinks"])
        self.assertEqual(inventory["providers"]["codex"]["roots"][0]["status"], "unreadable")
        self.assertNotIn("OUTSIDE_LINK_TARGET_SENTINEL", json.dumps(inventory))
        self.assertEqual(before, outside.read_bytes())

    def test_source_changes_after_inventory_are_refused_without_output(self):
        path = self.claude()
        index, inventory = self.inventory()
        source = self.source_for(inventory, path)
        with path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(self.claude_message("MUTATED_BODY_SENTINEL")) + "\n")
        result = self.call("read", "--index", index, "--source", source["id"],
                           "--start-line", 1, "--max-lines", 100)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("MUTATED_BODY_SENTINEL", result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_inherited_claude_scope_is_rechecked_when_parent_changes(self):
        parent = self.claude("parent-session", [self.claude_message(session="parent-session")])
        child = self.write_lines(parent.with_suffix("") / "subagents/agent-child.jsonl", [
            self.claude_message("CHILD_BODY_MUST_NOT_BE_EMITTED", session="parent-session",
                                cwd=False, agentId="child", isSidechain=True),
        ])
        index, inventory = self.inventory()
        source = self.source_for(inventory, child)
        self.write_lines(parent, [self.claude_message(session="parent-session", cwd=self.other_project)])
        result = self.call("read", "--index", index, "--source", source["id"],
                           "--start-line", 1, "--max-lines", 10)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("CHILD_BODY_MUST_NOT_BE_EMITTED", result.stdout + result.stderr)

    def test_reader_refuses_linked_index_and_replaced_source(self):
        path = self.claude(records=[self.claude_message("SOURCE_BODY_SENTINEL")])
        index, inventory = self.inventory()
        source = self.source_for(inventory, path)
        index_link = self.base / "linked-index.json"
        index_link.symlink_to(index)
        result = self.call("read", "--index", index_link, "--source", source["id"],
                           "--start-line", 1, "--max-lines", 10)
        self.assertNotEqual(result.returncode, 0)
        moved = self.base / "moved-source.jsonl"
        path.rename(moved)
        path.symlink_to(moved)
        result = self.call("read", "--index", index, "--source", source["id"],
                           "--start-line", 1, "--max-lines", 10)
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("SOURCE_BODY_SENTINEL", result.stdout + result.stderr)

    def test_output_is_exclusive_and_symlinks_never_overwrite_an_owner_file(self):
        self.claude()
        existing = self.base / "owner-index.json"
        existing.write_text("OWNER_FILE_SENTINEL\n", encoding="utf-8")
        link = self.base / "linked-index.json"
        link.symlink_to(existing)
        dangling = self.base / "dangling-index.json"
        dangling.symlink_to(self.base / "missing-target")
        for output in (existing, link, dangling):
            with self.subTest(output=output):
                result = self.call("inventory", "--project", self.project,
                                   "--output", output)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)
                self.assertEqual(existing.read_text(), "OWNER_FILE_SENTINEL\n")
        self.assertTrue(link.is_symlink())
        self.assertTrue(dangling.is_symlink())
        self.assertFalse((self.base / "missing-target").exists())

    def test_read_rejects_unknown_source_and_invalid_pagination(self):
        path = self.claude()
        index, inventory = self.inventory()
        source = self.source_for(inventory, path)
        for source_id, start, maximum in (("unknown-source", 1, 10),
                                          (source["id"], 0, 10),
                                          (source["id"], -1, 10),
                                          (source["id"], 1, 0),
                                          (source["id"], 1, -1)):
            with self.subTest(source=source_id, start=start, maximum=maximum):
                result = self.call("read", "--index", index, "--source", source_id,
                                   "--start-line", start, "--max-lines", maximum)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
