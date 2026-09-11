$ErrorActionPreference = 'Stop'
$taskName = 'RSSYXY Daily Intelligence'
$projectDir = 'D:\RSS'
$action = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument '/d /c "D:\RSS\daily-refresh.bat"' -WorkingDirectory $projectDir

# 触发器：开机时 + 每日 06:30
$triggerBoot = New-ScheduledTaskTrigger -AtStartup
$triggerDaily = New-ScheduledTaskTrigger -Daily -At '06:30'

$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 3)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger @($triggerBoot, $triggerDaily) -Settings $settings -Principal $principal -Description 'RSSYXY: crawl, AI translate, enrich, deploy on boot + daily 06:30. Logs to output\daily-refresh.log internally.' -Force | Out-Null
Write-Output "Created task: $taskName (boot + daily 06:30, internal logging)"
