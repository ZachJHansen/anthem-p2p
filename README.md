# anthem-p2p

> Verify the equivalence of external behavior for two answer set programs

## Overview

`anthem-p2p` compares two ASP programs (written in the input language of [`clingo`](https://github.com/potassco/clingo)) and verifies that they are equivalent within the context of a "user guide." It accomplishes this by invoking the software verifcation tool [`anthem`](https://github.com/potassco/anthem). 

## Usage

First clone the repository and cd into the resulting directory.

To verify that two programs are equivalent under a user guide: 

```sh
$ python3 anthem-p2p <program file> <program file> <user guide file>
```

This will produce four files: two .lp files containing `anthem-p2p` compliant versions of the programs, a text file containing the completed definitions of predicates occurring in the first program, and a specification file against which the second program is verified. 

For example, consider an unsafe version of a prime number program:

```sh
$ composite(I*J) :- I > 1, J > 1.
$ prime(I) :- I = a..b, not composite(I).
$ \#show prime/1.
```

The braces notation is a Bash shorthand for

```sh
$ anthem verify-program examples/example-2.lp examples/example-2.spec examples/example-2.lemmas
```

By default, `anthem` performs Clark’s completion on the translated formulas, detects which variables are integer, and simplifies the output by applying several basic transformation rules.

These processing steps can be turned off with the options `--no-complete`, `--no-simplify`, and `--no-detect-integers`.

## Building

`anthem` is built with Rust’s `cargo` toolchain.
After [installing Rust](https://rustup.rs/), `anthem` can be built as follows:

```sh
$ git clone https://github.com/potassco/anthem.git
$ cd anthem
$ cargo build --release
```

The `anthem` binary will then be available in the `target/release/` directory.
Alternatively, `anthem` can be invoked using `cargo` as follows:

```sh
$ cargo run -- verify-program <program file> <specification file>...
```

## Contributors

* [Patrick Lühne](https://www.luehne.de)
