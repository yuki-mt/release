# How to install
# https://github.com/cli/cli/blob/trunk/docs/install_linux.md
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key C99B11DEB97541F0
sudo apt-add-repository https://cli.github.com/packages
sudo apt update
sudo apt install gh

# login
gh auth login

# merge
# -d: delete the branch
# -s: squash
gh pr merge -d -s "[<number> | <url> | <branch>]"

# issue
gh issue create --title "I found a bug" --body "Nothing works"

# diff of PR
gh pr diff "[<number> | <url> | <branch>]"

# create PR
gh pr create --title "The bug is fixed" --body "Everything works again"
