# Integration setup & verification matrix

## GitHub and Codex (phase 1)
- GitHub account is `Craftageddon`; the explicitly approved repository is `Craftageddon/Toolkit`. The permissions retry created the setup branch successfully. See the publication PR for the exact commit, CI, and remote checks. Earlier access limitations in the ZIP are historical.
- Create/select explicit projects before any remote GitHub mutations. Work on review branches and open PRs rather than changing production branches directly.
- Put `AGENTS.md` into each project root. User-level Codex skills go into `$HOME\.codex\skills` using the installer.
- Set each project's versioned work area under `%USERPROFILE%\Desktop\Chat GPT Saved Files\<Project Name>\<Version>`. Codex working-directory access is required for actually writing it.

## Blender 5.2.2 MCP (phase 2)
- Official information: https://www.blender.org/lab/mcp-server/
- Blender 5.1+ required; 5.2.2 is consistent with this requirement, but not checked on user's computer.
- Official Blender MCP architecture requires separate Blender add-on + MCP server + compatible LLM client.
- Recommended safe install: back up settings, download from official Blender page, verify publisher and release, install add-on in Blender, configure server in local MCP-capable client (Codex if supported), then test only on a throwaway scene.
- Official Blender warns its MCP executes LLM-generated Python without guards. Do NOT connect a full-permission MCP host to sensitive or production files. Prefer a VM or an isolated Windows user/session with inaccessible sensitive drives and no unnecessary network access.
- Smoke test: new throwaway scene; create a named cube with exact 20 mm dimension; query scene; save in sandbox; close/reopen and inspect object. Record V1/V2/V3 evidence, including actual Blender version.
- The MCP config command and plugin filenames can change across releases: copy the current values from the official install page, do NOT hardcode unverified launch commands.

## AutoCAD 2026 (phase 3)
- Official API interface: https://help.autodesk.com/cloudhelp/2026/ENU/AutoCAD-Customization/files/GUID-E6429154-36DF-4D84-8ABC-9FCA15B66158.htm
- For small deterministic 2D patterns, start with restricted offline JSON -> AutoLISP generator in this package.
- Generate `*.lsp` locally; review source; create an **empty disposable test drawing in mm**; use AutoCAD APPLOAD and command `CFIMPORT`.
- Compare entity count, red and cyan layers, geometry bounds, hole radii, and exported DXF. Do not load into original work until all checks pass.
- The corrected v0.1.3 sample has bounded native AutoCAD 2026 import, DWG/DXF save/reopen and independent DXF checks. See `AUTOCAD_IMPORT_FIX_v0.1.3.md`. This does not provide a general automation bridge or certify other drawings. Run CFIMPORT once in an empty test drawing; it appends geometry.

## SharePoint / OneDrive (phase 5)
- SharePoint plugin installation was suggested but needs user approval and corporate tenant authorization. Network locations are not automatically accessible just because SharePoint is connected.
- Authorize least-privilege read access first. Verify expected Craftageddon Assets folder path against actual cloud item IDs before allowing writes. Avoid storing secrets in shared folders.

## Figma, Replit and Android (phases 6-7)
- Figma and Replit plugins are installed; use only when appropriate to target design/file. Figma libraries can document Ember Steel tokens, layout, states and variants.
- Android 16 / AYN Thor work package content remains reference-only; no ROM modifications during setup.
- Build and release in isolated, versioned project workspaces. Do not publish or flash without explicit confirmation.

## Verification (phase 8)
- Use V1/V2/V3 for *each* deliverable. Verify correctness, then functionality, then independently verify final output.
- For any local setup, V2 remains blocked until Windows application launch/test succeeds; V3 blocked until a distinct recheck or hardware test happens.
