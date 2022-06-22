import json
import argparse
import os
import sys
import requests
import yaml
from pprint import pprint
import time

# Secret YAML
file = open(os.path.join(sys.path[0], "secret.yaml"))
secret = yaml.full_load(file)
r = requests.post(secret["url"] + "/auth/login", json={"email": secret["email"], "password": secret["password"]})
access_token = r.json()['data']['access_token']
refresh_token = r.json()['data']['refresh_token']
file.close()

# Suppression d'une collection Directus
def delete(collection):
	try:
		# Création d'une liste des identifiants des données à supprimer grâce à une requête GET
		r = requests.get(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token)
		print("Récupération des données:", r, "\n")
		ids = [item["id"] for item in r.json()["data"]]

		print(len(ids), "données à supprimer :")
		# Suppression des données par parquets de 100
		try:
			for i in range(0, len(ids), 100):
				ids_slice = [ids[j] for j in range(i, i + 100) if j < len(ids)]
				print(i)
				try:
					r = requests.delete(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token, json=ids_slice)
					print("Suppression des données par paquets de 100 :", r)
				except Exception as e:
					print(e)
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
						secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token, json=ids[i])
					print("Suppression des données restantes :", r)
				except Exception as e:
					print(e)
		except:
			pass
	except:
		print("Il n'y a aucune donnée à supprimer\n")



# Envoi de données dans une collection Directus
def send_data(json, collection, paquet, range_min, range_max):
	print("Données à insérer:", len(json))

	# Envoi des données par paquets
	# L'utilisation de range() permet de n'envoyer qu'un certain nombre
	# de données à Directus pour ne pas le saturer. J'envoie généralement
	# 1500 données par exécution.
	for i in range(7600, 7800, paquet):
		data_slice = [json[j] for j in range(i, i + paquet) if j < len(json)]
		try:
			r = requests.post(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token, json=data_slice)
			print(i, r)
		except Exception as e:
			print(e)
			pprint(data_slice)
			print(r.json())

	# Envoi des données restantes (si elles n'atteignent pas le nombre du paquet)
	for i in range(range_min, range_max):
		print(i)
		try:
			r = requests.post(secret["url"] + f'/items/{collection}?limit=-1&access_token=' + access_token, json=json[i])
			print(r)
		except Exception as e:
			print(e)
			# pprint(data_to_send[i])
			print(r.json())
		# time.sleep(2)

def send_indexations(fichier):
	# Ajout de données à la collection (patch)
	print("\nENVOI DES INDEXATIONS DANS LA COLLECTION SOURCES_ARTICLES\n")
	with open(fichier) as json_file:
		sources_articles = json.load(json_file)

		print(len(sources_articles), "données à insérer:")
		n = 0
		for sa in sources_articles[n:]:
			print(n, "-", sa["id"])
			r = requests.get(secret["url"] + '/items/sources_articles/' + sa["id"] + '?access_token=' + access_token)
			if r.status_code == 200:
				try:
					new_items = r.json()
					print(new_items)
					#r = requests.patch(
					#	secret["url"] + '/items/sources_articles/' + sa["id"] + '?access_token=' + access_token,
					#	json=sa)
					#print("patch sur un item existant :", r)
				except Exception as e:
					print(e)
					print(r.json())
			else:
				try:
					r = requests.post(secret["url"] + '/items/sources_articles?access_token=' + access_token, json=sa)
					print("post d'un item n'existant pas déjà dans la collection :", r)
				except Exception as e:
					print(e)
					print(r.json())
			n += 1
