# Ubuntu Development Environment Setup

An Ansible playbook to automatically configure your Ubuntu development environment with modern CLI tools and configurations.

## What's Included

### Installed Tools

#### Essential Development Tools
- **git**, **curl**, **wget**, **build-essential** - Core development utilities

#### Shell & Terminal
- **zsh** - Modern shell with oh-my-zsh framework
- **tmux** - Terminal multiplexer with custom configuration

#### File & Directory Navigation
- **fzf** - Fuzzy finder for command line
- **broot** - Modern tree view and directory navigator
- **direnv** - Environment variable manager per directory
- **zoxide** - Smarter cd command that learns your habits

#### Search & Text Processing
- **ripgrep (rg)** - Ultra-fast recursive search tool
- **up (Ultimate Plumber)** - Interactive pipe building tool

#### Version Control & Git
- **gitui** - Blazing fast terminal UI for git

#### Utilities
- **ccze** - Colorizer for log files
- **bat** - Cat clone with syntax highlighting and Git integration
- **dust** - Modern disk usage analyzer
- **procs** - Modern replacement for ps with colored output and tree view
- **xh** - Friendly HTTP client (HTTPie-like)
- **Espanso** - Cross-platform text expander
- **asciinema** - Terminal session recorder
- **navi** - Interactive cheatsheet tool for the command-line
- **ssh-list** - Tool for managing SSH connections

### Configurations
- Custom `.zshrc` with sensible defaults and plugins
- Custom `.tmux.conf` with improved keybindings
- FZF integration with zsh
- Direnv hook for automatic environment loading

## Prerequisites

```bash
sudo apt install ansible
```

## Usage

### Installing the Development Environment

Run the playbook with:

```bash
ansible-playbook dev-setup.yml --ask-become-pass
```

This will:
1. Install all specified packages
2. Set up oh-my-zsh
3. Configure zsh as your default shell
4. Install tools from GitHub (fzf, up, ripgrep, espanso, dust, xh, broot, procs, bat, zellij, gping, bandwhich, zoxide, gitui, asciinema, navi, ssh-list)
5. Register and start Espanso text expander service
6. Apply your custom configurations

### Other Install Examples

#### Install only fzf

```bash
ansible-playbook dev-setup.yml --tags fzf
```

#### Setup only ZSH (includes oh-my-zsh, shell change, and related config)

```bash
ansible-playbook dev-setup.yml --tags zsh
```

#### Install multiple specific tools

```bash
ansible-playbook dev-setup.yml --tags "ripgrep,bat,dust"
```

#### Only run configuration tasks

```bash
ansible-playbook dev-setup.yml --tags config
```

#### Install basics and a few tools

```bash
ansible-playbook dev-setup.yml --tags "basics,fzf,ripgrep"
```

#### Skip certain tags

```bash
ansible-playbook dev-setup.yml --skip-tags espanso
```



### Checking for Updates

To check if newer versions of tools are available:

```bash
ansible-playbook version-checks.yml
```

This will:
- Query GitHub for the latest version of each tool
- Compare with your pinned versions in `vars/versions.yml`
- Display a summary showing which tools are up to date and which have updates available

Example output:
```
✓ Up to date (10): fzf, up, dust, xh, broot, procs, bottom, zellij, bandwhich, bat
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
   ansible-playbook version-checks.yml
   ```

2. Edit `vars/versions.yml` and update the desired version(s):
   ```yaml
   ripgrep_version: "15.2.0"  # Update from 15.1.0
   ```

3. Re-run the setup playbook:
   ```bash
   ansible-playbook dev-setup.yml --ask-become-pass
   ```

**Note**: The playbook only installs tools if they don't exist. To force a reinstall, remove the tool binary first:
```bash
sudo rm /usr/local/bin/rg  # Example for ripgrep
ansible-playbook dev-setup.yml --ask-become-pass
```

### Adding New Tools

To add a new tool, edit `dev-setup.yml`:

#### For apt packages:
Add to the `Install basic dependencies` task:
```yaml
- name: Install basic dependencies
  apt:
    name:
      - existing-package
      - your-new-package  # Add here
```

#### For tools requiring installation scripts:
Follow the pattern used for fzf or bat. Example structure:

1. Add the version to `vars/versions.yml`:
   ```yaml
   your_tool_version: "v1.2.3"
   ```

2. Add the installation tasks to `dev-setup.yml`:
   ```yaml
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
     when: not tool_stat.stat.exists
   ```

3. Add version check to `version-checks.yml` following the existing patterns

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
├── dev-setup.yml          # Main installation playbook
├── version-checks.yml     # Version update checker playbook
├── vars/
│   └── versions.yml      # Centralized tool version definitions
├── configs/
│   ├── zshrc.j2          # ZSH configuration template
│   └── tmux.conf.j2      # Tmux configuration template
└── README.md             # This file
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

- Run the playbook multiple times safely (it's idempotent)
- Test in a VM or container first
- Commit your customized configs to version control
- After running, restart your terminal or run `source ~/.zshrc`

## Troubleshooting

**Shell didn't change to zsh:**
```bash
chsh -s $(which zsh)
```

**oh-my-zsh installation failed:**
Check internet connectivity and GitHub access

**Permission errors:**
Make sure you're running with `--ask-become-pass` and entering your sudo password
