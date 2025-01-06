#!/bin/sh
set -e

cd aoc-tools
tar -xvf aoc-tools-*-x86_64-unknown-linux-musl.tar.gz
mv aoc-tools /usr/local/bin/
cd ../
aoc-tools --version

cd repo

# This script can pretty much do whatever, but the most basic thing would be
# ensuring the project's dependencies are installable and that the tests and
# benchmarks run

poetry install

# Without filtering any of the marks, this should run the example and real input
# tests as well as running the benchmarks.
poetry run pytest tests -m "bench" --benchmark-group-by=name --benchmark-json=benchmarks.json

aoc-tools python-summary benchmarks.json -l bench-suffixes.json
