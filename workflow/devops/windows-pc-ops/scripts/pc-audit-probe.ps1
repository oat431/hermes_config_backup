[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$ErrorActionPreference = 'SilentlyContinue'

function Sec($t) { Write-Output ("`n" + ('=' * 20) + " " + $t + " " + ('=' * 20)) }

# ---------- A. SYSTEM ----------
Sec 'SYSTEM'
$os  = Get-CimInstance Win32_OperatingSystem
$cs  = Get-CimInstance Win32_ComputerSystem
$bios = Get-CimInstance Win32_BIOS
Write-Output ("ComputerName       : " + $env:COMPUTERNAME)
Write-Output ("Domain/Workgroup   : " + $cs.Domain)
Write-Output ("Manufacturer       : " + $cs.Manufacturer)
Write-Output ("Model              : " + $cs.Model)
Write-Output ("BIOS               : " + $bios.Manufacturer + " " + $bios.SMBIOSBIOSVersion)
Write-Output ("OS Caption         : " + $os.Caption)
Write-Output ("OS Version         : " + $os.Version + " (build " + $os.BuildNumber + ") " + $os.OSArchitecture)
Write-Output ("OS InstallDate     : " + $os.InstallDate)
Write-Output ("LastBootUpTime     : " + $os.LastBootUpTime)
$up = (Get-Date) - $os.LastBootUpTime
Write-Output ("Uptime             : " + ("{0}d {1}h {2}m" -f $up.Days, $up.Hours, $up.Minutes))
$enc = Get-CimInstance Win32_SystemEnclosure
if ($enc) { Write-Output ("ChassisTypes       : " + ($enc.ChassisTypes -join ',')) }
$bat = Get-CimInstance Win32_Battery
if ($bat) { Write-Output ("Battery            : " + $bat.Name + " | charge " + $bat.EstimatedChargeRemaining + "%") }

# ---------- B. CPU ----------
Sec 'CPU'
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
Write-Output ("Name               : " + $cpu.Name.Trim())
Write-Output ("Cores / Threads    : " + $cpu.NumberOfCores + " / " + $cpu.NumberOfLogicalProcessors)
Write-Output ("MaxClockSpeed      : " + $cpu.MaxClockSpeed + " MHz")
$load = (Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
Write-Output ("LoadPercentage     : " + $load + " %")

# ---------- C. MEMORY ----------
Sec 'MEMORY'
$totalGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 1)
$freeGB  = [math]::Round($os.FreePhysicalMemory / 1MB, 1)
Write-Output ("Total / Free       : " + $totalGB + " GB total / " + $freeGB + " GB free")
$i = 0
foreach ($m in (Get-CimInstance Win32_PhysicalMemory)) {
  if ($m.Capacity) { $i++; Write-Output ("DIMM" + $i + "                : " + $m.Manufacturer + " " + [math]::Round($m.Capacity / 1GB, 0) + " GB @ " + $m.ConfiguredClockSpeed + " MHz (max " + $m.Speed + ")") }
}
foreach ($p in (Get-CimInstance Win32_PageFileUsage)) {
  Write-Output ("PageFile           : " + $p.Name + " | " + [math]::Round($p.AllocatedBaseSize / 1MB, 1) + " GB allocated")
}

# ---------- D. GPU ----------
Sec 'GPU'
Get-CimInstance Win32_VideoController | ForEach-Object {
  $res = ""
  if ($_.CurrentHorizontalResolution) { $res = " | " + $_.CurrentHorizontalResolution + "x" + $_.CurrentVerticalResolution + "@" + $_.CurrentRefreshRate + "Hz" }
  Write-Output ($_.Name + " | driver " + $_.DriverVersion + " | " + [math]::Round($_.AdapterRAM / 1GB, 1) + " GB VRAM" + $res)
}

# ---------- E. STORAGE ----------
Sec 'STORAGE-DISKS'
Get-PhysicalDisk | ForEach-Object {
  Write-Output ($_.FriendlyName + " | " + $_.MediaType + " | " + $_.BusType + " | " + [math]::Round($_.Size / 1GB, 0) + " GB | Health: " + $_.HealthStatus + " | " + $_.OperationalStatus)
}
Sec 'STORAGE-RELIABILITY'
Get-PhysicalDisk | Get-StorageReliabilityCounter | ForEach-Object {
  $p = $_ | Get-PhysicalDisk | Select-Object -First 1
  Write-Output ($p.FriendlyName + " | Temp: " + $_.Temperature + "C | Wear: " + $_.Wear + " | PowerOnHrs: " + $_.PowerOnHours)
}
Sec 'STORAGE-VOLUMES'
Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | ForEach-Object {
  $free = [math]::Round($_.FreeSpace / 1GB, 1); $sz = [math]::Round($_.Size / 1GB, 1)
  Write-Output ($_.DeviceID + " [" + $_.VolumeName + "] " + $_.FileSystem + " | " + $free + " GB free / " + $sz + " GB | " + [math]::Round(($free / $sz) * 100, 0) + "% free")
}
Sec 'TEMP-SIZES'
foreach ($p in @($env:TEMP, 'C:\Windows\Temp')) {
  $s = (Get-ChildItem $p -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object Length -Sum).Sum
  Write-Output ($p + " = " + [math]::Round($s / 1MB, 0) + " MB")
}

# ---------- F. NETWORK ----------
Sec 'NETWORK'
Get-NetIPConfiguration -ErrorAction SilentlyContinue | Where-Object { $_.IPv4DefaultGateway } | ForEach-Object {
  Write-Output ("Adapter : " + $_.InterfaceAlias)
  Write-Output ("  IPv4  : " + ($_.IPv4Address.IPAddress -join ', '))
  Write-Output ("  GW    : " + $_.IPv4DefaultGateway.NextHop)
  Write-Output ("  DNS   : " + (($_.DNSServer | Where-Object { $_.AddressFamily -eq 2 } | ForEach-Object { $_.ServerAddresses }) -join ', '))
}
Get-NetAdapter -Physical | ForEach-Object { Write-Output ("NIC " + $_.Name + " | " + $_.Status + " | " + $_.LinkSpeed + " | " + $_.InterfaceDescription) }
Sec 'NETWORK-TESTS'
$gw = (Get-NetIPConfiguration -ErrorAction SilentlyContinue | Where-Object { $_.IPv4DefaultGateway } | Select-Object -First 1).IPv4DefaultGateway.NextHop
if ($gw) { Write-Output ("Ping gateway " + $gw + "        : " + (Test-Connection -ComputerName $gw -Count 2 -Quiet)) }
Write-Output ("Ping internet 1.1.1.1    : " + (Test-Connection -ComputerName 1.1.1.1 -Count 2 -Quiet))
Write-Output ("Ping homelab TS 100.73.143.25: " + (Test-Connection -ComputerName 100.73.143.25 -Count 2 -Quiet))
$tsPath = 'C:\Program Files\Tailscale\tailscale.exe'
if (Test-Path $tsPath) {
  $tsIP = (& $tsPath ip -4 2>$null)
  Write-Output ("Tailscale IP(s)      : " + ($tsIP -join ', '))
} else { Write-Output "Tailscale CLI        : not found at default path" }

# ---------- G. SECURITY ----------
Sec 'SECURITY-DEFENDER'
$mp = Get-MpComputerStatus
if ($mp) {
  Write-Output ("AntivirusEnabled          : " + $mp.AntivirusEnabled)
  Write-Output ("RealTimeProtectionEnabled : " + $mp.RealTimeProtectionEnabled)
  Write-Output ("AntivirusSignatureVersion : " + $mp.AntivirusSignatureVersion)
  Write-Output ("SignatureLastUpdated      : " + $mp.AntivirusSignatureLastUpdated)
  Write-Output ("QuickScanAge (days)       : " + $mp.QuickScanAge)
  Write-Output ("TamperProtection          : " + $mp.IsTamperProtected)
} else { Write-Output "Defender status: unavailable" }
Sec 'SECURITY-FIREWALL'
Get-NetFirewallProfile | ForEach-Object { Write-Output ($_.Name + " | Enabled: " + $_.Enabled + " | DefaultIn: " + $_.DefaultInboundAction + " | DefaultOut: " + $_.DefaultOutboundAction) }
Sec 'SECURITY-BITLOCKER'
try {
  Get-BitLockerVolume -ErrorAction Stop | ForEach-Object { Write-Output ($_.MountPoint + " | " + $_.ProtectionStatus + " | " + $_.EncryptionPercentage + "% | " + $_.VolumeStatus) }
} catch { Write-Output "BitLocker query failed (needs elevation?)" }
Sec 'SECURITY-UPDATES'
Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 6 | ForEach-Object { Write-Output ($_.HotFixID + " | " + $_.Description + " | " + $_.InstalledOn) }
Sec 'SECURITY-PENDING-REBOOT'
Write-Output ("CBS RebootPending    : " + (Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending'))
Write-Output ("WU RebootRequired    : " + (Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired'))
Sec 'SECURITY-UAC'
$uac = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System'
Write-Output ("EnableLUA             : " + $uac.EnableLUA + " | ConsentPromptBehaviorAdmin: " + $uac.ConsentPromptBehaviorAdmin)

# ---------- H. SOFTWARE ----------
Sec 'SOFTWARE-INSTALLED'
$regPaths = @('HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*', 'HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*', 'HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*')
$installed = Get-ItemProperty $regPaths -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName } | Select-Object DisplayName, DisplayVersion, Publisher | Sort-Object DisplayName -Unique
$installed | ForEach-Object { Write-Output ($_.DisplayName + " | " + $_.DisplayVersion + " | " + $_.Publisher) }
Sec 'SOFTWARE-CLI'
foreach ($c in @('git','node','npm','python','py','pipx','uv','docker','tailscale','gh','kubectl','java','go','rustc','code','winget','curl')) {
  $cmd = Get-Command $c -ErrorAction SilentlyContinue
  if ($cmd) {
    try { $v = (& $c --version 2>&1 | Select-Object -First 1); Write-Output ($c + " -> " + $v) }
    catch { Write-Output ($c + " -> " + $cmd.Source) }
  }
}

# ---------- I. SERVICES ----------
Sec 'SERVICES-KEY'
foreach ($n in @('com.docker.service','Tailscale','Obsidian','MongoDB','mongod','couchdb','ssh-agent','OpenSSH Authentication Agent','wuauserv','WinDefend','WSearch','Spooler')) {
  $s = Get-Service -Name $n -ErrorAction SilentlyContinue
  if ($s) { Write-Output ($s.Name + " | " + $s.Status + " | " + $s.StartType) }
}

# ---------- J. PERFORMANCE ----------
Sec 'PERFORMANCE-TOP-PROCESSES'
Get-Process | Sort-Object WorkingSet64 -Descending | Select-Object -First 12 | ForEach-Object { Write-Output ($_.ProcessName + " | " + [math]::Round($_.WorkingSet64 / 1MB, 0) + " MB working set") }
Sec 'PERFORMANCE-CPU-SAMPLE'
$c = Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 2 -ErrorAction SilentlyContinue
if ($c) { $c.CounterSamples | ForEach-Object { Write-Output ("CPU sample: " + [math]::Round($_.CookedValue, 1) + " %") } }

# ---------- K. EVENT LOG (last 7 days) ----------
Sec 'EVENTS-SYSTEM'
Get-WinEvent -FilterHashtable @{ LogName = 'System'; Level = 1, 2, 3; StartTime = (Get-Date).AddDays(-7) } -MaxEvents 25 -ErrorAction SilentlyContinue | ForEach-Object {
  $m = $_.Message; if ($m.Length -gt 150) { $m = $m.Substring(0, 150) }
  Write-Output ($_.TimeCreated.ToString('MM-dd HH:mm') + " | " + $_.LevelDisplayName + " | " + $_.Id + " | " + $_.ProviderName + " | " + $m)
}
Sec 'EVENTS-APPLICATION'
Get-WinEvent -FilterHashtable @{ LogName = 'Application'; Level = 2; StartTime = (Get-Date).AddDays(-7) } -MaxEvents 12 -ErrorAction SilentlyContinue | ForEach-Object {
  $m = $_.Message; if ($m.Length -gt 150) { $m = $m.Substring(0, 150) }
  Write-Output ($_.TimeCreated.ToString('MM-dd HH:mm') + " | " + $_.Id + " | " + $_.ProviderName + " | " + $m)
}

# ---------- L. MISC ----------
Sec 'MISC'
Write-Output ("Now                : " + (Get-Date).ToString('yyyy-MM-dd HH:mm:ss zzz'))
$tz = Get-TimeZone
Write-Output ("TimeZone           : " + $tz.Id + " (UTC" + $tz.BaseUtcOffset + ")")
Write-Output ("PowerPlan          : " + (powercfg /getactivescheme))
