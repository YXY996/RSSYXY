$ErrorActionPreference = 'Stop'
$taskName = 'RSSYXY Daily Intelligence'
$projectDir = 'D:\RSS'
$logPath = Join-Path $projectDir 'output\daily-refresh.log'
$command = '"D:\RSS\daily-refresh.bat" >> "' + $logPath + '" 2>&1'
$action = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument ('/d /c ' + $command) -WorkingDirectory $projectDir

# 触发器：开机时 + 每日 06:30
$triggerBoot = New-ScheduledTaskTrigger -AtStartup
$triggerDaily = New-ScheduledTaskTrigger -Daily -At '06:30'

$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 2)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger @($triggerBoot, $triggerDaily) -Settings $settings -Principal $principal -Description 'RSSYXY: crawl, AI translate, enrich, deploy on boot + daily 06:30.' -Force | Out-Null
Write-Output "Created task: $taskName (boot + daily 06:30)"
