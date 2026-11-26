PROPOSED CONSOLIDATED REPLACEMENT FOR ADV26-AR-05694
November 25, 2026

Title: Coherent Saddle Encoding and Displacement Recovery: Residual-State Criteria and Timing Limits
The established filenames Conjugate_Phase_Geometry_AIP_Advances.tex and .pdf are retained to replace the files previously in this folder. The title inside is updated.

This package consolidates both manuscripts. It is prepared locally for a replacement if AIP Advances permits; no upload, withdrawal or submission was performed. It is not a second parallel submission.

Main files
- Conjugate_Phase_Geometry_AIP_Advances.pdf and .tex
- Conjugate_Phase_Geometry_Source.zip: complete current editable/reproducible package
- CHANGE_SUMMARY.txt and Integration_Map.txt: changes and source-to-result coverage
- verification.json / verification_transcript.txt / integration_checks.json
- Cover_Letter_AIP_Advances.pdf: request to replace under the existing tracking number
- Highlight_Conjugate_Phase_Geometry.jpg / .tif: updated 600 dpi RGB artwork; filenames retained for continuity; PDF/SVG/PNG also supplied

All mathematical and theorem/proof blocks from the newer manuscript are retained; earlier unique derivations and controls are mapped in Integration_Map.txt. Main text focuses on recovery. Appendices retain separately defined scalar, localization, history, geometric and conservation results. The timing law uses a matched coherent inverse. No experimental apparatus, broad error correction, curvature advantage, nonlinear stability or common microscopic theory is asserted.

Reproduce
Install requirements.txt, then run python run_checks.py. Run python make_recovery_figures.py, python make_field_figures.py, and python make_highlight.py to regenerate figures. Run python build_pdf.py with pdfLaTeX/REVTeX 4.2 installed, or compile the main TeX twice manually. The bibliography is embedded. Keep figures/ alongside the TeX.

All eight numerical scripts pass. The tests include exact finite registers, direct oscillators, cutoff refinement, reference entanglement, phase/loss bookkeeping, radial grid/domain refinement and independent integration controls. Results are deterministic synthetic calculations, not observations.

Previous delivery files are preserved under revision-history/Before_Integrated_Replacement_2026-11-25.zip in the V-drive destination. SHA256_MANIFEST.json identifies the current package.
