# Start menu crash loop + wedged AppX pipeline (session 2026-09-03)

Validated end-to-end on SAHACHAN-LAPTOP, Windows 11 Home Insider Preview Dev
build 26340. The crash loop started when the AppX deployment pipeline wedged
mid-servicing; **reboot resolved it** (0 crashes since boot).

## Crash signature

Event 1000 (Application Error), every ~2–4 min:

```
Faulting application name: StartMenuExperienceHost.exe, version: 10.0.26100.8951
Faulting module name: StartDocked.dll, version: 10.0.26100.9233
Exception code: 0xc000027b   (stowed exception — XAML/WinUI state failure)
```

0xc000027b in StartDocked.dll ≈ per-user layout/registration state failure, NOT
driver/hardware. **Version skew** (faulting DLL newer than its own package
exe/manifest) = partially serviced package — check both file versions on disk
before theorizing.

## Diagnosis path (order matters)

1. **Count + onset**: all crashes within 14d? first occurrence time? If the loop
   began TODAY, look at what changed today — not the last KB install.
   ```powershell
   $ev=Get-WinEvent -FilterHashtable @{LogName='Application';ProviderName='Application Error';StartTime=(Get-Date).AddDays(-14)} |
     Where-Object {$_.Message -match 'StartMenuExperienceHost'}
   $ev.Count; ($ev|Select-Object -Last 1).TimeCreated; $ev[0].TimeCreated
   ```
2. **Correlate onset against AppX + WU logs** around the first crash:
   `Microsoft-Windows-AppXDeploymentServer/Operational`,
   `Microsoft-Windows-WindowsUpdateClient/Operational`. Look for inbox-app
   updates (StartExperiencesApp, ScreenSketch), `REGISTRATION_REQUIRED_BLOCKING`
   flags, license-manager errors, trust-label waves.
3. **Check for a wedged pipeline** — signals:
   - event 678 "Deployment Register operation ... is hung and cancelled"
   - a Remove/Register op started but no completion event follows for 10+ min
   - ANY AppX cmdlet (Get-AppxPackage, Reset-AppxPackage,
     Add-AppxPackage -Register) hangs with zero output
   - stray hung `powershell.exe` clients (user diagnostics) alive for hours:
     `Get-CimInstance Win32_Process -Filter "Name='powershell.exe'"` → CommandLine
   - AppXDeploymentServer cleanup retry loop every ~6 min (error 0x5 deleting
     stale packages under `C:\Program Files\WindowsApps\Deleted\`)
4. Side-effect of a wedge: **Store app installs/updates hang** until reboot.

## Fix ladder (validated)

| Step | Result (session) |
|------|------------------|
| Clear Start host cache: kill `StartMenuExperienceHost`, MOVE (not delete) `%LOCALAPPDATA%\Packages\Microsoft.Windows.StartMenuExperienceHost_cw5n1h2txyewy\LocalState` (start2.bin + layout folder) to a temp backup | ❌ crashed again within 4 min — layout cache was NOT the cause |
| `Reset-AppxPackage` / `Add-AppxPackage -Register` NON-elevated | ❌ DANGEROUS — hung and queued a stuck Remove op on the package itself inside AppXDeploymentServer; blocked all later AppX ops |
| **Reboot** | ✅ **THE fix** — clears the wedged service state; queued reset replays cleanly; 0 crashes since boot; old package version purged from Deleted; StartExperiencesApp finished updating to 1.398.0.0 |
| If crashes persist after reboot: elevated `Reset-AppxPackage` on StartMenuExperienceHost + StartExperiencesApp → DISM /Online /Cleanup-Image /RestoreHealth + sfc /scannow → latest Insider flight + Feedback Hub | untested (not needed) |

Lesson: once the wedge is confirmed, STOP issuing AppX operations and reboot.

## Post-reboot verification (run these, don't eyeball)

```powershell
$os = Get-CimInstance Win32_OperatingSystem   # confirm LastBootUpTime
# R1: Start crashes since boot (expect 0)
Get-WinEvent -FilterHashtable @{LogName='Application';ProviderName='Application Error';StartTime=$os.LastBootUpTime} |
  Where-Object {$_.Message -match 'StartMenuExperienceHost'} | Measure-Object
# R2: WSearch 7011 timeouts since boot (expect 0)
Get-WinEvent -FilterHashtable @{LogName='System';ProviderName='Service Control Manager';StartTime=$os.LastBootUpTime} |
  Where-Object {$_.Message -match 'WSearch'} | Measure-Object
# AppX queue: recent ops should be completions/validation, no stuck ops
Get-WinEvent -FilterHashtable @{LogName='Microsoft-Windows-AppXDeploymentServer/Operational';StartTime=$os.LastBootUpTime} -MaxEvents 15
```

## Related R-items from the first audit (09-03)

- R1 Start crash loop → fixed by reboot. R2 WSearch timeouts → also cleared by
  reboot (same underlying wedge). R3 elevated pass → BitLocker OFF on all
  volumes (→ R8, user executes manually), Samsung NVMe 69 °C warm / WD 48 °C.
