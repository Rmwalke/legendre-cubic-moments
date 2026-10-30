# Cubic twists of Legendre moments

**Cohomological descent and Frobenius trace formulas**  
Rushikesh Murlidhar Walke — Independent Researcher, Maharashtra, India

[Read the Zenodo preprint, version 3](https://doi.org/10.5281/zenodo.23795811) ·
[Read the manuscript PDF](paper/Walke_Legendre_Manuscript_2026-10-30.pdf) ·
[Reproduction instructions](REPRODUCIBILITY.md) ·
[Mathematical claim ledger](review/CURRENT_CLAIM_LEDGER.json)

## Research overview

This research preprint studies cubic-character second and fourth moments of the
Legendre family. It presents rank-four rational descents, cohomological Frobenius
trace formulas, a rational Chow/Scholl realization, local calculations at the
primes 2 and 3, and an argument for strong absolute irreducibility within its
stated coefficient-prime scope. The cubic second-moment comparison concerns a
separate rank-two object and has a retained bounded exact certificate.

The manuscript and its claim ledger state the hypotheses, proof dependencies,
and coefficient-prime restrictions. They also distinguish the written arguments
from historical numerical special-value observations.

## Publication and review status

**Status recorded on 30 October 2026:**

- Public preprint: **version 3**, DOI **10.5281/zenodo.23795811**.
- Submitted to the **Journal de Théorie des Nombres de Bordeaux (JTNB)** on
  30 October 2026; receipt has been acknowledged.
- Assignment to an editor or referee and the start of external peer review
  have not been confirmed. Acceptance has not been confirmed.
- The manuscript records internal AI-assisted checking. It has not undergone
  independent specialist review or proof-assistant verification.

This is a research preprint and accompanying source collection. Cite the Zenodo
preprint; it is not an article published in JTNB.

The older records in `review/` and `historical/` are preserved snapshots. In
particular, the `journal_submission: false` and unpublished-draft wording in an
earlier snapshot do not supersede the submission status above. The current
mathematical scope is set out in the manuscript and
[`review/CURRENT_CLAIM_LEDGER.json`](review/CURRENT_CLAIM_LEDGER.json).

## Contents

| Location | Contents |
| --- | --- |
| `paper/` | Unchanged manuscript PDF supplied with the submitted V3 package |
| `manuscript/` | Matching LaTeX source, all section files, and build instructions |
| `local_checks/` | Three exact local-algebra scripts and their retained reports |
| `review/` | Retained claim/dependency ledger and internal review snapshots |
| `historical/` | Unchanged earlier source/supplement archive, including the bounded cubic certificate |
| `SHA256SUMS.txt` | Original supplement's integrity manifest, preserved unchanged |
| `REPOSITORY_SHA256SUMS.txt` | Integrity manifest for this prepared repository tree |
| `PROVENANCE.json` | Provenance and scope of the repository preparation |

All files extracted from the public source/supplement archive, and the supplied
manuscript PDF, retain their original bytes. The preparation adds repository
documentation, citation metadata, and an integrity manifest. It makes no change
to the mathematical manuscript or the existing scripts and reports.

## Reproducing the retained checks

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the three short commands and their
precise scope. The scripts use Python's standard library and write fresh outputs
to `results/` in the documented commands, leaving the retained reports intact.
No large prime scan or numerical L-function experiment is needed to inspect this
repository. No mathematical scripts were rerun during this packaging step.

**A passing algebra script does not certify the geometric constructions,
nearby-cycle hypotheses, or identification of the actual local representation.**
Some matrix checks are explicitly conditional on geometric inputs supplied in
the written arguments. Historical numerical values remain subject to the
limitations stated in the manuscript.

The manuscript does not claim rank-four automorphy, analytic continuation, a
proved functional-equation sign, arithmetic period identities, or a classical
elliptic BSD theorem.

## Citation

Walke, Rushikesh Murlidhar (2026). *Cubic twists of Legendre moments: cohomological descent and Frobenius trace formulas*. Version 3, Zenodo preprint.
https://doi.org/10.5281/zenodo.23795811

Citation metadata is supplied in [CITATION.cff](CITATION.cff) and
[CITATION.bib](CITATION.bib). The preferred citation is the preprint itself.

## Feedback

Comments and corrections are welcome. Please identify a manuscript section,
theorem, equation, or an exact script command and output. Especially useful
review targets are listed in Section 12 of the manuscript: the dyadic closure
constant and component/node actions, the nearby-cycle hypotheses, and the
local-at-3 global-to-local map with its Frobenius normalization.

## AI assistance and rights

AI assistance included mathematical drafting, computational work, references,
and internal checking; the manuscript's revision note describes its extent.
The author is responsible for the manuscript and its claims.

Existing copyright and license notices are preserved. This preparation does not
apply a new blanket software license. See [RIGHTS.md](RIGHTS.md).
