# jjdlr-dots

A minimal [Starship](https://starship.rs/guide/) prompt: repository-relative
path, Git branch, working-tree status, and the input indicator. No username,
hostname, shell framework, or language versions.

```text
jjdlr-dots ❯
jjdlr-dots/config ❯
jjdlr-dots/src/components on main ❯
notes on fix/login [!] ❯
```

| Element | Example | Color (Catppuccin Mocha) |
| --- | --- | --- |
| Path from the Git root | `jjdlr-dots/config` | bold blue `#89b4fa` |
| Branch, only inside a repo | `on main` | italic mauve `#cba6f7` |
| Commit, only detached | `at 3c7bb4d` | bold teal `#94e2d5` |
| Working tree | `[!]` modified, `[+]` staged, `[?]` untracked, `[✘]` deleted, `[⇡]` ahead | bold yellow `#f9e2af` |
| Input indicator | `❯` | green on success, red on failure |

Outside a repository the path shows the last components only, for example
`notes/drafts`, and `~` at your home directory.

**Limitations:** the path is capped at three components, so deeper inside a
repository the repository name scrolls out (`src/components/deep`). Branch names
are trimmed at 24 characters with `…`. Raise `truncation_length` in
`config/starship.toml` if you need more depth. Colors use 24-bit truecolor, which
modern terminals support; a 24-bit-incapable terminal falls back to approximations.
## Install

Clone or download this repository, open its directory, then run:

| System | Command | Prerequisite | Shell configured |
| --- | --- | --- | --- |
| macOS | `sh install.sh` | [Homebrew](https://brew.sh), unless Starship is installed | Zsh |
| Linux | `sh install.sh` | `curl`, unless Starship is installed | Bash |
| Windows | `.\install.ps1` | [WinGet](https://aka.ms/getwinget), unless Starship is installed | The PowerShell edition running the script |

To apply a newer repository config, run `sh install.sh --update` on macOS/Linux
or `.\install.ps1 -Update` on Windows. A differing installed config is backed up
as `<config>.bak-<UTC timestamp>` (for example, `starship.toml.bak-20260102T030405Z`)
before replacement. Identical configs are left alone, even with the flag.
Without the flag, a differing config safely stops installation without changes.

Open a **new terminal** afterward. On Windows, close and reopen the terminal
application so it receives the updated PATH. Windows PowerShell and PowerShell 7
have separate profiles: run the script in the one you use.

If Windows blocks a downloaded script, inspect it before using
`Unblock-File .\install.ps1`. This does not override execution policy; if policy
still prohibits scripts, follow your organization's policy rather than bypassing it.

## Preview an update

From the repository directory, in Zsh or Bash:

```sh
export STARSHIP_CONFIG="$PWD/config/starship.toml"
```

The next prompt uses the repository config for this shell session without overwriting
an installed file. For a persistent update, open a new shell without this override
and run `sh install.sh --update` to back up and replace the installed config.

## What changes

- `config/starship.toml` is copied to `$HOME/.config/starship.toml`.
  An existing `STARSHIP_CONFIG` environment variable selects that destination instead.
- Identical configs are never rewritten or backed up. By default, a differing
  config stops installation without changes and suggests the update flag.
  `--update` (`-Update` in PowerShell) backs it up to
  `<config>.bak-yyyyMMddTHHmmssZ` in UTC before replacing it; a failed backup
  stops replacement. A new config needs no backup.
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
checks require `pwsh` and are skipped when it is unavailable. Prompt rendering
checks require `starship` and `git`; they render isolated paths and assert the
repository-relative path, branch, working-tree markers, branch truncation,
detached commit, indicator colors, and the Catppuccin palette. Simulated package
manager tests do not replace a native installation check on each target system.

## License

MIT — see [LICENSE](LICENSE).
