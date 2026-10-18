# JMP author-review package

Prepared October 11, 2026, for **Jason D. Dutton's personal review**. This consolidation has not been submitted, uploaded to a journal, or sent to an editor. The author reports that all six related source/framework papers are already submitted to JMP; none of those records has been changed.

## Files

- `manuscript.tex` and `manuscript.pdf`: coherent, corrected conditional classical manuscript; author metadata and declarations remain pending.
- `references.bib` and `manuscript.bbl`: bibliography source and compiled reference list.
- `cover-letter.tex`, `cover-letter.pdf`, and `cover-letter.md`: draft editorial-guidance letter concerning consolidation of existing records, avoiding a redundant new submission or unverified exclusivity claims.
- `mathematical-audit.md`: provenance, source claim corrections, and unresolved mathematical issues.
- `submission-status.md`: author-reported tracking numbers, known overlap, and unresolved status checks.

## Build

Run these commands in this directory with REVTeX 4.2 and standard AIP/AMS LaTeX packages installed:

```text
pdflatex manuscript.tex
bibtex manuscript
pdflatex manuscript.tex
pdflatex manuscript.tex
pdflatex cover-letter.tex
```

The manuscript uses `aip,jmp,reprint,onecolumn` with REVTeX 4.2, following the official JMP one-column template's layout through the installed successor of its REVTeX 4.1 class. Also check a `preprint` build for review/production compatibility. It uses numerical AIP references, consecutive page numbers, a single-paragraph abstract without displayed equations or citations, and separate declarations and data availability sections. No journal acceptance or mathematical novelty is guaranteed by formatting compliance.

## Journal requirements checked

Official sources accessed October 11, 2026:

- [AIP author instructions](https://publishing.aip.org/resources/researchers/author-instructions/): LaTeX plus author-generated PDF, manuscript order, numbered pages, declaration and data availability sections.
- [Official JMP one-column template](https://www.overleaf.com/latex/templates/template-for-submission-to-the-journal-of-mathematical-physics/wntsmttxvvxf): one-column format, REVTeX/AIP setup, and preprint compatibility check.
- [AIP publication ethics](https://publishing.aip.org/resources/researchers/policies-and-ethics/research-integrity-and-publication-ethics/): substantially identical essentials across concurrently submitted manuscripts can constitute dual submission; consolidation and a new title do not eliminate overlap.
- [AIP AI policy](https://publishing.aip.org/resources/researchers/policies-and-ethics/ai-policy/): substantive synthesis or analysis affecting findings warrants methods disclosure with tool identification and purpose. This revision includes such disclosure.
- [AIP author obligations](https://publishing.aip.org/resources/researchers/policies-and-ethics/authors/): author approval and accountability.

## Before any submission

The final name is confirmed as Jason D. Dutton. Author confirmation remains required for affiliation, corresponding email, funding, conflicts, contributions, validation of all revised mathematics, and approval of the complete manuscript. Pending items are visible in this personal review draft rather than filled with invented declarations.

The author reports that all six related papers are **already submitted to JMP**. Their tracking identifiers are recorded in `submission-status.md`. This consolidated draft substantially overlaps GWFM, SEFI, and DEFI; overlap with the other three manuscripts requires their full texts. No journal account or complete submission history has been inspected, so current dispositions, publication status, and public-preprint status remain unverified. Keep this as a personal draft. Before any journal use, obtain editorial guidance on replacement/consolidation of existing records and resolve overlapping active submissions. If already published, disclose and cite the published work and assess whether a sufficiently distinct contribution remains. Identify any preprints and licenses. The draft letter neither requests nor enacts withdrawal.

No public publication record is inferred from a year on a PDF or from a source's bibliography. Review the related unified manuscript if it contains substantially overlapping results. Provide any required reused-material permissions. Source diagrams were omitted; the claims they illustrated were not proved by those diagrams.

This package is suitable for author review. It is not a cleared, submission-ready declaration package. Submission requires the user's explicit approval after all pending items are resolved.

## Validation completed

The final manuscript compiles to 9 pages and the guidance-letter draft to 1 page. A separate preprint-format check compiled to 13 pages. Final compiler logs contain no unresolved citations/references or overfull/underfull text boxes. The abstract contains 250 whitespace-delimited words. Rendered pages were visually inspected, including the potential Hessian and cover letter. Numerical spot checks of the displayed potential derivatives, Schur-complement identity, square completion, Origin conservation, and acceleration-zero counterexample passed. These checks supplement the displayed proofs; they do not establish full-system consistency, quantum equivalence, or independent peer review.
