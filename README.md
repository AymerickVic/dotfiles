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

## Adaptations par rapport au doc

- `macos-option-as-alt = left` (Ghostty) : clavier AZERTY, l'Option droite garde `{ } [ ] | \ ~`.
- lazygit lit `~/.config/lazygit` car `XDG_CONFIG_HOME` est défini dans `.zshrc`.
- Secrets locaux : `environment.sh` à la racine (ignoré par git, sourcé par `.zshrc`).
