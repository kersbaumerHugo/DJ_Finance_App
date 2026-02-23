#!/bin/bash

# Cores para deixar bonito
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # Sem cor

clear

echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║     🚀 Git Commit Facilitado 🚀       ║${NC}"
echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
echo ""

# Mostrar status atual
echo -e "${YELLOW}📊 Status atual:${NC}"
git status --short
echo ""

# Perguntar se quer ver diff
echo -e "${PURPLE}👀 Deseja ver as mudanças detalhadas? (s/n)${NC}"
read -r ver_diff
if [[ $ver_diff == "s" || $ver_diff == "S" ]]; then
    git diff
    echo ""
fi

# Perguntar o que adicionar
echo -e "${BLUE}📁 O que deseja adicionar?${NC}"
echo "  1) Adicionar TUDO (git add .)"
echo "  2) Adicionar arquivos específicos"
echo "  3) Adicionar apenas backend/"
echo "  4) Adicionar apenas frontend/"
echo -e "${BLUE}Escolha (1-4):${NC} "
read -r opcao_add

case $opcao_add in
    1)
        git add .
        echo -e "${GREEN}✅ Todos os arquivos adicionados${NC}"
        ;;
    2)
        echo -e "${BLUE}Digite os arquivos (ex: backend/models.py frontend/app.py):${NC}"
        read -r arquivos
        git add $arquivos
        echo -e "${GREEN}✅ Arquivos adicionados: $arquivos${NC}"
        ;;
    3)
        git add backend/
        echo -e "${GREEN}✅ Backend adicionado${NC}"
        ;;
    4)
        git add frontend/
        echo -e "${GREEN}✅ Frontend adicionado${NC}"
        ;;
    *)
        echo -e "${RED}❌ Opção inválida!${NC}"
        exit 1
        ;;
esac

echo ""

# Mostrar o que será commitado
echo -e "${YELLOW}📦 Arquivos que serão commitados:${NC}"
git status --short
echo ""

# Sugestões de mensagens
echo -e "${PURPLE}💡 Sugestões de mensagem:${NC}"
echo "  - feat: adiciona nova funcionalidade"
echo "  - fix: corrige bug no parser"
echo "  - docs: atualiza documentação"
echo "  - style: ajusta formatação"
echo "  - refactor: refatora código"
echo "  - test: adiciona testes"
echo "  - chore: atualiza dependências"
echo ""

# Pedir mensagem de commit
echo -e "${GREEN}✍️  Digite a mensagem do commit:${NC}"
read -r mensagem

if [ -z "$mensagem" ]; then
    echo -e "${RED}❌ Mensagem vazia! Abortando...${NC}"
    exit 1
fi

# Fazer o commit
git commit -m "$mensagem"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Commit realizado com sucesso!${NC}"
    echo ""
    
    # Perguntar se quer fazer push
    echo -e "${CYAN}🚀 Deseja fazer push para o GitHub? (s/n)${NC}"
    read -r fazer_push
    
    if [[ $fazer_push == "s" || $fazer_push == "S" ]]; then
        echo -e "${YELLOW}📤 Fazendo push...${NC}"
        git push
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}🎉 Push realizado com sucesso!${NC}"
        else
            echo -e "${RED}❌ Erro ao fazer push!${NC}"
        fi
    else
        echo -e "${BLUE}ℹ️  Push não realizado. Use 'git push' quando quiser.${NC}"
    fi
else
    echo -e "${RED}❌ Erro ao fazer commit!${NC}"
    exit 1
fi

echo ""
echo -e "${CYAN}╚════════════════════════════════════════╝${NC}"