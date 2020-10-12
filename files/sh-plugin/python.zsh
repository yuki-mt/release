__conda_setup="$($HOME/miniconda3/bin/conda 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
        . "$HOME/miniconda3/etc/profile.d/conda.sh"
    else
        export PATH="$HOME/miniconda3/bin:$PATH"
    fi
fi
unset __conda_setup

pyv() {
  gr
  dir=`pwd | sed -e 's/.*\/\(.*\)/\1/'`
  if [ -d "$HOME/miniconda3/envs/$dir" ]; then
    conda activate $dir
  else
    conda create --name $dir -y
    conda activate $dir
    conda install -y pip
    pip install flake8 mypy python-language-server neovim
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
