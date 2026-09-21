# Windows PC audit probe - ASCII ONLY, no smart quotes.
# Run: powershell.exe -NoProfile -ExecutionPolicy Bypass -File pc-audit-probe.ps1 > out.txt 2>&1
$ErrorActionPreference = 'SilentlyContinue'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)

function Sec($t) { Write-Output ("`n" + ('=' * 20) + " " + $t + " " + ('=' * 20)) }

Sec 'SYSTEM'
$os  = Get-CimInstance Win32_OperatingSystem
$cs  = Get-CimInstance Win32_ComputerSystem
$bios = Get-CimInstance Win32_BIOS
Write-Output ("ComputerName       : " + $env:COMPUTERNAME)
Write-Output ("Manufacturer/Model : " + $cs.Manufacturer + " / " + $cs.Model)
Write-Output ("BIOS               : " + $bios.SMBIOSBIOSVersion)
Write-Output ("OS                 : " + $os.Caption + " " + $os.BuildNumber + " " + $os.OSArchitecture)
Write-Output ("OS InstallDate     : " + $os.InstallDate)
Write-Output ("LastBootUpTime     : " + $os.LastBootUpTime)
$up = (Get-Date) - $os.LastBootUpTime
Write-Output ("Uptime             : " + ("{0}d {1}h {2}m" -f $up.Days, $up.Hours, $up.Minutes))
$bat = Get-CimInstance Win32_Battery
if ($bat) { Write-Output ("Battery            : " + $bat.Name + " | charge " + $bat.EstimatedChargeRemaining + "%") }

Sec 'CPU'
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
Write-Output ("CPU                : " + $cpu.Name.Trim() + " | " + $cpu.NumberOfCores + "C/" + $cpu.NumberOfLogicalProcessors + "T | " + $cpu.MaxClockSpeed + " MHz")
$load = (Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
Write-Output ("Load               : " + $load + " %")

Sec 'MEMORY'
Write-Output ("Total/Free         : " + [math]::Round($os.TotalVisibleMemorySize/1MB,1) + " GB / " + [math]::Round($os.FreePhysicalMemory/1MB,1) + " GB free")
Get-CimInstance Win32_PhysicalMemory | ForEach-Object { if ($_.Capacity) { Write-Output ("DIMM               : " + $_.Manufacturer + " " + [math]::Round($_.Capacity/1GB,0) + " GB @ " + $_.ConfiguredClockSpeed + " MHz") } }

Sec 'GPU'
Get-CimInstance Win32_VideoController | ForEach-Object {
  $res = ""; if ($_.CurrentHorizontalResolution) { $res = " | " + $_.CurrentHorizontalResolution + "x" + $_.CurrentVerticalResolution + "@" + $_.CurrentRefreshRate + "Hz" }
  Write-Output ($_.Name + " | driver " + $_.DriverVersion + " | " + [math]::Round($_.AdapterRAM/1GB,1) + " GB VRAM" + $res)
}

Sec 'STORAGE'
Get-PhysicalDisk | ForEach-Object { Write-Output ($_.FriendlyName + " | " + $_.MediaType + " | " + [math]::Round($_.Size/1GB,0) + " GB | Health: " + $_.HealthStatus) }
Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | ForEach-Object {
  $free = [math]::Round($_.FreeSpace/1GB,1); $sz = [math]::Round($_.Size/1GB,1)
  Write-Output ($_.DeviceID + " [" + $_.VolumeName + "] " + $_.FileSystem + " | " + $free + " GB free / " + $sz + " GB | " + [math]::Round(($free/$sz)*100,0) + "% free")
}
foreach ($p in @($env:TEMP, 'C:\Windows\Temp')) { $s = (Get-ChildItem $p -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum; Write-Output ("temp " + $p + " = " + [math]::Round($s/1MB,0) + " MB") }

Sec 'NETWORK'
Get-NetIPConfiguration -ErrorAction SilentlyContinue | Where-Object { $_.IPv4DefaultGateway } | ForEach-Object {
  Write-Output ("Adapter : " + $_.InterfaceAlias)
  Write-Output ("  IPv4  : " + ($_.IPv4Address.IPAddress -join ', '))
  Write-Output ("  GW    : " + $_.IPv4DefaultGateway.NextHop)
  Write-Output ("  DNS   : " + (($_.DNSServer | Where-Object { $_.AddressFamily -eq 2 } | ForEach-Object { $_.ServerAddresses }) -join ', '))
}
Get-NetAdapter -Physical | ForEach-Object { Write-Output ("NIC " + $_.Name + " | " + $_.Status + " | " + $_.LinkSpeed) }

Sec 'SECURITY'
$mp = Get-MpComputerStatus
if ($mp) {
  Write-Output ("Defender AV       : " + $mp.AntivirusEnabled + " realtime " + $mp.RealTimeProtectionEnabled + " tamper " + $mp.IsTamperProtected)
  Write-Output ("Signatures        : " + $mp.AntivirusSignatureVersion + " updated " + $mp.AntivirusSignatureLastUpdated + " | quick scan " + $mp.QuickScanAge + "d ago")
}
Get-NetFirewallProfile | ForEach-Object { Write-Output ("FW " + $_.Name + " | Enabled: " + $_.Enabled) }
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 5 | ForEach-Object { Write-Output ("KB               : " + $_.HotFixID + " | " + $_.InstalledOn) }

Sec 'SOFTWARE'
$regPaths = @('HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*','HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*','HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*')
$installed = Get-ItemProperty $regPaths -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName } | Select-Object DisplayName, DisplayVersion | Sort-Object DisplayName -Unique
$pat = 'obsidian|docker|tailscale|git|node\.js|python|visual studio|jetbrains|postman|7-zip|chrome|firefox|edge|cloudflare|warp|android|flutter|dbeaver|mongodb|nvidia|amd|intel|scoop|notion|discord|telegram|microsoft 365|office|steam'
$installed | Where-Object { $_.DisplayName -match $pat } | ForEach-Object { Write-Output ($_.DisplayName + " | " + $_.DisplayVersion) }
foreach ($c in @('git','node','python','py','pipx','uv','docker','tailscale','gh','java','go','winget')) {
  $cmd = Get-Command $c -ErrorAction SilentlyContinue
  if ($cmd) { try { Write-Output ($c + " -> " + (& $c --version 2>&1 | Select-Object -First 1)) } catch { Write-Output ($c + " -> " + $cmd.Source) } }
}

Sec 'PERFORMANCE'
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 10 | ForEach-Object { Write-Output ($_.ProcessName + " | " + [math]::Round($_.WorkingSet64/1MB,0) + " MB") }

Sec 'EVENTS-7D'
Get-WinEvent -FilterHashtable @{ LogName='System'; Level=1,2,3; StartTime=(Get-Date).AddDays(-7) } -MaxEvents 20 -ErrorAction SilentlyContinue | ForEach-Object {
  $m = $_.Message; if ($m.Length -gt 150) { $m = $m.Substring(0,150) }
  Write-Output ($_.TimeCreated.ToString('MM-dd HH:mm') + " | " + $_.LevelDisplayName + " | " + $_.Id + " | " + $_.ProviderName + " | " + $m)
}
Get-WinEvent -FilterHashtable @{ LogName='Application'; Level=2; StartTime=(Get-Date).AddDays(-7) } -MaxEvents 10 -ErrorAction SilentlyContinue | ForEach-Object {
  $m = $_.Message; if ($m.Length -gt 150) { $m = $m.Substring(0,150) }
  Write-Output ($_.TimeCreated.ToString('MM-dd HH:mm') + " | " + $_.Id + " | " + $_.ProviderName + " | " + $m)
}

Write-Output ("`nNow: " + (Get-Date).ToString('yyyy-MM-dd HH:mm:ss zzz'))
