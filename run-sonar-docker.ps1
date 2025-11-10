#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Levanta SonarQube en Docker y ejecuta SonarScanner para analizar el proyecto.

.DESCRIPTION
    - Requiere Docker instalado y en ejecución.
    - Requiere que exista `sonar-project.properties` en la raíz del repo.
    - Usa la variable de entorno SONAR_TOKEN para autenticar el scanner (opcional si SonarQube en local no requiere token).

.USAGE
    .\run-sonar-docker.ps1

.NOTES
    - El script levanta un contenedor de SonarQube (versión LTS). Si ya tiene SonarQube corriendo en localhost:9000, no es necesario levantar el contenedor.
#>

param(
    [int]$SonarPort = 9000,
    [string]$SonarVersion = "sonarqube:9.9-community",
    [switch]$NoUp,
    [int]$ScannerTimeoutSeconds = 300
)

Write-Host "👷 Iniciando SonarQube local (Docker) y SonarScanner..." -ForegroundColor Cyan

# Verificar Docker
$docker = Get-Command docker -ErrorAction SilentlyContinue
if (-not $docker) {
    Write-Host "❌ Docker no está instalado o no está en PATH." -ForegroundColor Red
    exit 1
}

# Verificar sonar-project.properties
if (-not (Test-Path -Path "sonar-project.properties")) {
    Write-Host "⚠️ No se encontró 'sonar-project.properties' en la raíz del proyecto." -ForegroundColor Yellow
    Write-Host "Asegúrese de que existe y contiene la configuración del proyecto SonarQube." -ForegroundColor Yellow
}

# Si la imagen ya está corriendo, avisar
$existing = docker ps --filter "ancestor=$SonarVersion" --format "{{.ID}}" | Out-String
if ($existing.Trim() -ne "") {
    Write-Host "ℹ️ Ya hay un contenedor de SonarQube corriendo con la imagen $SonarVersion" -ForegroundColor Green
} elseif (-not $NoUp) {
    Write-Host "⏳ Levantando contenedor SonarQube ($SonarVersion) en el puerto $SonarPort..." -ForegroundColor Yellow
    docker run -d --rm --name sonarqube-local -p ${SonarPort}:9000 -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true $SonarVersion | Out-Null

    Write-Host "🔎 Esperando a que SonarQube esté listo (puede tardar ~30-60s)..." -ForegroundColor Gray
    $start = Get-Date
    $ready = $false
    while ((Get-Date) - $start -lt ([TimeSpan]::FromMinutes(5))) {
        try {
            $resp = Invoke-WebRequest -UseBasicParsing -Uri "http://localhost:$SonarPort" -TimeoutSec 5 -ErrorAction Stop
            if ($resp.StatusCode -eq 200) {
                $ready = $true
                break
            }
        } catch {
            Start-Sleep -Seconds 5
        }
    }

    if (-not $ready) {
        Write-Host "❌ SonarQube no respondió en el puerto $SonarPort en el tiempo esperado." -ForegroundColor Red
        Write-Host "Revise los logs del contenedor: docker logs sonarqube-local" -ForegroundColor Yellow
        exit 1
    }
    Write-Host "✅ SonarQube está corriendo en http://localhost:$SonarPort" -ForegroundColor Green
}

# Preparar token/host para SonarScanner
$sonarHostUrl = "http://host.docker.internal:$SonarPort"
if (-not $env:SONAR_TOKEN) {
    Write-Host "⚠️ No se encontró la variable de entorno SONAR_TOKEN. Si su SonarQube requiere autenticación, exporte SONAR_TOKEN antes de ejecutar este script." -ForegroundColor Yellow
}

# Ejecutar SonarScanner en un contenedor temporal
Write-Host "🔎 Ejecutando SonarScanner (Docker)..." -ForegroundColor Cyan

# Mapear el proyecto actual al contenedor
$projectDir = (Get-Location).Path

# Construir argumentos para el comando docker run del scanner usando un array (evita problemas con flags y comillas)
$envArgs = @()
$envArgs += "-e"
$envArgs += "SONAR_HOST_URL=$sonarHostUrl"
if ($env:SONAR_TOKEN) {
    $envArgs += "-e"
    $envArgs += "SONAR_TOKEN=$env:SONAR_TOKEN"
}

$dockerArgs = @("run", "--rm", "-v", "$projectDir:/usr/src") + $envArgs + @("sonarsource/sonar-scanner-cli", "/bin/sh", "-c", "cd /usr/src && sonar-scanner -Dsonar.projectBaseDir=/usr/src")

Write-Host "🔁 Ejecutando: docker $($dockerArgs -join ' ')" -ForegroundColor Gray

try {
    & docker @dockerArgs
    $exit = $LASTEXITCODE
} catch {
    Write-Host "❌ Error al ejecutar SonarScanner: $_" -ForegroundColor Red
    exit 1
}

if ($exit -ne 0) {
    Write-Host "❌ SonarScanner finalizó con código $exit" -ForegroundColor Red
    Write-Host "Verifique que 'sonar.projectKey' y otras propiedades en sonar-project.properties sean correctas." -ForegroundColor Yellow
    exit $exit
}

Write-Host "✅ SonarScanner completado. Revisar el dashboard en http://localhost:$SonarPort" -ForegroundColor Green

Write-Host "🔔 Nota: Si SonarQube fue levantado por este script y desea detenerlo, ejecute: docker stop sonarqube-local" -ForegroundColor Cyan
# Script para ejecutar SonarQube Scanner usando Docker
# No requiere instalar SonarScanner localmente

Write-Host "🐳 Ejecutando análisis de SonarQube con Docker..." -ForegroundColor Cyan
Write-Host ""

# Verificar que Docker esté instalado
$docker = Get-Command docker -ErrorAction SilentlyContinue

if (-not $docker) {
    Write-Host "❌ Error: Docker no está instalado" -ForegroundColor Red
    Write-Host ""
    Write-Host "Instala Docker Desktop desde: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Verificar que Docker esté corriendo
try {
    docker ps | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw "Docker no está corriendo"
    }
} catch {
    Write-Host "❌ Error: Docker no está corriendo" -ForegroundColor Red
    Write-Host "Por favor, inicia Docker Desktop y vuelve a intentar" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Docker está corriendo" -ForegroundColor Green
Write-Host ""

# Verificar que SonarQube Server esté corriendo
$sonarUrl = "http://localhost:9000"
$sonarRunning = $false

try {
    $response = Invoke-WebRequest -Uri "$sonarUrl/api/system/status" -Method GET -TimeoutSec 2 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        $sonarRunning = $true
    }
} catch {
    $sonarRunning = $false
}

if (-not $sonarRunning) {
    Write-Host "⚠️  SonarQube Server no está corriendo en $sonarUrl" -ForegroundColor Yellow
    Write-Host ""
    $startSonar = Read-Host "¿Deseas iniciar SonarQube Server con Docker? (S/N)"
    
    if ($startSonar -eq "S" -or $startSonar -eq "s") {
        Write-Host ""
        Write-Host "🚀 Iniciando SonarQube Server..." -ForegroundColor Cyan
        
        # Detener contenedor existente si existe
        docker stop sonarqube 2>$null
        docker rm sonarqube 2>$null
        
        # Iniciar SonarQube
        docker run -d --name sonarqube -p 9000:9000 sonarqube:latest
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ SonarQube Server iniciado" -ForegroundColor Green
            Write-Host ""
            Write-Host "⏳ Esperando a que SonarQube esté listo (esto puede tardar 1-2 minutos)..." -ForegroundColor Cyan
            
            $maxAttempts = 60
            $attempt = 0
            $ready = $false
            
            while ($attempt -lt $maxAttempts -and -not $ready) {
                Start-Sleep -Seconds 5
                try {
                    $response = Invoke-WebRequest -Uri "$sonarUrl/api/system/status" -Method GET -TimeoutSec 2 -UseBasicParsing
                    $status = ($response.Content | ConvertFrom-Json).status
                    if ($status -eq "UP") {
                        $ready = $true
                    }
                } catch {
                    Write-Host "." -NoNewline
                }
                $attempt++
            }
            
            if ($ready) {
                Write-Host ""
                Write-Host "✅ SonarQube está listo!" -ForegroundColor Green
                Write-Host ""
                Write-Host "🔐 Accede a: $sonarUrl" -ForegroundColor Cyan
                Write-Host "   Usuario: admin" -ForegroundColor White
                Write-Host "   Contraseña: admin" -ForegroundColor White
                Write-Host ""
                Write-Host "⚠️  IMPORTANTE: Genera un token de acceso en:" -ForegroundColor Yellow
                Write-Host "   My Account → Security → Generate Tokens" -ForegroundColor White
                Write-Host ""
                $continue = Read-Host "Presiona Enter cuando hayas generado el token"
            } else {
                Write-Host ""
                Write-Host "⏱️  Tiempo de espera agotado. SonarQube puede tardar más en iniciar." -ForegroundColor Yellow
                Write-Host "   Verifica el estado en: $sonarUrl" -ForegroundColor White
                exit 1
            }
        } else {
            Write-Host "❌ Error al iniciar SonarQube" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host ""
        Write-Host "⚠️  No se puede continuar sin SonarQube Server" -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "✅ SonarQube Server está corriendo en $sonarUrl" -ForegroundColor Green
Write-Host ""

# Solicitar token si no está configurado
$token = $env:SONAR_TOKEN
if (-not $token -or $token -eq "squ_7e03efe21ed39abb1ef496a402fb224c56c99f06") {
    Write-Host "🔑 Token de SonarQube no configurado" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Genera un token en: $sonarUrl/account/security" -ForegroundColor Cyan
    Write-Host ""
    $token = Read-Host "Ingresa tu token de SonarQube"
    if (-not $token) {
        Write-Host "❌ Token requerido para continuar" -ForegroundColor Red
        exit 1
    }
}

# Generar reporte de cobertura
Write-Host "📊 Generando reporte de cobertura..." -ForegroundColor Cyan
pytest --cov=src --cov-report=xml --cov-report=html --cov-report=term

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error al ejecutar las pruebas" -ForegroundColor Red
    exit 1
}

# Verificar que existe el reporte de cobertura
if (-not (Test-Path "coverage.xml")) {
    Write-Host "⚠️  Advertencia: No se generó coverage.xml" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🚀 Ejecutando análisis con Docker..." -ForegroundColor Cyan
Write-Host ""

# Obtener ruta absoluta del proyecto
$projectPath = (Get-Location).Path

# Ejecutar sonar-scanner en Docker
docker run --rm `
    -v "${projectPath}:/usr/src" `
    -e SONAR_HOST_URL="$sonarUrl" `
    -e SONAR_TOKEN="$token" `
    sonarsource/sonar-scanner-cli `
    -Dsonar.projectKey=TaskManagerAPI `
    -Dsonar.sources=src `
    -Dsonar.tests=tests `
    -Dsonar.python.coverage.reportPaths=coverage.xml `
    -Dsonar.projectBaseDir=/usr/src

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Análisis completado exitosamente!" -ForegroundColor Green
    Write-Host "📈 Revisa los resultados en: $sonarUrl/dashboard?id=TaskManagerAPI" -ForegroundColor Cyan
    Write-Host ""
    
    # Abrir navegador
    $openBrowser = Read-Host "¿Deseas abrir el dashboard en el navegador? (S/N)"
    if ($openBrowser -eq "S" -or $openBrowser -eq "s") {
        Start-Process "$sonarUrl/dashboard?id=TaskManagerAPI"
    }
} else {
    Write-Host ""
    Write-Host "❌ Error al ejecutar el análisis" -ForegroundColor Red
    Write-Host ""
    Write-Host "Verifica:" -ForegroundColor Yellow
    Write-Host "  • Que el token sea correcto" -ForegroundColor White
    Write-Host "  • Que SonarQube Server esté corriendo" -ForegroundColor White
    Write-Host "  • Los logs del contenedor: docker logs sonarqube" -ForegroundColor White
    exit 1
}
