# anthem-p2p

> Verify the equivalence of external behavior for two answer set programs

## Overview

`anthem-p2p` compares two ASP programs (written in the input language of [`clingo`](https://github.com/potassco/clingo)) and verifies that they are equivalent within the context of a "user guide." It accomplishes this by invoking the software verifcation tool [`anthem`](https://github.com/potassco/anthem). See this [`manuscript`](http://www.cs.utexas.edu/users/vl/papers/refactoring6.pdf) for details on the inner workings. You can also experiment in your browser at this link (w.i.p.).


## Building

```sh
$ git clone https://github.dev/ZachJHansen/anthem-p2p.git
```

`anthem-p2p` cannot be executed without `anthem`, which is built with Rust’s `cargo` toolchain.
After [installing Rust](https://rustup.rs/), build the following `anthem` fork and transfer the executable to your anthem-p2p directory:

```sh
$ git clone https://github.com/jorgefandinno/anthem.git
$ cd anthem
$ cargo +nightly build --release
$ cp target/release/anthem <path to anthem-p2p/>
$ cd <path to anthem-p2p/>
```
Note that you will also need a working installation of `vampire.`
Installation instructions can be found [here](https://vprover.github.io/).
Add the Vampire binary to your path:
```sh
mv vampire ${HOME}/bin/
chmod 755 ${HOME}/bin/vampire
touch ${HOME}/.bashrc
export PATH="${HOME}/bin:${PATH}"
```
Then restart your shell.

## Usage

To verify that two programs are equivalent under a user guide: 

```sh
$ python3 anthem-p2p <program file> <program file> <user guide file>
```

This will produce three files: two .lp files containing `anthem-p2p` compliant versions of the logic programs, and a specification file against which the second program is verified. 

For example, consider an unsafe version of a prime number program (primes_int.1.lp):

```sh
$ composite(I*J) :- I > 1, J > 1.
$ prime(I) :- I = a..b, not composite(I).
$ #show prime/1.
```

We can refactor this into a safe program whose behavior is identical to the original program (under certain assumptions) if we restrict our attention to the extent of the prime/1 predicate (primes_int.2.lp):

```sh
$ composite(I*J) :- I = 2..b, J = 2..b.
$ prime(I) :- I = a..b, not composite(I).
$ #show prime/1.
```

We formalize our assumptions about valid inputs and usage of the program with a user guide (primes_int.ug):

```sh
$ input: a -> integer, b -> integer.
$ assume: a > 1 and b >= a.
$ output: prime/1.
```

Run the preceding example as follows:

```sh
$ python3 anthem-p2p.py primes_int.1.lp primes_int.2.lp primes_int.ug
```

In this particular example, the theorem-proving backend of `anthem` ([`vampire`](https://vprover.github.io/)) is unable to verify the equivalence of primes_int.2.lp with the resulting primes_int-final.spec within the default time limit (5 minutes).
The proof search can be accelerated by providing helper lemmas (primes.help.spec):

```sh
$ lemma: forall X (prime(X) <- exists N1 (exists N2, N3 (N2 = a and N3 = b and N2 <= N1 and N1 <= N3) and not composite_1(N1) and X = N1)).
$ lemma: forall X (prime(X) -> exists N1 (exists N2, N3 (N2 = a and N3 = b and N2 <= N1 and N1 <= N3) and not composite_1(N1) and X = N1)).
$ lemma: forall X, N1, N2 ( (N1 > 1 and N2 > 1 and X = N1 * N2) -> (N1 <= X and N2 <= X) ).
```

Execute `anthem-p2p` with helper lemmas and a specified timeout in seconds for Vampire:

```sh
$ python3 anthem-p2p.py primes_int.1.lp primes_int.2.lp primes_int.ug --lemmas primes.help.spec --time-limit 600
```

## Contributors

* Zach Hansen
