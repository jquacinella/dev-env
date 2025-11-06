#!/bin/bash

# Ubuntu Development Environment Setup Script
# This script installs uv and sets up a local virtual environment for running Ansible

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_header() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════${NC}"
    echo ""
}

# Check if running on a supported OS
check_os() {
    print_header "Checking Operating System"
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            print_info "Detected OS: $NAME $VERSION"
            
            if [[ "$ID" == "ubuntu" ]] || [[ "$ID" == "debian" ]] || [[ "$ID_LIKE" == *"ubuntu"* ]] || [[ "$ID_LIKE" == *"debian"* ]]; then
                print_success "Supported OS detected"
            else
                print_warning "This script is designed for Ubuntu/Debian. Your OS may work but is untested."
                read -p "Continue anyway? (y/N) " -n 1 -r
                echo
                if [[ ! $REPLY =~ ^[Yy]$ ]]; then
                    print_error "Setup cancelled"
                    exit 1
                fi
            fi
        fi
    else
        print_warning "Non-Linux OS detected: $OSTYPE"
        print_warning "This script is designed for Linux. Proceed with caution."
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_error "Setup cancelled"
            exit 1
        fi
    fi
}

# Check for required dependencies
check_dependencies() {
    print_header "Checking Dependencies"
    
    local missing_deps=()
    
    if ! command -v curl &> /dev/null; then
        missing_deps+=("curl")
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Missing required dependencies: ${missing_deps[*]}"
        print_info "Please install them first:"
        print_info "  sudo apt update && sudo apt install -y ${missing_deps[*]}"
        exit 1
    fi
    
    print_success "All required dependencies are installed"
}

# Install uv if not present
install_uv() {
    print_header "Installing uv"
    
    if command -v uv &> /dev/null; then
        UV_VERSION=$(uv --version 2>&1 | head -n1)
        print_success "uv is already installed: $UV_VERSION"
        return 0
    fi
    
    print_info "Installing uv package manager..."
    
    if curl -LsSf https://astral.sh/uv/install.sh | sh; then
        print_success "uv installed successfully"
        
        # Add uv to PATH for current session
        export PATH="$HOME/.local/bin:$PATH"
        
        # Verify installation
        if command -v uv &> /dev/null; then
            UV_VERSION=$(uv --version 2>&1 | head -n1)
            print_success "Verified uv installation: $UV_VERSION"
        else
            print_error "uv installation completed but command not found in PATH"
            print_info "You may need to restart your shell or run: source ~/.bashrc (or ~/.zshrc)"
            exit 1
        fi
    else
        print_error "Failed to install uv"
        print_info "Please install uv manually: https://github.com/astral-sh/uv"
        exit 1
    fi
}

# Create virtual environment
create_venv() {
    print_header "Creating Virtual Environment"
    
    local VENV_DIR=".venv"
    
    if [ -d "$VENV_DIR" ]; then
        print_warning "Virtual environment already exists at $VENV_DIR"
        read -p "Recreate it? This will remove the existing environment. (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Removing existing virtual environment..."
            rm -rf "$VENV_DIR"
        else
            print_info "Using existing virtual environment"
            return 0
        fi
    fi
    
    print_info "Creating virtual environment in $VENV_DIR..."
    
    if uv --native-tls venv "$VENV_DIR"; then
        print_success "Virtual environment created successfully"
    else
        print_error "Failed to create virtual environment"
        exit 1
    fi
}

# Install Ansible and dependencies
install_ansible() {
    print_header "Installing Ansible and Dependencies"
    
    print_info "Installing packages: ansible, jinja2, pyyaml"
    
    # Activate virtual environment for installation
    source .venv/bin/activate
    
    if uv --native-tls pip install ansible jinja2 pyyaml; then
        print_success "Ansible and dependencies installed successfully"
        
        # Verify installation
        print_info "Verifying installation..."
        ANSIBLE_VERSION=$(ansible --version | head -n1)
        print_success "Installed: $ANSIBLE_VERSION"
    else
        print_error "Failed to install Ansible and dependencies"
        exit 1
    fi
    
    deactivate
}

# Install Ansible Galaxy collections
install_ansible_collections() {
    print_header "Installing Ansible Galaxy Collections"

    print_info "Installing containers.podman collection..."

    # Activate virtual environment for installation
    source .venv/bin/activate

    if ansible-galaxy collection install containers.podman; then
        print_success "containers.podman collection installed successfully"

        # Verify installation
        print_info "Verifying installation..."
        if ansible-galaxy collection list | grep -q "containers.podman"; then
            print_success "Verified: containers.podman collection is installed"
        else
            print_warning "Collection installed but not showing in list"
        fi
    else
        print_error "Failed to install containers.podman collection"
        exit 1
    fi

    deactivate
}

# Create activation helper script
create_activate_script() {
    print_header "Creating Activation Helper"
    
    local ACTIVATE_SCRIPT="activate.sh"
    
    cat > "$ACTIVATE_SCRIPT" << 'EOF'
#!/bin/bash

# Activation helper for dev-env virtual environment

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

VENV_DIR=".venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}⚠${NC} Virtual environment not found at $VENV_DIR"
    echo -e "${BLUE}ℹ${NC} Run ./setup.sh first to create the environment"
    return 1 2>/dev/null || exit 1
fi

# Check if already activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo -e "${YELLOW}⚠${NC} A virtual environment is already active: $VIRTUAL_ENV"
    echo -e "${BLUE}ℹ${NC} Deactivate it first with: deactivate"
    return 1 2>/dev/null || exit 1
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

echo -e "${GREEN}✓${NC} Virtual environment activated!"
echo ""
echo -e "${BLUE}Available commands:${NC}"
echo "  ansible-playbook dev-setup.yml --ask-become-pass  # Run full setup"
echo "  ansible-playbook dev-setup.yml --tags fzf         # Install specific tool"
echo "  ansible-playbook version-checks.yml               # Check for updates"
echo "  deactivate                                        # Exit virtual environment"
echo ""
EOF

    chmod +x "$ACTIVATE_SCRIPT"
    print_success "Created activation helper: $ACTIVATE_SCRIPT"
}

# Main setup function
main() {
    print_header "Ubuntu Development Environment Setup"
    
    print_info "This script will:"
    echo "  1. Check your operating system"
    echo "  2. Install uv package manager (if needed)"
    echo "  3. Create a local virtual environment (.venv)"
    echo "  4. Install Ansible and dependencies"
    echo "  5. Install Ansible Galaxy collections (containers.podman)"
    echo "  6. Create an activation helper script"
    echo ""
    
    # Run setup steps
    check_os
    check_dependencies
    install_uv
    create_venv
    install_ansible
    install_ansible_collections
    create_activate_script
    
    # Final success message
    print_header "Setup Complete!"
    
    echo -e "${GREEN}✓${NC} Your development environment is ready!"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "  1. Activate the virtual environment:"
    echo -e "     ${YELLOW}source activate.sh${NC}"
    echo ""
    echo "  2. Run the Ansible playbook:"
    echo -e "     ${YELLOW}ansible-playbook dev-setup.yml --ask-become-pass${NC}"
    echo ""
    echo -e "${BLUE}Note:${NC} You'll need to activate the virtual environment each time you"
    echo "      open a new terminal session."
    echo ""
}

# Run main function
main
