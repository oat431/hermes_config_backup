---
name: windows-pc-audit
description: Windows PC audit & troubleshooting with dated vault notes.
---

# Windows PC Audit & Troubleshooting

Audit the user's Windows personal computer (NOT the homelab server — that is
`homelab-infra-audit`). Machine: `SAHACHAN-LAPTOP` (Acer Nitro ANV15-41). Its
living profile lives in the vault at
`home-lab/audit/personal-computer/Personal-Computer-Checklist.md` — read the
checklist + latest dated audit BEFORE starting so the new audit compares against
the previous snapshot (drift detection is the point).

Triggers: "audit my computer / check my PC / verify components", Windows
desktop issues (Start menu or search crashes, AppX/Store hangs, python/pipx
toolchain failures), or a dated follow-up to a previous PC audit.

## Vault conventions (mirror the homelab server tree)

Folder: `F:/obsidian_note/oralita_md/home-lab/audit/personal-computer/`

| File | Purpose | Shape |
|------|---------|-------|
| `Personal-Computer-Checklist.md` | Index | Frontmatter `tags: [personal-computer, moc, checklist]`, Audit Log table (Date \| Note [[wikilink]] \| Focus), standing checklist of numbered sections, Related links |
| `personal-computer-audit-YYYY-MM-DD.md` | Dated snapshot | H1 `# <Subject> Audit — <hostname>`, blockquote `> **Date:**` / `> **Checklist:** [[...]]` / `> **Status:**`, System Overview table, numbered sections with ✅/⚠️/❌ status tables, Findings & Recommendations table (R# rows with severity), Related |
| `YYYY-MM-DD-<issue>-fix.md` | Incident/fix note | Self-contained: Symptom, Evidence & Timeline table, Root Cause, Actions Attempted (with results — include failures honestly), Recommended Fix, Side Notes. `> **Status:**` header updated ✅ Resolved + timestamp once verified |

Append a row to the checklist Audit Log whenever an audit or incident note
lands. English, table-driven, full-detail self-contained. Every claim backed by
real command output; never fabricate statuses.

## Probe method (git-bash → PowerShell)

1. **Write a `.ps1` file** with write_file to `C:/Users/Admin/AppData/Local/Temp/`
   (native path — powershell -File gets no MSYS path translation).
2. **ASCII-check before running**: a stray curly quote/em-dash breaks the parser
   with confusing "string is missing the terminator" errors at odd offsets:
   `python -c "d=open(r'<file>',encoding='utf-8').read(); print(len([c for c in d if ord(c)>127]))"` — expect 0.
3. Run: `powershell.exe -NoProfile -ExecutionPolicy Bypass -File <native-path>`,
   redirect `> out.txt 2>&1` for long output, then read_file the result. NEVER
   inline `powershell -Command` from bash with double quotes — bash eats `$vars`
   (silent empty output or parse chaos). In scripts set
   `[Console]::OutputEncoding = UTF8` up front, `$ErrorActionPreference='Continue'`,
   try/catch around privilege-sensitive calls.
4. Long/hung commands: foreground cap 600s. On timeout CHECK STATE first
   (process list via CIM, result files, logs) — do not blindly re-run.

Reusable probe: `scripts/pc-audit-probe.ps1` (CIM hardware, storage health,
volumes, network, Defender/firewall/updates, installed essentials, CLI versions,
key services, top processes, 7-day System/Application errors).

## Essential component → query map

- Hardware/OS: `Get-CimInstance Win32_OperatingSystem/ComputerSystem/Processor/PhysicalMemory/VideoController/BIOS/SystemEnclosure/Battery`
- Disks: `Get-PhysicalDisk` (Health); volumes `Win32_LogicalDisk DriveType=3`; temp sizes
- Network: `Get-NetIPConfiguration`, `Get-NetAdapter -Physical`, `Test-Connection` GW/internet/Tailscale peer
- Security: `Get-MpComputerStatus`, `Get-NetFirewallProfile`, `Get-HotFix`, pending-reboot reg keys (CBS + WU RebootRequired), UAC reg
- Software: Uninstall registry keys (HKLM + WOW6432Node + HKCU), CLI `--version` probes
- Events: `Get-WinEvent -FilterHashtable @{LogName='System'|'Application'; Level=1,2,3; StartTime=...}`
- BitLocker + NVMe wear need ELEVATION (`manage-bde -status`, `Get-StorageReliabilityCounter`)

## Pitfalls (learned the hard way)

- **MSYS2 Python vs uv/pipx**: msys2/ucrt64 sits before Python312 on PATH, so
  git-bash `python3` = GCC-built MSYS2 python. uv/pipx (uv backend) REJECT it:
  `Unknown operating system: mingw_x86_64_ucrt_gnu`. Fix: pin
  `PIPX_DEFAULT_PYTHON` to the python.org interpreter
  (`C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe`);
  setx affects new shells only.
- **Start menu crash loop / AppX wedge**: `StartMenuExperienceHost.exe` Event
  1000 + `StartDocked.dll`, exception `0xc000027b` = stowed XAML exception.
  Correlate crash onset time against AppX/WU logs before guessing. A wedged
  AppXDeploymentServer makes EVERY AppX op hang with zero output; the cure is a
  REBOOT, not more AppX ops. Full ladder:
  `references/windows-appx-wedge-and-startmenu-crash.md`.
- **Non-elevated `Reset-AppxPackage` on a system package is dangerous**: it can
  hang AND queue a stuck Remove op inside AppXDeploymentServer that blocks all
  further AppX work (Store updates included) until reboot. Don't attempt it
  non-elevated; silent-hang IS the wedge symptom.
- **Elevated checks pattern**: `Start-Process powershell -Verb RunAs -Wait`
  pops UAC (user clicks Yes). Have the elevated script write results to a file;
  the bash launcher may time out while the elevated child still completes —
  verify via the RESULTS FILE, never the launcher exit code.
- **Security boundary**: disk encryption / key-material enablement stays manual
  (user executes); document as a recommendation row marked "user executes
  manually" — never automate it.
- **Insider Dev Channel** (this machine): expect shell instability; fix = latest
  flight + Feedback Hub when it is a genuine servicing bug.
- **Windows 11 Home disk-encryption nuance (R8 class)**: Device Encryption covers
  ONLY the OS drive (Settings → Privacy & security → Device encryption; needs TPM
  "Ready" + Microsoft account for recovery-key backup). Home has NO full BitLocker
  management UI for fixed data volumes; `manage-bde -on <vol>:` works on some Home
  builds and errors on others → **VeraCrypt** is the reliable fallback for data
  volumes. State the threat model plainly: OS-drive encryption is the critical one
  for a stolen laptop; data volumes only matter against physical drive removal.
  Enablement stays manual (key material = user's high-risk boundary) — document as
  a recommendation row marked "user executes manually", never automate.
- **Uninstalling MSI bloatware from git-bash**: raw
  `msiexec /X{GUID} /qn /norestart` runs NON-elevated and fails fast with exit 67
  (no UAC prompt) — winget elevates itself but raw msiexec does not. Run it via
  `Start-Process msiexec.exe -Verb RunAs -Wait -PassThru -ArgumentList @("/X$guid",
  "/qn", "/norestart")` (expect one UAC click per product) and verify DisplayName
  is gone from all three Uninstall registry hives. GUID comes from the registry
  `UninstallString` value (`MsiExec.exe /I{GUID}`).

## Verification & output discipline

- Post-fix, verify with REAL counts since a marker time (e.g. `crashes since
  boot: 0`, `WSearch 7011 since boot: 0`) before declaring resolution.
- Update incident note Status → ✅ Resolved with reboot/verify timestamp; append
  checklist Audit Log rows; keep audit snapshots as records (edit R# rows only to
  record outcomes).
- User prefs: review-then-execute (findings/docs first, changes only after
  explicit approval); real post-edit verification; full-detail self-contained
  notes; current web research for tool versions.
