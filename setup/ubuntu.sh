set -eu

# Before start

# sudo apt install -y git
# git clone --depth 1 https://github.com/yuki-mt/scripts.git
# cd scripts/setup
# bash ubuntu.sh

# # Step 1
sudo apt-get update -y
sudo apt install -y zsh
sudo chsh $USER -s $(which zsh)
git clone https://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh
sed -i -e 's/^alias.*//' ~/.oh-my-zsh/plugins/git/git.plugin.zsh
mkdir ~/workspace
ssh-keygen

# # Step 2 (new session)
# bash ./git.sh
#
# sudo apt-get install -y gcc make openssl libssl-dev libbz2-dev libreadline-dev libsqlite3-dev zlib1g-dev liblzma-dev unzip ripgrep jq tmux wget
# cp ../files/tmux.conf ~/.tmux.conf
# cp ../files/zshrc ~/.zshrc
# mkdir ~/.sh-plugin
# cp ../files/sh-plugin/* ~/.sh-plugin/
#
# source ~/.zshrc
# git clone --depth=1 https://github.com/pyenv/pyenv.git ~/.pyenv
# # check version by `pyenv install -l`
# pyenv install 3.9.1
#
# sudo apt install -y nodejs npm
# sudo npm install n -g
# sudo n stable
# sudo apt autoremove -y nodejs npm

# # Ruby
# git clone https://github.com/rbenv/rbenv.git ~/.rbenv
# git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build
# # check the latest version
# # rbenv install -l
# CONFIGURE_OPTS='--disable-install-rdoc' rbenv install 2.7.0
# rbenv global 2.7.0


# # Step 3 (new session)
# rm ./Miniconda3-latest-Linux-x86_64.sh
#
# pip install -U pip
# pip install mypy flake8 poetry
#
# sudo add-apt-repository -y ppa:neovim-ppa/stable
# pip install neovim
# sudo apt-get update -y
# sudo apt-get install -y neovim
# mkdir -p ~/.config/nvim
# cp ../files/vimrc ~/.config/nvim/init.vim
# curl -fLo ~/.local/share/nvim/site/autoload/plug.vim --create-dirs \
#     https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
# bash lsp.sh
#
# git clone https://github.com/junegunn/fzf.git ~/.fzf
# ~/.fzf/install
#
# # Docker
# sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
# curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
# sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
# sudo apt update -y
# sudo apt install -y docker-ce
# sudo usermod -a -G docker $USER
# sudo curl -L "https://github.com/docker/compose/releases/download/1.26.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
# sudo chmod +x /usr/local/bin/docker-compose
