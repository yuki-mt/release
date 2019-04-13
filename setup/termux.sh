### before install
# pkg upgrade
# pkg install -y git
# git clone https://github.com/yuki-mt/scripts
# cd scripts/setup
# ./termux.sh
###

## 1.
apt update && apt upgrade
pkg install -y sed vim-python curl proot clang make python-dev libcurl-dev libcrypt-dev openssl-dev ruby
apt install -y coreutils nodejs ruby-dev libxml2-dev libxslt-dev pkg-config make clang
npm install -y -g n
bash -c "$(curl -fsSL https://git.io/oh-my-termux)"

## 2.
# vim ~/.oh-my-zsh/plugins/git/git.plugin.zsh  # git のalias 削除

## 3.
# mkdir ~/workspace
# pkg install -y fzf tmux openssh
# ssh-keygen
# 
# ./git.sh
# cp ../files/termux/tmux.conf ~/.tmux.conf
# 
# cp ../files/termux/vimrc ~/.vimrc
# mkdir ~/.ctags.d
# cp ../files/ctags ~/.ctags.d/config.ctags
# cp -R ../files/dict ~/.vim/
# 
# cp ../files/termux/zshrc ~/.zshrc
# source ~/.zshrc
# pip install -U pip
# pip install flake8 mypy
# termux-chroot
# n latest
