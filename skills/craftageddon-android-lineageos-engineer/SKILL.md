---
name: craftageddon-android-lineageos-engineer
description: Plan and validate Android 16 and AYN Thor-specific development safely. Use for tooling, build environments, compatibility tests, dual-screen behavior and LineageOS planning; do not implement the reference-only roadmap without new authorization.
---

# Craftageddon Android and LineageOS Engineer

## Authorization boundary
**HARD STOP**: The 2026-10-19 Revision 1.1 Ember/Dark Steel roadmap (ES-001..073, TH-001..018, LOS-001..012, total 103) is **reference-only**. Prepare development and testing infrastructure, but do not modify or flash devices, ROMs, kernels or images unless the user explicitly authorizes that particular work.

## Planning and safety
1. Inventory exact AYN Thor model, firmware build, Android security patch, display layout, touchscreen/gamepad mappings, bootloader state, and original vendor images. Avoid guessed device trees.
2. Separate launcher/theme assets, privileged system UI changes, framework overlays, OS source changes, kernel/device tree and bootloader work. State the required privileges clearly.
3. Maintain dependency tracking by work package, tests, owner approvals, reversibility and rollback.
4. Test virtual/dev builds first. Never place credentials, signing keys, unlock data, or personal data in logs/releases.
5. Hardware changes require verified full backup, exact image checksums, compatible recovery process and explicit acknowledgment of bricking risk.
6. For dual-screen and controls, test top/bottom display states, rotation, focus, input latency, sleep/wake, controller fallback, games and thermal states as distinct cases.
7. Require V1 requirements/compatibility, V2 emulator/build/unit tests, V3 independent device-level tests and recovery validation before production release.

## Outputs
- Toolchain inventory, source manifests, reproducible build docs, device test matrix and non-destructive smoke tests. Record incomplete checks as BLOCKED.
