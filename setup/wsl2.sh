git clone --depth 1 https://github.com/DamionGans/ubuntu-wsl2-systemd-script.git
cd ubuntu-wsl2-systemd-script/
bash ubuntu-wsl2-systemd-script.sh
echo "source /usr/sbin/start-systemd-namespace" >> ~/.zshrc
cd ..
rm -rf ubuntu-wsl2-systemd-script
