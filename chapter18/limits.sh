#!/bin/bash
# Try settings until the chapter 18 simulator errors.
set -u
cd "$(dirname "$0")/../vm-paging"
PY="python3 paging-linear-translate.py"

run() {
  echo
  echo "===== $* ====="
  $PY "$@" 2>&1 | head -20
}

echo "normal case"
run -P 4k -a 16k -p 64k -n 0

echo "address space bigger than physical memory"
run -P 4k -a 64k -p 16k -n 0

echo "address space equal to physical memory"
run -P 4k -a 16k -p 16k -n 0

echo "page bigger than the address space"
run -P 8k -a 4k -p 64k -n 0

echo "address space not a multiple of the page"
run -P 4k -a 6k -p 64k -n 0

echo "physical memory not a multiple of the page"
run -P 4k -a 16k -p 17k -n 0

echo "address space not a power of two"
run -P 4k -a 12k -p 64k -n 0

echo "page size 3k (not a power of two)"
run -P 3k -a 32k -p 64k -n 0

echo "physical memory size 0"
run -P 4k -a 16k -p 0 -n 0

echo "sizes of 1g (sim cap)"
run -P 4k -a 1g -p 2g -n 0

echo "tiny sizes that still work"
run -P 16 -a 64 -p 256 -n 1 -v -c
