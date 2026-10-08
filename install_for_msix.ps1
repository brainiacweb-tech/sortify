# Script to stage SORTIFY into Program Files and Start Menu for MSIX Packaging Tool capture

$targetDir = "C:\Program Files\SORTIFY"
$exeSource = Join-Path $PSScriptRoot "dist\SORTIFY.exe"
$exeTarget = Join-Path $targetDir "SORTIFY.exe"

Write-Host "Creating installation directory at: $targetDir"
New-Item -ItemType Directory -Force -Path $targetDir | Out-Null

Write-Host "Copying binary to installation directory..."
Copy-Item -Path $exeSource -Destination $exeTarget -Force

Write-Host "Creating Start Menu shortcut..."
$startMenuDir = "C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
$shortcutPath = Join-Path $startMenuDir "SORTIFY.lnk"
$wsh = New-Object -ComObject WScript.Shell
$shortcut = $wsh.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $exeTarget
$shortcut.WorkingDirectory = $targetDir
$shortcut.Description = "SORTIFY - Smart File Organizer"
$shortcut.IconLocation = "$exeTarget,0"
$shortcut.Save()

Write-Host "Installation completed successfully! MSIX Packaging Tool will now detect SORTIFY.exe automatically."
