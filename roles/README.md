# Ansible Roles Structure

This directory contains modular Ansible roles for setting up a development environment. Each tool has been separated into its own role for better organization and maintainability.

## Structure

Each role follows this structure:
```
roles/
  <role_name>/
    tasks/
      main.yml     # Entry point with OS detection
      ubuntu.yml   # Ubuntu-specific implementation
```

## Available Roles

### System & Core
- **system**: System-level setup (apt cache updates)
- **basics**: Basic development tools (git, curl, wget, build-essential, etc.)
- **augeas**: Configuration file editing tool
- **config**: Configuration files setup

### Shell & Terminal
- **zsh**: Oh-my-zsh installation and configuration
- **zsh-autosuggestions**: Fish-like autosuggestions for zsh
- **zsh-syntax-highlighting**: Fish-like syntax highlighting for zsh
- **zsh-history-substring-search**: Fish-like history search feature
- **zsh-fzf-history-search**: FZF-powered history search
- **zsh-completions**: Additional completion definitions for zsh
- **spaceship-prompt**: Minimalistic, powerful and customizable Zsh prompt

### Containers & Virtualization
- **podman**: Daemonless container engine
- **podman-tui**: Terminal UI for Podman
- **distrobox**: Container system integration for running any Linux distribution

### File Navigation & Search
- **fzf**: Fuzzy finder for command line
- **fd**: Fast and user-friendly alternative to find
- **ripgrep**: Ultra-fast recursive search tool
- **broot**: Directory navigator with tree view
- **zoxide**: Smarter cd command that learns your habits

### File & Text Utilities
- **bat**: Cat clone with syntax highlighting and Git integration
- **eza**: Modern replacement for ls with colors and git integration
- **lsd**: Modern ls replacement with icons and colors
- **dust**: Intuitive disk usage analyzer
- **hexyl**: Command-line hex viewer with colored output

### Process & System Monitoring
- **procs**: Modern replacement for ps with colored output
- **bottom**: Cross-platform graphical process/system monitor
- **gping**: Ping tool with a graph
- **bandwhich**: Terminal bandwidth utilization tool

### Version Control & Git
- **gitui**: Blazing fast terminal UI for git
- **lazygit**: Simple terminal UI for git commands

### Development Tools & Editors
- **helix**: Post-modern modal text editor
- **nvm**: Node Version Manager
- **zeco**: Development environment container manager
- **zide**: Terminal-based IDE

### Database & API Tools
- **lazysql**: Terminal UI for SQL databases
- **slumber**: Terminal-based API client

### Terminal Multiplexers & Session Management
- **zellij**: Modern terminal workspace with layouts and panes
- **asciinema**: Terminal session recorder

### Productivity & Utilities
- **espanso**: Cross-platform text expander
- **up**: Ultimate Plumber (interactive pipe viewer)
- **xh**: Friendly and fast HTTP client
- **watchexec**: Executes commands in response to file modifications
- **navi**: Interactive cheatsheet tool for the command-line
- **ssh-list**: Tool for managing SSH connections
- **tldr**: Simplified and community-driven man pages with practical examples

## OS Support

Currently, all roles support Ubuntu (Ubuntu family). The `main.yml` file in each role detects the OS and includes the appropriate OS-specific task file.

### Adding Support for Other Operating Systems

To add support for another OS (e.g., Fedora):

1. Create a new task file in the role's `tasks/` directory (e.g., `fedora.yml`)
2. Update the `main.yml` to include the new OS:
   ```yaml
   - name: Include OS-specific tasks
     include_tasks: "{{ ansible_distribution | lower }}.yml"
     when: ansible_distribution in ["Ubuntu", "RedHat"]
   ```

## Usage

### Install Everything
```bash
ansible-playbook dev-setup.yml
```

### Install Specific Tools Using Tags
```bash
# Install only zsh and fzf
ansible-playbook dev-setup.yml --tags "zsh,fzf"

# Install all system monitoring tools
ansible-playbook dev-setup.yml --tags "bottom,procs,gping,bandwhich"

# Skip specific tools
ansible-playbook dev-setup.yml --skip-tags "espanso"
```

### Check Available Tags
```bash
ansible-playbook dev-setup.yml --list-tags
```

## Benefits of This Structure

1. **Modularity**: Each tool is isolated in its own role
2. **Maintainability**: Easy to update, add, or remove tools
3. **OS Flexibility**: Simple to add support for other operating systems
4. **Tag Support**: Install only the tools you need
5. **Clear Organization**: Easy to understand and navigate
6. **Reusability**: Roles can be used in other playbooks

## Adding New Tools

To add a new tool:

1. Create the role directory structure:
   ```bash
   mkdir -p roles/<tool_name>/tasks
   ```

2. Create `main.yml` with OS detection:
   ```yaml
   ---
   - name: Include OS-specific tasks
     include_tasks: "{{ ansible_distribution | lower }}.yml"
     when: ansible_distribution == "Ubuntu"
   ```

3. Create `ubuntu.yml` with the installation tasks

4. Add the role to `dev-setup.yml`:
   ```yaml
   - name: Include <tool_name> role
     include_role:
       name: <tool_name>
     tags:
       - <tool_name>
   ```

5. If the tool requires a version, add it to `vars/versions.yml`
