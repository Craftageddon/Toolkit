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
5. For tracked verification, use this skill's bundled `scripts/triple_verify.py` as described below to track evidence, hash-bound artifacts, and sequential approvals. Do not fabricate evidence, assert passing unrun tests or mark `FINALIZED` while blocked.
6. When a tracked file changes, re-snapshot and redo verification. Keep evidence and checksum manifest in versioned release folder.
7. Release only when the gate is eligible and approval to publish was granted. Always summarize limitations, unverified hardware/fit, and rollback instructions.

## Packaging hygiene
- Consistent file names, README, CHANGELOG, build/run steps, pinned versions, reproducible ZIP and SHA-256 hashes.
- Prevent secrets, private chat histories, executable downloads from untrusted sources, and personal data in archives.
- Avoid changing project `latest` pointers or wiping older versions; preserve archived source revisions.

## Bundled verification helper

The helper is included at [scripts/triple_verify.py](scripts/triple_verify.py),
relative to this SKILL.md. Resolve it from the directory containing this loaded
skill, not from the user's project or the current working directory. Pass its
absolute path to Python and always give an explicit absolute project `--root`.
It requires Python 3.10+ and only the standard library; it needs no network,
account connection, or separate toolkit checkout.

For an actual project whose artifacts and acceptance criteria are known:

```text
python "<skill-directory>/scripts/triple_verify.py" init --root "<project-directory>" --project "Project name" --artifact "relative/path/to/artifact"
python "<skill-directory>/scripts/triple_verify.py" status --root "<project-directory>"
```

Repeat `--artifact` for every release artifact. Evidence files belong under the
project's `verification/evidence/` directory. Read the helper's subcommand help
when recording checks: V3 requires `--independence` describing the actual
independent method. Use `resnapshot` after an artifact changes, then repeat the
affected approvals. Finalization checks recorded evidence integrity; it does
not grant permission to publish.

For a checklist/template-only request, create the checklist directly and leave
unperformed gates NOT RUN. Do not initialize a tracker, manufacture evidence,
or finalize a project solely to demonstrate this skill. If a real project's
requirements or artifacts are absent, document them as prerequisites. If the
bundled helper itself is missing, report an incomplete skill installation;
do not mistake a project-relative path lookup failure for a missing helper.
