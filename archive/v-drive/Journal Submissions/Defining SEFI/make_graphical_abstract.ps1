$ffmpeg = 'C:\ffmpeg\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe'
$font = 'C\:/Windows/Fonts/arial.ttf'
$output = 'Graphical_Abstract_SEFI.mp4'

& $ffmpeg -y `
  -loop 1 -t 5 -i 'Fig5_Photonic_Implementation.jpg' `
  -loop 1 -t 5 -i 'Fig2_Worldline_Geometry.jpg' `
  -loop 1 -t 5 -i 'Fig1_Stability_Surface.jpg' `
  -loop 1 -t 5 -i 'Highlight.jpg' `
  -filter_complex "
[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,zoompan=z='min(zoom+0.0007,1.06)':d=150:s=1920x1080:fps=30,drawbox=x=0:y=0:w=iw:h=170:color=black@0.52:t=fill,drawtext=fontfile='$font':text='FROM PHOTONIC INTUITION':fontcolor=white:fontsize=54:x=90:y=58,drawtext=fontfile='$font':text='Stable patterns can be measured, corrected, and understood geometrically.':fontcolor=white@0.92:fontsize=28:x=92:y=118,fade=t=in:st=0:d=0.5,fade=t=out:st=4.5:d=0.5,setpts=PTS-STARTPTS[v0];
[1:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,zoompan=z='min(zoom+0.0007,1.06)':d=150:s=1920x1080:fps=30,drawbox=x=0:y=0:w=iw:h=170:color=black@0.52:t=fill,drawtext=fontfile='$font':text='ONE CONTINUOUS ENTITY':fontcolor=white:fontsize=54:x=90:y=58,drawtext=fontfile='$font':text='A particle is represented as a worldline through spacetime.':fontcolor=white@0.92:fontsize=28:x=92:y=118,fade=t=in:st=0:d=0.5,fade=t=out:st=4.5:d=0.5,setpts=PTS-STARTPTS[v1];
[2:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,zoompan=z='min(zoom+0.0007,1.06)':d=150:s=1920x1080:fps=30,drawbox=x=0:y=0:w=iw:h=170:color=black@0.52:t=fill,drawtext=fontfile='$font':text='TWO ORIENTATIONS, ONE ENTITY':fontcolor=white:fontsize=54:x=90:y=58,drawtext=fontfile='$font':text='Electron and positron sectors become opposite orientations of one path.':fontcolor=white@0.92:fontsize=28:x=92:y=118,fade=t=in:st=0:d=0.5,fade=t=out:st=4.5:d=0.5,setpts=PTS-STARTPTS[v2];
[3:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,zoompan=z='min(zoom+0.0007,1.06)':d=150:s=1920x1080:fps=30,drawbox=x=0:y=0:w=iw:h=190:color=black@0.58:t=fill,drawtext=fontfile='$font':text='OBSERVER GEOMETRY':fontcolor=white:fontsize=54:x=90:y=58,drawtext=fontfile='$font':text='Quantum intuition begins where the entity and the observer meet.':fontcolor=white@0.92:fontsize=28:x=92:y=118,fade=t=in:st=0:d=0.5,fade=t=out:st=4.5:d=0.5,setpts=PTS-STARTPTS[v3];
[v0][v1]xfade=transition=fade:duration=0.8:offset=4.2[x1];
[x1][v2]xfade=transition=fade:duration=0.8:offset=8.4[x2];
[x2][v3]xfade=transition=fade:duration=0.8:offset=12.6,format=yuv420p[v]
" -map '[v]' -r 30 -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -movflags +faststart $output

if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Get-Item $output | Select-Object FullName,Length,LastWriteTime
& $ffmpeg -i $output -hide_banner 2>&1 | Select-String 'Duration|Stream #0:0'
