# Stack Herdr — base : https://learn.datalumina.com/docs/herdr/folders

export PATH="$HOME/.local/bin:/opt/homebrew/bin:/opt/homebrew/sbin:$PATH"
export PATH="$HOME/bin:$HOME/.bun/bin:$HOME/pentest-stack/bin:$PATH"

# lazygit (et le reste) lisent ~/.config au lieu de ~/Library/Application Support
export XDG_CONFIG_HOME="$HOME/.config"

# Runtimes (node, go) : mise est la seule source
eval "$(mise activate zsh)"

# Ce que faisait oh-my-zsh : historique partagé entre panes Herdr + complétion
HISTSIZE=50000
SAVEHIST=50000
setopt SHARE_HISTORY HIST_IGNORE_DUPS
autoload -Uz compinit && compinit

# Tools
export BAT_THEME="TwoDark"
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border --cycle'

if [[ -t 0 && -t 1 ]] && command -v fzf >/dev/null; then
  source <(fzf --zsh)
fi
command -v zoxide >/dev/null && eval "$(zoxide init zsh)"
command -v direnv >/dev/null && eval "$(direnv hook zsh)"

# Aliases
alias ls="eza"
alias ll="eza -la"
alias tree="eza --tree"
alias cat="bat"
alias vim="nvim"
alias tailscale="/Applications/Tailscale.app/Contents/MacOS/Tailscale"

# quick port killer (usage: kill_port 3000)
kill_port() { lsof -ti:"${1:-3000}" | xargs kill 2>/dev/null; }

# Pentest
export OLLAMA_API_BASE=http://localhost:11434
alias pai='pentest-ai'
alias scan-port='nmap -sV -sC -T4'
alias web-recon='ffuf -w /usr/share/wordlists/dirb/common.txt -u'

# bun completions
[ -s "$HOME/.bun/_bun" ] && source "$HOME/.bun/_bun"

# Secrets locaux (jamais versionnés, voir .gitignore)
[ -f "$HOME/dotfiles/environment.sh" ] && source "$HOME/dotfiles/environment.sh"

PROMPT='%F{cyan}%~%f %F{magenta}❯%f '

# Plugins zsh (brew) — syntax-highlighting doit être sourcé en dernier
source /opt/homebrew/share/zsh-autosuggestions/zsh-autosuggestions.zsh
source /opt/homebrew/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
