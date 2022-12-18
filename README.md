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

In this particular example, the theorem-proving backend of `anthem` (`vampire`) is unable to verify the equivalence of primes_int.2.lp with the resulting primes_int-final.spec within the default time limit (5 minutes).
The proof search can be accelerated by providing helper lemmas (primes.help.spec):

```sh
$ lemma: forall X (prime(X) <- exists N1 (exists N2, N3 (N2 = a and N3 = b and N2 <= N1 and N1 <= N3) and not composite_1(N1) and X = N1)).
$lemma: forall X (prime(X) -> exists N1 (exists N2, N3 (N2 = a and N3 = b and N2 <= N1 and N1 <= N3) and not composite_1(N1) and X = N1)).
$lemma: forall X, N1, N2 ( (N1 > 1 and N2 > 1 and X = N1 * N2) -> (N1 <= X and N2 <= X) ).
```

Execute `anthem-p2p` with helper lemmas:

```sh
$ python3 anthem-p2p.py primes_int.1.lp primes_int.2.lp primes_int.ug primes.help.spec
```

Currently `anthem-p2p` comes with an executable version of `anthem` and `vampire` included within the repository.

## Contributors

* Zach Hansen
