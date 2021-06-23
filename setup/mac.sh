set -eu

# Before start

# mkdir ~/workspace
# xcode-select --install
# /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
# brew upgrade
# brew install zsh git
# curl -L https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sh
# sed -i -e 's/^alias.*//' ~/.oh-my-zsh/plugins/git/git.plugin.zsh
# sudo vi /etc/shells <- add "/usr/local/bin/zsh"
# chsh -s /usr/local/bin/zsh
# cd ~/workspace
# git clone https://github.com/yuki-mt/scripts.git
# cd scripts/setup
# ./mac.sh

ssh-keygen
./git.sh

brew install pyenv
export PATH="$HOME/.pyenv/shims:$HOME/.pyenv/bin:${PATH}"
# sudo installer -pkg /Library/Developer/CommandLineTools/Packages/mac
# # check version by `pyenv install -l`
pyenv install 3.9.1
pyenv global 3.9.1
pip install -U pip
pip install mypy flake8 poetry neovim
poetry config virtualenvs.in-project true

# ruby
brew install rbenv ruby-build
export PATH="$HOME/.rbenv/bin:$PATH"
eval "$(rbenv init -)"
rbenv install -v 2.6.3
rbenv rehash
rbenv global 2.6.3

# node
brew install nodebrew
nodebrew setup
nodebrew install-binary stable
nodebrew use stable # ?

# tmux
cp ../files/tmux.conf ~/.tmux.conf
brew install tmux
brew install reattach-to-user-namespace

# fzf
brew install fzf
$(brew --prefix)/opt/fzf/install

# zshrc
cp ../files/zshrc ~/.zshrc
mkdir ~/.sh-plugin
mv ~/.fzf.zsh ~/.sh-plugin/fzf.zsh
cp ../files/sh-plugin/* ~/.sh-plugin/
source ~/.zshrc

# PHP
# brew install php@73
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer

# vim
brew install neovim
mkdir -p ~/.config/nvim
cp ../files/vimrc ~/.config/nvim/init.vim
curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
    https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
./lsp.sh


# MySQL, Redis
brew install mysql redis

# Docker
brew install kubernetes-cli
