pip install python-language-server
npm install -g tslint tsserver typescript

composer global require 'jetbrains/phpstorm-stubs:dev-master'
composer global require 'felixfbecker/language-server'
cd ~/.composer
composer run-script --working-dir=vendor/felixfbecker/language-server parse-stubs
