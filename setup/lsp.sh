pip install python-language-server
npm install -g tslint tsserver typescript

curl -L https://github.com/yuloh/composer-termux/releases/download/1.6.2/composer.phar -o composer.phar
chmod +x ./composer.phar
mv ./composer.phar ~/.local/bin/composer
composer global require 'jetbrains/phpstorm-stubs:dev-master'
composer global require 'felixfbecker/language-server'
cd ~/.composer
composer run-script --working-dir=vendor/felixfbecker/language-server parse-stubs
