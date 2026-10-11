# Why the collection works this way

Recorded on 2026-10-10.

## Summary

Collect real incidents broadly, preserve their temporal dependencies, and separate
observations from fresh evaluations. Keep documentation, problems, results, and
commands separate. The main limitation is that packaging checks cannot establish
whether an incident is real or its explanation is correct.

## Preserve the sequence that caused the difficulty

A small task must retain the earlier fact and the later decision that depends
on it. Reducing only the final broken code creates a bug-fixing task and loses
the behavior we wanted to study. Padding a prompt to make it long does not
replace the original dependency.

## Accept incomplete evidence and label it

An incident can be valuable before anyone builds a reproduction. We separate
incident reports, runnable packages, fresh model reproduction, and evidence
from a temporal comparison. Only real fresh model runs support model
reproduction; inserting a known bad solution checks the judge.

## Use the earlier structure without importing the benchmark

The earlier environment-collection contract separated documentation, problems,
results, and commands. This kit keeps those boundaries with smaller forms
suitable for contributors. Its metadata is not a drop-in implementation of the
older benchmark schemas, and no historical results are copied here.

## Keep originals private and submissions reviewable

Past sessions can contain other people's code, credentials, or personal
information. Agents inspect only owner-selected sources and prepare sanitized
derivatives. The owner reviews the exact files before upload. Ignoring raw
histories in Git helps prevent accidents but is not a privacy check.

## Use local, dependency-free collection tools

Python's standard library is enough to create and inspect packages. The kit
does not choose an agent provider, run paid experiments, install project
dependencies, or execute contributions during metadata validation. Each
reproduction declares its own requirements and isolation needs.

## Publish the kit while keeping incident collection local

The owner initially requested a local repository, then authorized publication
to DylanZSZ/agent-failure-repo. Installing the kit still collects and uploads
nothing automatically. Each contributor controls their history and sharing.

## Ship a standalone skill from maintained sources

The installable skill includes a generated copy of the collection guides,
templates, and local tools. Source files remain in the repository's normal
locations; the bundle builder checks that packaged copies match them. This
keeps installation usable without the original checkout while avoiding manual
edits to two versions of the same guide.

## Make the README directly executable by the agent

The primary entrypoint is a message asking an existing agent to follow the
README. Skill installation remains optional. The README states the full
workflow and its completion condition so setup does not become the delivery.
A local start command creates or resumes a private workspace; it does not
pretend to read history or invoke a model. Agents preserve the original target
project when moving into the collection workspace.
