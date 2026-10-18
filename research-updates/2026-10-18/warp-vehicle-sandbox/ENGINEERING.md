# SEFI vehicle engineering sandbox

Jason D. Dutton research program | October 18, 2026

## Engineering decision

We can engineer the geometric model, ordinary structure, control software, instrumentation, and a physical analog demonstrator now. We cannot presently specify a functioning SEFI displacement propulsion module: the manuscripts give neither a measured source-to-displacement coupling nor an energy/momentum law that predicts its output from electrical or mechanical inputs. This is a missing physical mechanism, not merely a difficult-to-manufacture component.

The sandbox therefore has three separate objects:

1. A full-scale **reference vehicle** used for geometry, interfaces, and ordinary load accounting. It has no validated SEFI propulsion performance.
2. A **digital displacement experiment** that tests explicit mathematical maps and flow rules. It predicts coordinate deformation under declared inputs, not actual spacecraft motion.
3. A **small, instrumented mechanical analog** that can test sensing, synchronization, deformation control, and accounting using ordinary actuators. Motion is supplied by measured conventional forces. It is not a warp-drive prototype.

No hardware was purchased, built, energized, or flight-tested. No speculative actuator is represented as available technology.

## The two source manuscripts

### Capsule construction

Source: `V:/V Drive and GitHub Content/Journal Submissions/Warp/Warp.tex`

Title: *Displacement-Engineered Warp Fields: Tic-Tac Geometry, Stability Surfaces, and Identity-Space Confinement*.

The source selects length 14 m, radius 2 m, and nominal layer thickness 1 m. It defines a spatial map Phi(x)=x+Delta(x), with a tapered boundary layer, amplitude bounds, and an effective displacement/time ratio. Its introduction explicitly describes a kinematic model without a stress-energy source, propulsion mechanism, or experimental validation. That scope governs the engineering interpretation even where later passages use stronger language.

Important repairs before implementation:

* Non-intersection concerns Phi, not Delta alone. The source's lower bound on differences of Delta does not establish injectivity. Counterexample: Delta(x)=-x satisfies a nonzero difference bound but sends every point to Phi(x)=0. Conversely Delta=0 gives a valid identity map, so a minimum displacement gradient is not generally required.
* A useful sufficient condition is a global Lipschitz constant G<1 for Delta on a convex Euclidean domain. Then |Phi(x)-Phi(y)| >= (1-G)|x-y|. This follows from the reverse triangle inequality. It is a mathematical non-collapse guarantee, not a spacetime stability or thrust theorem.
* The source taper 1-u^n reaches zero at u=1 with derivative -n. Extending it by zero outside the layer creates a first-derivative discontinuity. The accompanying finite-alpha Gaussian does not vanish exactly at the outer edge either. A globally smooth implementation needs revised matching conditions.
* The stated curvature bound adds an inverse-length curvature to a displacement-gradient term that is dimensionless. It cannot be used as a dimensional engineering limit without additional scales and a corrected derivation. The transformed acceleration also needs second spatial derivatives and, for time-dependent maps, time derivatives.
* A radius profile with a finite meridional curvature does not by itself establish a regular closed hull or bound both principal surface curvatures. Endcaps and transitions need a proper surface construction.
* Delta_0/delta_t is a chosen displacement divided by a chosen time. Without actuator dynamics, it provides no achievable velocity, acceleration, power, or response-time specification.

### Flow and envelope construction

Source: `V:/V Drive and GitHub Content/Journal Submissions/The New Warp/warp.tex`

Title: *Displacement-Engineered Warp Fields: Stability Surfaces and Worldline Geometry*.

The source introduces D(x,I), an envelope C(D,grad D,Hess D,I)=0, the curl of D, flow gamma_dot=D(gamma), and identity evolution I_dot=f(D). It describes RK4 integration and figures with carrier-field thresholds and a stability residual.

Implementation blockers:

* D, C, and f need explicit functions, coefficients, units, domains, initial conditions, and boundary conditions before the numerical results can be independently reproduced. Figure thresholds alone do not supply them. The inspected folder contains images, a video, and manuscript files; no executable simulation, raw grid, or parameter dataset was found there. Such assets may exist elsewhere.
* A displacement in meters and a flow field in meters/second are different quantities. Distinguish Phi_t(x) from the velocity u(x,t) that generates a flow. A static coordinate map is not a propulsion law.
* The ordinary curl is a three-dimensional spatial operation. A four-dimensional D requires a defined spatial projection or a specified differential-form construction.
* C=0 ordinarily defines a surface, not an entire stable volume. A signed residual and a domain can define candidate interior regions, but actual dynamical stability still requires analysis.
* The source's identity-space formulation is not automatically identical to the earlier four O/A/S/W internal coordinates. A mapping between the state spaces must be stated before combining them.
* Neither manuscript closes the link from a conserved SEFI charge to a mechanical force or source coupling. Preserve that link as an unanswered research question.

## Reference vehicle and mission assumptions

Use the source dimensions as design choices, not verified dimensions of an observed craft. Select an uncrewed reference body; defer crew systems, high-speed atmosphere operation, and all FTL mission requirements. There is no justified mass estimate until structure, payload, power, cooling, and propulsion are specified. Adjustable mass is a scenario input, not a prediction.

For transparent geometry accounting, the sandbox uses a spherocylinder: cylinder length c=L-2R, radius R, and two hemispherical ends. This is a replacement CAD reference, not the source's polynomial radius profile. Its volume is pi R^2 c + 4 pi R^3/3 and area 2 pi R c + 4 pi R^2. A true outward normal offset of thickness delta keeps c fixed, increases radius to R+delta, and increases total length to L+2delta. The layer volume is the difference of those two volumes. Neither that volume nor its thickness determines field energy.

At the 14 m / 2 m / 1 m reference, the body is about 159.2 cubic meters and the geometric shell about 236.7 cubic meters. The shell is an analysis region, not an assumed physical material or device. Cylinder-to-hemisphere joins are tangent-continuous but change curvature; a manufactured curvature-controlled hull would use a higher-continuity CAD loft and verification.

Ordinary total-system checks remain useful: force F=M a, kinetic energy M v^2/2 at nonrelativistic speeds, and waste heat P_heat=P_input-P_useful-dE_storage/dt for a properly defined energy boundary. An envelope that changes local passenger loads would need a separate metric or mechanical analysis; it does not automatically remove the total system's momentum requirements. The sandbox does not turn F=M a into an assumed SEFI force law.

## A corrected, testable displacement sandbox

Define an explicitly hypothetical spatial map with a uniform interior displacement A n and a normal-distance transition across thickness delta. Let s be distance from the reference hull, u=s/delta, and n a fixed displacement direction. Set Delta=A f(u)n, with f=1 inside, f=0 outside, and f(u)=1-10u^3+15u^4-6u^5 for 0<u<1. This matches the first two derivatives at the transition endpoints.

For a regular normal-distance region with |grad s|=1, max |f'|=15/8, giving G <= (15/8)|A|/delta. A conservative global Lipschitz version can be used for the Euclidean map. G<1 supplies the preceding non-collapse bound; G>=1 means that sufficient guarantee is unavailable, not that intersection or failure has been proved. Hull regularity and a suitable distance function must still be checked. No one-dimensional inequality proves a real envelope stable.

For delta=1 m, this sufficient test needs |A|<0.5333 m. An illustrative A=0.1 m gives G<=0.1875 and a lower separation factor 0.8125. This is a map test only. It neither permits stepping a vehicle 0.1 m without a force nor supplies a repetition frequency. Temporal modulation adds time derivatives and must be modeled separately.

## Subsystems and what is available

| Subsystem | Available today | Work we would do | Unresolved dependency |
|---|---|---|---|
| Geometry | CAD, meshing, structural solvers, normal-offset geometry | Smooth hull and layer meshes; mesh convergence; interface locations | Actual hull loads depend on mission and propulsion |
| Structure | Conventional metals/composites, machining and molding | Small mockup and attachment design; full-scale structural sizing only after loads | No justified material thickness or mass yet |
| Sensing | Position encoders, inertial sensors, temperature and electrical sensors, DAQ | Calibrate channels; synchronize clocks; record uncertainty | No sensor for an undefined SEFI field quantity |
| Controller | Microcontrollers, real-time computers, conventional feedback software | State estimator, map evaluator, limit checker, data logging | Explicit C and f; mapping sensor readings into theory variables |
| Analog actuation | Small motors, voice coils, mechanical linkages, low-voltage drivers | Design an ordinary distributed displacement demonstrator and measure reaction forces | These actuators move matter; they do not implement a spacetime displacement operator |
| Power | Batteries, regulated supplies, converters | Measured power budget, supply isolation, switching and storage accounting | A propulsion power rating cannot be calculated without a source law |
| Thermal management | Fans, heat sinks, liquid cooling, radiators as mission permits | Thermal model and measured losses; choose cooling from actual dissipation | Unknown actuator losses prevent a full vehicle cooling design |
| Force metrology | Load cells, displacement sensing, calibrated balances | Fixture design, null tests, thermal and cable-force characterization | Force sensitivity must follow a quantitative predicted signal |
| Conventional propulsion comparator | Fans/propellers in air; reaction propulsion in space | Simulate and budget a declared mission using measured components | Such thrust is conventional and must not be called SEFI propulsion |
| SEFI propulsion module | No validated implementation established by either manuscript | First derive a measurable coupling and source dynamics | Could require new physics; no build recipe follows yet |

Representative current manufacturer capability: NI's DAQ portfolio measures voltage, current, and sensor channels; the USB-6451 page lists analog/digital channels and documented software interfaces. It is an example of an instrumentation class, not a purchase selection. The previously surfaced USB-6215 page says it is no longer available for purchase, so it is not a proposed new procurement. No prices, stock promises, or compatibility approvals are inferred.

Do not specify superconducting magnets, plasma chambers, high-power lasers, or a nuclear source as the missing propulsion module. They are real technologies, but the manuscripts provide no law showing that any of them produces the required Delta. Increasing ordinary field strength is not a substitute for deriving that coupling.

## What we build ourselves and how

### Stage A — reproducible digital model

1. Freeze the two input versions and source hashes; retain the originals unchanged.
2. Implement the corrected map independently of any vehicle dynamics. Verify identity-map behavior, derivative matching, injectivity sufficient bounds, and convergence with spatial resolution.
3. Define a separate flow model u(x,t) only when its governing equations and units are explicit. Check uniqueness, initial data, boundaries, and conservation. If a metric is proposed, calculate curvature and required source terms; check whether effects are just a coordinate transformation.
4. Create an actuator interface with input channels, state, output observables, power, losses, momentum exchange, and uncertainty. Mark every unspecified conversion factor as unknown, not zero and not a freely tunable performance knob.
5. Parameter sweeps may explore assumptions. They cannot establish feasibility of the assumptions themselves. Keep inferred speed, thrust, power density, and range unavailable until the physical model determines them.

### Stage B — instrumented desktop analog

Design assumption: an approximately 0.3 m uncrewed mockup on a guided bench fixture, powered by a current-limited low-voltage supply. This scale is arbitrary for software and metrology development, not a scaling law from the 14 m reference.

Use a lightweight central body and segmented surrounding fixture, ordinary small displacement actuators, position sensing, and reaction-force measurement. Fabricate the body and actuator brackets by ordinary printing or machining. Characterize each actuator separately against its measured displacement, force, electrical consumption, and bandwidth; record hysteresis and thermal drift. Then command a smooth spatial displacement pattern and test tracking and synchronization. A segmented fixture samples the proposed envelope geometry; it does not make a continuous physical warp envelope.

The fixture should measure the force transmitted to its support. The outer structure must be included in the system boundary. Motion on a rail can use the rail as a reaction path and cannot demonstrate isolated propulsion. Internal moving masses can shift the chassis while leaving the whole-system center of mass consistent with conservation. Do not interpret those shifts as thrust.

Test equal-and-opposite actuator commands, sham commands, reversals, disconnected/dummy loads, different cable routing, and thermal settling. Log displacement, actuator current/voltage, support force, temperatures, and clock synchronization. Develop the protocol before examining any apparent anomaly. Ordinary mechanical force is the calibration target at this stage; no null result here alone falsifies an unspecified SEFI interaction.

### Stage C — independent physical-coupling experiment

Only after a proposed source law predicts a measurable nonstandard signal should a qualified lab design the corresponding experiment. Specify what field is generated, by what source, with what energy density, and how it couples to test matter. Identify predicted force or phase shift, distance law, orientation dependence, modulation, magnitude, and the conditions for a null result. Include all conventional electromagnetic, acoustic, thermal, mechanical, and gravitational effects in the comparison.

A force balance, isolated power and readout, environmental characterization, and where appropriate vacuum testing may be needed. Vacuum alone does not eliminate electromagnetic interactions or cable forces. Demand reversals, independent replication, complete energy/momentum accounting, and a signal above a preregistered uncertainty budget before vehicle integration. Do not scale from a visual envelope plot or an uncalibrated microforce reading.

### Stage D — vehicle integration gate

Proceed only when the coupling has survived replication and its thrust/power/heat/response limits are measured. Then size source, drivers, mounts, thermal rejection, attitude control, structure, and emergency behavior. Characterize interactions with nearby matter and fields. Flight, crew accommodation, atmosphere entry, and high-speed operation require separate programs; they cannot be assigned performance from a kinematic map.

## Requirements for the unknown propulsion module

The central deliverable is a function or dynamical law mapping measured actuator inputs into a physical field and then into matter/metric response. Required outputs include total thrust vector, torque, energy stored in the field, emitted or exported momentum, heat, and observable effects on a separate test body. Required inputs include specified source distributions, supply power, geometry, and boundary conditions. If the natural SEFI charge is part of the mechanism, define Q explicitly and show its preservation from the same equations. Do not assume conservation of Q implies conservation or transfer of linear momentum.

No currently identified component closes that interface. It is premature to choose coil turns, frequencies, field strengths, fuel, shielding, or a power-plant size. The first missing object is the coupling equation and an experimentally distinguishable prediction.

## Current-physics scale checks

Known electric propulsion accelerates propellant; NASA's Dawn description reports a maximum 91 mN for each engine and identifies xenon flow and electrical input as operating variables. It is a useful comparator for the difference between real thrust and a geometrical trajectory. It is not a surface-launch or hover system.

An onboard collimated photon emitter has ideal thrust F=P_out/c. One kilowatt of emitted optical power gives about 3.34 micronewtons. A remotely illuminated ideal mirror can receive 2P_incident/c, with balancing momentum in the external source. These are different system boundaries, not interchangeable efficiency claims. A closed reflective cavity does not acquire an external momentum source merely because its field pressure is large.

Magnetic energy density B^2/(2 mu_0), a mechanical displacement amplitude, and a spacetime curvature are different quantities. There is no conversion equation between them in the manuscripts. Ordinary gravitational effects from laboratory energy distributions do not justify identifying a coil with a controllable warp actuator.

## Sources and verification

The two author manuscripts were read in LaTeX, with primary definitions, engineering appendix, and numerical-method sections inspected. Their originals were left unchanged. Source hashes accompany this workbook. This is not a visual review of every source figure or a reproduction of their reported simulations.

Current capability and physics sources checked October 18, 2026:

* NI DAQ portfolio: https://www.ni.com/en/shop/hardware-portfolio/daq-sensor-io.html
* NI USB-6451 instrumentation example: https://www.ni.com/en-za/shop/model/usb-6451.html
* NI USB-6215 discontinued purchase status: https://www.ni.com/en/shop/hardware/voltage/model-usb-6215
* NASA Dawn ion propulsion: https://science.nasa.gov/mission/dawn/technology/ion-propulsion/
* NASA solar electric propulsion: https://www.nasa.gov/space-technology-mission-directorate/tdm/solar-electric-propulsion/
* NIST photon-force measurement: https://www.nist.gov/programs-projects/photoforce-project
* Bobrick and Martire, physical warp-drive analysis, including the need for propulsion: https://arxiv.org/abs/2102.06824

The interactive calculations use the declared spherocylinder geometry, quintic taper, nonrelativistic load accounting, and ideal photon momentum only. They contain no SEFI thrust/power predictor. They are a design and consistency sandbox, not certification or evidence of a functioning vehicle.
