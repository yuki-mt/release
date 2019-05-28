### before install
# pkg upgrade
# pkg install -y git
# git clone https://github.com/yuki-mt/scripts
# cd scripts/setup
# ./termux.sh
###

## 1.
pkg upgrade

pkg install -y zsh
bash -c "$(curl -fsSL https://git.io/oh-my-termux)"


## 2.
# vim ~/.oh-my-zsh/plugins/git/git.plugin.zsh  # git のalias 削除

## 3.
# cp ../files/termux/zshrc ~/.zshrc
# source ~/.zshrc

# mkdir ~/workspace

# pkg install -y sed vim-python curl proot clang make python-dev libcurl-dev libcrypt-dev openssl-dev ruby fzf tmux openssh
# apt install -y coreutils nodejs ruby-dev libxml2-dev libxslt-dev pkg-config make clang

# ssh-keygen

# ./git.sh
# cp ../files/termux/tmux.conf ~/.tmux.conf
#
# cp ../files/termux/vimrc ~/.vimrc


# pip install -U pip
# pip install flake8 mypy
# curl -L https://its-pointless.github.io/setup-pointless-repo.sh | sh
# apt install -y freetype freetype-dev libpng libpng-dev pkg-config libzmq libzmq-dev
# pkg install -y libjpeg-turbo-dev libjpeg-turbo-progs
# pkg install -y scipy
# LDFLAGS=" -lm -lcompiler_rt" pip install jupyter pandas matplotlib

apt install -y php
curl -sS https://getcomposer.org/installer | php
mv composer.phar ~/.local/bin/composer


# termux-chroot
# npm install -y -g n
# n latest
