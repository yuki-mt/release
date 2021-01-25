export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init -)"

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

pip-freeze() {
   gr
  if [ -f ".requirements.ignore" ]; then
    pip freeze | sort > tmp-req.txt
    comm -13 .requirements.ignore tmp-req.txt > requirements.txt
    rm tmp-req.txt
  else
    echo '.requirements.ignore is not found.'
    pip freeze | sort > requirements.txt
  fi
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
