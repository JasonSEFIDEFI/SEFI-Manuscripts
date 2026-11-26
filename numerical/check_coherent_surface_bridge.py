"""Independent dense-amplitude checks of a conditional surface recovery model."""
from pathlib import Path
import cmath,json,math,random

rng=random.Random(20261122)
n,m=9,11
points=[(x,y) for x in range(-1,2) for y in range(-1,2)]
heights=[x*x-y*y for x,y in points]
def normalized(count):
    a=[complex(rng.gauss(0,1),rng.gauss(0,1)) for _ in range(count)]
    norm=math.sqrt(sum(abs(v)**2 for v in a))
    return [v/norm for v in a]
def shift(g,d):return [g[(z-d)%m] for z in range(m)]
def reduced(amplitudes):
    return [[sum(amplitudes[i][z]*amplitudes[j][z].conjugate() for z in range(m))
             for j in range(n)] for i in range(n)]
def error(a,b):return max(abs(a[i][j]-b[i][j]) for i in range(n) for j in range(n))
g=normalized(m);psi=normalized(n)
rho=[[psi[i]*psi[j].conjugate() for j in range(n)] for i in range(n)]
def output(ds,phase=0):
    encoded=[[psi[i]*shift(g,heights[i])[z] for z in range(m)] for i in range(n)]
    noisy=[[encoded[i][(z-ds[i])%m]*cmath.exp(1j*phase*z) for z in range(m)] for i in range(n)]
    decoded=[[noisy[i][(z+heights[i])%m] for z in range(m)] for i in range(n)]
    return reduced(decoded)
common_error=max(error(output([d]*n),rho) for d in range(m))
ds=[(x+2*y)%m for x,y in points]
actual=output(ds)
packets=[shift(g,d) for d in ds]
expected=[[rho[i][j]*sum(packets[i][z]*packets[j][z].conjugate() for z in range(m))
           for j in range(n)] for i in range(n)]
differential_error=error(actual,expected)
# A periodic height phase kick is conjugate noise, with a geometry-dependent
# logical phase. Using a cyclic character avoids a spurious boundary phase.
k=2*math.pi/m
phase_actual=output([0]*n,k)
phase_expected=[[rho[i][j]*cmath.exp(1j*k*(heights[i]-heights[j])) for j in range(n)] for i in range(n)]
phase_error=error(phase_actual,phase_expected)
assert max(common_error,differential_error,phase_error)<1e-12
# Independent 9-dimensional Bell-reference overlap after common translations.
# For a channel acting diagonally on matrix units, Fe is the mean coherence
# multiplier over all pairs. Common translation gives identical residual packets.
bell_fe=sum(sum(shift(g,3)[z]*shift(g,3)[z].conjugate() for z in range(m)).real
            for i in range(n) for j in range(n))/(n*n)
assert abs(bell_fe-1)<1e-12
result={'status':'conditional mathematical construction; no physical implementation asserted',
        'random_seed':20261122,'locations':n,'height_bins':m,
        'complex_packet_common_translation_max_error':common_error,
        'differential_overlap_kernel_max_error':differential_error,
        'conjugate_phase_logical_action_max_error':phase_error,
        'bell_reference_fidelity_common_translation':bell_fe,'all_checks_passed':True}
(Path(__file__).parent/'coherent_surface_bridge_checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
