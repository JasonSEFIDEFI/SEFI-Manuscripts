# Candidate photonics replacement figures

Generated as reproducible mathematical plots and diagrams. These are review candidates, not a revised journal submission.

## Files

Each figure has a 350 dpi PNG and a PDF with vector elements. The script and CSV permit reproduction.

## Captions and scope

### Figure 1: figure_01_stability_manifold
Illustrative proposed constraint manifold and reference trajectory; surface geometry alone does not establish dynamical stability.
Type: conceptual mathematical illustration

### Figure 2: figure_02_reference_trajectory
Reference curve (t, sin t, 0.25 t² − 0.25 sin² t), for −2 ≤ t ≤ 2, on the illustrative manifold.
Type: computed mathematical illustration

### Figure 3: figure_03_identity_constraint
Proposed constraint S(q)=0 defining a permissible set. A constraint definition does not by itself establish conservation under dynamics.
Type: conceptual schematic

### Figure 4: figure_04_vertical_displacement
q=(1,0.5,0.4375), Πv(q)=(1,0.5,0.1875). The orange displacement is vertical; the gray surface normal is a different direction.
Type: computed geometric diagram

### Figure 5: figure_05_projection_mapping
Prescribed vertical projection removes the specified vertical perturbation by construction; physical quantum recovery is not demonstrated.
Type: computed mathematical illustration

### Figure 6: figure_06_frenet_frame
Calculated curve frame at u=0 for the helix (cos u, sin u, 0.5u). Curvature 0.8, torsion 0.4; curve normal and surface normal are distinct concepts.
Type: computed geometric diagram

### Figure 7: figure_07_frame_components
A deliberately transverse displacement decomposed in the normal–binormal plane of a curve. General displacement can include a tangent component.
Type: mathematical schematic

### Figure 8: figure_08_proposed_workflow
Conceptual roles and proposed analysis sequence. All connections are marked proposed; this is not a verified implementation architecture for SEFI_QEC_Stack.
Type: conceptual schematic; software audit pending

### Figure 9: figure_09_validation_surface
Computed saddle surface and reference curve using proposed illustration parameters alpha=beta=0.25. These are not recovered original experimental settings.
Type: computed toy-model plot

### Figure 10: figure_10_validation_projection
Perturbation epsilon*cos(t) and its removal by vertical projection. Post-projection constraint satisfaction follows algebraically from the prescribed map; this is not quantum error-rate evidence.
Type: computed toy-model plot

## Review before submission

The submitted PDF and original image contents were not visually inspected. Match figure numbering and update captions against that PDF. Figure 8 is explicitly conceptual, pending a software audit. Parameters for Figures 2, 4, 5, 9 and 10 are proposed illustration choices, not recovered original data. The vertical projection is not nearest-point projection, a vertical perturbation is not generally binormal, and the toy model does not establish physical photonic QEC. Existing captions and text require reconciliation where they assert these equivalences.