$ErrorActionPreference = "Continue"

function Pause {
    Write-Host "`nPressione qualquer tecla para continuar..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}

try {
    Clear-Host
    
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "     Git Commit Facilitado" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    
    $isGitRepo = git rev-parse --git-dir 2>$null
    if (-not $isGitRepo) {
        Write-Host "ERRO: Nao e um repositorio Git!" -ForegroundColor Red
        Pause
        exit
    }
    
    Write-Host "Status atual:" -ForegroundColor Yellow
    git status --short
    Write-Host ""
    
    $verDiff = Read-Host "Ver mudancas detalhadas? (s/n)"
    if ($verDiff -eq "s" -or $verDiff -eq "S") {
        git diff
        Write-Host ""
    }
    
    Write-Host "O que adicionar?" -ForegroundColor Blue
    Write-Host "  1) Adicionar TUDO"
    Write-Host "  2) Arquivos especificos"
    Write-Host "  3) Apenas backend/"
    Write-Host "  4) Apenas frontend/"
    $opcao = Read-Host "Escolha (1-4)"
    
    switch ($opcao) {
        "1" { 
            git add .
            Write-Host "Tudo adicionado" -ForegroundColor Green
        }
        "2" {
            $arquivos = Read-Host "Digite os arquivos"
            Invoke-Expression "git add $arquivos"
            Write-Host "Arquivos adicionados" -ForegroundColor Green
        }
        "3" {
            git add backend/
            Write-Host "Backend adicionado" -ForegroundColor Green
        }
        "4" {
            git add frontend/
            Write-Host "Frontend adicionado" -ForegroundColor Green
        }
        default {
            Write-Host "Opcao invalida!" -ForegroundColor Red
            Pause
            exit
        }
    }
    
    Write-Host "`nSera commitado:" -ForegroundColor Yellow
    git status --short
    Write-Host ""
    
    Write-Host "Sugestoes:" -ForegroundColor Magenta
    Write-Host "  - feat: nova funcionalidade"
    Write-Host "  - fix: correcao de bug"
    Write-Host "  - docs: documentacao"
    Write-Host "  - refactor: refatoracao"
    Write-Host ""
    
    $mensagem = Read-Host "Digite a mensagem do commit"
    
    if ([string]::IsNullOrWhiteSpace($mensagem)) {
        Write-Host "Mensagem vazia! Abortando..." -ForegroundColor Red
        Pause
        exit
    }
    
    Write-Host "`nFazendo commit..." -ForegroundColor Yellow
    git commit -m "$mensagem"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Commit realizado com sucesso!" -ForegroundColor Green
        
        Write-Host ""
        $push = Read-Host "Fazer push para GitHub? (s/n)"
        
        if ($push -eq "s" -or $push -eq "S") {
            Write-Host "`nFazendo push..." -ForegroundColor Yellow
            git push
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Push realizado com sucesso!" -ForegroundColor Green
            } else {
                Write-Host "Erro ao fazer push!" -ForegroundColor Red
            }
        } else {
            Write-Host "Push nao realizado." -ForegroundColor Blue
        }
    } else {
        Write-Host "Erro ao fazer commit!" -ForegroundColor Red
    }
    
} catch {
    Write-Host "`nERRO: $_" -ForegroundColor Red
} finally {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Pause
}