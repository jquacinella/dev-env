# Dev-Env Tools Presentation Outline

## Introduction (2-3 minutes)
**Opening**: "Today I'll introduce you to a curated collection of modern CLI tools that will transform how we work as sysadmins. These tools are faster, more user-friendly, and more powerful than their traditional counterparts."

**Key Points**:
- All tools installed via Ansible playbook (reproducible, version-controlled)
- Drop-in replacements for familiar commands (minimal learning curve)
- Focused on productivity and better UX for daily sysadmin tasks

---

## 1. Foundation: Z Shell (Zsh) & Oh-My-Zsh (5-7 minutes)

### Summary
Zsh is a modern, feature-rich shell that extends bash capabilities with powerful auto-completion, better globbing, and extensive customization. Oh-My-Zsh is a framework that makes zsh configuration simple and adds 200+ plugins.

### Why Sysadmins Should Adopt It
- **Command correction**: Typo detection and suggestions reduce errors
- **Advanced tab completion**: Context-aware completions for commands, flags, and file paths
- **Shared history**: Access command history across all terminal sessions
- **Plugin ecosystem**: Instantly add git status, AWS tools, kubectl integration, etc.

### Features to Demonstrate
1. **Intelligent auto-completion**
   - Show tab completion for command flags (`kill -<TAB>`)
   - Demonstrate directory completion with partial matches

2. **Command history search**
   - Press `Ctrl+R` for reverse history search
   - Use arrow keys with substring search (type `ssh` then up arrow)

3. **Oh-My-Zsh plugins included**:
   - `zsh-autosuggestions`: Ghost text from history (type `git ` and see suggestion)
   - `zsh-syntax-highlighting`: Real-time command validation (red=invalid, green=valid)
   - `zsh-history-substring-search`: Arrow key search in history
   - `zsh-fzf-history-search`: Fuzzy search history with `Ctrl+R`
   - `zsh-completions`: Additional completion definitions

4. **Spaceship Prompt**
   - Shows git branch, status, and changes at a glance
   - Displays execution time for long-running commands
   - Shows current directory, Python/Node versions when relevant

### Implementation Notes
- Demo creating a git repo and showing branch info in prompt
- Show a misspelled command getting corrected
- Type partial command and show autosuggestion from history

---

## 2. Terminal Workspace: Zellij (5 minutes)

### Summary
Zellij is a modern terminal multiplexer (think tmux, but with better UX). It provides terminal workspace management with tabs, panes, layouts, and session persistence. Sessions survive disconnects, perfect for SSH sessions to remote servers.

### Why Sysadmins Should Adopt It
- **Session persistence**: Start long-running processes, disconnect, reconnect later
- **No memorizing keybindings**: On-screen hints show available shortcuts
- **Built-in layouts**: Quickly split screen for monitoring logs + running commands
- **Better than screen/tmux**: Modern defaults, easier configuration, better clipboard integration

### Features to Demonstrate
1. **Starting and attaching sessions**
   - `zellij` to start
   - `zellij attach` to reconnect

2. **Pane management**
   - Show keybinding hints at bottom (Ctrl+p for panes)
   - Split horizontally and vertically
   - Resize panes with shortcuts

3. **Tab management**
   - Create multiple tabs for different tasks
   - Rename tabs for organization

4. **Real-world use case**
   - Tab 1: Run `tail -f /var/log/syslog`
   - Tab 2: Edit configuration file
   - Tab 3: Run service restart commands
   - Disconnect and reconnect to show persistence

### Implementation Notes
- Create a 3-pane layout: logs (top), editor (bottom-left), commands (bottom-right)
- Show clipboard integration (copy from pane)
- Demonstrate floating panes for quick commands

---

## 3. File & Directory Navigation (8-10 minutes)

### 3.1 FZF - Fuzzy Finder

**Summary**: FZF is an interactive command-line fuzzy finder. It filters any list (files, history, processes) in real-time as you type, using fuzzy matching.

**Why Adopt It**:
- Find files without remembering exact names
- Search command history interactively (better than Ctrl+R)
- Integrates with other tools (git, vim, cd)

**Demo**:
- `Ctrl+R`: Search command history with fuzzy matching
- `Ctrl+T`: Find and insert file path into current command
- `Alt+C`: Fuzzy find directory and cd into it
- Pipe any list to fzf: `ls /var/log | fzf`

---

### 3.2 Zoxide - Smart CD

**Summary**: Zoxide is a smarter cd command that learns your most-visited directories and lets you jump to them with minimal typing.

**Why Adopt It**:
- No more `cd ../../var/log/nginx` repeatedly
- Jump to frequent dirs with partial names: `z ngi` → `/var/log/nginx`
- Remembers your habits and ranks directories by frequency

**Demo**:
- cd to a few different directories
- Show `z <partial-name>` jumping directly
- Use `zi` for interactive selection with fzf
- Show `zoxide query` to see ranked directories

---

### 3.3 Eza & LSD - Modern LS Replacements

**Summary**: Modern replacements for `ls` with colors, icons, git integration, and tree views. Eza is more feature-rich; LSD focuses on visual appeal.

**Why Adopt It**:
- **Git integration**: See modified/staged files at a glance
- **Color-coded permissions**: Instantly spot permission issues
- **Tree view**: Replace `tree` command with `eza --tree`
- **Icons**: Visual file type identification

**Demo**:
- `eza -la`: Show detailed listing with icons and colors
- `eza --git`: Show git status alongside files
- `eza --tree --level=2`: Show directory tree
- Compare `ls -la` vs `eza -la` side by side

---

### 3.4 FD - Fast Find Alternative

**Summary**: User-friendly alternative to `find` with sane defaults, speed (parallel search), and respects .gitignore.

**Why Adopt It**:
- **10x faster** than find on large directories
- **Simple syntax**: `fd pattern` instead of `find . -name "*pattern*"`
- **Smart defaults**: Ignores .git, node_modules automatically
- **Colorized output**: Easy to scan results

**Demo**:
- `fd nginx` vs `find . -name "*nginx*"`
- `fd -e conf`: Find all .conf files
- `fd -t d lib`: Find directories named lib
- `fd -H .env`: Include hidden files in search

---

### 3.5 Yazi - Terminal File Manager

**Summary**: Blazing fast terminal file manager with vim-like keybindings, preview, and bulk operations. Think midnight commander, but modern.

**Why Adopt It**:
- **Visual file browsing**: See directory structure at a glance
- **File preview**: View text files, images, PDFs without opening
- **Bulk operations**: Select multiple files for copy/move/delete
- **Fast navigation**: Keyboard-driven, no mouse needed

**Demo**:
- Launch `yazi`
- Navigate with arrow keys or vim keys (hjkl)
- Preview files (show config file, log file)
- Bulk select files and copy/move
- Show image preview capability

---

### 3.6 Broot - Modern Tree View & Navigator

**Summary**: Interactive directory navigator that displays tree views, file sizes, and lets you fuzzy search and navigate large directory structures.

**Why Adopt It**:
- **Handle large directories**: Doesn't hang on huge file trees
- **See disk usage**: Combined tree + du functionality
- **Fuzzy search**: Type to filter tree in real-time
- **Quick navigation**: cd to searched directory

**Demo**:
- `br` to launch broot
- Navigate large directory (like /var or /usr)
- Type search term to filter tree
- Show disk usage mode
- Use `:cd` to jump to selected directory

---

## 4. Search & Text Processing (5-7 minutes)

### 4.1 Ripgrep (rg) - Ultra-Fast Search

**Summary**: Blazing fast recursive search tool that respects .gitignore. Built for speed with Rust, replaces grep/ag/ack.

**Why Adopt It**:
- **Speed**: 10-100x faster than grep on large codebases
- **Smart defaults**: Automatically skips .git, binaries, respects .gitignore
- **Better output**: Colored, with line numbers, grouped by file
- **Simple syntax**: Works like grep but better

**Demo**:
- `rg "error" /var/log`: Search all logs for "error"
- `rg -i "failed"`: Case-insensitive search
- `rg -t py "import"`: Search only Python files
- Compare speed: `grep -r "pattern" .` vs `rg "pattern"`
- `rg -A 3 -B 3 "error"`: Show context around matches

---

### 4.2 Bat - Cat with Superpowers

**Summary**: A cat clone with syntax highlighting, git integration, line numbers, and paging. Displays files beautifully in the terminal.

**Why Adopt It**:
- **Syntax highlighting**: Instantly understand code/config files
- **Git integration**: Shows added/modified/deleted lines
- **Line numbers**: Reference specific lines easily
- **Automatic paging**: No more `cat file | less`

**Demo**:
- `bat /etc/nginx/nginx.conf`: Show syntax highlighting
- `bat --style=numbers,changes script.py`: Show git changes
- Compare `cat` vs `bat` on a config file
- `bat --paging=never`: For quick views without pager

---

### 4.3 Hexyl - Command-Line Hex Viewer

**Summary**: Beautiful hex viewer with colored output that distinguishes ASCII, null bytes, and binary data.

**Why Adopt It**:
- **Binary file inspection**: Debug binary configs, examine executables
- **Colored output**: Easily distinguish data types
- **Side-by-side view**: Hex + ASCII representation

**Demo**:
- `hexyl /bin/ls | head -50`: View binary file
- `hexyl suspicious-file.bin`: Examine unknown file types
- Show how colors highlight different byte types

---

### 4.4 UP - Ultimate Plumber

**Summary**: Interactive pipe-building tool. Write complex pipe commands interactively, seeing results in real-time.

**Why Adopt It**:
- **Learn by doing**: See pipe results as you type
- **Debug pipelines**: Identify where pipes break
- **Build complex commands**: Iteratively refine grep/awk/sed chains

**Demo**:
- `up /var/log/syslog`
- Interactively build: `grep error | grep -v INFO | awk '{print $1, $5}'`
- Show real-time updates as you modify the command
- Copy final command when done

---

## 5. Process & System Monitoring (8-10 minutes)

### 5.1 Procs - Modern Process Viewer

**Summary**: Modern replacement for `ps` with colored output, tree view, and better default columns (CPU%, memory, runtime, command).

**Why Adopt It**:
- **Human-readable output**: Colors and clear formatting
- **Tree view**: See process parent-child relationships
- **Sensible defaults**: Shows useful info without complex flags
- **Search and filter**: Built-in grep-like filtering

**Demo**:
- `procs`: Show all processes with color
- `procs nginx`: Search for specific process
- `procs --tree`: Show process tree
- Compare `ps aux` vs `procs`

---

### 5.2 Bottom - System Monitor

**Summary**: Cross-platform graphical process/system monitor for the terminal. Think htop + iotop + nethogs combined with a better interface.

**Why Adopt It**:
- **All-in-one monitoring**: CPU, memory, disk, network, processes
- **Graphs and charts**: Visual representation of resource usage
- **Customizable**: Multiple views and layouts
- **Lightweight**: Terminal-based, works over SSH

**Demo**:
- `btm` to launch
- Show CPU/memory graphs
- Switch to process view and sort by CPU
- Show network usage graph
- Demonstrate killing processes from within btm

---

### 5.3 Nmon - Performance Monitoring

**Summary**: System performance monitoring tool specifically designed for Linux. Shows CPU, memory, disk I/O, network in a single dashboard.

**Why Adopt It**:
- **Comprehensive view**: All system stats in one place
- **Interactive**: Toggle different views with key presses
- **Recording mode**: Capture performance data to file for later analysis
- **Perfect for troubleshooting**: Quick overview during incidents

**Demo**:
- `nmon` to launch
- Press `c` for CPU, `m` for memory, `d` for disk, `n` for network
- Show how to enable multiple views simultaneously
- Mention recording mode: `nmon -f -s 10 -c 60` (60 samples, 10s apart)

---

### 5.4 Iotop - I/O Monitoring

**Summary**: Shows I/O usage by processes, like top but for disk operations. Essential for diagnosing disk bottlenecks.

**Why Adopt It**:
- **Find I/O hogs**: Identify which process is hammering disk
- **Real-time updates**: See disk reads/writes as they happen
- **Sort by I/O**: Quickly find the culprit during disk slowdowns

**Demo**:
- `sudo iotop`: Show real-time disk I/O
- Sort by disk write (`w` key) and disk read (`r` key)
- Show total disk bandwidth at top
- Use case: "Database slow? Check if logs are overwhelming disk"

---

### 5.5 Iftop - Network Bandwidth Monitor

**Summary**: Shows network bandwidth usage by connection. See which IPs/hosts are consuming bandwidth in real-time.

**Why Adopt It**:
- **Network troubleshooting**: Find bandwidth hogs instantly
- **Connection tracking**: See active connections and their speeds
- **Per-host stats**: Identify which services/hosts use most bandwidth

**Demo**:
- `sudo iftop -i eth0`: Monitor specific interface
- Show inbound/outbound traffic bars
- Press `t` to toggle between different views
- Use case: "Bandwidth spike? See exactly which connection is responsible"

---

### 5.6 Gping - Graphical Ping

**Summary**: Ping tool with a graph. Visualizes ping response times over time, making network issues obvious.

**Why Adopt It**:
- **Visual debugging**: See latency spikes and packet loss at a glance
- **Multiple hosts**: Ping several hosts simultaneously
- **Trend analysis**: Spot intermittent network issues

**Demo**:
- `gping 8.8.8.8`: Show graph of ping times
- `gping 8.8.8.8 1.1.1.1 google.com`: Compare multiple hosts
- Show how latency spikes appear as graph peaks

---

### 5.7 Bandwhich - Network Bandwidth by Process

**Summary**: Shows which processes are using network bandwidth, broken down by connection.

**Why Adopt It**:
- **Process-level visibility**: See exactly which app is using bandwidth
- **Real-time monitoring**: Watch network usage as it happens
- **Connection details**: Remote IPs, ports, protocols

**Demo**:
- `sudo bandwhich`: Launch bandwidth monitor
- Show processes sorted by network usage
- Identify remote IPs and ports
- Use case: "Mystery bandwidth usage? Find the process responsible"

---

## 6. Version Control Tools (4-5 minutes)

### 6.1 GitUI

**Summary**: Blazing fast terminal UI for git written in Rust. Keyboard-driven interface for commits, staging, branching, and history.

**Why Adopt It**:
- **Speed**: Faster than lazygit, handles large repos smoothly
- **Keyboard-centric**: No mouse needed, vim-like navigation
- **Visual workflow**: See changes, stage hunks, write commits visually
- **Async operations**: Background fetch, doesn't block UI

**Demo**:
- `gitui` in a git repo
- Show staging files with Space
- View diffs inline
- Create commit with `c`
- View commit history and branches
- Show stash management

---

### 6.2 Lazygit

**Summary**: Simple terminal UI for git with intuitive interface. More beginner-friendly than gitui, excellent for learning git concepts.

**Why Adopt It**:
- **Beginner-friendly**: Clear labels and help text
- **Visual branching**: See branch structure clearly
- **Interactive rebase**: Squash, reword, reorder commits easily
- **Conflict resolution**: Handle merge conflicts visually

**Demo**:
- `lazygit` in a git repo
- Navigate with arrow keys
- Stage files, create commits
- Show branch management (create, checkout, merge)
- Demonstrate cherry-picking commits

**Comparison**: GitUI for speed and large repos, Lazygit for learning and visual clarity

---

## 7. Containers & Virtualization (5-7 minutes)

### 7.1 Podman

**Summary**: Daemonless container engine that's compatible with Docker. Rootless containers by default, more secure than Docker. Drop-in replacement (`alias docker=podman`).

**Why Adopt It**:
- **No daemon**: No single point of failure, no root daemon
- **Rootless containers**: Better security, no privilege escalation risks
- **Docker compatible**: Same commands, same images, same Dockerfiles
- **Systemd integration**: Generate systemd units from containers

**Demo**:
- `podman run -it ubuntu bash`: Run container
- `podman ps`: List containers
- `podman images`: List images
- Show rootless operation: `podman info | grep rootless`
- Generate systemd unit: `podman generate systemd --name container_name`

---

### 7.2 Podman-TUI

**Summary**: Terminal UI for Podman. Manage containers, images, volumes, and networks visually.

**Why Adopt It**:
- **Visual management**: See all containers/images at a glance
- **Bulk operations**: Select multiple containers for operations
- **Logs and stats**: View container logs and resource usage inline
- **Faster than CLI**: Navigate and manage without typing commands

**Demo**:
- `podman-tui` to launch
- Navigate between containers, images, volumes tabs
- Show container logs in split view
- Start/stop containers with shortcuts
- Inspect container details

---

### 7.3 Distrobox

**Summary**: Allows running any Linux distribution inside containers with tight integration to host system. Home directory, users, and devices are shared.

**Why Adopt It**:
- **Test on different distros**: Run Fedora tools on Ubuntu, CentOS on Debian
- **Package availability**: Use packages from any distro's repos
- **Isolated environments**: Separate dev environments per project
- **Seamless integration**: Apps run as if native (X11, Wayland, audio work)

**Demo**:
- `distrobox create --name fedora --image fedora:latest`: Create Fedora container
- `distrobox enter fedora`: Enter container
- Show home directory is shared (`ls ~`)
- Install Fedora-specific package: `sudo dnf install htop`
- Exit and show container is preserved
- `distrobox-export --app firefox`: Export app to host

---

## 8. Development & Productivity Tools (6-8 minutes)

### 8.1 Helix - Modal Text Editor

**Summary**: Post-modern modal text editor with built-in LSP support, multiple cursors, and tree-sitter parsing. Like Neovim but with better defaults.

**Why Adopt It**:
- **Zero configuration**: LSP, syntax highlighting work out of the box
- **Multiple cursors**: Edit multiple locations simultaneously
- **Built-in LSP**: Code completion, go-to-definition, diagnostics
- **Modern architecture**: Tree-sitter parsing for accurate syntax

**Demo**:
- `hx /etc/nginx/nginx.conf`: Open file
- Show syntax highlighting
- Demonstrate multiple cursors: `C` to add cursor below
- Show LSP features if editing code (completions, diagnostics)
- Explain vim-like modal editing

---

### 8.2 Lazysql - Database TUI

**Summary**: Terminal UI for SQL databases (MySQL, PostgreSQL, SQLite). Browse tables, run queries, view results in a visual interface.

**Why Adopt It**:
- **Visual query building**: See schema while writing queries
- **No GUI needed**: Works over SSH, lightweight
- **Multiple connections**: Manage several databases simultaneously
- **Safe operations**: Confirm before destructive queries

**Demo**:
- `lazysql` (if database available)
- Connect to database
- Browse tables and schema
- Run SELECT query and show results table
- Show query history

---

### 8.3 Slumber - API Client

**Summary**: Terminal-based HTTP/REST API client. Think Postman/Insomnia but in the terminal with vim-like keybindings.

**Why Adopt It**:
- **Test APIs without GUI**: Works over SSH, scriptable
- **Collection management**: Save and organize API requests
- **Environment variables**: Switch between dev/staging/prod
- **Response formatting**: JSON/XML syntax highlighting

**Demo**:
- `slumber`
- Create GET request to public API (httpbin.org/get)
- Show response with syntax highlighting
- Demonstrate headers, query params
- Save request to collection

---

### 8.4 NVM - Node Version Manager

**Summary**: Manage multiple Node.js versions on the same system. Switch Node versions per project without conflicts.

**Why Adopt It**:
- **Multiple versions**: Test apps on different Node versions
- **Per-project versions**: `.nvmrc` file sets version automatically
- **Easy switching**: `nvm use 18` to switch instantly
- **No sudo required**: Install packages globally without root

**Demo**:
- `nvm list`: Show installed versions
- `nvm install 20`: Install Node 20
- `nvm use 18`: Switch to Node 18
- `node --version`: Verify version
- Show `.nvmrc` file auto-detection

---

### 8.5 Zeco & Zide

**Summary**:
- **Zeco**: Development environment container manager, creates consistent dev environments
- **Zide**: Terminal-based IDE combining editor, terminal, and file browser

**Why Adopt It**:
- **Reproducible environments**: Same dev setup across team
- **Isolated dependencies**: Project dependencies don't conflict
- **Quick onboarding**: New devs get working environment in minutes

**Demo** (brief):
- Mention these are more advanced tools for development workflows
- Show quick overview if time permits

---

## 9. Utilities & Helpers (5-7 minutes)

### 9.1 TLDR - Simplified Man Pages

**Summary**: Community-driven man pages with practical examples. Get straight to the examples without reading entire man pages.

**Why Adopt It**:
- **Quick reference**: See common use cases immediately
- **Examples-focused**: Learn by example, not by reading specs
- **Covers most tools**: 1000+ commands with examples
- **Faster than googling**: Instant offline access

**Demo**:
- `tldr tar`: Compare with `man tar`
- `tldr rsync`: Show common rsync use cases
- `tldr curl`: See HTTP request examples
- `tldr find`: Better than remembering find syntax

---

### 9.2 Navi - Interactive Cheatsheets

**Summary**: Interactive cheatsheet tool. Search cheatsheets, insert commands with placeholders filled interactively.

**Why Adopt It**:
- **Command templates**: Save complex commands with placeholders
- **Interactive prompts**: Fill in variables before executing
- **Community cheatsheets**: Import others' command collections
- **Custom cheatsheets**: Create team-specific command references

**Demo**:
- `navi`: Launch cheatsheet browser
- Search for "ssh tunnel"
- Show interactive variable prompts
- Execute selected command
- Mention creating custom cheatsheets

---

### 9.3 Dust - Disk Usage Analyzer

**Summary**: Modern du replacement that visualizes disk usage in a tree format. Instantly find what's consuming disk space.

**Why Adopt It**:
- **Visual tree**: See directory sizes at a glance
- **Sorted by size**: Largest directories first
- **Faster than du**: Parallel directory scanning
- **Color-coded**: Easy to spot large directories

**Demo**:
- `dust /var/log`: Analyze log directory
- Compare with `du -sh * | sort -h`
- Show how quickly it identifies large directories
- Use `dust -d 3`: Limit depth for quick overview

---

### 9.4 XH - HTTP Client

**Summary**: Friendly HTTP client with expressive syntax. Like HTTPie but faster (written in Rust).

**Why Adopt It**:
- **Human-friendly**: Simpler than curl for API testing
- **JSON support**: Automatic JSON serialization
- **Colored output**: Easy to read responses
- **Download progress**: Shows progress bars for large files

**Demo**:
- `xh httpbin.org/get`: Simple GET request
- `xh POST httpbin.org/post name=admin`: POST with JSON
- `xh -d httpbin.org/image/png > image.png`: Download file
- Compare with curl equivalent

---

### 9.5 Espanso - Text Expander

**Summary**: Cross-platform text expander. Type shortcuts that expand to longer text (snippets, commands, templates).

**Why Adopt It**:
- **Time saver**: Expand common commands/emails instantly
- **Consistent templates**: Ensure team uses correct command syntax
- **Works everywhere**: Terminal, browser, any application
- **Dynamic expansions**: Insert date, output of commands

**Demo**:
- Show trigger: `:email` expands to full email signature
- `:date` expands to current date
- `:sshprod` expands to full SSH command with args
- Show configuration file location and format

---

### 9.6 Watchexec - File Watcher

**Summary**: Executes commands when files change. Monitor config files, auto-restart services, trigger tests on code changes.

**Why Adopt It**:
- **Auto-restart services**: Restart app when config changes
- **Development workflow**: Run tests automatically on save
- **Log monitoring**: Trigger alerts when logs match pattern
- **Better than inotify-tools**: Simple syntax, powerful filtering

**Demo**:
- `watchexec -w /etc/nginx/nginx.conf -- nginx -t`: Test config on change
- `watchexec -e py -- pytest`: Run tests when Python files change
- Show real-time response to file modifications

---

### 9.7 Asciinema - Terminal Recorder

**Summary**: Record and share terminal sessions. Perfect for documentation, demos, and reproducing issues.

**Why Adopt It**:
- **Lightweight recordings**: Text-based, tiny file sizes
- **Shareable**: Upload to asciinema.org or self-host
- **Copy-paste enabled**: Viewers can copy text from recordings
- **Better than video**: Faster, searchable, smaller files

**Demo**:
- `asciinema rec demo.cast`: Start recording
- Run a few commands
- `exit`: Stop recording
- `asciinema play demo.cast`: Replay recording
- Mention uploading: `asciinema upload demo.cast`

---

### 9.8 SSH-List - SSH Connection Manager

**Summary**: Tool for managing and quickly connecting to SSH hosts. Fuzzy search your SSH config.

**Why Adopt It**:
- **Quick connections**: Search and connect without typing full hostnames
- **SSH config integration**: Reads from `~/.ssh/config`
- **Faster than aliases**: Fuzzy search beats remembering aliases

**Demo**:
- `ssh-list`: Show list of configured hosts
- Demonstrate fuzzy search
- Select and connect to host

---

### 9.9 CCZE - Log Colorizer

**Summary**: Colorizer for log files. Reads logs and applies color coding to different log levels, IPs, timestamps, etc.

**Why Adopt It**:
- **Easier log reading**: Colors help spot errors/warnings quickly
- **Works with pipes**: `tail -f /var/log/syslog | ccze`
- **Multiple log formats**: Supports syslog, Apache, Postfix, etc.

**Demo**:
- `tail -100 /var/log/syslog | ccze -A`: Colorize syslog
- Show how ERROR/WARNING stand out in red/yellow
- Compare colored vs uncolored log output

---

## 10. Getting Started & Adoption Strategy (3-5 minutes)

### Installation
- **One command setup**: `./setup.sh && source activate.sh && ansible-playbook dev-setup.yml --ask-become-pass`
- **Selective installation**: Install only what you need with tags: `--tags "zsh,fzf,ripgrep"`
- **Version controlled**: All tool versions pinned in `vars/versions.yml`

### Recommended Adoption Path
**Week 1: Foundation**
- Install Zsh and get comfortable with Oh-My-Zsh
- Start using Zellij for session management
- Adopt fzf for command history (Ctrl+R)

**Week 2: Navigation & Search**
- Replace ls with eza/lsd
- Use ripgrep instead of grep
- Try bat instead of cat
- Start using zoxide to jump between directories

**Week 3: Monitoring**
- Use procs instead of ps
- Install bottom and use during troubleshooting
- Try gping when diagnosing network issues

**Week 4+: Specialized Tools**
- Adopt gitui/lazygit for version control
- Try helix for quick file edits
- Explore container tools (podman, distrobox) for isolation
- Add utilities based on your workflow needs

### Creating Aliases for Transition
Add to `.zshrc`:
```bash
alias ls='eza'
alias cat='bat'
alias find='fd'
alias grep='rg'
alias ps='procs'
alias du='dust'
alias curl='xh'  # for simple requests
```

### Team Adoption Tips
1. **Start with non-destructive tools**: Try tools that don't replace critical commands first
2. **Share configurations**: Commit custom `.zshrc` and configs to team repo
3. **Create cheatsheets**: Use Navi to share team-specific command collections
4. **Demo in standups**: Show one tool per week to team
5. **Pair sessions**: Help teammates get comfortable with new tools

### Version Management
- Check for updates: `python3 scripts/update-versions.py`
- Update specific tool: Edit `vars/versions.yml` and run playbook with `force_update=true`

---

## Conclusion (2 minutes)

### Key Takeaways
- **Productivity boost**: These tools genuinely make daily tasks faster and easier
- **Better UX**: Modern tools prioritize usability and helpful defaults
- **Minimal risk**: Most are drop-in replacements, easy to revert if needed
- **Reproducible setup**: Ansible playbook means consistent environments across team

### Next Steps
1. Clone the repo and run setup
2. Start with Zsh + Zellij + FZF (foundation tools)
3. Gradually adopt other tools that match your workflow
4. Share feedback and contribute improvements to the playbook

### Resources
- Repository: [Link to your repo]
- Documentation: Check README.md for detailed usage
- Questions: [Your contact method]

**Final thought**: "These tools represent years of open-source development focused on solving real sysadmin problems. Don't try to adopt everything at once—pick 3-5 tools that address your pain points and go from there. The time investment pays back quickly."

---

## Time Allocation Summary
- Introduction: 2-3 min
- Zsh/Oh-My-Zsh: 5-7 min
- Zellij: 5 min
- File Navigation: 8-10 min
- Search & Text: 5-7 min
- Monitoring: 8-10 min
- Version Control: 4-5 min
- Containers: 5-7 min
- Development Tools: 6-8 min
- Utilities: 5-7 min
- Adoption Strategy: 3-5 min
- Conclusion: 2 min

**Total: 58-76 minutes** (Adjust by skipping or condensing sections based on your time slot)

## Presentation Tips
1. **Start each tool demo from scratch** - don't assume it's already running
2. **Use real examples** - actual log files, real repos, production-like scenarios
3. **Show both success and failure** - demonstrate how tools handle errors
4. **Keep a "cheat sheet" tab open** - TLDR or Navi for quick reference during demos
5. **Have a backup plan** - Pre-record critical demos in case of technical issues
6. **Encourage interruptions** - Let people ask questions during demos
7. **Share the outline** - Send this document to attendees beforehand
8. **Record the session** - Use asciinema or screen recording for those who can't attend
