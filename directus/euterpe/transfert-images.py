import os
import sys
import requests
import yaml
import time
import base64
import json
from pprint import pprint

# YAML Secret
file = open(os.path.join(sys.path[0], "secret.yaml"))
secret = yaml.full_load(file)
r = requests.post(secret["url"] + "/auth/login",
                  json={"email": secret["email"], "password": secret["password"]})
access_token = r.json()['data']['access_token']
refresh_token = r.json()['data']['refresh_token']
file.close()

# # Checking how many files are currently in Directus
# r = requests.get(secret["url"] + '/files?limit=-1&access_token=' + access_token)
# print(len(r.json()["data"]), "files currently in Directus-Euterpe\n")
#
# # Transfering the images
# print("Sending new files to Directus :\n")
# n = 1
#
# for i in range(1130838, 1130969):
# 	try:
# 		print("Sending image", i)
#
# 		with open(f'../../../../../../d/images/{i}.JPG', 'rb') as img:
# 			name_img = os.path.basename(f'../../../../../../d/images/{i}.JPG')
# 			files = {'image': (name_img, img,'image/jpeg',
# 			                   {'Expires': '0'})}
#
# 			with requests.Session() as s:
# 				r = s.post(secret["url"] + '/files?limit=-1&access_token=' + access_token, files=files)
# 				print(r.status_code)
# 				print("files sent :", n, "\n")
# 				n += 1
# 	except Exception as e:
# 		status_code = r.status_code
# 		print(status_code)
# 		print(e, "\n")

# Checking if the files were added
ids = []
r = requests.get(secret["url"] + f'/files?limit=-1&access_token=' + access_token)

for e in r.json()["data"]:
	ids.append(e["title"])

errors = []
for i in range(1117289, 1130969):
	if str(i) not in ids:
		errors.append(i)

print(len(errors), "to be added \n")

n = 1
for error in errors:
	try:
		print("Sending image", error)

		with open(f'../../../../../../d/images/{error}.JPG', 'rb') as img:
			name_img = os.path.basename(f'../../../../../../d/images/{error}.JPG')
			files = {'image': (name_img, img,'image/jpeg',
			                   {'Expires': '0'})}

			with requests.Session() as s:
				r = s.post(secret["url"] + '/files?limit=-1&access_token=' + access_token, files=files)
				print(r.status_code)
				print("files sent :", n, "\n")
				n += 1
	except Exception as e:
		status_code = r.status_code
		print(status_code)
		print(e, "\n")

