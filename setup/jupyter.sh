# enable Hinterland in Nbextentions
poetry add jupyter-contrib-nbextensions jupyter-nbextensions-configurator
poetry run jupyter contrib nbextension install
poetry run jupyter nbextensions_configurator enable

mkdir -p $(poetry run jupyter --data-dir)/nbextensions
cd $(poetry run jupyter --data-dir)/nbextensions
git clone https://github.com/lambdalisue/jupyter-vim-binding vim_binding
poetry run jupyter nbextension enable vim_binding/vim_binding

mkdir -p ~/.jupyter/custom
cp ../files/custom.js ~/.jupyter/custom
