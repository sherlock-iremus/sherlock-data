import os
import sys
import requests
import yaml

# Secret YAML
file = open(os.path.join(sys.path[0], "secret.yaml"))
secret = yaml.full_load(file)
r = requests.post(secret["url"] + "/auth/login",
                  json={"email": secret["email"], "password": secret["password"]})
access_token = r.json()['data']['access_token']
refresh_token = r.json()['data']['refresh_token']
file.close()

# Test
r = requests.get(secret["url"] + '/files?limit=-1&access_token=' + access_token)
print(r.json())

# Les images à transférer
for i in range(1117289, 1118331):
	image = {
		"url": f"https://github.com/Amleth/euterpe-data/blob/master/images/{i}?raw=true",
		"data": {
			"title": i
		}
	}

	# Transfert (requête post)
	r = requests.post(secret["url"] + '/files?limit=-1&access_token=' + access_token, json={
		"url": f"https://github.com/Amleth/euterpe-data/blob/master/images/{i}?raw=true",
		"data": {
			"title": i
		}
	})
	print(r)
