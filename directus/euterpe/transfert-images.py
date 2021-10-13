import os
import sys
import requests
import yaml
from time import time

# YAML Secret
file = open(os.path.join(sys.path[0], "secret.yaml"))
secret = yaml.full_load(file)
r = requests.post(secret["url"] + "/auth/login",
                  json={"email": secret["email"], "password": secret["password"]})
access_token = r.json()['data']['access_token']
refresh_token = r.json()['data']['refresh_token']
file.close()

# Checking how many files are currently in Directus
r = requests.get(secret["url"] + '/files?limit=-1&access_token=' + access_token)
print(len(r.json()["data"]), "files currently in Directus-Euterpe\n")

# Transfering the images
print("Sending new files to Directus\n")
n = 1
errors = []

for i in range(1128103, 1130969):
	try:
		print("Sending image", i)
		files = {'media': open(f'../../../../../../d/images/{i}.JPG', 'rb')}
		response = requests.post(secret["url"] + '/files?limit=-1&access_token=' + access_token, files=files)
		print(r, "\n")
		n += 1
		print(n, "files sent")
		time.sleep(5)
	except:
		print("error : the file might have already been sent or does not exist")
		errors.append(i)

# Checking if the files were added
r = requests.get(secret["url"] + '/files?limit=-1&access_token=' + access_token)
print(len(r.json()["data"]), "files currently in Directus-Euterpe\n")

print(errors)
