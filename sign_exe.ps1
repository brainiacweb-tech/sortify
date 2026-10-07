$thumbprint = "122CF6559D57CB5FE3D7C3F811679486548E01B9"
$cert = Get-Item "Cert:\CurrentUser\My\$thumbprint"
$exePath = Join-Path (Get-Location) "dist\SORTIFY.exe"

Write-Host "Signing executable: $exePath"
$result = Set-AuthenticodeSignature -FilePath $exePath -Certificate $cert -HashAlgorithm SHA256
Write-Host "Signature Type: $($result.SignatureType)"
Write-Host "Signer Subject: $($result.SignerCertificate.Subject)"
