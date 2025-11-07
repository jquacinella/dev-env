# Ubuntu Development Environment Setup

An Ansible playbook to automatically configure your Ubuntu development environment with modern CLI tools and configurations.

## Quick Start

Get started in 3 simple steps:

```bash
# 1. Run the setup script (installs uv and creates virtual environment)
./setup.sh

# 2. Activate the virtual environment
source activate.sh

# 3. Run the Ansible playbook
ansible-playbook dev-setup.yml --ask-become-pass
```

That's it! The setup script handles all prerequisites automatically.

## What's Included

### Installed Tools

#### Essential Development Tools
- **git**, **curl**, **wget**, **build-essential** - Core development utilities
- **augeas** - Configuration file editing tool

#### Shell & Terminal
- **zsh** - Modern shell with oh-my-zsh framework
- **spaceship-prompt** - Minimalistic, powerful and customizable Zsh prompt
- **tmux** - Terminal multiplexer with custom configuration
- **zsh-autosuggestions** - Fish-like autosuggestions for zsh
- **zsh-syntax-highlighting** - Fish-like syntax highlighting for zsh
- **zsh-history-substring-search** - Fish-like history search feature
- **zsh-fzf-history-search** - FZF-powered history search
- **zsh-completions** - Additional completion definitions for zsh
- **zellij** - Modern terminal workspace with layouts and panes

#### Containers & Virtualization
- **podman** - Daemonless container engine (requires Ubuntu 20.10+)
- **podman-tui** - Terminal UI for Podman
- **distrobox** - Container system integration for running any Linux distribution

#### File & Directory Navigation
- **fzf** - Fuzzy finder for command line
- **fd** - Fast and user-friendly alternative to find
- **broot** - Modern tree view and directory navigator
- **zoxide** - Smarter cd command that learns your habits
- **eza** - Modern replacement for ls with colors and git integration
- **lsd** - Modern ls replacement with icons and colors

#### Search & Text Processing
- **ripgrep (rg)** - Ultra-fast recursive search tool
- **up (Ultimate Plumber)** - Interactive pipe building tool
- **bat** - Cat clone with syntax highlighting and Git integration
- **hexyl** - Command-line hex viewer with colored output

#### Process & System Monitoring
- **procs** - Modern replacement for ps with colored output and tree view
- **bottom** - Cross-platform graphical process/system monitor
- **gping** - Ping tool with a graph
- **bandwhich** - Terminal bandwidth utilization tool

#### Version Control & Git
- **gitui** - Blazing fast terminal UI for git
- **lazygit** - Simple terminal UI for git commands

#### Development Tools & Editors
- **helix** - Post-modern modal text editor
- **nvm** - Node Version Manager
- **zeco** - Development environment container manager
- **zide** - Terminal-based IDE

#### Database & API Tools
- **lazysql** - Terminal UI for SQL databases
- **slumber** - Terminal-based API client

#### Documentation & Help
- **tldr** - Simplified and community-driven man pages with practical examples
- **navi** - Interactive cheatsheet tool for the command-line

#### Productivity & Utilities
- **ccze** - Colorizer for log files
- **dust** - Modern disk usage analyzer
- **xh** - Friendly HTTP client (HTTPie-like)
- **Espanso** - Cross-platform text expander
- **watchexec** - Executes commands in response to file modifications
- **asciinema** - Terminal session recorder
- **ssh-list** - Tool for managing SSH connections

### Configurations
- Custom `.zshrc` with sensible defaults and plugins
- Custom `.tmux.conf` with improved keybindings
- FZF integration with zsh

## Prerequisites

### Automated Setup (Recommended)

The included [`setup.sh`](setup.sh) script automatically handles all prerequisites:

1. **Checks your OS** - Verifies Ubuntu/Debian compatibility
2. **Installs uv** - Fast Python package manager (if not already installed)
3. **Creates virtual environment** - Local `.venv` directory for isolated Python packages
4. **Installs Ansible** - Along with required dependencies (jinja2, pyyaml)
5. **Creates activation helper** - [`activate.sh`](activate.sh) for easy environment activation

Simply run:

```bash
./setup.sh
```

The script is idempotent and safe to run multiple times.

### Manual Setup (Alternative)

If you prefer to set up manually or already have Ansible installed system-wide:

```bash
sudo apt update
sudo apt install ansible
```

## Setup

### First-Time Setup

1. **Clone this repository:**
   ```bash
   git clone <repository-url>
   cd dev-env
   ```

2. **Run the setup script:**
   ```bash
   ./setup.sh
   ```
   
   This will:
   - Install uv package manager (if needed)
   - Create a local virtual environment in `.venv/`
   - Install Ansible and dependencies
   - Create an `activate.sh` helper script

3. **Activate the virtual environment:**
   ```bash
   source activate.sh
   ```
   
   You'll need to do this each time you open a new terminal session.

### Troubleshooting Setup

**If uv installation fails:**
- Ensure you have `curl` installed: `sudo apt install curl`
- Check your internet connection
- Try installing uv manually: https://github.com/astral-sh/uv

**If the virtual environment already exists:**
- The setup script will ask if you want to recreate it
- Or manually remove it: `rm -rf .venv` then run `./setup.sh` again

**If you see "command not found: uv":**
- Restart your terminal or run: `source ~/.bashrc` (or `~/.zshrc`)
- The uv binary is installed to `~/.local/bin/`

## Usage

### Installing the Development Environment

**Important:** Always activate the virtual environment first!

```bash
# Activate the environment (do this in each new terminal session)
source activate.sh

# Run the full playbook
ansible-playbook dev-setup.yml --ask-become-pass
```

This will:
1. Install all specified packages
2. Set up oh-my-zsh with spaceship-prompt and plugins
3. Configure zsh as your default shell
4. Install container tools (podman, podman-tui, distrobox)
5. Install CLI tools from GitHub (fzf, fd, ripgrep, watchexec, espanso, dust, xh, broot, procs, bottom, bat, hexyl, eza, lsd, zoxide, gitui, lazygit, lazysql, slumber, helix, zellij, gping, bandwhich, asciinema, navi, ssh-list, tldr, zeco, zide)
6. Register and start Espanso text expander service
7. Apply your custom configurations

### Other Install Examples

**Remember:** Activate the virtual environment first with `source activate.sh`

#### Install only fzf

```bash
source activate.sh
ansible-playbook dev-setup.yml --tags fzf
```

#### Setup only ZSH (includes oh-my-zsh, shell change, theme, plugins, and related config)

```bash
source activate.sh
ansible-playbook dev-setup.yml --tags zsh
```

#### Install only ZSH plugins

```bash
source activate.sh
ansible-playbook dev-setup.yml --tags zsh-plugins
```

#### Install spaceship-prompt theme

```bash
source activate.sh
ansible-playbook dev-setup.yml --tags spaceship-prompt
```

#### Install a specific ZSH plugin

```bash
source activate.sh
ansible-playbook dev-setup.yml --tags zsh-autosuggestions
```

#### Install multiple specific tools

```bash
source activate.sh
ansible-playbook dev-setup.yml --tags "ripgrep,bat,dust"
```

#### Only run configuration tasks

```bash
source activate.sh
ansible-playbook dev-setup.yml --tags config
```

#### Install basics and a few tools

```bash
source activate.sh
ansible-playbook dev-setup.yml --tags "basics,fzf,ripgrep"
```

#### Skip certain tags

```bash
source activate.sh
ansible-playbook dev-setup.yml --skip-tags espanso
```

### Checking for Updates

To check if newer versions of tools are available:

```bash
source activate.sh
ansible-playbook version-checks.yml
```

This will:
- Query GitHub for the latest version of each tool (all tools and plugins)
- Compare with your pinned versions in `vars/versions.yml`
- Display a summary showing which tools are up to date and which have updates available

**Coverage**: All tools including CLI utilities, ZSH plugins (autosuggestions, syntax-highlighting, history-substring-search, fzf-history-search, completions), spaceship-prompt theme, NVM, and Podman are checked for updates.

**Note**: Podman is installed from Ubuntu's official repositories, so the version check compares your installed version against the latest upstream release. To update podman, use `sudo apt update && sudo apt upgrade podman`.

You can also check specific tools or categories:
```bash
source activate.sh

# Check only ZSH-related tools
ansible-playbook version-checks.yml --tags zsh

# Check only plugins
ansible-playbook version-checks.yml --tags zsh-plugins

# Check a specific tool
ansible-playbook version-checks.yml --tags gitui
```

Example output:
```
✓ Up to date (24): fzf, up, dust, xh, broot, procs, bottom, zellij, bandwhich, bat, ...
⚠ Updates available (3):
  - ripgrep: 15.1.0 → 15.2.0
  - espanso: v2.3.0 → v2.4.0
  - gping: gping-v1.20.1 → gping-v1.21.0
```

## Customization

### Managing Tool Versions

All tool versions are centrally managed in `vars/versions.yml`. This approach provides:
- **Reproducibility**: Same versions installed every time
- **Speed**: No API calls during installation
- **Control**: Easy to update or rollback versions

To update a tool version:

1. Check for available updates:
   ```bash
   source activate.sh
   ansible-playbook version-checks.yml
   ```

2. Edit `vars/versions.yml` and update the desired version(s):
   ```yaml
   ripgrep_version: "15.2.0"  # Update from 15.1.0
   ```

3. Re-run the setup playbook with the `force_update` flag:
   ```bash
   source activate.sh
   ansible-playbook dev-setup.yml --ask-become-pass -e force_update=true -t ripgrep
   ```

**Alternative Method (Manual Removal)**:
If you prefer not to use `force_update`, you can manually remove the binary first:
```bash
sudo rm /usr/local/bin/rg  # Example for ripgrep
source activate.sh
ansible-playbook dev-setup.yml --ask-become-pass
```

**Important Notes**:
- **Using `force_update=true`**: Forces reinstallation of all tools, even if they already exist. This is the easiest way to update tools.
- **ZSH plugins**: Automatically update to the version specified in `vars/versions.yml` due to `update: yes` in their Git configuration (no force_update needed).
- **Without force_update**: Binary tools only install if they don't exist, requiring manual removal first.

### Adding New Tools

This project uses a modular role-based structure. To add a new tool:

#### For apt packages:
Add to the `Install basic dependencies` task in the basics role or create a new role.

#### For tools requiring installation scripts:
Create a new role following the existing pattern. Example structure:

1. Create the role directory structure:
   ```bash
   mkdir -p roles/your-tool/tasks
   ```

2. Add the version to `vars/versions.yml`:
   ```yaml
   your_tool_version: "v1.2.3"
   ```

3. Create `roles/your-tool/tasks/main.yml`:
   ```yaml
   ---
   - name: Include OS-specific tasks
     include_tasks: "{{ ansible_distribution | lower }}.yml"
   ```

4. Create `roles/your-tool/tasks/ubuntu.yml` with installation tasks:
   ```yaml
   ---
   - name: Check if tool is installed
     stat:
       path: /usr/local/bin/your-tool
     register: tool_stat

   - name: Install tool
     block:
       - name: Download tool
         get_url:
           url: "https://github.com/owner/repo/releases/download/{{ your_tool_version }}/tool.tar.gz"
           dest: "/tmp/tool.tar.gz"

       - name: Install tool
         # ... extract and install steps
     when: not tool_stat.stat.exists or force_update | default(false)
   ```

5. Add the role to `dev-setup.yml`:
   ```yaml
   - role: your-tool
     tags: your-tool
   ```

6. Add version check to `version-checks.yml` following the existing patterns

### Customizing Configurations

1. **ZSH Configuration**: Edit `configs/zshrc.j2`
   - Change theme, plugins, aliases
   - Add custom environment variables
   
2. **Tmux Configuration**: Edit `configs/tmux.conf.j2`
   - Modify keybindings
   - Customize status bar
   - Adjust colors

### Enabling Configuration Files

By default, custom config file deployment is disabled. To enable:

1. Customize the templates in the `configs/` directory
2. In `dev-setup.yml`, change `when: false` to `when: true` for the config tasks:

```yaml
- name: Copy custom zshrc
  template:
    src: ./configs/zshrc.j2
    dest: "{{ user_home }}/.zshrc"
  when: true  # Change from false to true
```

## Structure

```
.
├── setup.sh               # Setup script (installs uv, creates venv, installs Ansible)
├── activate.sh            # Virtual environment activation helper (generated by setup.sh)
├── .venv/                 # Python virtual environment (created by setup.sh)
├── dev-setup.yml          # Main installation playbook
├── version-checks.yml     # Version update checker playbook
├── vars/
│   └── versions.yml       # Centralized tool version definitions
├── configs/
│   ├── zshrc.j2           # ZSH configuration template
│   └── tmux.conf.j2       # Tmux configuration template
├── roles/                 # Modular Ansible roles for each tool
│   ├── README.md          # Roles documentation
│   ├── system/            # System-level setup
│   ├── basics/            # Basic development tools
│   ├── augeas/            # Configuration file editor
│   ├── config/            # Configuration files deployment
│   ├── zsh/               # Oh-my-zsh installation
│   ├── zsh-autosuggestions/        # ZSH plugin
│   ├── zsh-syntax-highlighting/    # ZSH plugin
│   ├── zsh-history-substring-search/  # ZSH plugin
│   ├── zsh-fzf-history-search/     # ZSH plugin
│   ├── zsh-completions/   # ZSH plugin
│   ├── spaceship-prompt/  # ZSH theme
│   ├── podman/            # Container engine
│   ├── podman-tui/        # Podman terminal UI
│   ├── distrobox/         # Container system integration
│   ├── fzf/               # Fuzzy finder
│   ├── fd/                # Fast find alternative
│   ├── up/                # Ultimate Plumber
│   ├── ripgrep/           # Fast search tool
│   ├── watchexec/         # File watcher
│   ├── espanso/           # Text expander
│   ├── dust/              # Disk usage analyzer
│   ├── xh/                # HTTP client
│   ├── broot/             # Directory navigator
│   ├── procs/             # Process viewer
│   ├── bottom/            # System monitor
│   ├── zellij/            # Terminal multiplexer
│   ├── zeco/              # Development container manager
│   ├── zide/              # Terminal IDE
│   ├── gping/             # Graphical ping
│   ├── bandwhich/         # Network monitor
│   ├── bat/               # Better cat
│   ├── hexyl/             # Hex viewer
│   ├── helix/             # Text editor
│   ├── eza/               # Modern ls replacement
│   ├── lsd/               # Modern ls with icons
│   ├── zoxide/            # Smarter cd
│   ├── gitui/             # Git terminal UI
│   ├── lazygit/           # Git terminal UI
│   ├── lazysql/           # SQL terminal UI
│   ├── slumber/           # API client
│   ├── asciinema/         # Terminal recorder
│   ├── navi/              # Interactive cheatsheet
│   ├── ssh-list/          # SSH connection manager
│   ├── tldr/              # Simplified man pages
│   └── nvm/               # Node Version Manager
└── README.md              # This file
```

Each role follows a consistent structure:
```
roles/<tool_name>/
└── tasks/
    ├── main.yml           # Entry point with OS detection
    └── ubuntu.yml         # Ubuntu-specific implementation
```

## Adding More Tools - Examples

### Neovim (from official PPA)
```yaml
- name: Add Neovim PPA
  apt_repository:
    repo: ppa:neovim-ppa/stable
    state: present

- name: Install Neovim
  apt:
    name: neovim
    state: present
```

### Node.js (via NodeSource)
```yaml
- name: Add NodeSource repository
  shell: curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -
  args:
    creates: /etc/apt/sources.list.d/nodesource.list

- name: Install Node.js
  apt:
    name: nodejs
    state: present
```

## Tips

- **Always activate the virtual environment** before running Ansible commands: `source activate.sh`
- Run the playbook multiple times safely (it's idempotent)
- Test in a VM or container first
- Commit your customized configs to version control
- After running the playbook, restart your terminal or run `source ~/.zshrc`
- The `.venv/` directory is local to this project and won't interfere with system Python packages
- You can safely delete `.venv/` and re-run `./setup.sh` if you encounter issues
