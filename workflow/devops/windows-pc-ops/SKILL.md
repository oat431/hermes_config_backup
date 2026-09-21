---
name: windows-pc-ops
description: Audit or fix the user's Windows PC (SAHACHAN-LAPTOP).
---

# Windows PC Operations (SAHACHAN-LAPTOP)

Audit, toolchain support, and Windows debugging on the user's Windows 11 client
laptop (SAHACHAN-LAPTOP, Acer Nitro ANV15-41). Personal-computer counterpart of
the `homelab-infra-audit` skill (Linux/Docker server audits). Server audit notes
live under `home-lab/audit/server`; PC notes under `home-lab/audit/personal-computer`.

## When to use

- "Audit my computer" / "check my essential components" (PC = this Windows host)
- Windows toolchain or install errors on this host (pipx, uv, python, node, winget)
- Event-log / AppX / shell (Start menu) debugging on this machine
- Any task needing PowerShell probes launched from git-bash

## Machine profile (verified 2026-09-03)

| Item | Value |
|------|-------|
| Host | SAHACHAN-LAPTOP, Acer Nitro ANV15-41 (laptop) |
| OS | Windows 11 Home Insider Preview Dev Channel, build 26340 - expect shell instability |
| CPU/RAM/GPU | Ryzen 5 6600H 6C/12T, 32 GB DDR5, RTX 3050 6GB + Radeon 660M |
| Disks | Samsung 512 GB NVMe (C:), WD SN770 1 TB (E: + F:, vault on F:) |
| Network | Ethernet 192.168.1.123, GW 192.168.1.1; Tailscale 100.90.67.14 -> homelab 100.73.143.25 |
| DNS | AdGuard public 94.140.14.49/.59 BY DESIGN. Homelab AdGuard (192.168.1.121) blocks google.com (0.0.0.0, direct-verified) - INTENTIONAL user-side Google block; laptop stays on public AdGuard. Re-pointing = 1 elevated Set-DnsClientServerAddress |
| Security | Defender on, tamper on; firewall enabled; BitLocker/Device Encryption ON for all volumes (user enabled 2026-09-03, verified elevated) |

## Vault output conventions (mirror the server audits)

- Folder: `F:\obsidian_note\oralita_md\home-lab\audit\personal-computer\`
- English docs, table-driven, status column OK / WARN / FAIL (server style uses emoji; ASCII is safe in files)
- Dated snapshot: `personal-computer-audit-YYYY-MM-DD.md` - System Overview table, then numbered sections (1. Hardware & Base Platform, 2. Storage & Disk Health, 3. Memory & Performance, 4. Networking, 5. Security, 6. Software & Toolchain, 7. Services, 8. Event Log Findings, 9. Findings & Recommendations), Related links at end
- Index: `Personal-Computer-Checklist.md` with frontmatter `tags: [personal-computer, moc, checklist]`, an Audit Log table of dated notes (wikilinks), Standing Checklist of the 9 sections, Related links
- Incident/fix notes: `YYYY-MM-DD-<issue>-fix.md`, self-contained: Symptom, Evidence & Timeline table, Root Cause, Actions Attempted (with real results), Recommended Fix (exact commands), Side Notes. Register every dated note in the checklist Audit Log.
- Only report live-verified values; never fabricate. User prefers review-then-execute: audit/read first, get approval before changes.

## Audit workflow

1. Read the newest existing audit note to copy conventions before writing anything.
2. Write the probe as a `.ps1` file in `$LOCALAPPDATA/Temp` (see pitfalls - never inline `-Command`).
3. Pre-check the file is pure ASCII (smart quotes / em dashes break PowerShell parsing):
   `python -c "d=open(r'<path>',encoding='utf-8').read(); print(len([c for c in d if ord(c)>127]))"`
4. Run: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:/Users/Admin/AppData/Local/Temp/<probe>.ps1"`
   (MSYS path conversion is off for native programs - pass C:/... paths, never /c/...)
5. Probe sections (see `scripts/pc-audit-probe.ps1`, a verified working probe): SYSTEM, CPU, MEMORY,
   GPU, STORAGE-DISKS, STORAGE-RELIABILITY (blank non-elevated - note as gap), STORAGE-VOLUMES,
   TEMP-SIZES, NETWORK, NETWORK-TESTS (gateway/internet/Tailscale ping), SECURITY (Defender,
   firewall, updates, pending-reboot keys, UAC), SOFTWARE-INSTALLED (registry uninstall keys),
   SOFTWARE-CLI (version probes), SERVICES-KEY, PERFORMANCE, EVENTS (System+Application, 7d).
6. Close gaps with targeted follow-ups: `type -a`/`Get-Command` PATH resolution (first hit wins and
   may differ from the registry install), `reg query` for Insider ring, `py -0p` / `uv python list`.
7. Write the docs, verify with a folder listing.

## Toolchain and PATH facts (this host, learned the hard way)

- git-bash PATH order: Hermes venv python first, then MSYS2 `C:\Program Files\msys2\ucrt64\bin`
  BEFORE python.org Python312. Result: `python3` in bash = MSYS2 GCC build 3.12.7, NOT native.
- uv and pipx (scoop 1.17+, uv backend) REJECT MSYS2/MinGW Python builds: `Unknown operating
  system: mingw_x86_64_ucrt_gnu` (msys2/MINGW-packages#30922). Never feed MSYS2 python to uv/pipx;
  fix = point at a native interpreter. `PIPX_DEFAULT_PYTHON` is set to python.org Python312
  (2026-09-03); `setx` only affects new shells.
- Native interpreters: python.org 3.12 (py launcher default), Astral 3.11.15 (uv-managed).
- User PATH reordered 2026-09-03: Python312 + Scripts + Launcher now BEFORE msys2 ucrt64 in HKCU
  Environment; python3.exe shim added to Python312 dir. Fresh cmd/PowerShell/git-bash resolve
  python/python3 to native 3.12.10. MSYS2 terminals still prepend their own bins (by design).
  Backups: %TEMP%\PATH-backup-*.txt.
- node via nvm4w (C:\nvm4w\nodejs; hermes-bundled node dir is earlier on PATH); kubectl = Docker
  Desktop bundled (v1.36); java = GraalVM 25; Go 1.25.3; scoop holds only pipx; no VS Code.

## Software state & cooling notes (updated 2026-09-03)

- Editor = **Zed 1.17.2 native installer** (`AppData\Local\Programs\Zed`, CLI on PATH;
  config `%APPDATA%\Zed\settings.json`, AGENTS.md there too). The Store/MSIX Zed build
  was removed (native is the right route). DeepSeek wired for edit-predictions + agent;
  OpenClaw ACP via npm global (`openclaw acp`).
- Installed 2026-09-03: 7-Zip 26.02, VLC 3.0.23, fzf 0.74.3 (winget). Removed: Acer
  Jumpstart + UEIP telemetry (elevated msiexec by GUID). ~13 Acer services remain
  (Agent, Care Center, Quick Access, NitroSense deps) - do NOT mass-disable; fan
  control breaks.
- Cooling/noise (ANV15-41, known-loud model): NitroSense **Auto** for daily use (fans
  stop at idle by design); **Performance mode spins fans hard even on light tasks**.
  Advise FPS cap via NVIDIA App + raised rear edge; do NOT advise repaste (machine is
  new); Samsung NVMe 69 C under load is normal.
- **WSL2 = Docker Desktop's engine backend on this Home-edition PC (no Hyper-V on Home).**
  The user opens Docker Desktop REGULARLY (local images/containers: mongo:8, postgres,
  sevensolution-api, local-postgres). NEVER `wsl --uninstall` here - mistake made
  2026-09-03: user said 'uninstall WSL, I don't know why I need it' meaning Ubuntu, but
  the removal also killed the docker-desktop distro. Recovery: `wsl --install
  --no-distribution` (platform only, NO Ubuntu distro - user does not want one; no
  reboot needed) then start Docker Desktop - it re-creates its distro; the data VHD
  survives WSL removal, so images/containers were preserved.

## Windows debugging - read `references/windows-appx-debugging.md` first

Shell crash loops / AppX trouble on this Insider Dev machine. Headline rules:

1. Gather evidence before acting: crash signature, counts and FIRST-occurrence time windows,
   on-disk file version skew vs package version, WU-client and AppX deployment logs around onset.
2. **NEVER run `Reset-AppxPackage` (or queue AppX deployment ops) on inbox/system packages while
   the deployment pipeline may be wedged.** Non-elevated resets can hang and queue a stuck Remove
   op in AppXDeploymentServer that blocks the ENTIRE AppX pipeline (Store updates included) until
   a reboot. Diagnose the wedge first - see the reference for symptoms and the safe ladder.

## Related

- Skill `homelab-infra-audit` - server counterpart (Linux/Docker, audit/server)
- Vault: `[[Personal-Computer-Checklist]]`, `[[Homelab-Infra-Checklist]]`
