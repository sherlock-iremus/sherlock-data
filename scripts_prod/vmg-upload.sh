source ../ENV

mv $REPOSITORIES/voix-du-mercure-galant/public $REPOSITORIES/voix-du-mercure-galant/voix-du-mercure-galant
rsync -varz --delete -P $REPOSITORIES/voix-du-mercure-galant/voix-du-mercure-galant tbottini@cchum-kvm-data-iremus.in2p3.fr:sherlock/apache/public_html
ssh tbottini@data-iremus.huma-num.fr "chmod 755 -R ./sherlock/apache/public_html/voix-du-mercure-galant/static"