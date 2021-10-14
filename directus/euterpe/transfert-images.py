import os
import sys
import requests
import yaml
import time
import base64
import json

# YAML Secret
file = open(os.path.join(sys.path[0], "secret.yaml"))
secret = yaml.full_load(file)
r = requests.post(secret["url"] + "/auth/login",
                  json={"email": secret["email"], "password": secret["password"]})
access_token = r.json()['data']['access_token']
refresh_token = r.json()['data']['refresh_token']
file.close()

# Checking how many files are currently in Directus
# r = requests.get(secret["url"] + '/files?limit=-1&access_token=' + access_token)
# print(len(r.json()["data"]), "files currently in Directus-Euterpe\n")

# Transfering the images
print("Sending new files to Directus :\n")
n = 1
errors = []

# Anticipating Directus crash due to request overload
status_code = 200

while status_code != 401:

	for i in range(1129072, 1130969):
		try:
			print("Sending image", i)

			with open(f'../../../../../../d/images/{i}.JPG', 'rb') as img:
				name_img = os.path.basename(f'../../../../../../d/images/{i}.JPG')
				files = {'image': (name_img, img,'image/jpeg',
				                   {'Expires': '0'})}

				with requests.Session() as s:
					r = s.post(secret["url"] + '/files?limit=-1&access_token=' + access_token, files=files)
					status_code = r.status_code
					print(status_code)
					print("files sent :", n, "\n")
					n += 1
		except:
			print("error : this file will be added to the list of errors")
			status_code = r.status_code
			print(status_code)
			print(r.json(), "\n")
			errors.append(i)

# Checking if the files were added
r = requests.get(secret["url"] + '/files?limit=-1&access_token=' + access_token)
print(len(r.json()["data"]), "files currently in Directus-Euterpe\n")

print("These file might have already been sent or do not exist:\n" + errors)
