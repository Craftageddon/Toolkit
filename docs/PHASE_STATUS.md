# Craftageddon setup state | 2026-10-20

This is a **truthful status inventory**, not a report that any unobserved installation succeeded.

| Phase | Work completed in this package | Pending verification or authorization |
|---|---|---|
| 1. GitHub / Codex | `AGENTS.md`, reusable skills, GitHub-ready source, CI checks and safe branch publishing script; setup branch creation succeeded after permissions update; publication tracked in the draft PR | Review exact commit and V1/V2/V3 evidence in PR, merge reviewed PR, local Codex skill load |
| 2. Blender MCP | Official setup and security guide, 20 mm smoke-test scene script | User-authorized local install, VM/isolation, real Blender test, compatible client config |
| 3. AutoCAD | Restricted offline JSON-to-AutoLISP generator plus sample | Source review, physical AutoCAD 2026 APPLOAD/CFIMPORT, import/export and units checks |
| 4. Craftageddon skills | Six `SKILL.md` files authored | Install in target Codex skills directory and confirm Codex discovers each |
| 5. Microsoft files | SharePoint connector identified and suggestion surfaced | Account connection and tenant authorization; validate actual folder IDs and access |
| 6. Figma / Android | Existing Figma/Product Design tools identified; Ember Steel + Android safe-planning skills | Target design system/document approval; no ROM / OS work authorized |
| 7. Testing + release | Offline unit tests, verifier, ZIP packager, integrity manifest | Windows execution and each application's integration test |
| 8. Triple verification | Evidence-based V1/V2/V3 release gate implemented, tested offline | Real project-specific and hardware/application evidence before declaring final |

**Android reference boundary:** The 2026-10-19 Revision 1.1 plan with 103 work packages is stored as reference only and was NOT implemented here.

**Safety:** No account data, production drawings, firmware, live assets, local machine settings, GitHub repositories, or device images were changed by building this archive.

**Release class:** DEVELOPMENT STARTER / INTEGRATIONS NOT VERIFIED.

**GitHub permission retry (2026-10-20):** The ZIP recorded earlier 403 failures. Creating `setup/craftageddon-ai-toolchain-v0.1.1` now succeeded. An independent Git remote read confirmed both branches at the preserved baseline before source publication. See `PUBLICATION_RETRY_2026-10-20.md` and the draft PR for source/CI/remote validation evidence.
