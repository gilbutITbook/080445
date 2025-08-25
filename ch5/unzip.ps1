# ZIP 파일이 있는 폴더로 이동
Set-Location "C:\Path\To\ZipFiles"

# 압축을 풀 대상 루트 폴더
$extractFolder = "C:\Path\To\Extracted"

# 대상 폴더가 없으면 생성
if (-Not (Test-Path $extractFolder)) {
    New-Item -ItemType Directory -Path $extractFolder | Out-Null
}

# 모든 ZIP 파일을 찾아 압축 해제
Get-ChildItem -Filter *.zip | ForEach-Object {
    $zipFile = $_.FullName
    $subFolder = Join-Path $extractFolder $_.BaseName

    # 압축 해제
    Expand-Archive -Path $zipFile -DestinationPath $subFolder -Force
}
