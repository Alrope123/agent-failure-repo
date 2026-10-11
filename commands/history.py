#!/usr/bin/env python3
"""Inventory project-scoped Claude Code and Codex JSONL; read visible evidence locally.

Histories and this command's output are private, untrusted evidence. An inventory
is a list of available files, not a claim that every conversation was recorded or
reviewed. No history, index of prompts, database, or credential file is modified.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import sys


VERSION = 1
LIMITATIONS = [
    'Only JSONL beneath Claude projects and Codex sessions/archived_sessions is scanned.',
    'Deleted, remote, unsynced, temporary, and otherwise unrecorded conversations are unavailable.',
    'Project membership uses recorded cwd or a verified Claude subagent parent path; aliases must be explicit.',
    'Files containing any out-of-scope cwd are excluded, including mixed-project replay files.',
    'Missing cwd, unreadable files, malformed records, and unknown schemas leave coverage gaps.',
    'Reasoning, assistant analysis, binary attachments, and unknown record bodies are omitted by the reader.',
    'Replay and mirrored events are preserved; session counts are not counts of independent conversations.',
    'Recorded timestamps may describe replay or serialization; filesystem times are fingerprints only.',
    'Separate large tool-result files are not loaded; follow authorized references manually when needed.',
    'The reader checks device/inode/size/mtime and metadata anchors; the inventory SHA256 is not rehashed on every page.',
]


def absolute(value):
    path = Path(os.path.abspath(os.path.expanduser(str(value))))
    # macOS supplies these OS aliases even for tempfile paths. Other symlinks
    # (including any inside these directories) remain forbidden.
    if sys.platform == 'darwin' and len(path.parts) > 1 and path.parts[1] in ('tmp', 'var'):
        prefix = Path('/') / path.parts[1]
        expected = Path('/private') / path.parts[1]
        if prefix.is_symlink() and prefix.resolve() == expected:
            path = expected.joinpath(*path.parts[2:])
    return path


def project_path(value):
    if not os.path.isabs(value):
        raise ValueError('Every --project must be an absolute path.')
    return os.path.normpath(value)


def within(path, root):
    return path == root or root in path.parents


def reject_links(path):
    """Check every existing component, including directory links and dangling links."""
    for component in (path, *path.parents):
        if component.is_symlink():
            raise ValueError('Symbolic links are not permitted: ' + str(component))


def open_regular(path, write=False):
    """Walk directory descriptors so symlink replacement cannot redirect an open."""
    path = absolute(path)
    reject_links(path)
    if os.open not in os.supports_dir_fd:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL if write else os.O_RDONLY
        descriptor = os.open(path, flags | getattr(os, 'O_NOFOLLOW', 0), 0o600)
        try:
            reject_links(path)
            opened, named = os.fstat(descriptor), path.stat()
            if (not stat.S_ISREG(opened.st_mode)
                    or (opened.st_dev, opened.st_ino) != (named.st_dev, named.st_ino)):
                raise ValueError('File identity changed during open: ' + str(path))
        except BaseException:
            os.close(descriptor)
            raise
        return os.fdopen(descriptor, 'wb' if write else 'rb')
    directory_flags = os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0) | getattr(os, 'O_NOFOLLOW', 0)
    directory = os.open(path.anchor, directory_flags)
    try:
        for part in path.parts[1:-1]:
            child = os.open(part, directory_flags, dir_fd=directory)
            os.close(directory)
            directory = child
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL if write else os.O_RDONLY
        descriptor = os.open(path.name, flags | getattr(os, 'O_NOFOLLOW', 0),
                             0o600, dir_fd=directory)
    finally:
        os.close(directory)
    if not stat.S_ISREG(os.fstat(descriptor).st_mode):
        os.close(descriptor)
        raise ValueError('Expected a regular file: ' + str(path))
    return os.fdopen(descriptor, 'wb' if write else 'rb')


def stat_fields(value):
    return {key: getattr(value, 'st_' + key) for key in ('dev', 'ino', 'size', 'mtime_ns')}


def source_id(provider, path):
    digest = hashlib.sha256((provider + '\0' + str(path)).encode()).hexdigest()
    return provider + '-' + digest[:24]


def history_filename(path, provider):
    return path.suffix == '.jsonl' or (provider == 'claude' and '.jsonl.superseded-' in path.name)


def scalar_metadata(value, keys):
    return {key: value[key] for key in keys
            if key in value and isinstance(value[key], (str, int, float, bool))}


def relation_metadata(payload):
    """Keep identity references, not arbitrary source/fork payloads."""
    keys = ('parent_thread_id', 'parent_session_id', 'forked_from_id',
            'fork_parent_thread_id', 'forked_from', 'parent_id')
    result = scalar_metadata(payload, keys)
    source = payload.get('source')
    if isinstance(source, str):
        result['source_kind'] = source
    elif isinstance(source, dict):
        subagent = source.get('subagent')
        if isinstance(subagent, dict):
            spawned = subagent.get('thread_spawn')
            if isinstance(spawned, dict):
                result.update(scalar_metadata(spawned, ('parent_thread_id', 'depth')))
    history_base = payload.get('history_base')
    if isinstance(history_base, dict):
        result['history_base'] = scalar_metadata(history_base,
            ('id', 'session_id', 'thread_id', 'rollout_id', 'parent_thread_id'))
        result['history_base_note'] = 'Separate ancestry reference; not automatically followed.'
    elif history_base is not None:
        result['history_base_note'] = 'Unsupported ancestry-reference schema; not automatically followed.'
    return result


def metadata_for(record, provider, state, line):
    kind = record.get('type')
    payload = record.get('payload')
    metadata = record if provider == 'claude' else (
        payload if kind in ('session_meta', 'turn_context') and isinstance(payload, dict) else {})
    if 'cwd' in metadata:
        cwd = metadata['cwd']
        if isinstance(cwd, str) and os.path.isabs(cwd):
            state['cwds'].setdefault(os.path.normpath(cwd), line)
        else:
            state['invalid_cwd_lines'].append(line)
    timestamp = record.get('timestamp')
    if isinstance(timestamp, str):
        if state['first_timestamp'] is None:
            state['first_timestamp'] = timestamp
        state['last_timestamp'] = timestamp
    if provider == 'claude':
        identity = record.get('sessionId')
        if isinstance(identity, str):
            if state['session_id'] is None:
                state['session_id'] = identity
                state['thread_id'] = identity
                state['identity_line'] = line
            elif state['session_id'] != identity:
                state['metadata_notes'].append({'line': line, 'kind': 'additional_session_id',
                                                'session_id': identity})
        return
    if kind == 'session_meta' and isinstance(payload, dict):
        identity = scalar_metadata(payload, ('id', 'session_id', 'parent_thread_id'))
        relations = relation_metadata(payload)
        if state['identity_line'] is None:
            state['identity_line'] = line
            state['session_id'] = identity.get('id')
            state['thread_id'] = identity.get('session_id', identity.get('id'))
            state['parent_id'] = relations.get('parent_thread_id', relations.get('parent_id'))
            state['relations'] = relations
        else:
            state['metadata_notes'].append({
                'line': line, 'kind': 'later_session_meta_possible_replay',
                'identity': identity, 'relations': relations,
            })


def scan_source(path, provider, root, projects):
    state = dict(cwds={}, invalid_cwd_lines=[], first_timestamp=None,
                 last_timestamp=None, session_id=None, thread_id=None, parent_id=None,
                 identity_line=None, relations={}, metadata_notes=[])
    malformed = []
    nonobjects = []
    line_count = 0
    digest = hashlib.sha256()
    offsets, byte_offset = [], 0
    with open_regular(path) as stream:
        before = stat_fields(os.fstat(stream.fileno()))
        for line_count, raw in enumerate(stream, 1):
            if (line_count - 1) % 256 == 0:
                offsets.append([line_count, byte_offset])
            byte_offset += len(raw)
            digest.update(raw)
            try:
                record = json.loads(raw)
            except (ValueError, UnicodeError, RecursionError):
                malformed.append(line_count)
                continue
            if not isinstance(record, dict):
                nonobjects.append(line_count)
                continue
            metadata_for(record, provider, state, line_count)
        after = stat_fields(os.fstat(stream.fileno()))
    if before != after:
        raise ValueError('Source changed while it was being scanned: ' + str(path))
    cwds = sorted(state['cwds'])
    in_scope = [cwd for cwd in cwds if any(within(Path(cwd), Path(p)) for p in projects)]
    out_of_scope = len(cwds) - len(in_scope)
    if out_of_scope:
        status = 'unknown' if in_scope else 'excluded'
        reason = 'mixed_project_cwds' if in_scope else 'out_of_scope_cwd'
    elif state['invalid_cwd_lines']:
        status, reason = 'unknown', 'invalid_cwd_metadata'
    elif in_scope:
        status, reason = 'matched', 'recorded_cwd'
    else:
        status, reason = 'unknown', 'missing_cwd'
    source = {
        'id': source_id(provider, path), 'provider': provider, 'path': str(path),
        'root': str(root), 'status': status, 'eligible': status == 'matched',
        'session_id': state['session_id'], 'thread_id': state['thread_id'],
        'parent_id': state['parent_id'], 'identity_line': state['identity_line'],
        'relations': state['relations'], 'line_count': line_count,
        'malformed_lines': len(malformed), 'malformed_line_numbers': malformed,
        'non_object_line_numbers': nonobjects,
        'fingerprint': {**after, 'sha256': digest.hexdigest()},
        'line_offsets': offsets,
        'scope': {'reason': reason, 'matched_cwds': in_scope,
                  'cwd_evidence': [{'cwd': cwd, 'line': state['cwds'][cwd]} for cwd in in_scope],
                  'cwd_count': len(cwds), 'out_of_scope_cwd_count': out_of_scope,
                  'invalid_cwd_lines': state['invalid_cwd_lines']},
        'timestamps': {'first_recorded': state['first_timestamp'],
                       'last_recorded': state['last_timestamp']},
        'metadata_notes': state['metadata_notes'],
    }
    return source


def scan_tree(root, report, provider):
    """All JSONL, including nested subagents; never follow directory/file symlinks."""
    try:
        reject_links(root)
        if not root.exists():
            report['status'] = 'missing'
            return
        if not root.is_dir():
            report['status'] = 'unreadable'
            report['errors'].append({'path': str(root), 'error': 'not_a_directory'})
            return
        report['status'] = 'available'
        pending = [root]
        while pending:
            directory = pending.pop()
            try:
                reject_links(directory)
                with os.scandir(directory) as listing:
                    entries = sorted(list(listing), key=lambda entry: entry.name)
                for entry in entries:
                    path = Path(entry.path)
                    if entry.is_symlink():
                        report['skipped_symlinks'].append(str(path))
                    elif entry.is_dir(follow_symlinks=False):
                        pending.append(path)
                    elif entry.is_file(follow_symlinks=False) and history_filename(path, provider):
                        yield path
            except (OSError, ValueError) as exc:
                report['errors'].append({'path': str(directory), 'error': str(exc)})
                report['status'] = 'partial' if directory != root else 'unreadable'
    except (OSError, ValueError) as exc:
        report['status'] = 'unreadable'
        report['errors'].append({'path': str(root), 'error': str(exc)})
        if root.is_symlink() or any(p.is_symlink() for p in root.parents):
            report['skipped_symlinks'].append(str(root))


def parent_path(source):
    if source['provider'] != 'claude':
        return None
    relative = Path(source['path']).relative_to(source['root'])
    parts = relative.parts
    if (len(parts) >= 4 and parts[2] == 'subagents'
            and parts[-1].startswith('agent-') and parts[-1].endswith('.jsonl')):
        return str(Path(source['root']) / parts[0] / (parts[1] + '.jsonl'))
    return None


def inherit_scope(source, by_path):
    if source['status'] != 'unknown' or source['scope']['reason'] != 'missing_cwd':
        return
    expected = parent_path(source)
    parent = by_path.get(expected)
    if parent and parent['eligible'] and parent['scope']['reason'] == 'recorded_cwd':
        source['status'], source['eligible'] = 'matched', True
        source['parent_id'] = parent['session_id'] or Path(expected).stem
        source['scope'].update(reason='verified_parent_path', parent_source_id=parent['id'],
                               parent_fingerprint=parent['fingerprint'])
        source['metadata_notes'].append({'kind': 'scope_inherited_from_parent_path',
                                        'parent_source_id': parent['id']})


def inventory(projects, claude_home, codex_home, output):
    projects = sorted(set(project_path(p) for p in projects))
    output = absolute(output)
    reject_links(output)
    if output.exists():
        raise ValueError('Output already exists; choose a new index path: ' + str(output))
    if not output.parent.is_dir():
        raise ValueError('The output parent directory must already exist.')
    providers = {}
    sources = []
    for provider, home, subdirs in (
            ('claude', absolute(claude_home), ('projects',)),
            ('codex', absolute(codex_home), ('sessions', 'archived_sessions'))):
        report = {'home': str(home), 'roots': [], 'counts': dict.fromkeys(
            ('matched', 'excluded', 'unknown', 'unreadable'), 0), 'exclusion_reasons': {}}
        providers[provider] = report
        for subdir in subdirs:
            root = home / subdir
            root_report = {'path': str(root), 'status': 'missing', 'errors': [],
                           'skipped_symlinks': [], 'scanned_files': 0}
            report['roots'].append(root_report)
            for path in scan_tree(root, root_report, provider):
                root_report['scanned_files'] += 1
                try:
                    source = scan_source(path, provider, root, projects)
                except (OSError, ValueError) as exc:
                    source = {'id': source_id(provider, path), 'provider': provider,
                              'path': str(path), 'root': str(root), 'eligible': False,
                              'status': 'unreadable', 'error': str(exc)}
                sources.append(source)
        states = [r['status'] for r in report['roots']]
        report['availability'] = ('available' if all(s == 'available' for s in states)
                                  else 'partial' if any(s in ('available', 'partial') for s in states)
                                  else 'unavailable')
    by_path = {source['path']: source for source in sources}
    for source in sources:
        inherit_scope(source, by_path)
        report = providers[source['provider']]
        report['counts'][source['status']] += 1
        if source['status'] == 'excluded':
            reason = source['scope']['reason']
            report['exclusion_reasons'][reason] = report['exclusion_reasons'].get(reason, 0) + 1
    result = {'format_version': VERSION, 'created_at': datetime.now(timezone.utc).isoformat(),
              'projects': projects, 'providers': providers,
              'sources': sorted((s for s in sources if s['status'] != 'excluded'),
                                key=lambda s: (s['provider'], s['path'])),
              'limitations': LIMITATIONS}
    encoded = (json.dumps(result, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
    with open_regular(output, write=True) as stream:
        stream.write(encoded)
    return {'index': str(output), 'source_count': len(result['sources']),
            'providers': providers, 'history_reviewed': False}


class Projection:
    """Allowlisted visible content. Unknown bodies are accounted for, never dumped."""
    def __init__(self):
        self.omissions = Counter()
        self.omission_anchors = []
        self.gaps = []
        self.line = 0

    def omit(self, reason, kind=None):
        self.omissions[reason] += 1
        self.omission_anchors.append({'line': self.line, 'reason': reason,
                                      'type': kind if isinstance(kind, str) else None})
        if reason in ('unknown_record', 'unknown_block', 'invalid_content', 'unsupported_metadata'):
            self.gaps.append({'line': self.line, 'reason': reason,
                              'type': kind if isinstance(kind, str) else None})

    def data(self, value):
        """Tool arguments and structured results are task data, not protocol blocks.

        Only blocks() and provider record dispatch interpret hidden/binary types.
        Ordinary tool data can legitimately have keys such as type or source.
        """
        return value

    def blocks(self, content, provider):
        if isinstance(content, str):
            return [{'type': 'text', 'text': content}]
        if not isinstance(content, list):
            self.omit('invalid_content')
            return []
        result = []
        for block in content:
            if isinstance(block, str):
                result.append({'type': 'text', 'text': block})
                continue
            if not isinstance(block, dict):
                self.omit('unknown_block')
                continue
            kind = block.get('type')
            if kind in ('text', 'input_text', 'output_text') and isinstance(block.get('text'), str):
                result.append({'type': kind, 'text': block['text']})
            elif kind == 'tool_use' and provider == 'claude':
                result.append({'type': kind, **scalar_metadata(block, ('id', 'name')),
                               'input': self.data(block.get('input'))})
            elif kind == 'tool_result' and provider == 'claude':
                result.append({'type': kind,
                               **scalar_metadata(block, ('tool_use_id', 'is_error')),
                               'content': self.blocks(block.get('content', ''), provider)})
            elif kind in ('thinking', 'redacted_thinking', 'reasoning', 'encrypted_reasoning'):
                self.omit('reasoning')
            elif kind in ('image', 'image_url', 'input_image', 'output_image', 'document',
                          'audio', 'input_audio', 'file'):
                self.omit('binary_attachment')
            else:
                self.omit('unknown_block', kind)
        return result

    def metadata(self, record):
        return scalar_metadata(record, ('uuid', 'parentUuid', 'timestamp', 'sessionId',
            'agentId', 'isSidechain', 'isMeta', 'isCompactSummary', 'model', 'id',
            'turn_id', 'call_id', 'tool_use_id', 'status', 'version', 'gitBranch'))

    def settings(self, payload, event):
        """Project known provenance, permissions and standing instructions explicitly."""
        event.update(scalar_metadata(payload, ('originator', 'cli_version', 'model_provider',
            'approval_policy', 'approval_mode', 'sandbox_mode', 'model', 'effort',
            'reasoning_effort', 'summary')))
        for key in ('base_instructions', 'developer_instructions', 'user_instructions', 'instructions'):
            value = payload.get(key)
            if isinstance(value, str):
                event[key] = value
            elif isinstance(value, dict) and isinstance(value.get('text'), str):
                event[key] = {'text': value['text']}
                if set(value) - {'text'}:
                    self.omit('unsupported_metadata', key)
            elif value is not None:
                self.omit('unsupported_metadata', key)
        allowed = {
            'sandbox_policy': ('type', 'writable_roots', 'network_access',
                               'exclude_tmpdir_env_var', 'exclude_slash_tmp'),
            'collaboration_mode': ('mode', 'settings'),
            'truncation_policy': ('mode', 'limit'),
            'git': ('branch', 'commit_hash', 'repository_url'),
        }
        for key, fields in allowed.items():
            value = payload.get(key)
            if isinstance(value, dict):
                event[key] = {field: self.data(value[field]) for field in fields if field in value}
                if set(value) - set(fields):
                    self.omit('unsupported_metadata', key)
            elif isinstance(value, str):
                event[key] = value
            elif value is not None:
                self.omit('unsupported_metadata', key)
        for key in ('dynamic_tools', 'tool_settings'):
            value = payload.get(key)
            if value is not None:
                self.omit('unsupported_metadata', key)

    def claude(self, record):
        kind = record.get('type')
        base = {'line': self.line, **self.metadata(record)}
        if kind in ('user', 'assistant'):
            message = record.get('message')
            if not isinstance(message, dict):
                self.omit('invalid_content', kind)
                return None
            if kind == 'assistant' and (message.get('channel') == 'analysis'
                                         or record.get('channel') == 'analysis'):
                self.omit('assistant_analysis')
                return None
            content = self.blocks(message.get('content'), 'claude')
            event = {**base, 'type': 'message', 'role': kind, 'content': content,
                     **self.metadata(message)}
            if isinstance(message.get('usage'), dict):
                event['usage'] = self.data(message['usage'])
            return event
        if kind == 'system' and record.get('subtype') in ('compact_boundary', 'microcompact_boundary'):
            event = {**base, 'type': 'compaction_boundary', 'subtype': record['subtype']}
            if isinstance(record.get('content'), str):
                event['content'] = record['content']
            metadata = record.get('compactMetadata')
            if isinstance(metadata, dict):
                event['compact_metadata'] = scalar_metadata(metadata, ('trigger', 'preTokens', 'postTokens'))
            return event
        if kind in ('attachment', 'file-history-snapshot', 'file-history-delta', 'progress',
                    'queue-operation', 'last-prompt', 'ai-title', 'mode', 'permission-mode'):
            self.omit('non_conversation_metadata', kind)
        else:
            self.omit('unknown_record', kind)
        return None

    def codex(self, record):
        kind = record.get('type')
        payload = record.get('payload')
        base = {'line': self.line, **self.metadata(record)}
        if not isinstance(payload, dict):
            self.omit('unknown_record', kind)
            return None
        subtype = payload.get('type')
        if kind == 'response_item':
            if subtype in ('reasoning', 'encrypted_reasoning'):
                self.omit('reasoning')
                return None
            if payload.get('role') == 'assistant' and (payload.get('channel') == 'analysis'
                                                       or payload.get('phase') == 'analysis'):
                self.omit('assistant_analysis')
                return None
            base.update(self.metadata(payload))
            if subtype == 'message':
                role = payload.get('role')
                if role not in ('user', 'assistant', 'system', 'developer', 'tool'):
                    self.omit('unknown_record', subtype)
                    return None
                return {**base, 'type': 'message', 'role': role,
                        'channel': payload.get('channel') if isinstance(payload.get('channel'), str) else None,
                        'content': self.blocks(payload.get('content'), 'codex'),
                        'mirror_note': 'event_msg may repeat this message; retained without deduplication'}
            if subtype in ('function_call', 'custom_tool_call', 'local_shell_call', 'web_search_call',
                           'function_call_output', 'custom_tool_call_output', 'local_shell_call_output'):
                event = {**base, 'type': subtype,
                         **scalar_metadata(payload, ('name', 'call_id', 'id', 'status', 'is_error'))}
                for key in ('arguments', 'input', 'output', 'action'):
                    if key in payload:
                        if key == 'output' and isinstance(payload[key], list):
                            event[key] = self.blocks(payload[key], 'codex')
                        else:
                            event[key] = self.data(payload[key])
                return event
        elif kind == 'event_msg':
            if (subtype in ('agent_reasoning', 'reasoning')
                    or payload.get('channel') == 'analysis' or payload.get('phase') == 'analysis'):
                self.omit('reasoning')
                return None
            if subtype in ('user_message', 'agent_message'):
                text = payload.get('message')
                if not isinstance(text, str):
                    self.omit('invalid_content', subtype)
                    return None
                for key in ('images', 'local_images', 'attachments'):
                    if payload.get(key):
                        self.omissions['binary_attachment'] += len(payload[key]) if isinstance(payload[key], list) else 1
                return {**base, 'type': subtype, 'message': text,
                        **self.metadata(payload),
                        'mirror_note': 'response_item may repeat this message; retained without deduplication'}
            if subtype in ('exec_command_begin', 'exec_command_end', 'patch_apply_begin', 'patch_apply_end',
                           'mcp_tool_call_begin', 'mcp_tool_call_end', 'web_search_begin', 'web_search_end'):
                event = {**base, 'type': subtype, **self.metadata(payload)}
                for key in ('command', 'cwd', 'arguments', 'invocation', 'stdout', 'stderr',
                            'aggregated_output', 'formatted_output', 'output', 'result', 'error',
                            'exit_code', 'success', 'changes', 'action', 'query'):
                    if key in payload:
                        event[key] = self.data(payload[key])
                return event
            if subtype in ('task_started', 'task_complete', 'task_completed', 'task_aborted',
                           'turn_started', 'turn_complete', 'turn_completed', 'turn_aborted',
                           'context_compacted', 'token_count'):
                event = {**base, 'type': subtype, **self.metadata(payload)}
                for key in ('info', 'rate_limits', 'usage'):
                    if isinstance(payload.get(key), dict):
                        event[key] = self.data(payload[key])
                event.update(scalar_metadata(payload, ('model_context_window', 'last_agent_message', 'reason')))
                return event
        elif kind == 'session_meta':
            event = {**base, 'type': kind,
                    **scalar_metadata(payload, ('id', 'session_id', 'parent_thread_id', 'cwd', 'timestamp')),
                    'relations': relation_metadata(payload),
                    'identity_note': 'First session_meta defines file identity; later metadata may be ancestor replay'}
            self.settings(payload, event)
            return event
        elif kind == 'turn_context':
            event = {**base, 'type': kind, **scalar_metadata(payload,
                ('turn_id', 'cwd', 'model', 'approval_policy', 'effort', 'summary', 'collaboration_mode'))}
            self.settings(payload, event)
            return event
        elif kind == 'compacted':
            event = {**base, 'type': kind}
            for key in ('message', 'summary'):
                if isinstance(payload.get(key), str):
                    event[key] = payload[key]
            if 'replacement_history' in payload:
                self.omit('replacement_history')
            return event
        self.omit('unknown_record', subtype if kind in ('event_msg', 'response_item') else kind)
        return None


def validate_source(source, index):
    provider = source.get('provider')
    if provider not in ('claude', 'codex'):
        raise ValueError('Unknown source provider.')
    home = Path(index['providers'][provider]['home'])
    if not home.is_absolute():
        raise ValueError('Provider home must be absolute.')
    allowed = [home / sub for sub in (('projects',) if provider == 'claude'
                                     else ('sessions', 'archived_sessions'))]
    root = Path(source['root'])
    registered = [Path(r['path']) for r in index['providers'][provider]['roots']]
    path = Path(source['path'])
    if (root not in allowed or root not in registered or not path.is_absolute()
            or '..' in path.parts or not within(path, root) or not history_filename(path, provider)
            or source['id'] != source_id(provider, path)):
        raise ValueError('Source is outside its registered history root or has an invalid identity.')
    reject_links(path)
    return path, root, provider


def read_window(stream, source, start, maximum):
    """Seek to an inventory checkpoint, then retain original physical line anchors."""
    checkpoint = (1, 0)
    for line, offset in source['line_offsets']:
        if line > start:
            break
        if line < 1 or offset < 0 or offset > source['fingerprint']['size']:
            raise ValueError('Invalid line checkpoint in history index.')
        checkpoint = line, offset
    stream.seek(checkpoint[1])
    records = []
    for line in range(checkpoint[0], start + maximum):
        raw = stream.readline()
        if not raw:
            break
        if line < start:
            continue
        try:
            record = json.loads(raw)
        except (ValueError, UnicodeError, RecursionError):
            records.append((line, None, 'invalid_json'))
            continue
        if not isinstance(record, dict):
            records.append((line, None, 'non_object_record'))
        else:
            records.append((line, record, None))
    return records


def read_page(source, index, start, maximum):
    path, _, provider = validate_source(source, index)
    projects = [Path(project_path(p)) for p in index['projects']]
    scope = source['scope']
    if (source.get('eligible') is not True or source.get('status') != 'matched'
            or scope['reason'] not in ('recorded_cwd', 'verified_parent_path')):
        raise ValueError('Source is not eligible for project-scoped reading.')
    expected_stat = {key: source['fingerprint'][key] for key in ('dev', 'ino', 'size', 'mtime_ns')}
    with open_regular(path) as stream:
        if stat_fields(os.fstat(stream.fileno())) != expected_stat:
            raise ValueError('Source changed since inventory; create a new index before reading.')

        def anchor(line):
            records = read_window(stream, source, line, 1)
            if not records or records[0][2]:
                raise ValueError('Source metadata anchor is missing or malformed.')
            return records[0][1]

        identity_line = source.get('identity_line')
        if identity_line is not None:
            record = anchor(identity_line)
            if provider == 'claude':
                if record.get('sessionId') != source['session_id']:
                    raise ValueError('Source identity no longer matches the index.')
            else:
                payload = record.get('payload')
                if (record.get('type') != 'session_meta' or not isinstance(payload, dict)
                        or payload.get('id') != source['session_id']
                        or payload.get('session_id', payload.get('id')) != source['thread_id']
                        or relation_metadata(payload) != source['relations']):
                    raise ValueError('Source identity no longer matches the index.')
        if scope['reason'] == 'recorded_cwd' and not scope.get('cwd_evidence'):
            raise ValueError('Source has no recorded project membership evidence.')
        for evidence in scope['cwd_evidence']:
            record = anchor(evidence['line'])
            payload = record if provider == 'claude' else record.get('payload', {})
            cwd = payload.get('cwd') if isinstance(payload, dict) else None
            if (not isinstance(cwd, str) or not os.path.isabs(cwd)
                    or os.path.normpath(cwd) != evidence['cwd']
                    or not any(within(Path(os.path.normpath(cwd)), p) for p in projects)):
                raise ValueError('Source project membership no longer matches the index.')
        records = read_window(stream, source, start, maximum)
        if stat_fields(os.fstat(stream.fileno())) != expected_stat:
            raise ValueError('Source changed while it was being read; create a new index.')
    return records


def read_history(index_path, identifier, start, maximum):
    if start < 1 or maximum < 1:
        raise ValueError('--start-line and --max-lines must be positive integers.')
    with open_regular(absolute(index_path)) as stream:
        index = json.load(stream)
    if (not isinstance(index, dict) or type(index.get('format_version')) is not int
            or index['format_version'] != VERSION):
        raise ValueError('Unsupported history index.')
    projects = [project_path(p) for p in index['projects']]
    if not projects:
        raise ValueError('Index has no authorized projects.')
    matches = [s for s in index['sources'] if s.get('id') == identifier]
    if len(matches) != 1:
        raise ValueError('Select one registered source ID from the inventory.')
    source = matches[0]
    if source.get('eligible') is not True or source.get('status') != 'matched':
        raise ValueError('Source is not eligible for project-scoped reading.')
    path, _, provider = validate_source(source, index)
    records = read_page(source, index, start, maximum)
    if source['scope']['reason'] == 'verified_parent_path':
        parent_id = source['scope'].get('parent_source_id')
        parents = [s for s in index['sources'] if s.get('id') == parent_id]
        if len(parents) != 1 or parents[0]['path'] != parent_path(source):
            raise ValueError('Inherited parent identity is invalid.')
        parent = parents[0]
        read_page(parent, index, 1, 1)
        if (parent['scope']['reason'] != 'recorded_cwd'
                or parent.get('fingerprint') != source['scope'].get('parent_fingerprint')):
            raise ValueError('Parent source changed since inventory; create a new index.')
    projection = Projection()
    events, errors = [], []
    for line, record, error in records:
        if error:
            errors.append({'line': line, 'error': error})
            projection.omissions[error] += 1
            continue
        projection.line = line
        event = projection.claude(record) if provider == 'claude' else projection.codex(record)
        if event is not None:
            events.append(event)
    end = min(source['line_count'], start + maximum - 1)
    eof = end >= source['line_count']
    return {'source_id': identifier, 'provider': provider, 'path': str(path),
            'start_line': start, 'end_line': end, 'line_count': source['line_count'],
            'next_start_line': None if eof else end + 1, 'eof': eof,
            'events': events, 'omissions': dict(projection.omissions), 'errors': errors,
            'omission_anchors': projection.omission_anchors,
            'schema_gaps': projection.gaps,
            'metadata_notes': source['metadata_notes'],
            'fingerprint_check': 'device/inode/size/mtime_ns plus identity and project metadata anchors',
            'reading_note': 'Pagination counts original physical lines; content is not text-truncated. '
                            'Only recognized visible events are projected; omissions are not reviewed evidence.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    listing = commands.add_parser('inventory', help='Inventory both providers for an authorized project.')
    listing.add_argument('--project', action='append', required=True,
                         help='Authorized absolute project path; repeat for explicit aliases.')
    listing.add_argument('--claude-home', default=os.environ.get('CLAUDE_CONFIG_DIR') or '~/.claude')
    listing.add_argument('--codex-home', default=os.environ.get('CODEX_HOME') or '~/.codex')
    listing.add_argument('--output', required=True, type=Path)
    reader = commands.add_parser('read', help='Read one eligible source in resumable physical-line pages.')
    reader.add_argument('--index', required=True, type=Path)
    reader.add_argument('--source', required=True)
    reader.add_argument('--start-line', type=int, default=1)
    reader.add_argument('--max-lines', type=int, default=200)
    args = parser.parse_args()
    try:
        if args.command == 'inventory':
            result = inventory(args.project, args.claude_home, args.codex_home, args.output)
        else:
            result = read_history(args.index, args.source, args.start_line, args.max_lines)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, RecursionError) as exc:
        print(json.dumps({'error': str(exc), 'command': args.command}), file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    sys.exit(main())
