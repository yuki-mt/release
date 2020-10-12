### before install
# pkg upgrade
# pkg install -y git
# git clone https://github.com/yuki-mt/scripts
# cd scripts/setup
# ./termux.sh
###

## 1.
pkg upgrade
pkg install -y zsh curl sed
bash -c "$(curl -fsSL https://git.io/oh-my-termux)"

## 2.
# sed -i -e 's/^alias.*//' $HOME/.oh-my-zsh/plugins/git/git.plugin.zsh
#
# cp ../files/termux/zshrc ~/.zshrc
# mkdir ~/.sh-plugin
# cp ../files/sh-plugin/* ~/.sh-plugin/
# pkg install -y openssl openssh
# source ~/.zshrc
#
# mkdir ~/workspace
#
# pkg install -y neovim proot clang make ruby fzf tmux python rsync
# apt install -y coreutils nodejs pkg-config
#
# ssh-keygen
#
# ./git.sh
# cp ../files/termux/tmux.conf ~/.tmux.conf
# curl -fLo ~/.vim/autoload/plug.vim --create-dirs https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
# cp ../files/termux/vimrc ~/.config/nvim/init.vim
#
#
# pip install -U pip
# pip install flake8 mypy neovim
# curl -L https://its-pointless.github.io/setup-pointless-repo.sh | sh
# apt install -y freetype libpng libzmq
# pkg install -y libjpeg-turbo-progs
# pkg install -y scipy
# LDFLAGS=" -lm -lcompiler_rt" pip install jupyter pandas matplotlib
#
# apt install -y php
# curl -sS https://getcomposer.org/installer | php
# mv composer.phar /data/data/com.termux/files/usr/bin/composer
#
# termux-chroot
# npm install -y -g n
# termux-chroot
# n latest
