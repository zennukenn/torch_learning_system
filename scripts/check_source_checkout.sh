#!/usr/bin/env bash
set -u

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
learning_root=$(cd -- "${script_dir}/.." && pwd)
source_root="${PYTORCH_SOURCE_ROOT:-${learning_root}/sources/pytorch}"

printf 'Learning system root: %s\n' "${learning_root}"
printf 'Learning system revision: '
git -C "${learning_root}" rev-parse HEAD || exit 1
printf 'PyTorch source root: %s\n' "${source_root}"

if [[ ! -d "${source_root}/.git" ]]; then
  printf 'ERROR: PyTorch Git checkout is missing.\n' >&2
  exit 2
fi

for required_path in torch aten c10; do
  if [[ ! -e "${source_root}/${required_path}" ]]; then
    printf 'ERROR: required source path is missing: %s\n' "${required_path}" >&2
    exit 3
  fi
done

printf 'PyTorch revision: '
git -C "${source_root}" rev-parse HEAD || exit 4
printf 'Exact tag: '
if ! git -C "${source_root}" describe --tags --exact-match 2>/dev/null; then
  printf '(not exactly tagged)\n'
fi
printf 'PyTorch worktree:\n'
git -C "${source_root}" status --short --branch || exit 5

submodule_status=$(git -C "${source_root}" submodule status --recursive) || exit 6
printf 'Recursive submodules: '
if [[ -z "${submodule_status}" ]]; then
  printf 'none declared\n'
elif printf '%s\n' "${submodule_status}" | grep -Eq '^[-+U]'; then
  printf 'INCOMPLETE OR MISMATCHED\n' >&2
  printf '%s\n' "${submodule_status}"
  exit 7
else
  submodule_count=$(printf '%s\n' "${submodule_status}" | wc -l)
  printf 'ok (%s entries)\n' "${submodule_count}"
fi
