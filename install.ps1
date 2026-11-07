# Run from the PowerShell edition you use; its $PROFILE is configured.
$ErrorActionPreference = 'Stop'

try {
    $sourceConfig = Join-Path $PSScriptRoot 'config/starship.toml'
    $config = if ($env:STARSHIP_CONFIG) { $env:STARSHIP_CONFIG } else {
        Join-Path $HOME '.config/starship.toml'
    }
    $init = 'Invoke-Expression (&starship init powershell)'

    if (-not (Test-Path -LiteralPath $sourceConfig -PathType Leaf)) {
        throw 'Missing config/starship.toml; run from a complete checkout.'
    }
    if (Test-Path -LiteralPath $config) {
        if (-not (Test-Path -LiteralPath $config -PathType Leaf) -or
            (Get-FileHash -LiteralPath $config).Hash -ne
            (Get-FileHash -LiteralPath $sourceConfig).Hash) {
            throw 'Existing Starship config differs; nothing changed.'
        }
    }
    if ((Test-Path -LiteralPath $PROFILE) -and
        -not (Test-Path -LiteralPath $PROFILE -PathType Leaf)) {
        throw 'Shell profile is not a regular file; nothing changed.'
    }

    if (-not (Get-Command starship -ErrorAction SilentlyContinue)) {
        if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
            throw 'Install WinGet (App Installer) first: https://aka.ms/getwinget'
        }
        winget install --id Starship.Starship --exact --source winget
        if ($LASTEXITCODE -ne 0) { throw 'Starship installation failed.' }
    }

    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $config) | Out-Null
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $PROFILE) | Out-Null
    if (-not (Test-Path -LiteralPath $config)) {
        Copy-Item -LiteralPath $sourceConfig -Destination $config
    }
    $lines = if (Test-Path -LiteralPath $PROFILE) {
        @(Get-Content -LiteralPath $PROFILE)
    } else { @() }
    if ($lines -notcontains $init) {
        Add-Content -LiteralPath $PROFILE -Value ("`n" + $init)
    }
    Write-Output 'Starship configured. Open a new terminal.'
} catch {
    [Console]::Error.WriteLine($_.Exception.Message)
    exit 1
}
