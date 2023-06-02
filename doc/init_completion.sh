#!/bin/sh
# Check if current shell is Bash
if [ -n "$BASH_VERSION" ]; then
    source $HOME/.emulsionrc/emulsion-bash-completion.sh
else
    # Check if current shell is Zsh
    if [ -n "$ZSH_VERSION" ]; then
        autoload -U compinit ; compinit
        source $HOME/.emulsionrc/emulsion-zsh-completion.sh
    else
        echo "EMULSION completion script not initialized (expected shell: bash or zsh)"
    fi
fi
