param (
    [string]$Version = "latest"
)

$ImageName = "aditya040305/drift-guard-agent"

Write-Host "Building Docker image ${ImageName}:${Version}..."
docker build -t "${ImageName}:${Version}" .

if ($LASTEXITCODE -ne 0) {
    Write-Error "Docker build failed."
    exit $LASTEXITCODE
}

Write-Host "Tagging as latest..."
docker tag "${ImageName}:${Version}" "${ImageName}:latest"

Write-Host "Pushing ${ImageName}:${Version} to Docker Hub..."
docker push "${ImageName}:${Version}"

Write-Host "Pushing ${ImageName}:latest to Docker Hub..."
docker push "${ImageName}:latest"

Write-Host "Done!"
