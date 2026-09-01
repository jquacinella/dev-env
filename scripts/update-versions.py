#!/usr/bin/env python3
"""Check upstream sources for the latest version of each pinned tool and
optionally rewrite vars/versions.yml in place.

Sources mirror version-checks.yml: GitHub releases/tags and crates.io.
Only stdlib is used, so no extra dependencies are required.

Usage:
  scripts/update-versions.py              # report what is outdated (no changes)
  scripts/update-versions.py --write      # apply updates to vars/versions.yml
  scripts/update-versions.py --only fzf,bat        # restrict to specific tools
  scripts/update-versions.py --only zeco_version   # (var name also accepted)

Set GITHUB_TOKEN (or GH_TOKEN) to raise the GitHub API rate limit from
60 to 5000 requests/hour. Without it, ~40 unauthenticated calls per run
will work but repeated runs may hit the limit.

Output is colorized with Rich when it is installed (`pip install rich`);
otherwise it falls back to plain text.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

try:
    from rich import box
    from rich.console import Console
    from rich.table import Table

    _console = Console()
    HAVE_RICH = True
except ImportError:
    _console = None
    HAVE_RICH = False

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERSIONS_FILE = os.path.join(REPO_ROOT, "vars", "versions.yml")

# Maps each versions.yml variable to its upstream source:
#   ("gh_release", "owner/repo") -> GitHub latest stable release tag_name
#                                   (falls back to gh_tags if no releases exist)
#   ("gh_tags",    "owner/repo") -> highest non-prerelease GitHub tag
#   ("crates",     "cratename")  -> crates.io max_stable_version
TOOLS = {
    "fzf_version":        ("gh_release", "junegunn/fzf"),
    "up_version":         ("gh_release", "akavel/up"),
    "ripgrep_version":    ("gh_release", "BurntSushi/ripgrep"),
    "fd_version":         ("gh_release", "sharkdp/fd"),
    "watchexec_version":  ("gh_release", "watchexec/watchexec"),
    "espanso_version":    ("gh_release", "espanso/espanso"),
    "dust_version":       ("gh_release", "bootandy/dust"),
    "xh_version":         ("gh_release", "ducaale/xh"),
    "broot_version":      ("gh_release", "Canop/broot"),
    "procs_version":      ("gh_release", "dalance/procs"),
    "bottom_version":     ("gh_release", "ClementTsang/bottom"),
    "zellij_version":     ("gh_release", "zellij-org/zellij"),
    "gping_version":      ("gh_release", "orf/gping"),
    "bandwhich_version":  ("gh_release", "imsnif/bandwhich"),
    "bat_version":        ("gh_release", "sharkdp/bat"),
    "hexyl_version":      ("gh_release", "sharkdp/hexyl"),
    "helix_version":      ("gh_release", "helix-editor/helix"),
    "eza_version":        ("gh_release", "eza-community/eza"),
    "lsd_version":        ("gh_release", "lsd-rs/lsd"),
    "zoxide_version":     ("gh_release", "ajeetdsouza/zoxide"),
    "atuin_version":      ("gh_release", "atuinsh/atuin"),
    "gitui_version":      ("gh_release", "gitui-org/gitui"),
    "lazygit_version":    ("gh_release", "jesseduffield/lazygit"),
    "lazysql_version":    ("gh_release", "jorgerojas26/lazysql"),
    "slumber_version":    ("gh_release", "LucasPickering/slumber"),
    "asciinema_version":  ("gh_release", "asciinema/asciinema"),
    "navi_version":       ("gh_release", "denisidoro/navi"),
    "ssh_list_version":   ("gh_release", "akinoiro/ssh-list"),
    "tldr_version":       ("gh_release", "tealdeer-rs/tealdeer"),
    "nvm_version":        ("gh_release", "nvm-sh/nvm"),
    "podman_tui_version": ("gh_release", "containers/podman-tui"),
    "distrobox_version":  ("gh_release", "89luca89/distrobox"),
    "zeco_version":       ("crates", "zeco"),
    "zide_version":       ("gh_release", "josephschmitt/zide"),
    "yazi_version":       ("gh_release", "sxyazi/yazi"),
    "rustnet_version":    ("gh_release", "domcyrus/rustnet"),
    "ast_grep_version":   ("gh_release", "ast-grep/ast-grep"),
    "glow_version":       ("gh_release", "charmbracelet/glow"),
    "hyperfine_version":  ("gh_release", "sharkdp/hyperfine"),
    "duf_version":        ("gh_release", "muesli/duf"),
    "zsh_autosuggestions_version":          ("gh_tags", "zsh-users/zsh-autosuggestions"),
    "zsh_syntax_highlighting_version":      ("gh_tags", "zsh-users/zsh-syntax-highlighting"),
    "zsh_history_substring_search_version": ("gh_tags", "zsh-users/zsh-history-substring-search"),
    "zsh_completions_version":              ("gh_tags", "zsh-users/zsh-completions"),
    "spaceship_prompt_version":             ("gh_release", "spaceship-prompt/spaceship-prompt"),
}
# Deliberately not auto-tracked:
#   zsh_fzf_history_search_version -> pinned to the "master" branch (no releases)
#   podman                         -> installed from Ubuntu apt repositories

PRERELEASE_RE = re.compile(r"(alpha|beta|rc|pre|dev|nightly|snapshot)", re.I)


def line_re(var):
    """Match a `var: "value"` line, capturing the quoted value separately."""
    return re.compile(
        rf'^(?P<pre>\s*{re.escape(var)}\s*:\s*")(?P<val>[^"]*)(?P<post>".*)$',
        re.MULTILINE,
    )


def numeric_core(tag):
    """Strip any leading non-digit prefix ('v', 'gping-v', ...) from a tag."""
    m = re.search(r"\d", tag)
    return tag[m.start():] if m else tag


def version_key(tag):
    """Sortable key from the numeric components of a tag."""
    parts = re.findall(r"\d+", numeric_core(tag))
    return tuple(int(p) for p in parts) if parts else (0,)


def reconcile(current, latest_tag):
    """Apply the current pin's prefix convention to the upstream tag.

    The leading non-digit prefix of the existing value (e.g. "", "v",
    "gping-v") is preserved, so we never flip a tool's formatting.
    """
    m = re.search(r"\d", current)
    prefix = current[: m.start()] if m else ""
    return prefix + numeric_core(latest_tag)


def http_json(url, token=None):
    headers = {
        "User-Agent": "dev-env-version-updater",
        "Accept": "application/json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def fetch_latest(kind, ident, token):
    if kind == "gh_release":
        try:
            data = http_json(
                f"https://api.github.com/repos/{ident}/releases/latest", token
            )
            return data["tag_name"]
        except urllib.error.HTTPError as e:
            if e.code == 404:  # repo publishes git tags but no GitHub releases
                return fetch_latest("gh_tags", ident, token)
            raise
    if kind == "gh_tags":
        data = http_json(
            f"https://api.github.com/repos/{ident}/tags?per_page=100", token
        )
        names = [t["name"] for t in data]
        if not names:
            raise RuntimeError("no tags found")
        stable = [n for n in names if not PRERELEASE_RE.search(n)] or names
        return max(stable, key=version_key)
    if kind == "crates":
        data = http_json(f"https://crates.io/api/v1/crates/{ident}")
        return data["crate"]["max_stable_version"]
    raise ValueError(f"unknown source kind: {kind}")


def emit(text, style=None):
    """Print a line, applying a Rich style when Rich is available."""
    if HAVE_RICH and style:
        _console.print(text, style=style)
    else:
        print(text)


def report(updates, uptodate, errors):
    """Render the check results, colorized with Rich when available."""
    if HAVE_RICH:
        if updates:
            table = Table(
                title=f"Updates available ({len(updates)})",
                title_style="bold dark_orange",
                title_justify="left",
                box=box.SIMPLE_HEAD,
                header_style="bold",
            )
            table.add_column("Tool")
            table.add_column("Current", style="dim")
            table.add_column("", justify="center")
            table.add_column("Latest", style="bold green")
            for var, cur, new in updates:
                table.add_row(var, cur, "->", new)
            _console.print(table)
        else:
            _console.print("All checked tools are up to date.", style="bold green")
        _console.print(f"Up to date: {len(uptodate)}", style="green")
        if errors:
            table = Table(
                title=f"Could not check ({len(errors)})",
                title_style="bold red",
                title_justify="left",
                box=box.SIMPLE_HEAD,
                header_style="bold",
            )
            table.add_column("Tool")
            table.add_column("Reason", style="red")
            for var, msg in errors:
                table.add_row(var, msg)
            _console.print(table)
        return

    if updates:
        print(f"Updates available ({len(updates)}):")
        for var, cur, new in updates:
            print(f"  {var:<40} {cur:<16} -> {new}")
    else:
        print("All checked tools are up to date.")
    print(f"\nUp to date: {len(uptodate)}")
    if errors:
        print(f"\nCould not check ({len(errors)}):")
        for var, msg in errors:
            print(f"  {var:<40} {msg}")


def parse_args():
    p = argparse.ArgumentParser(
        description="Check upstream sources and update vars/versions.yml."
    )
    p.add_argument(
        "--write",
        action="store_true",
        help="apply updates to vars/versions.yml (default: report only)",
    )
    p.add_argument(
        "--only",
        metavar="LIST",
        help="comma-separated tool names to check (e.g. 'fzf,bat' or 'fzf_version')",
    )
    return p.parse_args()


def select_tools(only):
    if not only:
        return dict(TOOLS)
    wanted = {w.strip() for w in only.split(",") if w.strip()}
    selected = {}
    for var, src in TOOLS.items():
        short = var[: -len("_version")] if var.endswith("_version") else var
        if var in wanted or short in wanted:
            selected[var] = src
    if not selected:
        sys.exit(f"error: no tracked tools matched --only {only!r}")
    return selected


def main():
    args = parse_args()
    tools = select_tools(args.only)
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

    with open(VERSIONS_FILE, encoding="utf-8") as f:
        text = f.read()

    current = {}
    for var in tools:
        m = line_re(var).search(text)
        if m:
            current[var] = m.group("val")

    print(f"Checking {len(tools)} tool(s) against upstream sources"
          + ("" if token else " (no GITHUB_TOKEN; rate-limited)") + "...\n")

    updates, uptodate, errors = [], [], []
    for var, (kind, ident) in tools.items():
        if var not in current:
            errors.append((var, "not found in versions.yml"))
            continue
        try:
            latest_tag = fetch_latest(kind, ident, token)
        except Exception as e:  # network, rate limit, missing key, etc.
            errors.append((var, f"{ident}: {e}"))
            continue
        new = reconcile(current[var], latest_tag)
        (updates if new != current[var] else uptodate).append(
            (var, current[var], new)
        )

    report(updates, uptodate, errors)

    if updates and args.write:
        new_text = text
        for var, _cur, new in updates:
            new_text = line_re(var).sub(
                lambda m, n=new: m.group("pre") + n + m.group("post"),
                new_text,
                count=1,
            )
        with open(VERSIONS_FILE, "w", encoding="utf-8") as f:
            f.write(new_text)
        rel = os.path.relpath(VERSIONS_FILE, REPO_ROOT)
        emit(f"\nWrote {len(updates)} update(s) to {rel}.", style="bold green")
    elif updates:
        emit(
            "\nRun again with --write to apply these changes to vars/versions.yml.",
            style="dark_orange",
        )

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
