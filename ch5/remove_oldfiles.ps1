# 압축 대상 파일이 있는 바탕화면의 경로
$desktopPath = [System.Environment]::GetFolderPath('Desktop')
# 1년 이상 수정되지 않은 파일 목록 가져오기
$oneYearAgo = (Get-Date).AddYears(-1)
$filesToCompress = Get-ChildItem -Path $desktopPath | `
Where-Object { $_.LastWriteTime -lt $oneYearAgo }
# 압축할 파일 목록 작성 
$filesToCompressList = $filesToCompress.FullName
#압축 파일 이름 지정(예: "DesktopArchive.zip"）
$archiveName = "DesktopArchive.zip"
$archivePath = Join-Path -Path $desktopPath -ChildPath $archiveName
# 파일 압축 
if ($filesToCompress.Count -gt 0) {
 Compress-Archive -Path $filesToCompressList -DestinationPath $archivePath
 Write-Host "ok"
 # 압축 후 원본 파일 삭제
 # Remove-Item -Path $filesToCompressList -Force
 # Write-Host "removed"
} else {
 Write-Host "not found"
}