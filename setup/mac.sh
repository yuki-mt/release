set -eu

# Before start

# mkdir ~/workspace
# xcode-select --install
# /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
# brew upgrade
# brew install zsh git
# curl -L https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh | sh
# sed -i -e 's/^alias.*//' ~/.oh-my-zsh/plugins/git/git.plugin.zsh
# cd ~/workspace
# git clone https://github.com/yuki-mt/scripts.git
# cd scripts/setup
# ./mac.sh

# git
./git.sh

# python
brew install pyenv
export PATH="$HOME/.pyenv/shims:$HOME/.pyenv/bin:${PATH}"
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

# zshrc
cp ../files/zshrc ~/.zshrc
source ~/.zshrc

# PHP
brew install homebrew/php/php73
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer

# vim
brew install vim
cp ../files/vimrc ~/.vimrc
./lsp.sh

# fzf
brew install fzf
$(brew --prefix)/opt/fzf/install

# tmux
cp ../files/tmux.conf ~/.tmux.conf
brew install tmux
brew install reattach-to-user-namespace

# MeCab
brew install mecab mecab-ipadic
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
cd mecab-ipadic-neologd/seed
xz -dkv mecab-user-dict-seed.*.csv.xz
export PATH=$PATH:/usr/local/Cellar/mecab/0.996/libexec/mecab

dic_path="/usr/lib64/mecab/dic/ipadic"
# or dic_path="/usr/local/lib/mecab/dic/ipadic"

mecab-dict-index -d $dic_path \
  -u mecab-user-dict-seed.dic -f utf-8 -t utf-8 \
  mecab-user-dict-seed.*.csv
sudo mv mecab-user-dict-seed.dic $dic_path
cd -
rm -rf mecab-ipadic-neologd

# MySQL, Redis
brew install mysql@5.7 redis

# Docker
brew install kubernetes-cli
