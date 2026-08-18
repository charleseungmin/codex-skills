param(
    [Parameter(Position = 0)]
    [ValidateSet("status", "start", "capture", "screenshot", "logs", "current", "launch", "tap", "swipe", "text", "key", "reverse")]
    [string]$Command = "status",

    [string]$Label = "session",
    [string]$Package,
    [string]$Name,
    [string]$Text,
    [int]$X,
    [int]$Y,
    [int]$X1,
    [int]$Y1,
    [int]$X2,
    [int]$Y2,
    [int]$Duration = 300,
    [int]$KeyCode,
    [int]$Port = 18089,
    [int]$LogLines = 500,
    [string]$OutRoot
)

$ErrorActionPreference = "Stop"

function Get-RepoRoot {
    $root = git rev-parse --show-toplevel 2>$null
    if ($LASTEXITCODE -eq 0 -and $root) {
        return $root.Trim()
    }
    return (Get-Location).Path
}

function Get-ArtifactRoot {
    if ($OutRoot) {
        return $OutRoot
    }
    return (Join-Path (Get-RepoRoot) "artifacts\adb")
}

function Get-SessionFile {
    return (Join-Path (Get-ArtifactRoot) ".current-session")
}

function New-SafeLabel([string]$value) {
    if ([string]::IsNullOrWhiteSpace($value)) {
        return "session"
    }
    return ($value -replace '[^a-zA-Z0-9가-힣._-]+', '-').Trim('-')
}

function New-Session([string]$sessionLabel) {
    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $safeLabel = New-SafeLabel $sessionLabel
    $root = Get-ArtifactRoot
    New-Item -ItemType Directory -Force -Path $root | Out-Null
    $dir = Join-Path $root "$timestamp-$safeLabel"
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    Set-Content -Path (Get-SessionFile) -Value $dir -Encoding UTF8
    return $dir
}

function Get-Session {
    $sessionFile = Get-SessionFile
    if (Test-Path $sessionFile) {
        $dir = (Get-Content $sessionFile -Raw).Trim()
        if ($dir -and (Test-Path $dir)) {
            return $dir
        }
    }
    return New-Session $Label
}

function Get-NextIndex([string]$dir) {
    $actions = Join-Path $dir "actions.jsonl"
    if (!(Test-Path $actions)) {
        return 1
    }
    return ((Get-Content $actions | Measure-Object).Count + 1)
}

function Invoke-Adb {
    param([string[]]$AdbArgs)
    $output = & adb @AdbArgs 2>&1
    $code = $LASTEXITCODE
    [PSCustomObject]@{
        Code = $code
        Output = ($output -join [Environment]::NewLine)
    }
}

function Get-CurrentActivity {
    $result = Invoke-Adb @("shell", "dumpsys", "window")
    $lines = $result.Output -split "`r?`n"
    $focus = $lines | Where-Object { $_ -match "mCurrentFocus|mFocusedApp" }
    return ($focus -join [Environment]::NewLine).Trim()
}

function Save-Logcat {
    param(
        [string]$Path,
        [int]$Lines = 500
    )
    $result = Invoke-Adb @("logcat", "-d", "-t", "$Lines")
    Set-Content -Path $Path -Value $result.Output -Encoding UTF8
}

function Save-Screenshot {
    param([string]$Path)
    $remote = "/sdcard/codex_adb_screen.png"
    $capture = Invoke-Adb @("shell", "screencap", "-p", $remote)
    if ($capture.Code -ne 0) {
        throw $capture.Output
    }
    $pull = Invoke-Adb @("pull", $remote, $Path)
    if ($pull.Code -ne 0) {
        throw $pull.Output
    }
}

function Write-Action {
    param(
        [string]$Dir,
        [string]$Action,
        [hashtable]$Data,
        [string]$CommandLine,
        [string]$Screenshot,
        [string]$Log,
        [string]$CurrentActivity
    )
    $entry = [ordered]@{
        time = (Get-Date).ToString("o")
        action = $Action
        command = $CommandLine
        screenshot = if ($Screenshot) { Split-Path $Screenshot -Leaf } else { $null }
        log = if ($Log) { Split-Path $Log -Leaf } else { $null }
        currentActivity = $CurrentActivity
        data = $Data
    }
    ($entry | ConvertTo-Json -Compress -Depth 8) | Add-Content -Path (Join-Path $Dir "actions.jsonl") -Encoding UTF8
}

function Capture-State {
    param(
        [string]$Action,
        [hashtable]$Data = @{},
        [string]$CommandLine = ""
    )
    $dir = Get-Session
    $index = Get-NextIndex $dir
    $safeAction = New-SafeLabel $Action
    if ($Name) {
        $safeAction = New-SafeLabel $Name
    }
    $prefix = "{0:D3}_{1}" -f $index, $safeAction
    $screen = Join-Path $dir "$prefix.png"
    $log = Join-Path $dir "$prefix.logcat.txt"
    $activity = Get-CurrentActivity
    Save-Screenshot $screen
    Save-Logcat -Path $log -Lines $LogLines
    Write-Action -Dir $dir -Action $Action -Data $Data -CommandLine $CommandLine -Screenshot $screen -Log $log -CurrentActivity $activity
    [PSCustomObject]@{
        session = $dir
        screenshot = $screen
        log = $log
        currentActivity = $activity
    }
}

function Assert-Device {
    $result = Invoke-Adb @("devices")
    if ($result.Code -ne 0) {
        throw $result.Output
    }
    $deviceLines = $result.Output -split "`r?`n" | Where-Object { $_ -match "`tdevice$" }
    if (-not $deviceLines) {
        throw "No adb device is connected. Output:`n$($result.Output)"
    }
}

Assert-Device

switch ($Command) {
    "status" {
        $devices = Invoke-Adb @("devices")
        $current = Get-CurrentActivity
        Write-Output $devices.Output
        Write-Output ""
        Write-Output $current
    }
    "start" {
        $dir = New-Session $Label
        Capture-State -Action "start" -Data @{ label = $Label } -CommandLine "start"
    }
    { $_ -in @("capture", "screenshot") } {
        Capture-State -Action "capture" -Data @{} -CommandLine "capture"
    }
    "logs" {
        $dir = Get-Session
        $index = Get-NextIndex $dir
        $log = Join-Path $dir ("{0:D3}_manual.logcat.txt" -f $index)
        Save-Logcat -Path $log -Lines $LogLines
        Write-Action -Dir $dir -Action "logs" -Data @{ lines = $LogLines } -CommandLine "logs" -Screenshot $null -Log $log -CurrentActivity (Get-CurrentActivity)
        Write-Output $log
    }
    "current" {
        Get-CurrentActivity
    }
    "launch" {
        if (-not $Package) {
            throw "-Package is required for launch."
        }
        $result = Invoke-Adb @("shell", "monkey", "-p", $Package, "-c", "android.intent.category.LAUNCHER", "1")
        Start-Sleep -Milliseconds 900
        Capture-State -Action "launch" -Data @{ package = $Package; output = $result.Output } -CommandLine "launch -Package $Package"
    }
    "tap" {
        $result = Invoke-Adb @("shell", "input", "tap", "$X", "$Y")
        Start-Sleep -Milliseconds 450
        Capture-State -Action "tap" -Data @{ x = $X; y = $Y; output = $result.Output } -CommandLine "tap -X $X -Y $Y"
    }
    "swipe" {
        $result = Invoke-Adb @("shell", "input", "swipe", "$X1", "$Y1", "$X2", "$Y2", "$Duration")
        Start-Sleep -Milliseconds 650
        Capture-State -Action "swipe" -Data @{ x1 = $X1; y1 = $Y1; x2 = $X2; y2 = $Y2; duration = $Duration; output = $result.Output } -CommandLine "swipe -X1 $X1 -Y1 $Y1 -X2 $X2 -Y2 $Y2 -Duration $Duration"
    }
    "text" {
        if ($null -eq $Text) {
            throw "-Text is required for text."
        }
        $escaped = $Text.Replace(" ", "%s")
        $result = Invoke-Adb @("shell", "input", "text", $escaped)
        Start-Sleep -Milliseconds 450
        Capture-State -Action "text" -Data @{ text = $Text; output = $result.Output } -CommandLine "text -Text <redacted>"
    }
    "key" {
        $result = Invoke-Adb @("shell", "input", "keyevent", "$KeyCode")
        Start-Sleep -Milliseconds 450
        Capture-State -Action "key" -Data @{ keyCode = $KeyCode; output = $result.Output } -CommandLine "key -KeyCode $KeyCode"
    }
    "reverse" {
        $result = Invoke-Adb @("reverse", "tcp:$Port", "tcp:$Port")
        $list = Invoke-Adb @("reverse", "--list")
        Capture-State -Action "reverse" -Data @{ port = $Port; output = $result.Output; reverseList = $list.Output } -CommandLine "reverse -Port $Port"
    }
}
