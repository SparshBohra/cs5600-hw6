#!/bin/bash
# Run tlb with 1, 2, 4, ... 4096 pages.
# On Linux, taskset keeps the process on CPU 0 (one TLB).
set -e
cd "$(dirname "$0")"

if [ ! -x ./tlb ]; then
  echo "compile first: gcc -O0 -Wall tlb.c -o tlb"
  exit 1
fi

OUT="${1:-results/tlb_results.txt}"
mkdir -p "$(dirname "$OUT")"
TARGET=20000000

{
  echo "# host=$(hostname)"
  echo "# uname=$(uname -a)"
  echo "# pagesize=$(getconf PAGESIZE)"
  n=1
  while [ "$n" -le 4096 ]; do
    trials=$((TARGET / n))
    if [ "$trials" -lt 5000 ]; then
      trials=5000
    fi
    if command -v taskset >/dev/null 2>&1; then
      taskset -c 0 ./tlb "$n" "$trials"
    else
      ./tlb "$n" "$trials"
    fi
    n=$((n * 2))
  done
} | tee "$OUT"
