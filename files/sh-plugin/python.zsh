export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
alias pp='poetry run python'
alias pr='poetry run'
alias pi='poetry run ipython'

pyv() {
  gr
  dir=`pwd | sed -e 's/.*\/\(.*\)/\1/'`
  if [ -f "./pyproject.toml" ]; then
    poetry shell
  else
    poetry init
  fi
  cd -
}

pytest-setup() {
  gr
  mkdir tests
  touch tests/__init__.py
  cat <<EOF > tests/test_sample.py
import unittest


class TestStringMethods(unittest.TestCase):
    def test_add_num(self):
        self.assertEqual(7, 3 + 4)
EOF

  echo "run the following"
  local reset_color="\033[0m"
  local bold_green="\033[1;32m"
  local message='python -m unittest'
  echo -e "\n$bold_green $message $reset_color\n"
}
