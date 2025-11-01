# Ansible Role Tagging Guide

## Overview

This document describes the tagging pattern used in this Ansible playbook to ensure consistent tag application across all roles.

## Tagging Pattern

All roles must have tags applied at **two levels**:

1. **In `roles/<role_name>/tasks/main.yml`**: Tags on the `include_tasks` directive
2. **In `roles/<role_name>/tasks/ubuntu.yml`**: Tags on **every task** in the file

## Tag Structure

Tags must match exactly what is defined in [`dev-setup.yml`](dev-setup.yml) for each role's `include_role` directive.

### Example: Single Tag Role

For a role with a single tag (e.g., `fzf`):

**`roles/fzf/tasks/main.yml`:**
```yaml
---
- name: Include OS-specific tasks
  tags: ['fzf']
  include_tasks: "{{ ansible_distribution | lower }}.yml"
  when: ansible_distribution == "Ubuntu"
```

**`roles/fzf/tasks/ubuntu.yml`:**
```yaml
---
- name: Clone fzf repository
  tags: ['fzf']
  git:
    repo: 'https://github.com/junegunn/fzf.git'
    dest: "{{ user_home }}/.fzf"
    version: "{{ fzf_version }}"
    depth: 1
    update: yes
  become: no

- name: Install fzf
  tags: ['fzf']
  shell: "{{ user_home }}/.fzf/install --all --no-bash --no-fish"
  args:
    creates: "{{ user_home }}/.fzf/bin/fzf"
  become: no
```

### Example: Multiple Tags Role

For a role with multiple tags (e.g., `ripgrep` with tags `ripgrep` and `rg`):

**`roles/ripgrep/tasks/main.yml`:**
```yaml
---
- name: Include OS-specific tasks
  tags: ['ripgrep', 'rg']
  include_tasks: "{{ ansible_distribution | lower }}.yml"
  when: ansible_distribution == "Ubuntu"
```

**`roles/ripgrep/tasks/ubuntu.yml`:**
```yaml
---
- name: Check if ripgrep is installed
  tags: ['ripgrep', 'rg']
  stat:
    path: /usr/local/bin/rg
  register: ripgrep_stat

- name: Download and install ripgrep
  tags: ['ripgrep', 'rg']
  block:
    # ... block content
  when: not ripgrep_stat.stat.exists
```

## Complete Tag Mapping

Here's the complete mapping of roles to their tags as defined in [`dev-setup.yml`](dev-setup.yml):

| Role | Tags |
|------|------|
| system | `always`, `system` |
| basics | `basics`, `git`, `curl`, `wget`, `build-essential`, `zsh`, `tmux`, `ccze`, `direnv`, `redshift`, `xsel` |
| zsh | `zsh` |
| zsh-autosuggestions | `zsh`, `zsh-plugins`, `zsh-autosuggestions` |
| zsh-syntax-highlighting | `zsh`, `zsh-plugins`, `zsh-syntax-highlighting` |
| zsh-history-substring-search | `zsh`, `zsh-plugins`, `zsh-history-substring-search` |
| zsh-fzf-history-search | `zsh`, `zsh-plugins`, `zsh-fzf-history-search` |
| zsh-completions | `zsh`, `zsh-plugins`, `zsh-completions` |
| powerlevel10k | `zsh`, `zsh-theme`, `powerlevel10k` |
| config | `config`, `zsh`, `tmux`, `direnv` |
| fzf | `fzf` |
| up | `up` |
| ripgrep | `ripgrep`, `rg` |
| espanso | `espanso` |
| dust | `dust` |
| xh | `xh` |
| broot | `broot` |
| procs | `procs` |
| bottom | `bottom`, `btm` |
| zellij | `zellij` |
| gping | `gping` |
| bandwhich | `bandwhich` |
| bat | `bat` |
| eza | `eza` |
| zoxide | `zoxide` |
| gitui | `gitui` |
| asciinema | `asciinema` |
| navi | `navi` |
| ssh-list | `ssh-list` |
| tldr | `tldr` |
| nvm | `nvm` |

## Why This Pattern?

This tagging pattern ensures:

1. **Consistency**: All tasks within a role can be targeted by the same tag(s)
2. **Flexibility**: Users can run specific roles or groups of roles using tags
3. **Maintainability**: Tags are defined in one place ([`dev-setup.yml`](dev-setup.yml)) and replicated to roles

## Adding a New Role

When adding a new role:

1. Define the role and its tags in [`dev-setup.yml`](dev-setup.yml)
2. Add the same tags to `roles/<role_name>/tasks/main.yml` on the `include_tasks` directive
3. Add the same tags to **every task** in `roles/<role_name>/tasks/ubuntu.yml`

## Usage Examples

Run only the zellij role:
```bash
ansible-playbook dev-setup.yml --tags zellij
```

Run all ZSH-related roles:
```bash
ansible-playbook dev-setup.yml --tags zsh
```

Run multiple specific tools:
```bash
ansible-playbook dev-setup.yml --tags "ripgrep,bat,dust"
```

Skip a specific role:
```bash
ansible-playbook dev-setup.yml --skip-tags espanso