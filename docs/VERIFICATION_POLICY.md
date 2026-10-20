# Three independent verification checks

The checks are required for *every deliverable*, not just one project-wide checklist at release time.

| Gate | What to prove | Example evidence | Failure state |
|---|---|---|---|
| V1 - Requirements | Complete match to approved dimensions, format, scope and constraints | signed matrix with acceptance criteria, dimension comparison, visual source audit | REWORK |
| V2 - Technical | It builds, opens in the target tool, passes automated and manual functional tests | test logs, screenshots, file inspections, mesh/DXF validators | REWORK / BLOCKED |
| V3 - Independent validation | Different method or reviewer checks end-to-end use, hardware when applicable | second fresh inspection, separate app export/reimport, physical print/fit report | REWORK / BLOCKED |

### Separate checks and independence
- V3 must use a different method from V2; a repeat of the same test log is not independent validation.
- Ideally V3 uses a different reviewer or a second independent tool. One-person projects can use a separate method and a fresh session, but must explicitly identify limits.
- For complex systems, V1/V2/V3 each cover all requirements, though their specific techniques differ.
- Do not count three reruns of the same test as three independent checks.
- Evidence must be produced from actual tests, not written as though an unperformed test passed.
- When code/files change, update artifacts and repeat affected verifications. The verifier invalidates all previous approval if tracked artifact hashes change.
- Hardware/firmware releases cannot pass V3 without the required physical verification; offline CAD releases cannot claim printed function without an actual print.

### Releasing
State is **DRAFT -> V1 PASS -> V2 PASS -> V3 PASS -> FINALIZED**, with FAILED/BLOCKED alternatives. The `finalize` command is an explicit last approval after these checks; the script prevents it when the evidence is absent, altered, same-method for V2/V3, or source artifacts changed. Keep an immutable copy of the evidence bundle with release artifacts.

### Security
The verifier is a bookkeeping and integrity helper, NOT a replacement for professional engineering review or a security boundary against a malicious editor of its own files. Any action changing device firmware, deleting original drawings, or granting broad MCP code execution still needs owner approval.
