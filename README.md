# dotfiles

Une seule stack, celle de [Herdr](https://learn.datalumina.com/docs/herdr) :
Ghostty → Herdr → agents (Claude, Codex…) + Neovim (viewer) + lazygit + zoxide.

## Installation (macOS)

```bash
brew install --cask ghostty
brew install herdr neovim lazygit git-delta zoxide fzf eza bat fd ripgrep stow mise \
  zsh-autosuggestions zsh-syntax-highlighting
git clone <ce-repo> ~/dotfiles && cd ~/dotfiles && stow .
herdr integration install claude
```

Puis désactiver les raccourcis Mission Control sur Ctrl+flèches
(Réglages Système → Clavier → Raccourcis clavier → Mission Control).

## Glaido → Herdr à la voix (MCP)

Comme dans la vidéo (chapitre 26:04), `glaido/herdr_mcp.py` est un serveur MCP (stdio, `uv`)
qui pilote Herdr par sa CLI. À déclarer dans `~/Glaido/mcp.json` (chemins absolus) :

```json
"herdr": { "command": "/Users/<moi>/.local/bin/uv",
           "args": ["run", "--script", "/Users/<moi>/dotfiles/glaido/herdr_mcp.py"] }
```

Outils : `list_workspaces`, `agent_status` (lecture, auto) et `start_agent` (Glaido demande confirmation).
Activer d'abord le mode Command dans Glaido : Account → General → fonctions beta.

## Adaptations par rapport au doc

- `macos-option-as-alt = left` (Ghostty) : clavier AZERTY, l'Option droite garde `{ } [ ] | \ ~`.
- lazygit lit `~/.config/lazygit` car `XDG_CONFIG_HOME` est défini dans `.zshrc`.
- Secrets locaux : `environment.sh` à la racine (ignoré par git, sourcé par `.zshrc`).
