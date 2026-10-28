# Photonics manuscript: replacement figure prompts

Prepared for Jason Duran Dutton, October 28, 2026.

These are prompts and production specifications, not generated figures. They follow the ten figure placements in `SEFI-Manuscripts/photonic-qec-full/photonic-qec-full.tex` reviewed in this chat. Confirm against the submitted PDF before replacing files. Existing figures have not been visually inspected; these specifications follow the manuscript equations, captions, and figure references.

## Shared instructions for every figure

Produce a restrained scientific figure on a white background. Use consistent typography, generous spacing, legible labels at final publication size, and a colorblind-friendly palette: blue for the reference trajectory, orange for the perturbed trajectory, and green for the projected trajectory. Differentiate curves with line styles as well as color. Avoid decorative glow, photorealistic photons, invented apparatus, ornamental equations, and claims of experimental validation. Keep titles outside the artwork where possible and put explanations in the caption. Use vector artwork for diagrams; create numerical plots from code and the stated equations rather than asking an image generator to invent data. Retain editable sources. Check the journal's current artwork requirements separately before submission.

Distinguish conceptual schematics, mathematical illustrations, and numerical demonstrations. None of these figures by itself demonstrates a physical quantum error-correction channel, logical-qubit recovery, or experimental hardware performance. The surface coordinates below are abstract, dimensionless configuration coordinates, not laboratory position or frequency unless a physical mapping is independently supplied.

## Figure 1 — Proposed DEFI stability manifold

Existing image: fig9.jpg. Label: fig:stability_surface.

**Prompt:** Create a clean conceptual mathematical diagram of a proposed stability manifold Sigma in an abstract three-dimensional configuration space. Show a translucent pale-gray saddle surface, a blue reference trajectory lying on it, and one direction arrow along that trajectory. Label the surface Sigma and the trajectory gamma_Sigma(t). Label axes x, y, z, with a small note that coordinates are abstract and dimensionless. Use the illustrative surface z = alpha*x^2 - beta*y^2, alpha and beta positive. Make it clear that this is an illustrative geometry for the proposed SEFI/GWFM/DEFI framework. Do not imply a measured energy landscape or physical proof of stability. Do not use the surface shape alone to imply dynamical attraction.

**Caption draft:** Conceptual stability manifold Sigma and a reference trajectory constrained to it in the proposed geometric framework. The surface is illustrative; its shape alone does not establish dynamical stability or physical photonic error correction.

## Figure 2 — Reference trajectory on the manifold

Existing image: fig8.jpg. Label: fig:mode_evolution.

**Prompt:** Make a mathematical illustration of a reference trajectory moving along a saddle surface. Use alpha = beta = 0.25 and gamma_Sigma(t) = (t, sin(t), 0.25*t^2 - 0.25*sin(t)^2), with -2 <= t <= 2. Plot the surface over -2 <= x <= 2 and -1.2 <= y <= 1.2. Draw the trajectory blue, with three clearly marked points at t = -1, 0, and 1 and an arrow showing increasing t. Use abstract dimensionless axes, a faint surface mesh, and a camera angle that keeps all marked points readable. Present this as a reference configuration-space curve, not a literal photon path or an experimentally measured optical mode.

**Caption draft:** Reference curve gamma_Sigma(t) on the illustrative saddle manifold for alpha = beta = 0.25. The parameter t is dimensionless in this example.

## Figure 3 — Identity constraint and permissible set

Existing image: fig2.jpg. Label: fig:sefi_invariants.

**Prompt:** Draw a conceptual constraint diagram with two aligned panels. Left: an abstract configuration space M containing a highlighted surface Sigma = {q : S(q) = 0}; mark q_on on the surface and q_off outside it. Right: a clearly labeled conceptual flow from proposed identity constraints to the permissible set Sigma to a reference trajectory gamma_Sigma(t). Use neutral language: proposed constraint, permissible set, and reference trajectory. Show S(q_on) = 0 and S(q_off) != 0. Do not invent conserved quantities, symmetry groups, a field equation, or experimentally measured identity variables. Avoid suggesting that S alone proves a dynamical conservation law.

**Caption draft:** Schematic of the proposed constraint S(q) = 0 defining the permissible set Sigma. A specific physical interpretation and dynamical preservation of the constraint require additional model definitions.

## Figure 4 — Displacement from the surface

Existing image: fig7.jpg. Label: fig:error_displacement.

**Prompt:** Create a precise geometric schematic of a point q off a saddle surface and its vertical projection Pi_v(q) onto the surface. Use f(x,y) = 0.25*x^2 - 0.25*y^2, q = (1, 0.5, 0.4375), and Pi_v(q) = (1, 0.5, 0.1875). Draw d = q - Pi_v(q) as a vertical arrow from the projected point to q. Label the z direction. Add a small inset showing the surface normal at the projected point, proportional to (-0.5, 0.25, 1), in a different line style to show that the vertical displacement generally differs from the surface normal. Label the operation vertical projection. Do not label the vertical arrow orthogonal, nearest-point, or binormal. Do not assign this displacement to photon loss, dephasing, or frequency drift without a defined physical mapping.

**Caption draft:** Vertical displacement d = q - Pi_v(q) for the illustrative graph surface. Vertical projection generally differs from Euclidean nearest-point projection, and the vertical direction is not generally the curve binormal or surface normal.

**Author review:** The existing caption mentions normal and binormal components. That wording must be reconciled with the actual projection used; a truthful replacement cannot retain an inaccurate caption.

## Figure 5 — Geometric correction map

Existing image: fig1.jpg. Labels: fig:correction_dynamics and fig:projection_mapping.

**Prompt:** Produce a two-panel mathematical illustration of a prescribed vertical projection map. Panel (a), before projection: a blue reference trajectory on the saddle and an orange vertically perturbed trajectory. Panel (b), after projection: the green projected trajectory coincides with the reference. Use f(x,y) = 0.25*x^2 - 0.25*y^2, gamma_Sigma(t) = (t, sin(t), f(t,sin(t))), gamma(t) = gamma_Sigma(t) + (0,0,0.15*cos(t)), and Pi_v(x,y,z) = (x,y,f(x,y)), for -2 <= t <= 2. Draw short vertical arrows indicating the mapping. Use a dashed blue reference so coincident curves remain intelligible. Label prescribed map, not autonomous dynamics. Do not invent a correction rate, feedback equation, measurement apparatus, or physical recovery fidelity.

**Caption draft:** The prescribed map Pi_v removes the chosen vertical perturbation by construction. This illustrates geometric restoration in a toy model; it does not establish physical implementability as a quantum recovery operation.

## Figure 6 — Curve curvature and torsion

Existing image: fig6.jpg. Label: fig:gwfm_geometry.

**Prompt:** Create an accurate differential-geometry diagram of a unit-radius helix gamma(u) = (cos(u), sin(u), 0.5*u). Mark u = 0 and draw its unit tangent T, principal normal N, and binormal B with a shared origin at that point. Use calculated vectors: T = (0, 1, 0.5)/sqrt(1.25), N = (-1, 0, 0), B = (0, -0.5, 1)/sqrt(1.25). Show a light osculating-plane patch spanned by T and N. Label curvature kappa = 0.8 and torsion tau = 0.4 in dimensionless coordinates. Identify this as an illustrative Frenet–Serret frame, not a photonic measurement or a solution derived from DEFI. Render vector directions exactly from coordinates.

**Caption draft:** Frenet–Serret frame of an illustrative helix, showing tangent T, principal normal N, and binormal B. These curve-frame vectors must be distinguished from a surface normal.

**Author review:** Frenet–Serret derivative equations without speed factors use arc length. Do not label u as arc length for this helix; its speed is sqrt(1.25).

## Figure 7 — Displacement components in a curve frame

Existing image: fig5.jpg. Label: fig:error_vector_field.

**Prompt:** Draw a mathematically accurate vector-decomposition diagram at u = 0 on the same illustrative helix as Figure 6. Use the same T, N, B vectors and define d = 0.20*N + 0.15*B. Draw d as a black vector and its normal and binormal components in distinguishable colors and dashed construction lines. Label d_N = 0.20, d_B = 0.15, and d_T = 0 for this deliberately chosen transverse example. In a small separate text box state the general decomposition d = d_T*T + d_N*N + d_B*B. Do not imply every displacement has zero tangential component. Do not equate the curve normal with the surface normal. Do not identify N and B components with specific physical quantum error channels unless such a mapping is separately derived.

**Caption draft:** Illustrative transverse displacement resolved in a curve's normal and binormal directions. General displacements may also have a tangential component; this diagram does not establish a mapping to physical quantum error channels.

## Figure 8 — Proposed software and analysis workflow

Existing image: fig3.jpg. Labels: fig:qec_stack and fig:discussion_geometry.

**Prompt:** Design a restrained scientific block diagram for a proposed geometric analysis workflow. Separate conceptual roles from software implementation with two clearly labeled lanes. Conceptual lane: SEFI—proposed identity constraints; GWFM—trajectory geometry; DEFI—proposed coupled dynamics. Analysis lane: stated model and parameters; synthetic trajectory generation; constraint residual and geometric diagnostics; prescribed projection; comparison and saved outputs. Use dashed arrows for proposed relationships and solid arrows only for verified implemented data flow. Do not assert any block exists in SEFI_QEC_Stack until its source has been checked. Do not depict hardware control, quantum syndrome extraction, physical photon-loss recovery, or logical fidelity as implemented capabilities without evidence. Add a legend separating proposed from implemented elements.

**Caption draft:** Proposed relationship between the conceptual framework and a geometric analysis workflow. Implemented blocks and proposed extensions must be identified from a source-code audit before finalizing this diagram.

**Production gate:** Review the specific software version referenced by the submitted paper before drawing the final architecture. This prompt deliberately does not invent an implementation.

## Figure 9 — Explicit validation geometry

Existing image: fig9.jpg, reused from Figure 1. Label: fig:validation_surface.

**Prompt:** Generate a reproducible numerical plot, using code, of z = 0.25*x^2 - 0.25*y^2 on -2 <= x <= 2 and -1.2 <= y <= 1.2. Add the blue reference curve gamma_Sigma(t) = (t, sin(t), 0.25*t^2 - 0.25*sin(t)^2), -2 <= t <= 2. Label abstract dimensionless x, y, z axes, Sigma, and the curve. State alpha = beta = 0.25 in the caption. Use a light mesh and no heatmap unless the color quantity is defined with a colorbar. Make this a separate quantitative figure from Figure 1, preserving the existing figure placement. If the original submitted calculation used other parameter values, use those instead and update the specification consistently.

**Caption draft:** Illustrative validation geometry Sigma: z = alpha*x^2 - beta*y^2, shown here with alpha = beta = 0.25 and the specified reference curve. Parameter values are proposed for the replacement illustration and must be reconciled with the submitted calculation.

## Figure 10 — Perturbed curve, projection, and residual

Existing image: fig10.jpg. Labels: fig:validation_displacement and fig:validation_correction.

**Prompt:** Create a two-panel, code-generated numerical figure from exactly specified toy-model equations. Use alpha = beta = 0.25, epsilon = 0.15, -2 <= t <= 2, and at least 401 evenly spaced samples. Define f(x,y) = alpha*x^2 - beta*y^2, gamma_Sigma(t) = (t,sin(t),f(t,sin(t))), gamma(t) = gamma_Sigma(t) + (0,0,epsilon*cos(t)), and gamma_corr(t) = Pi_v(gamma(t)) with Pi_v(x,y,z) = (x,y,f(x,y)). Panel (a): show a faint saddle surface, dashed blue reference, orange perturbed curve, and green projected curve; make coincident lines clear through styles or an inset. Panel (b): plot the before-projection vertical residual abs(epsilon*cos(t)) and after-projection residual, computed directly from coordinates, against dimensionless t. Label this vertical constraint residual, not state infidelity, photon-loss probability, or quantum error rate. Report the computed maximum post-projection residual without fabricating numerical noise. State that exact restoration follows from the prescribed map and chosen perturbation. Export the underlying sample table and plotting script with the figure.

**Caption draft:** Toy-model vertical perturbation and its removal by the prescribed projection. The pre-projection residual is |epsilon*cos(t)|; the projected curve satisfies z = f(x,y) by construction. This is an algebraic/numerical consistency demonstration rather than evidence of physical photonic quantum error correction.

## Replacement checklist

- Confirm the figure order against the actual submitted PDF.
- Preserve the original submitted files separately; do not overwrite them while preparing candidates.
- Keep existing figure labels and references; use distinct new filenames for candidate replacements.
- Update captions where the present wording conflicts with the illustrated mathematics.
- Use identical parameters and visual conventions across related figures.
- Distinguish curve normals, surface normals, binormals, and vertical directions.
- Identify conceptual and numerical artwork explicitly.
- Check every diagram against the manuscript and every plot against its generating code.
- For figures 9–10, retain source code, parameters, and numerical output. Values here are proposed illustration choices, not recovered original experiment settings.
- Verify current journal format, sizing, resolution, and submission requirements before final export.
