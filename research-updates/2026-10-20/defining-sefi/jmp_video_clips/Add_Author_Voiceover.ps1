param(
    [Parameter(Mandatory=$true)][string]$AudioFile,
    [switch]$CleanVersion
)
$ErrorActionPreference = 'Stop'
$videoEncoder = 'C:/ffmpeg/ffmpeg-9.0.1-essentials_build/bin/ffmpeg.exe'
$videoProbe = 'C:/ffmpeg/ffmpeg-9.0.1-essentials_build/bin/ffprobe.exe'
$recording = (Resolve-Path -LiteralPath $AudioFile).Path
$sourceName = if ($CleanVersion) { 'JMP_Graphical_Abstract_Clean_1080p.mp4' } else { 'JMP_Graphical_Abstract_Captioned_1080p.mp4' }
$videoSource = Join-Path $PSScriptRoot $sourceName
$narratedOutput = Join-Path $PSScriptRoot 'JMP_Graphical_Abstract_With_Author_Voice.mp4'
if (Test-Path -LiteralPath $narratedOutput) { throw 'The narrated output already exists. Preserve or rename it before running again.' }
$recordingDuration = [double](& $videoProbe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 $recording)
if ($recordingDuration -lt 145 -or $recordingDuration -gt 155) { throw 'Record close to 150 seconds using the chapter timestamps. This helper does not time-stretch your voice.' }
& $videoEncoder -hide_banner -i $videoSource -i $recording -map 0:v:0 -map 1:a:0 -c:v libx264 -preset slow -b:v 330k -maxrate 360k -bufsize 720k -threads 2 -pix_fmt yuv420p -c:a aac -b:a 128k -af 'apad,atrim=duration=150,loudnorm=I=-16:TP=-1.5:LRA=11' -t 150 -movflags +faststart $narratedOutput
if ($LASTEXITCODE -ne 0) { throw 'Narrated video encoding failed.' }
if ((Get-Item -LiteralPath $narratedOutput).Length -ge 10000000) { throw 'The narrated file exceeds the 10 MB target and needs a smaller encode before upload.' }
Write-Output "Saved narrated video: $narratedOutput"
