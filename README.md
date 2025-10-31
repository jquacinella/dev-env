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

#### Search & Text Processing
- **ripgrep (rg)** - Ultra-fast recursive search tool
- **up (Ultimate Plumber)** - Interactive pipe building tool

#### Utilities
- **ccze** - Colorizer for log files
- **bcat** - Browser-based pipe viewer
- **bat** - Cat clone with syntax highlighting and Git integration
- **dust** - Modern disk usage analyzer
- **procs** - Modern replacement for ps with colored output and tree view
- **xh** - Friendly HTTP client (HTTPie-like)
- **Espanso** - Cross-platform text expander

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

Run the playbook with:

```bash
ansible-playbook dev-setup.yml --ask-become-pass
```

This will:
1. Install all specified packages
2. Set up oh-my-zsh
3. Configure zsh as your default shell
4. Install tools from GitHub (fzf, bcat, up, ripgrep, espanso, dust, xh, broot, procs)
5. Register and start Espanso text expander service
6. Apply your custom configurations

## Customization

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
Follow the pattern used for fzf or bcat. Example structure:

```yaml
- name: Check if tool is installed
  stat:
    path: /path/to/tool
  register: tool_stat

- name: Install tool
  block:
    - name: Clone/download tool
      # ... download steps
    
    - name: Run installation
      # ... install steps
  when: not tool_stat.stat.exists
```

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
├── dev-setup.yml          # Main playbook
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
