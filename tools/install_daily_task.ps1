$ErrorActionPreference = 'Stop'
$taskName = 'RSSYXY Daily Intelligence'
$projectDir = 'D:\RSS'
$logPath = Join-Path $projectDir 'output\daily-refresh.log'
$command = '"D:\RSS\daily-refresh.bat" >> "' + $logPath + '" 2>&1'
$action = New-ScheduledTaskAction -Execute 'cmd.exe' -Argument ('/d /c ' + $command) -WorkingDirectory $projectDir
$trigger = New-ScheduledTaskTrigger -Daily -At '06:30'
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun -MultipleInstances IgnoreNew -ExecutionTimeLimit (New-TimeSpan -Hours 2)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description 'Daily RSSYXY crawl, local LiteLLM Chinese briefing, and GitHub sync.' -Force | Out-Null
Write-Output "Created task: $taskName (daily 06:30, start when available)"
