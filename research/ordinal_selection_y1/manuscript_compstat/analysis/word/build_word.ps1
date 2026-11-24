# Build the Word versions of the manuscript, supplement and cover letter.
# Usage: powershell -File build_word.ps1 -Python <python with nothing special> -NodeModules <dir containing docx and jszip> [-RenderDir <dir>]
# With -RenderDir, the documents are also exported to PDF through Microsoft Word (COM) for checking.
param(
  [Parameter(Mandatory = $true)][string]$Python,
  [Parameter(Mandatory = $true)][string]$NodeModules,
  [string]$RenderDir = ''
)
$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$ms = (Resolve-Path "$here/../..").Path
$tmp = Join-Path $env:TEMP 'compstat_word_build'
New-Item -ItemType Directory -Force $tmp | Out-Null
& $Python -B "$here/latex_to_json.py" $ms main "$tmp/main.json"
if ($LASTEXITCODE) { throw 'latex_to_json main failed' }
& $Python -B "$here/latex_to_json.py" $ms supplement "$tmp/supplement.json"
if ($LASTEXITCODE) { throw 'latex_to_json supplement failed' }
$env:NODE_PATH = $NodeModules
node "$here/build_docx.js" "$tmp/main.json" "$tmp/supplement.json" "$ms/figures" "$ms/cover_letter.txt" "$ms/word"
if ($LASTEXITCODE) { throw 'build_docx failed' }
$docs = 'manuscript', 'supplementary_information', 'cover_letter'
& $Python -B "$here/strip_zip_dirs.py" @($docs | ForEach-Object { "$ms/word/$_.docx" })
if ($RenderDir) {
  New-Item -ItemType Directory -Force $RenderDir | Out-Null
  $word = New-Object -ComObject Word.Application
  $word.Visible = $false
  $word.DisplayAlerts = 0
  try {
    foreach ($n in $docs) {
      $doc = $word.Documents.Open((Resolve-Path "$ms/word/$n.docx").Path, $false, $true)
      $pdf = (Join-Path (Resolve-Path $RenderDir).Path "$n.pdf")
      $doc.ExportAsFixedFormat($pdf, 17)
      "$n pages: $($doc.ComputeStatistics(2))"
      $doc.Close([ref]0)
    }
  } finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
  }
}
