python3 -m venv my-venv

./my-venv/bin/pip install lxml rdflib requests pyaml

source ./my-venv/bin/activate

pip3 install --upgrade pip

cd ./python_packages/sherlock_helpers && ../../my-venv/bin/pip install -e . && cd ../..
cd ./python_packages/grist_helpers && ../../my-venv/bin/pip install -e . && cd ../..