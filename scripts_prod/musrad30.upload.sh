ssh tbottini@cchum-kvm-data-iremus.in2p3.fr "rm -rf sherlock/apache/public_html/musrad30"
ssh tbottini@cchum-kvm-data-iremus.in2p3.fr "mkdir sherlock/apache/public_html/musrad30"
scp -r ./cra-apps/musrad30/build/* tbottini@cchum-kvm-data-iremus.in2p3.fr:sherlock/apache/public_html/musrad30