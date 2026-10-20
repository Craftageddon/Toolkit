---
name: craftageddon-release-qa
description: Package and audit every Craftageddon deliverable using three separate verification gates. Use for source checks, CI, test evidence, versioned releases, artifact hashes and completion decisions.
---

# Craftageddon Release QA

## Mandatory release flow
1. Assign version and source revision; save original project files; collect artifact list and acceptance criteria.
2. Gate **V1 Requirements & Design**: inspect exact file outputs, scale, dimensions, constraints, owner preferences and a pass/fail matrix.
3. Gate **V2 Technical & Functional**: run automated tests and open outputs using intended applications, document environment and error logs.
4. Gate **V3 Independent Final Validation**: use a distinct test method/reviewer, ideally a clean environment or physical assembly, and document exceptions.
5. Use `scripts/triple_verify.py` to track evidence, hash-bound artifacts, and sequential approvals. Do not fabricate evidence, assert passing unrun tests or mark `FINALIZED` while blocked.
6. When a tracked file changes, re-snapshot and redo verification. Keep evidence and checksum manifest in versioned release folder.
7. Release only when the gate is eligible and approval to publish was granted. Always summarize limitations, unverified hardware/fit, and rollback instructions.

## Packaging hygiene
- Consistent file names, README, CHANGELOG, build/run steps, pinned versions, reproducible ZIP and SHA-256 hashes.
- Prevent secrets, private chat histories, executable downloads from untrusted sources, and personal data in archives.
- Avoid changing project `latest` pointers or wiping older versions; preserve archived source revisions.
