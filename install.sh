#!/bin/sh
# Run with sh install.sh; no shell framework or dotfile manager is required.
set -eu

fail() { printf '%s\n' "$1" >&2; exit 1; }
root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
source_config="$root/config/starship.toml"
config=${STARSHIP_CONFIG:-"$HOME/.config/starship.toml"}

case "$(uname -s)" in
    Darwin) shell=zsh; profile="${ZDOTDIR:-$HOME}/.zshrc" ;;
    Linux) shell=bash; profile="$HOME/.bashrc" ;;
    *) fail "Supported systems: macOS (Zsh) and Linux (Bash)." ;;
esac

[ -f "$source_config" ] || fail "Missing config/starship.toml; run from a complete checkout."
if [ -e "$config" ] || [ -L "$config" ]; then
    cmp -s "$source_config" "$config" ||
        fail "Existing Starship config differs; nothing changed."
fi
if [ -e "$profile" ] && [ ! -f "$profile" ]; then
    fail "Shell profile is not a regular file; nothing changed."
fi

if ! command -v starship >/dev/null 2>&1; then
    if [ "$shell" = zsh ]; then
        command -v brew >/dev/null 2>&1 || fail "Install Homebrew first: https://brew.sh"
        brew install starship || fail "Starship installation failed."
    else
        command -v curl >/dev/null 2>&1 || fail "Install curl first using your system package manager."
        installer=$(mktemp)
        trap 'rm -f "$installer"' EXIT
        curl --proto '=https' --tlsv1.2 -fsSL https://starship.rs/install.sh --output "$installer" ||
            fail "Could not download the official Starship installer."
        mkdir -p "$HOME/.local/bin"
        sh "$installer" --yes --bin-dir "$HOME/.local/bin" ||
            fail "Starship installation failed."
    fi
fi

mkdir -p "$(dirname -- "$config")" "$(dirname -- "$profile")"
if [ ! -e "$config" ]; then
    cp "$source_config" "$config"
fi
append_once() {
    if [ ! -f "$profile" ] || ! grep -Fqx "$1" "$profile"; then
        printf '\n%s\n' "$1" >> "$profile"
    fi
}
if [ "$shell" = bash ]; then
    append_once 'export PATH="$HOME/.local/bin:$PATH"'
fi
append_once "eval \"\$(starship init $shell)\""
printf '%s\n' "Starship configured. Open a new terminal."
