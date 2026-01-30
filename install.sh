#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# Define Dictionary Tool - Installer / Установщик словаря Define
# ═══════════════════════════════════════════════════════════════════════════════

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${BLUE}${BOLD}"
cat << 'EOF'
    +===============================================================+
    |                                                               |
    |       DEFINE - Terminal Dictionary / Терминальный словарь    |
    |                                                               |
    +===============================================================+
EOF
echo -e "${NC}"

# Detect OS
OS="$(uname -s)"
echo -e "${CYAN}Detected OS / Обнаружена ОС:${NC} $OS"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Version selection
echo ""
echo -e "${BOLD}Choose version to install / Выберите версию:${NC}"
echo ""
echo -e "  ${GREEN}[1]${NC} Python (recommended / рекомендуется)"
echo -e "      - Full grammar support (cases, conjugation, gender)"
echo -e "      - 180+ idioms database"
echo -e "      - No external dependencies (Python stdlib only)"
echo ""
echo -e "  ${YELLOW}[2]${NC} Bash (lightweight / легковесный)"
echo -e "      - Single file, 2955 lines"
echo -e "      - Requires: curl, jq"
echo -e "      - Original battle-tested version"
echo ""
echo -e "  ${CYAN}[3]${NC} Both (as define-py and define-bash)"
echo ""

read -p "Enter choice / Введите выбор [1/2/3]: " VERSION_CHOICE

case "$VERSION_CHOICE" in
    1|2|3) ;;
    *) echo -e "${RED}Invalid choice. Exiting.${NC}"; exit 1 ;;
esac

# Check dependencies based on choice
if [[ "$VERSION_CHOICE" == "2" || "$VERSION_CHOICE" == "3" ]]; then
    echo -e "\n${YELLOW}Checking bash dependencies / Проверка зависимостей bash...${NC}"
    MISSING=()
    command -v curl &>/dev/null || MISSING+=("curl")
    command -v jq &>/dev/null || MISSING+=("jq")

    if [[ ${#MISSING[@]} -gt 0 ]]; then
        echo -e "${RED}Missing / Отсутствует: ${MISSING[*]}${NC}"
        echo ""
        if [[ "$OS" == "Darwin" ]]; then
            echo -e "Install with / Установите: ${GREEN}brew install ${MISSING[*]}${NC}"
        elif command -v apt &>/dev/null; then
            echo -e "Install with / Установите: ${GREEN}sudo apt install ${MISSING[*]}${NC}"
        elif command -v pacman &>/dev/null; then
            echo -e "Install with / Установите: ${GREEN}sudo pacman -S ${MISSING[*]}${NC}"
        fi
        echo ""
        read -p "Continue anyway? / Продолжить? [y/N] " -n 1 -r
        echo
        [[ ! $REPLY =~ ^[Yy]$ ]] && exit 1
    else
        echo -e "${GREEN}* All bash dependencies installed${NC}"
    fi
fi

if [[ "$VERSION_CHOICE" == "1" || "$VERSION_CHOICE" == "3" ]]; then
    echo -e "\n${YELLOW}Checking Python / Проверка Python...${NC}"
    if ! command -v python3 &>/dev/null; then
        echo -e "${RED}Error: Python 3 not found / Python 3 не найден${NC}"
        echo -e "Install Python 3.8+ and try again"
        exit 1
    fi
    PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
    echo -e "${GREEN}* Python ${PYTHON_VERSION} found${NC}"
fi

# Determine install location
DEFAULT_DIR="$HOME/.local/bin"
if [[ "$OS" == "Darwin" ]]; then
    [[ -d "$HOME/bin" ]] && DEFAULT_DIR="$HOME/bin"
fi

echo -e "\n${YELLOW}Where to install? / Куда установить?${NC}"
echo -e "Default / По умолчанию: ${CYAN}$DEFAULT_DIR${NC}"
read -p "Press Enter for default or type path: " INSTALL_DIR
INSTALL_DIR="${INSTALL_DIR:-$DEFAULT_DIR}"
INSTALL_DIR="${INSTALL_DIR/#\~/$HOME}"

mkdir -p "$INSTALL_DIR"

# Install functions
install_python() {
    local suffix="$1"
    echo -e "\n${YELLOW}Installing Python version...${NC}"
    
    # Create wrapper scripts that call the Python CLI
    cat > "${INSTALL_DIR}/define${suffix}" << EOF
#!/bin/bash
exec python3 "${SCRIPT_DIR}/cli.py" "\$@"
EOF
    chmod +x "${INSTALL_DIR}/define${suffix}"
    echo -e "${GREEN}*${NC} define${suffix}"
    
    for cmd in определить словарь слово; do
        cat > "${INSTALL_DIR}/${cmd}${suffix}" << EOF
#!/bin/bash
exec python3 "${SCRIPT_DIR}/cli.py" "\$@"
EOF
        chmod +x "${INSTALL_DIR}/${cmd}${suffix}"
        echo -e "${GREEN}*${NC} ${cmd}${suffix}"
    done
}

install_bash() {
    local suffix="$1"
    echo -e "\n${YELLOW}Installing Bash version...${NC}"
    
    cp "${SCRIPT_DIR}/bash/define" "${INSTALL_DIR}/define${suffix}"
    chmod +x "${INSTALL_DIR}/define${suffix}"
    echo -e "${GREEN}*${NC} define${suffix}"
    
    for cmd in определить словарь слово; do
        if [[ -f "${SCRIPT_DIR}/bash/${cmd}" ]]; then
            cp "${SCRIPT_DIR}/bash/${cmd}" "${INSTALL_DIR}/${cmd}${suffix}"
            chmod +x "${INSTALL_DIR}/${cmd}${suffix}"
            echo -e "${GREEN}*${NC} ${cmd}${suffix}"
        fi
    done
}

# Install based on choice
case "$VERSION_CHOICE" in
    1)
        install_python ""
        ;;
    2)
        install_bash ""
        ;;
    3)
        install_python "-py"
        install_bash "-bash"
        echo ""
        echo -e "${CYAN}Both versions installed. Set default 'define' command?${NC}"
        echo -e "  [1] Python (define-py)"
        echo -e "  [2] Bash (define-bash)"
        echo -e "  [3] None (use define-py or define-bash explicitly)"
        read -p "Choice [1/2/3]: " DEFAULT_CHOICE
        
        case "$DEFAULT_CHOICE" in
            1)
                ln -sf "${INSTALL_DIR}/define-py" "${INSTALL_DIR}/define"
                for cmd in определить словарь слово; do
                    ln -sf "${INSTALL_DIR}/${cmd}-py" "${INSTALL_DIR}/${cmd}"
                done
                echo -e "${GREEN}* Default set to Python${NC}"
                ;;
            2)
                ln -sf "${INSTALL_DIR}/define-bash" "${INSTALL_DIR}/define"
                for cmd in определить словарь слово; do
                    ln -sf "${INSTALL_DIR}/${cmd}-bash" "${INSTALL_DIR}/${cmd}"
                done
                echo -e "${GREEN}* Default set to Bash${NC}"
                ;;
            *)
                echo "No default set. Use define-py or define-bash."
                ;;
        esac
        ;;
esac

# Check if in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo -e "\n${YELLOW}NOTE: Add to PATH / Добавьте в PATH:${NC}"
    
    SHELL_NAME=$(basename "$SHELL")
    if [[ "$SHELL_NAME" == "zsh" ]]; then
        RC_FILE="$HOME/.zshrc"
    elif [[ "$SHELL_NAME" == "bash" ]]; then
        [[ "$OS" == "Darwin" ]] && RC_FILE="$HOME/.bash_profile" || RC_FILE="$HOME/.bashrc"
    else
        RC_FILE="$HOME/.profile"
    fi
    
    echo -e "Add this line to ${CYAN}$RC_FILE${NC}:"
    echo -e "${GREEN}export PATH=\"$INSTALL_DIR:\$PATH\"${NC}"
    echo ""
    read -p "Add automatically? / Добавить автоматически? [Y/n] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        echo "" >> "$RC_FILE"
        echo "# Define dictionary tool" >> "$RC_FILE"
        echo "export PATH=\"$INSTALL_DIR:\$PATH\"" >> "$RC_FILE"
        echo -e "${GREEN}* Added to $RC_FILE${NC}"
        echo -e "${YELLOW}Run: source $RC_FILE${NC}"
    fi
fi

echo -e "\n${GREEN}${BOLD}Installation complete! / Установка завершена!${NC}"
echo ""
echo -e "${BLUE}Try it / Попробуйте:${NC}"
echo -e "  define hello"
echo -e "  define -f love"
echo -e "  определить привет"
echo ""
