# Windows Shell / AppX Debugging - Start menu crash case (2026-09-03)

Verified on SAHACHAN-LAPTOP (Win11 Home Insider Preview Dev, build 26340).
The AppX deployment pipeline on this machine wedges under inbox-app servicing
churn (ScreenSketch / StartExperiencesApp updates, package removals) - expect
recurrence on this Insider build. This reference is the reusable playbook.

## Case signature (Start menu crash loop)

- Event 1000 Application Error, recurring every 2-4 min:
  Faulting app: StartMenuExperienceHost.exe; Faulting module: StartDocked.dll;
  Exception 0xc000027b (stowed XAML exception = state/render failure, not driver fault).
- Diagnostic tell: ON-DISK VERSION SKEW - package reports 10.0.26100.8951 but
  StartDocked.dll on disk is 10.0.26100.9233 (partial servicing). Check:
  `Get-ChildItem <pkgdir> -Filter *.dll | % { $_.VersionInfo.FileVersion }`
- 38 crashes, ALL on one day, first at 11:44 -> correlate onset with AppX/WU logs,
  not with the oldest file date. The trigger appeared at onset time.

## Evidence commands (run BEFORE touching anything)

1. Crash count / first / last / recency (is it still live?):
   ```powershell
   $ev = Get-WinEvent -FilterHashtable @{LogName='Application'; ProviderName='Application Error'; StartTime=(Get-Date).AddDays(-14)} |
         Where-Object { $_.Message -match 'StartMenuExperienceHost' }
   $ev.Count; ($ev | Select-Object -Last 1).TimeCreated; $ev[0].TimeCreated
   $ev[0].Message   # full signature: exception code, module versions, paths
   ```
2. AppX deployment activity around onset (inbox app servicing = prime suspect):
   `Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-AppXDeploymentServer/Operational'; StartTime=...; EndTime=...}`
   Watch: event 819 (packages to install/remove), 617 status updates,
   642 PACKAGE_STATUS_REGISTRATION_REQUIRED_BLOCKING, 678 "hung and cancelled".
3. Windows Update client log (same window):
   `Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-WindowsUpdateClient/Operational'; ...}`
4. Wedge symptoms - STOP and check BEFORE queuing any AppX op:
   - event 678 "Register operation ... is hung and cancelled"
   - cleanup retry loops: event 471 error 0x5 deleting stale packages in
     C:\Program Files\WindowsApps\Deleted\ every ~6 min
   - resiliency files accumulating: C:\ProgramData\Microsoft\Windows\AppRepository\*.rslc
   - stray client processes hung for hours:
     `Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" | select ProcessId, CreationDate, CommandLine`
     (a `Get-AppxPackage | ConvertTo-Json` from 12:01 was still alive at 16:47)

## PITFALL (learned the hard way) - never queue AppX ops into a wedged pipeline

- Non-elevated `Get-AppxPackage ... | Reset-AppxPackage` on an inbox/system package
  does NOT fail fast - it HANGS and queues a deployment Remove op on that package
  inside AppXDeploymentServer (log event 603/607 with the package as main parameter,
  no completion event). That stuck op then blocks EVERY subsequent AppX operation
  (re-register, reset, remove, and all Store app installs/updates) until reboot.
- Same for `Add-AppxPackage -Register` while a stuck op is queued: hangs silently
  (zero output). Check for stuck ops FIRST; if any exist, the clean cure is a REBOOT
  (resiliency replays the queued op cleanly on boot). Elevated AppXSvc restart is the
  less-disruptive alternative but may not clear everything.
- Cache clear of the Start host (`%LOCALAPPDATA%\Packages\Microsoft.Windows.StartMenuExperienceHost_cw5n1h2txyewy\LocalState`,
  move to a TEMP backup, not delete) is safe and sometimes sufficient for
  0xc000027b loops - but did NOT fix this case (crashes continued within 4 min).

## Fix ladder (in order)

1. Reboot - clears wedged AppXSvc state, replays queued reset. Verify no new
   Event 1000s in 10 min after login.
2. If still crashing, ELEVATED reset (admin PowerShell):
   `Get-AppxPackage Microsoft.Windows.StartMenuExperienceHost | Reset-AppxPackage`
   `Get-AppxPackage Microsoft.StartExperiencesApp | Reset-AppxPackage`
3. System file repair (admin, slow): `DISM /Online /Cleanup-Image /RestoreHealth` then `sfc /scannow`.
4. Latest Insider Dev flight (file skew 8951/9233 may only resolve on the next build) +
   report via Feedback Hub. Insider Dev = instability by design; document, don't rage.

## Writing it up (vault conventions)

Dated incident note `YYYY-MM-DD-<issue>-fix.md` under
`home-lab/audit/personal-computer/` (mirror the server audit style): Symptom,
Evidence & Timeline table, Root Cause (label hypothesis confidence), Actions
Attempted with REAL results (including the one that backfired - blameless
accuracy prevents repeating it), Recommended Fix with exact commands, Side
Notes. Register the note in `Personal-Computer-Checklist.md` Audit Log.

## PowerShell-from-git-bash pitfalls (applies to all probes)

- NEVER inline `powershell -Command "..."` from bash with double quotes: bash
  expands `$var` before PowerShell sees it -> parser garbage (empty tokens,
  broken strings). Always write a `.ps1` file and run `-File`.
- Smart quotes / em dashes in .ps1 files break parsing outside string literals.
  Keep script files pure ASCII; pre-check:
  `python -c "d=open(r'<path>',encoding='utf-8').read(); print(len([c for c in d if ord(c)>127]))"`
- Run via `powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:/...ps1"`
  (native tools need C:/ paths, not /c/ MSYS paths).
- Redirected output is line-flushed, so zero output for a long time = hung early
  (usually AppX/service lock), not slow progress.
