$ErrorActionPreference = 'Stop'
$ffmpeg = 'C:\ffmpeg\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$work = Join-Path $root 'jmp_video_clips'
New-Item -ItemType Directory -Force -Path $work | Out-Null

$font = 'C\:/Windows/Fonts/arial.ttf'
$bold = 'C\:/Windows/Fonts/arialbd.ttf'
$scenes = @(
    @{ Name='01_title'; Image='Highlight.jpg'; Seconds=8; Kicker='JOURNAL OF MATHEMATICAL PHYSICS'; Title='Unified Geometric Field Theory'; Body='Worldline and identity-space invariants' },
    @{ Name='02_operator'; Image='Fig2_Worldline_Geometry.jpg'; Seconds=12; Kicker='THE UNIFIED OPERATOR'; Title='One field over spacetime and identity space'; Body='T = geometry + identity dynamics + invariant potentials' },
    @{ Name='03_stability'; Image='Fig1_Stability_Surface.jpg'; Seconds=12; Kicker='STABILITY MANIFOLDS'; Title='Ideal evolution lives on invariant surfaces'; Body='Curvature, torsion, identity coordinates, and dynamics are preserved together' },
    @{ Name='04_error'; Image='Fig3_Error_Displacement.jpg'; Seconds=12; Kicker='ERROR DISPLACEMENT'; Title='Deviation becomes geometry'; Body='Worldline and identity-space errors form a unified displacement vector' },
    @{ Name='05_correction'; Image='Fig4_Correction_Mapping.jpg'; Seconds=12; Kicker='CORRECTION MAPPING'; Title='Correction is projection'; Body='The field is mapped back to the stability manifold' },
    @{ Name='06_photonic'; Image='Fig5_Photonic_Implementation.jpg'; Seconds=12; Kicker='PHOTONIC IMPLEMENTATION'; Title='Geometric stabilizers and syndrome observables'; Body='A proposed route from invariants to photonic quantum error correction' },
    @{ Name='07_cosmology'; Image='Highlight.jpg'; Seconds=10; Kicker='COSMOLOGICAL EXTENSION'; Title='The same structure extends to FRW spacetime'; Body='Worldline geometry, identity evolution, and scaling laws share one operator framework' },
    @{ Name='08_end'; Image='Highlight.jpg'; Seconds=7; Kicker='CONCLUSION'; Title='One operator. Coupled geometries. Testable questions.'; Body='A phenomenological framework for unified geometric behavior' }
)

$clips = @()
foreach ($scene in $scenes) {
    $input = Join-Path $root $scene.Image
    $output = Join-Path $work ($scene.Name + '.mp4')
    $kicker = $scene.Kicker.Replace(':','\\:').Replace("'","\\'")
    $title = $scene.Title.Replace(':','\\:').Replace("'","\\'")
    $body = $scene.Body.Replace(':','\\:').Replace("'","\\'")
    $filter = "scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,zoompan=z='min(zoom+0.00035,1.08)':d=1:s=1280x720:fps=30,drawbox=x=0:y=0:w=1280:h=720:color=0x08141ccc:t=fill,drawbox=x=0:y=0:w=1280:h=8:color=0xD9942B:t=fill,drawtext=fontfile='$bold':text='$kicker':fontcolor=0xF4C46A:fontsize=22:x=70:y=70,drawtext=fontfile='$bold':text='$title':fontcolor=white:fontsize=42:x=70:y=125:line_spacing=8,drawtext=fontfile='$font':text='$body':fontcolor=0xE5E9EC:fontsize=25:x=70:y=610:line_spacing=6"
    & $ffmpeg -y -loglevel error -loop 1 -i $input -t $scene.Seconds -vf $filter -r 30 -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -an $output
    $clips += $output
}

$list = Join-Path $work 'concat.txt'
$lines = $clips | ForEach-Object { "file '$_'" }
Set-Content -Path $list -Value $lines -Encoding ascii
$outputVideo = Join-Path $root 'JMP_Video_Abstract_Unified_Geometric_Field_Theory.mp4'
& $ffmpeg -y -loglevel error -f concat -safe 0 -i $list -c copy $outputVideo
Write-Output "Created: $outputVideo"
& $ffmpeg -i $outputVideo -hide_banner 2>&1 | Select-String 'Duration|Video:'
