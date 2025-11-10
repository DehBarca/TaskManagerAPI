#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Script para ejecutar Ruff y generar reportes para SonarQube
    
.DESCRIPTION
    Este script ejecuta el linter Ruff en el código del proyecto y genera:
    1. Reporte JSON para integración con SonarQube
    2. Reporte legible en consola
    3. Validación de estilo de código
    
.EXAMPLE
    .\run-linter.ps1
    
.EXAMPLE
    .\run-linter.ps1 -Fix
    Para arreglar automáticamente los problemas encontrados
#>

param(
    [switch]$Fix,
    [switch]$Format
)

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "🔍 RUFF - Análisis de Calidad de Código" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Verificar si Ruff está instalado
$ruffInstalled = Get-Command ruff -ErrorAction SilentlyContinue
if (-not $ruffInstalled) {
    Write-Host "❌ Error: Ruff no está instalado" -ForegroundColor Red
    Write-Host "💡 Instala con: pip install ruff" -ForegroundColor Yellow
    exit 1
}

# Mostrar versión de Ruff
$ruffVersion = ruff --version
Write-Host "📦 Versión: $ruffVersion" -ForegroundColor Gray
Write-Host ""

# Paso 1: Linting con reporte JSON para SonarQube
Write-Host "📋 Paso 1/3: Ejecutando linting..." -ForegroundColor Yellow
Write-Host "   Generando reporte JSON para SonarQube..." -ForegroundColor Gray

if ($Fix) {
    ruff check src/ tests/ --fix --output-format=json > ruff-report.json
    $lintExitCode = $LASTEXITCODE
} else {
    ruff check src/ tests/ --output-format=json > ruff-report.json
    $lintExitCode = $LASTEXITCODE
}

# Mostrar también en consola (formato legible)
Write-Host ""
Write-Host "   Resultado en consola:" -ForegroundColor Gray
ruff check src/ tests/
Write-Host ""

# Paso 2: Verificar formato de código
Write-Host "📐 Paso 2/3: Verificando formato..." -ForegroundColor Yellow

if ($Format) {
    ruff format src/ tests/
    Write-Host "   ✅ Código formateado" -ForegroundColor Green
} else {
    ruff format --check src/ tests/
    $formatExitCode = $LASTEXITCODE
    
    if ($formatExitCode -eq 0) {
        Write-Host "   ✅ Formato correcto" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Hay archivos con formato incorrecto" -ForegroundColor Yellow
        Write-Host "   💡 Ejecuta: .\run-linter.ps1 -Format" -ForegroundColor Cyan
    }
}

Write-Host ""

# Paso 3: Análisis del reporte JSON
Write-Host "📊 Paso 3/3: Analizando resultados..." -ForegroundColor Yellow

if (Test-Path "ruff-report.json") {
    $reportContent = Get-Content "ruff-report.json" -Raw | ConvertFrom-Json
    $issueCount = $reportContent.Count
    
    Write-Host "   📄 Reporte generado: ruff-report.json" -ForegroundColor Green
    Write-Host "   📊 Issues encontrados: $issueCount" -ForegroundColor $(if ($issueCount -eq 0) { "Green" } else { "Yellow" })
    
    if ($issueCount -gt 0) {
        # Agrupar por tipo de issue
        $issuesByType = $reportContent | Group-Object -Property code | Sort-Object Count -Descending
        
        Write-Host ""
        Write-Host "   📈 Resumen por tipo de issue:" -ForegroundColor Cyan
        foreach ($group in $issuesByType | Select-Object -First 5) {
            Write-Host "      • $($group.Name): $($group.Count) ocurrencias" -ForegroundColor White
        }
    }
} else {
    Write-Host "   ⚠️  No se pudo generar ruff-report.json" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan

# Resumen final
if ($lintExitCode -eq 0) {
    Write-Host "✅ ÉXITO: El código cumple con todas las reglas de linting" -ForegroundColor Green
    Write-Host ""
    Write-Host "📤 Siguiente paso:" -ForegroundColor Cyan
    Write-Host "   Ejecuta el análisis de SonarQube:" -ForegroundColor White
    Write-Host "   .\run-sonar-docker.ps1" -ForegroundColor Yellow
    exit 0
} else {
    Write-Host "⚠️  ADVERTENCIA: Se encontraron $issueCount problemas" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "💡 Opciones para arreglar:" -ForegroundColor Cyan
    Write-Host "   1. Automático: .\run-linter.ps1 -Fix -Format" -ForegroundColor White
    Write-Host "   2. Manual: Revisa los errores arriba" -ForegroundColor White
    Write-Host ""
    Write-Host "📤 Puedes continuar con SonarQube de todas formas:" -ForegroundColor Cyan
    Write-Host "   .\run-sonar-docker.ps1" -ForegroundColor Yellow
    exit 1
}
