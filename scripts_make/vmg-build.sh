source ../ENV

cd $REPOSITORIES/voix-du-mercure-galant
pnpm i
yarn
gatsby clean
gatsby build --prefix-paths --verbose
cd -
