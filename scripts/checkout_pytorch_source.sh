#!/usr/bin/env bash
set -uo pipefail

script_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
learning_root=$(cd -- "${script_dir}/.." && pwd)
pin_file="${learning_root}/config/PYTORCH_SOURCE_PIN"
source_parent="${learning_root}/sources"
source_root="${source_parent}/pytorch"

if [[ ! -f "${pin_file}" ]]; then
  printf 'ERROR: source pin is missing: %s\n' "${pin_file}" >&2
  exit 1
fi
read -r expected_tag expected_commit extra < "${pin_file}" || true
if [[ -n "${extra:-}" || ! "${expected_tag:-}" =~ ^v[0-9] || ! "${expected_commit:-}" =~ ^[0-9a-f]{40}$ ]]; then
  printf 'ERROR: invalid source pin; expected <tag> <40-character-commit>.\n' >&2
  exit 1
fi
if [[ -e "${source_root}" ]]; then
  printf 'ERROR: target already exists; refusing to overwrite: %s\n' "${source_root}" >&2
  printf 'Run scripts/check_source_checkout.sh to inspect it.\n' >&2
  exit 2
fi

mkdir -p -- "${source_parent}"
printf 'Cloning PyTorch %s with full history and recursive submodules into %s\n' "${expected_tag}" "${source_root}"
git clone --branch "${expected_tag}" --recursive https://github.com/pytorch/pytorch.git "${source_root}" || exit 3

actual_commit=$(git -C "${source_root}" rev-parse HEAD) || exit 4
if [[ "${actual_commit}" != "${expected_commit}" ]]; then
  printf 'ERROR: cloned tag resolved to %s, expected %s. Leaving checkout for inspection.\n' \
    "${actual_commit}" "${expected_commit}" >&2
  exit 5
fi

bash "${learning_root}/scripts/check_source_checkout.sh"
