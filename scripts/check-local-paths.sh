#!/usr/bin/env bash

set -uo pipefail

# Keep detector fragments separate so this tracked implementation cannot match itself.
linux_root='/home/'
macos_root='/Users/'
windows_root='[A-Za-z]:[\\]Users[\\]'
# Account names use this conservative set; excluding regex metacharacters avoids
# treating archived detector examples as leaked paths.
user_segment='[A-Za-z0-9._-]+'
windows_user_segment='[A-Za-z0-9._-]+'

patterns=(
  "${linux_root}${user_segment}/"
  "${macos_root}${user_segment}/"
  "${windows_root}${windows_user_segment}[\\]"
)

if (($#)); then
  search=(grep -nIH -E)
else
  search=(git grep -nI -E)
fi

args=()
for pattern in "${patterns[@]}"; do
  args+=(-e "$pattern")
done

if (($#)); then
  args+=(-- "$@")
else
  args+=(-- .)
fi

set +e
"${search[@]}" "${args[@]}"
status=$?
set -e

case "$status" in
  0)
    printf '%s\n' 'Local user paths detected. Replace machine-specific roots with <workspace-root> or another neutral value.' >&2
    exit 1
    ;;
  1)
    printf '%s\n' 'No local user paths detected.'
    ;;
  *)
    printf 'Local path validation could not complete (scanner exit %s).\n' "$status" >&2
    exit "$status"
    ;;
esac
