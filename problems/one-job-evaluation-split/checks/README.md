# Reviewer-owned checks

Implement a check independent of the evaluated agent's self-report. Keep it
outside the agent's workspace. Report setup validity, task correctness, and
the intended failure separately. Treat evaluated code as untrusted when a
judge imports or runs it. Metadata validation does not execute these files.
