# 2024 Advent of Code Solutions

These are roughly a port of my [rust
solutions](https://github.com/mattcl/aoc2024), with a similar
performance-oriented goal.


## Total runtime ~793.1 ms

```
❯ aoc-tools python-summary benchmarks.json -l bench-suffixes.json
+------------------------------------------------------+
| Problem                     Time (ms)   % Total Time |
+======================================================+
| 01 historian hysteria         0.77458          0.098 |
| 02 red nosed reports          3.09283          0.390 |
| 03 mull it over               1.30733          0.165 |
| 04 ceres search               6.11644          0.771 |
| 05 print queue                1.73810          0.219 |
| 06 guard gallivant           23.64848          2.982 |
| 07 bridge repair             16.60854          2.094 |
| 08 resonant collinearity      0.63158          0.080 |
| 09 disk fragmenter           15.75009          1.986 |
| 10 hoof it                    2.48683          0.314 |
| 11 plutonium pebbles         64.04271          8.075 |
| 12 garden groups             20.48014          2.582 |
| 13 claw contraption           0.80211          0.101 |
| 14 restroom redoubt          30.33278          3.825 |
| 15 warehouse woes             9.46622          1.194 |
| 16 reindeer maze             29.53723          3.724 |
| 17 chronospatial computer     0.74833          0.094 |
| 18 ram run                   14.55448          1.835 |
| 19 linen layout              16.88883          2.130 |
| 20 race condition            41.49726          5.233 |
| 21 keypad conundrum           1.25048          0.158 |
| 22 monkey market            485.25099         61.188 |
| 23 lan party                  2.63399          0.332 |
| 24 crossed wires              0.50582          0.064 |
| 25 code chronicle             2.90690          0.367 |
| Total                       793.05306        100.000 |
+------------------------------------------------------+
```

This package distributes a library named
`mattcl-aoc2024` that
exposes a module named `aoc` and an executable named
`mattcl-aoc` that, given a day and input, will
provide the solution.

```
mattcl-aoc 3 my_input.txt
```


This project is designed to be compatible with a [comparative benchmarking
pipeline](https://github.com/mattcl/aoc-benchmarks/blob/master/SPECIFICATION.md),
which explains some of the layout and design decisions.

For comparative benchmarking this also provides an executable named
`mattcl-aoc-bench` that does not rely on `click` but is less
robust (not relying on click cuts down startup time).


## Developing

### Prerequisites

1. python >=3.10, <3.13 (3.12 preferred) (recommended install via
   [pyenv](https://github.com/pyenv/pyenv) or equivalent)
2. [poetry](https://python-poetry.org/docs/#installing-with-pipx) >=1.5.1 or
   compatible (recommended install via [pipx](https://pypa.github.io/pipx/))
3. _Optionally_ [just](https://github.com/casey/just#packages) for convenience commands
4. _Optionally_ docker


This project is managed by `poetry`, so the environment is set up by running
`poetry install`, and packages are managed via `poetry update` and `poetry
lock`. The `poetry.lock` _should_ be checked in, as this repo distributes an
executable.

You can switch into the context of the created virtualenv by running `poetry
shell`.


### Naming conventions

Solutions for a given day should be exposed by a module with name `day<formatted
number>`, where `<formatted number>` is a zero-padded (width 2) integer
corresponding to the day (e.g. `day05` or `day15`). The zero-padding is mainly
to maintain a sorted ordering visually. These modules should exist directly
under the top-level `aoc` directory (the project module).

Inputs should follow the same naming convention, with inputs located
under the top-level `inputs` directory with the names `day01.txt`,
`day01_example.txt`, `day02.txt`, etc.

Tests have no naming restrictions, and are located under the top-level `tests`
directory.


### Starting work on a new day's problem

You can either copy the templates and create the input placeholders by yourself,
or you can run one of the following. By default, the template that generated
this project also generated the day 1 placeholder module/tests/inputs.

```
# without just
./scripts/new.sh DAY  # where DAY is 1-25

# with just
just new DAY
```


### Running a solution for a given day

```
# with plain poetry
poetry run mattcl-aoc DAY PATH_TO_INPUT

# with poetry shell activated (or if you just installed the distribution)
mattcl-aoc DAY PATH_TO_INPUT

# example
mattcl-aoc 2 inputs/day02.txt
```

For information on how the CLI works see [aoc/cli.py](aoc/cli.py).


### Running tests

Test cases are marked with `@pytest.mark.example`, `@pytest.mark.real`, and
`@pytest.mark.bench` to indicate if they are tests against example input, real
inputs, or benchmarks, respectively. Tests can be selected or filtered using the
normal `pytest`
[arguments](https://docs.pytest.org/en/latest/example/markers.html#mark-run).

The reason tests are marked differently is to allow for faster test runs while
developing by excluding known-slow tests like tests against real inputs and
benchmarks.

Filesystem watching support is provided with
[`pytest-watcher`](https://github.com/olzhasar/pytest-watcher).

Benchmark support is provided with
[`pytest-benchmark`](https://pypi.org/project/pytest-benchmark/).


### Running all tests and benchmarks

```
# with plain poetry
poetry run pytest tests --benchmark-group-by=name

# with poetry shell activated
pytest tests --benchmark-group-by=name

# with just
just all
```


### Running just unit tests and tests against examples

```
# with plain poetry
poetry run pytest tests -m "not bench and not real"

# with poetry shell activated
pytest tests -m "not bench and not real"

# with just
just unit
```


### Running all tests except benchmarks

```
# with plain poetry
poetry run pytest tests -m "not bench"

# with poetry shell activated
pytest tests -m "not bench"

# with just
just test
```


### Running benchmarks

```
# with plain poetry
poetry run pytest tests -m "bench" --benchmark-group-by=name

# with poetry shell activated
pytest tests -m "bench" --benchmark-group-by=name

# with just
just bench
```


### Running tests in response to code changes

It's recommended not to run the testing loop with benchmarks and real-input
tests because of the potential slowness, but you do you.

```
# with plain poetry
poetry run ptw . -m "not bench and not real"

# with poetry shell activated
ptw . -m "not bench and not real"

# with just
just watch
