source ../ENV

ssh-add

cd $REPOSITORIES/sherlock-app
yarn run build

ssh tbottini@data-iremus.huma-num.fr "rm -rf /home/tbottini/sherlock/apache/public_html/sherlock/"
scp -r ./dist tbottini@data-iremus.huma-num.fr:/home/tbottini/sherlock/apache/public_html/
ssh tbottini@data-iremus.huma-num.fr "mv /home/tbottini/sherlock/apache/public_html/dist/ /home/tbottini/sherlock/apache/public_html/sherlock/"
scp $REPOSITORIES/sherlock-app/.htaccess tbottini@data-iremus.huma-num.fr:/home/tbottini/sherlock/apache/public_html/sherlock/
ssh tbottini@data-iremus.huma-num.fr "chmod 777 -R /home/tbottini/sherlock/apache/public_html/sherlock/" 