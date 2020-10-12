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

# git
./git.sh

# python
brew install pyenv
export PATH="$HOME/.pyenv/shims:$HOME/.pyenv/bin:${PATH}"
# sudo installer -pkg /Library/Developer/CommandLineTools/Packages/mac
pyenv install 3.6.8
pyenv global 3.6.8
pip install -U pip
pip install mypy flake8

# ruby
brew install rbenv ruby-build
export PATH="$HOME/.rbenv/bin:$PATH"
eval "$(rbenv init -)"
rbenv install -v 2.6.3
rbenv rehash
rbenv global 2.6.3

# node
git clone git://github.com/creationix/nvm.git ~/.nvm
source ~/.nvm/nvm.sh
nvm install v10.15.3
nvm alias default v10.15.3

# tmux
cp ../files/tmux.conf ~/.tmux.conf
brew install tmux
brew install reattach-to-user-namespace

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

# fzf
brew install fzf
$(brew --prefix)/opt/fzf/install

# MySQL, Redis
brew install mysql@5.7 redis

# Docker
brew install kubernetes-cli
