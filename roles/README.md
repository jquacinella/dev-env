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

- **system**: System-level setup (apt cache updates)
- **basics**: Basic development tools (git, curl, wget, build-essential, etc.)
- **zsh**: Oh-my-zsh installation and configuration
- **zsh-autosuggestions**: Fish-like autosuggestions for zsh
- **zsh-syntax-highlighting**: Fish-like syntax highlighting for zsh
- **zsh-history-substring-search**: Fish-like history search feature
- **zsh-fzf-history-search**: FZF-powered history search
- **zsh-completions**: Additional completion definitions for zsh
- **fzf**: Fuzzy finder
- **up**: Ultimate Plumber (interactive pipe viewer)
- **ripgrep**: Fast code search tool
- **espanso**: Text expander
- **dust**: Modern disk usage tool
- **xh**: HTTP client
- **broot**: Directory navigator
- **procs**: Process viewer
- **bottom**: System monitor
- **zellij**: Terminal multiplexer
- **gping**: Graphical ping
- **bandwhich**: Network bandwidth monitor
- **bat**: Better cat
- **zoxide**: Smarter cd command that learns your habits
- **gitui**: Blazing fast terminal UI for git
- **asciinema**: Terminal session recorder
- **navi**: Interactive cheatsheet tool for the command-line
- **ssh-list**: Tool for managing SSH connections
- **tldr**: Simplified and community-driven man pages
- **nvm**: Node Version Manager
- **config**: Configuration files setup

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
