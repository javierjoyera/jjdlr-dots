# jjdlr-dots

A minimal [Starship](https://starship.rs/guide/) prompt: only the input indicator,
without a username, hostname, directory, or extra modules. No shell framework.

## Install

Clone or download this repository, open its directory, then run:

| System | Command | Prerequisite | Shell configured |
| --- | --- | --- | --- |
| macOS | `sh install.sh` | [Homebrew](https://brew.sh), unless Starship is installed | Zsh |
| Linux | `sh install.sh` | `curl`, unless Starship is installed | Bash |
| Windows | `.\install.ps1` | [WinGet](https://aka.ms/getwinget), unless Starship is installed | The PowerShell edition running the script |

Open a **new terminal** afterward. On Windows, close and reopen the terminal
application so it receives the updated PATH. Windows PowerShell and PowerShell 7
have separate profiles: run the script in the one you use.

If Windows blocks a downloaded script, inspect it before using
`Unblock-File .\install.ps1`. This does not override execution policy; if policy
still prohibits scripts, follow your organization's policy rather than bypassing it.

## What changes

- `config/starship.toml` is copied to `$HOME/.config/starship.toml`.
  An existing `STARSHIP_CONFIG` environment variable selects that destination instead.
- An identical config is kept. A different one stops installation with
  `Existing Starship config differs; nothing changed.`
  Keep or back up your existing config yourself before choosing to replace it.
- The appropriate initialization line is appended to `.zshrc`, `.bashrc`, or
  PowerShell's `$PROFILE`; existing contents are not replaced. Zsh honors `ZDOTDIR`.
- Linux also adds `$HOME/.local/bin` to PATH in `.bashrc`. A login Bash session
  must source `.bashrc` from its login profile, as most distributions already do.
- Running the installer again does not duplicate its exact initialization lines.
  It does not remove or migrate other prompt customizations.

If Starship is missing, macOS uses `brew install starship`; Windows uses
`winget install --id Starship.Starship --exact --source winget`. Linux downloads
and executes the official HTTPS installer from `https://starship.rs/install.sh`,
installing into `$HOME/.local/bin` without sudo. These commands require network
access and trust the upstream distribution. Existing Starship installations are
not upgraded.

Missing prerequisites, incomplete checkouts, unsupported Unix systems, and
non-file profiles stop with an explanatory error. A failed Starship installation
stops before copying the config or editing the profile; the external installer
may still have made changes of its own.

## Keep it public-safe

Commit only the portable configuration and scripts. Do not copy your personal
shell profiles, credentials, machine names, or absolute local paths into this
repository. Home and profile paths are resolved on the machine running the script.

## Checks

Run `python3 -B tests/test_install.py`. Tests use temporary homes and fake package
managers, never install software or change your real shell profile. PowerShell
checks require `pwsh` and are skipped when it is unavailable. Simulated package
manager tests do not replace a native installation check on each target system.

## License

MIT — see [LICENSE](LICENSE).
