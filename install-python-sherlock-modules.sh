python3 -m venv my-venv

./my-venv/bin/pip install lxml rdflib requests pyaml openpyxl

source ./my-venv/bin/activate

pip3 install --upgrade pip

cd ./python_packages/sherlockcachemanagement && ../../my-venv/bin/pip install -e . && cd ../..
#cd ./python_packages/helpers_excel && ../../my-venv/bin/pip install -e . && cd ../..
#cd ./python_packages/directus_graphql_helpers && ../../my-venv/bin/pip install -e . && cd ../..
cd ./python_packages/nocodb_helpers && ../../my-venv/bin/pip install -e . && cd ../..
cd ./python_packages/sherlock_helpers && ../../my-venv/bin/pip install -e . && cd ../..
cd ./python_packages/grist_helpers && ../../my-venv/bin/pip install -e . && cd ../..


