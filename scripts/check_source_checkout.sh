#!/usr/bin/env bash
set -uo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
learning_root=$(cd -- "${script_dir}/.." && pwd)
source_root="${PYTORCH_SOURCE_ROOT:-${learning_root}/sources/pytorch}"
pin_file="${learning_root}/config/PYTORCH_SOURCE_PIN"

if [[ ! -f "${pin_file}" ]]; then
  printf 'ERROR: source pin is missing: %s\n' "${pin_file}" >&2
  exit 1
fi

read -r expected_tag expected_commit extra < "${pin_file}" || true
if [[ -n "${extra:-}" || ! "${expected_tag:-}" =~ ^v[0-9] || ! "${expected_commit:-}" =~ ^[0-9a-f]{40}$ ]]; then
  printf 'ERROR: source pin must contain exactly: <tag> <40-character-commit>\n' >&2
  exit 1
fi

printf 'Learning system root: %s\n' "${learning_root}"
printf 'Learning system revision: '
git -C "${learning_root}" rev-parse HEAD || exit 2
printf 'PyTorch source root: %s\n' "${source_root}"
printf 'Expected source pin: %s %s\n' "${expected_tag}" "${expected_commit}"

if [[ ! -d "${source_root}" ]] || ! git -C "${source_root}" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf 'ERROR: PyTorch Git checkout is missing or invalid.\n' >&2
  exit 3
fi

for required_path in torch aten c10 torchgen; do
  if [[ ! -e "${source_root}/${required_path}" ]]; then
    printf 'ERROR: required source path is missing: %s\n' "${required_path}" >&2
    exit 4
  fi
done

actual_commit=$(git -C "${source_root}" rev-parse HEAD) || exit 5
printf 'PyTorch revision: %s\n' "${actual_commit}"
if [[ "${actual_commit}" == "${expected_commit}" ]]; then
  printf 'Pin relation: exact baseline\n'
elif git -C "${source_root}" merge-base --is-ancestor "${expected_commit}" "${actual_commit}"; then
  printf 'Pin relation: descendant learning revision\n'
else
  printf 'ERROR: checkout is neither the pinned baseline nor its descendant.\n' >&2
  exit 6
fi

if ! git -C "${source_root}" tag --points-at "${expected_commit}" | grep -Fxq -- "${expected_tag}"; then
  printf 'ERROR: expected tag is not attached to the pinned commit: %s\n' "${expected_tag}" >&2
  exit 7
fi
printf 'Baseline tag: %s\n' "${expected_tag}"

shallow=$(git -C "${source_root}" rev-parse --is-shallow-repository) || exit 8
printf 'Full history: '
if [[ "${shallow}" != "false" ]]; then
  printf 'NO (shallow checkout)\n' >&2
  exit 9
fi
printf 'yes\n'

printf 'Origin: '
git -C "${source_root}" remote get-url origin || exit 10
printf 'PyTorch worktree:\n'
git -C "${source_root}" status --short --branch || exit 11

submodule_status=$(git -C "${source_root}" submodule status --recursive) || exit 12
printf 'Recursive submodules: '
if [[ -z "${submodule_status}" ]]; then
  printf 'none declared\n'
elif printf '%s\n' "${submodule_status}" | grep -Eq '^[-+U]'; then
  printf 'INCOMPLETE OR MISMATCHED\n' >&2
  printf '%s\n' "${submodule_status}"
  exit 13
else
  submodule_count=$(printf '%s\n' "${submodule_status}" | wc -l)
  printf 'ok (%s entries)\n' "${submodule_count}"
fi
