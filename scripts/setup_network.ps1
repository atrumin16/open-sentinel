param (
    [string]$DomainLocal = "alertas.local",
    [string]$DomainTailscale = "",
    [int]$Port = 8888
)

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  OPENSENTINEL // CADDY & TAILSCALE SETUP" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

if ([string]::IsNullOrWhiteSpace($DomainTailscale)) {
    $DomainTailscale = Read-Host "Enter your Tailscale domain or custom domain (e.g. dash.yourdomain.com) [Press Enter to skip]"
}

# 1. Setup Caddy
$CaddyDir = "C:\Caddy"
Write-Host "[1/4] Checking Caddy installation..." -ForegroundColor Yellow
if (-Not (Test-Path "$CaddyDir\caddy.exe")) {
    if (-Not (Test-Path $CaddyDir)) {
        New-Item -ItemType Directory -Path $CaddyDir | Out-Null
    }
    Write-Host "Downloading Caddy to $CaddyDir..."
    try {
        Invoke-WebRequest -Uri "https://caddyserver.com/api/download?os=windows&arch=amd64" -OutFile "$CaddyDir\caddy.exe"
        Write-Host "[OK] Caddy downloaded successfully." -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Failed to download Caddy. Please check your internet connection." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "[OK] Caddy is already installed." -ForegroundColor Green
}

# 2. Generate Caddyfile
Write-Host "[2/4] Generating Caddyfile..." -ForegroundColor Yellow
$Domains = $DomainLocal
if (-Not [string]::IsNullOrWhiteSpace($DomainTailscale)) {
    $Domains += ", $DomainTailscale"
}

$CaddyfileContent = @"
$Domains {
    @allowed {
        remote_ip 100.64.0.0/10 127.0.0.0/8 ::1 192.168.0.0/16 10.0.0.0/8 172.16.0.0/12
    }
    handle @allowed {
        reverse_proxy 127.0.0.1:$Port
    }
    handle {
        respond `"Access Denied. Only Tailscale or LAN devices are allowed.`" 403
    }
}
"@
Set-Content -Path "$CaddyDir\Caddyfile" -Value $CaddyfileContent
Write-Host "[OK] Caddyfile configured for: $Domains" -ForegroundColor Green

# 3. Create Windows Startup Task for Caddy
Write-Host "[3/4] Configuring Caddy Startup task..." -ForegroundColor Yellow
$VbsContent = @"
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "cmd.exe /c cd ""$CaddyDir"" && caddy.exe run --config Caddyfile", 0, False
"@
Set-Content -Path "$CaddyDir\start_caddy.vbs" -Value $VbsContent

$StartupDir = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$ShortcutScript = @"
`$ws = New-Object -ComObject WScript.Shell
`$s = `$ws.CreateShortcut('$StartupDir\CaddyProxy.lnk')
`$s.TargetPath = 'wscript.exe'
`$s.Arguments = '""$CaddyDir\start_caddy.vbs""'
`$s.WorkingDirectory = '$CaddyDir'
`$s.Description = 'Caddy Reverse Proxy'
`$s.Save()
"@
Invoke-Expression $ShortcutScript
Write-Host "[OK] Startup task created." -ForegroundColor Green

# 4. Restart Caddy
Write-Host "[4/4] Restarting Caddy proxy..." -ForegroundColor Yellow
Stop-Process -Name "caddy" -Force -ErrorAction SilentlyContinue
Start-Process -FilePath "wscript.exe" -ArgumentList """$CaddyDir\start_caddy.vbs"""
Write-Host "[OK] Caddy is running in background." -ForegroundColor Green
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host " SETUP COMPLETE!" -ForegroundColor Green
Write-Host " Your OpenSentinel instance is now protected and accessible via:"
Write-Host " - $DomainLocal (Local DNS/Hosts)"
if (-Not [string]::IsNullOrWhiteSpace($DomainTailscale)) {
    Write-Host " - $DomainTailscale (Tailscale/Internet)"
}
Write-Host "==================================================" -ForegroundColor Cyan
