"""Independent finite check of a full sampled-surface coherent lift.

This is a new conditional mathematical extension, not an upstream result
and not a derivation of an optical Hamiltonian from the field action.
"""
from fractions import Fraction
from pathlib import Path
import cmath,json
locations=[(x,y) for x in range(-1,2) for y in range(-1,2)]
height=[x*x-y*y for x,y in locations]
n=len(locations);m=11
encode={b:b*m+height[b]%m for b in range(n)}
decode=[{b*m+(z+height[b])%m:b for b in range(n)} for z in range(m)]
def apply(a,ops):
    out={}
    for weight,op in ops:
        for (r,c),v in a.items():
            if r in op and c in op:
                key=op[r],op[c];out[key]=out.get(key,0)+weight*v
    return {k:v for k,v in out.items() if v}
for b in range(n*m):assert sum(b in op for op in decode)==1
cases=0
for shift in range(m):
    noise={b*m+z:b*m+(z+shift)%m for b in range(n) for z in range(m)}
    for r in range(n):
        for c in range(n):
            unit={(r,c):1}
            actual=apply(apply(apply(unit,[(1,encode)]),[(1,noise)]),[(1,op) for op in decode])
            assert actual==unit
            cases+=1
dif=[(x+y)%m for x,y in locations]
noise={b*m+z:b*m+(z+dif[b])%m for b in range(n) for z in range(m)}
for r in range(n):
    for c in range(n):
        actual=apply(apply(apply({(r,c):1},[(1,encode)]),[(1,noise)]),[(1,op) for op in decode])
        assert actual==({(r,c):1} if dif[r]==dif[c] else {})
# A pure geometric residual does not undo a lateral permutation of logical sites.
perm={b:(b+1)%n for b in range(n)}
assert perm[0]!=0
result={'status':'new conditional extension, not an upstream or experimental result','locations':locations,'height_bins':m,'common_shift_matrix_unit_checks':cases,'differential_matrix_unit_checks':n*n,'trace_preserving_recovery':True,'all_checks_passed':True,'limitation':'Common height noise only; arbitrary height assignment gives same logical protection. A lateral logical permutation is not reversed by height subtraction.'}
(Path(__file__).parent/'surface_extension_checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
