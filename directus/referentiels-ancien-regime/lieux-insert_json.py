import json
import argparse
import os
import sys
import requests
import yaml
from pprint import pprint
import time

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--json_concepts")
parser.add_argument("--json_index")
args = parser.parse_args()

# Secret YAML
file = open(os.path.join(sys.path[0], "secret.yaml"))
secret = yaml.full_load(file)
r = requests.post(secret["url"] + "/auth/login", json={"email": secret["email"], "password": secret["password"]})
access_token = r.json()['data']['access_token']
refresh_token = r.json()['data']['refresh_token']
file.close()

# Constantes
slice_size = 1
sleep_time = 0

########################################################################################
## lieux
########################################################################################

# RECUPERATION DES DONNEES

r = requests.get(secret["url"] + '/items/lieux?limit=-1&access_token=' + access_token)

print("""

COLLECTION 'lieux'

Récupération des données:""")
print(r)
ids = [item["id"] for item in r.json()["data"]]


# SUPPRESSION DES DONNEES A REMPLACER

print("""

""")
print(len(ids), "données à supprimer:")

# Suppression des données par paquets de 100
try:
	for i in range(0, len(ids), 100):
		ids_slice = [ids[j] for j in range(i, i+100) if j < len(ids)]
		print(i)
		r = requests.delete(secret["url"] + '/items/lieux?limit=-1&access_token=' + access_token, json=ids_slice)
		print(r)
	n = i
except:
	pass
	n = 0

# Suppression des données restantes (non envoyées car elles n'atteignent pas la centaine de données)
try:
	for i in range(n, len(ids), 1):
		print(i)
		try:
			r = requests.delete(
				secret["url"] + f'/items/lieux?limit=-1&access_token=' + access_token, json=ids[i])
			print("Suppression des données restantes :", r)
		except Exception as e:
			print(e)
except:
	pass


r = requests.get(secret["url"] + '/items/lieux?limit=-1&access_token=' + access_token)
print(r)


# INSERTION DES NOUVELLES DONNEES

with open(args.json_concepts) as json_file:
	data_concepts = json.load(json_file)

	print("""
	
	""")
	print(len(data_concepts), "données à insérer:")

	for i in range(0, len(data_concepts), slice_size):
		# print(data_concepts)
		lieux_slice = [data_concepts[j] for j in range(i, i+slice_size) if j < len(data_concepts)]
		print(i)
		try:
			r = requests.post(secret["url"] + '/items/lieux?access_token=' + access_token, json=lieux_slice)
			r.raise_for_status()
		except Exception as e:
			print(e)
			print(lieux_slice)
		print(r)
		time.sleep(sleep_time)

	for i in range(5300, 5338):
		print(i)
		print(data_concepts[i])
		try:
			r = requests.post(secret["url"] + '/items/lieux?access_token=' + access_token, json=data_concepts[i])
			r.raise_for_status()
		except Exception as e:
			print(e)
		print(r)
		time.sleep(sleep_time)

########################################################################################
## INDEXATIONS
########################################################################################

# RECUPERATION DES DONNEES

print("""

##########################################################################################

COLLECTION 'SOURCES ARTICLES'

Récupération des données:""")
r = requests.get(secret["url"] + '/items/sources_articles?limit=-1&access_token=' + access_token)
print(r)

ids = [item["id"] for item in r.json()["data"]]


# INSERTION DES NOUVELLES DONNEES

with open(args.json_index) as json_file:
	sources_articles = json.load(json_file)

	for sa in sources_articles:
		r = requests.get(secret["url"] + '/items/sources_articles/'+sa["id"]+'?access_token=' + access_token)
		if r.status_code == 200:
			r = requests.patch(secret["url"] + '/items/sources_articles/' + sa["id"] + '?access_token=' + access_token, json=sa)
		else:
			r = requests.post(secret["url"] + '/items/sources_articles?access_token=' + access_token, json=sa)
		print(r.json())
