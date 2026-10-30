# Repository verification — 30 October 2026

The supplied GitHub-ready ZIP was compared with the public repository at commit
[`e48371c1`](https://github.com/Rmwalke/legendre-cubic-moments/commit/e48371c1602c9abc9b0c00603ad9df3415ea8688).
All 43 files inside its `legendre-cubic-moments/` directory matched GitHub's blob
hashes and byte counts. GitHub also contains `.gitignore`; its bytes and checksum
were checked separately. The ZIP's outer `START_HERE_MR.txt` is an upload guide,
not part of the repository payload.

## Results

| Check | Result |
| --- | --- |
| Original supplement manifest | All 34 entries passed SHA-256 verification |
| Repository manifest at the audited commit | All 43 entries passed SHA-256 verification |
| Historical source/supplement ZIP | SHA-256 matched; ZIP CRC check passed for its 267 files |
| `p2_completion_checks.py` | 20 checks passed |
| `p2_exact_checks.py` | 41 checks passed |
| `p3_exact_checks.py` | 26 checks passed |
| Retained reports | All three freshly generated reports matched the retained files byte for byte |
| Manuscript source structure | All 17 section inputs present; 84 labels with no duplicates or unresolved references; no missing cited bibliography keys |
| README and citation metadata | Relative file links resolved; title, author, V3 DOI, and preprint status were consistent |

The manuscript PDF has 629,151 bytes and SHA-256:

```text
ae20cad11a7739e1a1257143b6b7e700e9726af3e5fc577ed47dae38b7d5e894
```

The historical ZIP has 2,943,449 bytes and SHA-256:

```text
bd19f7bd50a151a1fe6b805e99aee473214b4d880f3c1e35c13ff9d35efc1060
```

The later repository maintenance adds this record and
[`scripts/verify_repository.py`](scripts/verify_repository.py), updates the reader
instructions, and refreshes `REPOSITORY_SHA256SUMS.txt`. The updated manifest
contains 45 entries and excludes itself. Original manuscript, PDF, algebra
scripts, retained reports, historical ZIP, and `SHA256SUMS.txt` are unchanged.

## Repeat the checks

With Python 3.8 or later, run from the repository root:

```sh
python scripts/verify_repository.py
```

The command verifies both manifests before executing the three small scripts.
It checks all 87 results and compares the generated JSON with the retained
reports. JSON is compared by content so platform newline conventions do not
affect the comparison. Outputs use a temporary directory under `results/`, which
is removed on completion. A failed verification exits with a nonzero status.

To verify only file integrity:

```sh
python scripts/verify_repository.py --integrity-only
```

## Scope and remaining verification

- These are repository and finite algebra checks, not independent specialist
  peer review or a verification of the full mathematical proof. The scripts'
  geometric assumptions and scope limits remain in force.
- A new LaTeX build could not run in the audit environment because the installed
  TeX runtime lacked `pdflatex.fmt` and could not locate `latex.ltx`. The supplied
  PDF's bytes were verified; a fresh build and visual comparison remain open.
- The V3 DOI is consistent throughout the repository. Live access to the DOI
  resolver and Zenodo record could not be confirmed by the available retrieval
  service. This is not evidence that the DOI is invalid.
- Journal submission status is the previously recorded status. The journal's
  submission system was not inspected during this repository audit.

No large prime scan or numerical L-function experiment was run. No new preprint
version, journal acceptance, or new mathematical proof validation is implied.
