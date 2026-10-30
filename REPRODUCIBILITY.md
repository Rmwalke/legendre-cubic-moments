# Reproducing the retained computations

These instructions reproduce specific small algebra checks in the supplied
supplement. They do not constitute a full verification of the manuscript.
The mathematical source files, scripts, and retained reports have not been edited.

## Verify the repository in one command

Use Python 3.8 or later from the repository root:

```sh
python scripts/verify_repository.py
```

This standard-library command checks both SHA-256 manifests before running the
three small algebra scripts. It verifies all 87 results and compares each
generated JSON report with its retained counterpart. Temporary outputs are
created under `results/` and removed on completion. It returns a nonzero exit
status on failure and does not compile LaTeX or run historical experiments.

For file integrity alone, use:

```sh
python scripts/verify_repository.py --integrity-only
```

The dated audit results and remaining limits are in [VERIFICATION.md](VERIFICATION.md).

## Small exact local checks

Use Python 3.8 or later. The three scripts use only Python's standard library;
there is no `pip install` step. Run the following from the repository root.
If your system names Python 3 `python3` rather than `python`, substitute that name.

```sh
python local_checks/p2_complete/p2_completion_checks.py --output results/p2_completion_checks.json
python local_checks/p2_local/p2_exact_checks.py --output results/p2_exact_checks.json
python local_checks/p3_local/p3_exact_checks.py --output results/p3_exact_checks.json
```

Each script creates its output directory as needed. The explicit `--output`
arguments prevent overwriting the retained historical reports beside the scripts.
Inspect the generated JSON as well as the terminal output.

| Script | Retained check count | Success field | Scope |
| --- | ---: | --- | --- |
| `p2_completion_checks.py` | 20 | `all_passed` | Exact closure identities and finite representation matrices |
| `p2_exact_checks.py` | 41 | `all_checks_passed` | Exact chart identities, counts, and stated conditional determinant obstructions |
| `p3_exact_checks.py` | 26 | `all_checks_passed` | Exact identities and conditional Weil–Deligne matrix consequences |

The counts above describe the reports retained in the source package. A later
repository audit on 30 October 2026 reran the scripts and obtained byte-identical
reports; the original reports remain unchanged.
The reports include `scope`, `scope_limit`, or other explanations of the limits.
In particular, the p=3 matrix calculation assumes its proposed geometric
identification; the scripts do not prove nearby-cycle theorems or their hypotheses.

## Build the manuscript

Use a standard TeX Live or equivalent LaTeX installation with the packages named
in the source. From the repository root:

```sh
cd manuscript
pdflatex Walke_Legendre_Manuscript_2026-10-30.tex
pdflatex Walke_Legendre_Manuscript_2026-10-30.tex
pdflatex Walke_Legendre_Manuscript_2026-10-30.tex
```

Three passes stabilize contents and references. No shell escape is required.
The supplied PDF is in `paper/`; compiling does not verify the mathematics.
Different TeX installations can produce different PDF bytes and metadata.

## Earlier cubic certificate and numerical material

The unchanged archive under `historical/` contains the earlier bounded cubic
certificate, its separate implementation and retained logs, and historical
numerical experiments. Consult `historical/READ_FIRST.txt` before using it.
That archive concerns earlier stages; its old task lists and sign labels are
not the current manuscript status.

There is no instruction here to rerun large prime scans or numerical L-function
programs. Such a run should answer a specific mathematical question with defined
inputs, normalization, and validation criteria.

## File integrity

On a system with `sha256sum`, run from the repository root:

```sh
sha256sum -c SHA256SUMS.txt
sha256sum -c REPOSITORY_SHA256SUMS.txt
```

The first manifest is the original supplement manifest. The second covers this
prepared tree, excluding itself. It describes this snapshot; later intentional
edits require an updated manifest. Hash agreement checks byte identity only.
