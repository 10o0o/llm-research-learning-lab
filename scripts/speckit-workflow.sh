#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
helper="$HOME/.local/bin/speckit-codex"
if [[ ! -x "$helper" ]]; then
  printf '%s\n' 'speckit-codex가 없습니다. dotfiles의 WSL 프로필을 적용하세요.' >&2
  exit 2
fi
cd -- "$project_root"
exec "$helper" "$@"
