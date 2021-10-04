import argparse
from rdflib import Literal as l, RDF, RDFS, URIRef as u
import sys, os
from openpyxl import load_workbook
from pprint import pprint
import requests

# Helpers
sys.path.append(os.path.abspath(os.path.join('rdfizers/', '')))
from helpers_rdf import *
from sherlockcachemanagement import Cache
sys.path.append(os.path.abspath(os.path.join('python_packages/helpers_excel', '')))
from helpers_excel import *

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--ttl")
parser.add_argument("--xlsx")
parser.add_argument("--cache")
parser.add_argument("--cache_tei")
parser.add_argument("--cache_personnes")
parser.add_argument("--cache_lieux")
parser.add_argument("--vocab_estampes")
args = parser.parse_args()

# Caches
cache = Cache(args.cache)
if args.cache_tei:
	cache_tei = Cache(args.cache_tei)
if args.cache_personnes:
	cache_personnes = Cache(args.cache_personnes)
if args.cache_lieux:
	cache_lieux = Cache(args.cache_lieux)

# Initialisation du graphe
init_graph()

###################################################################################################
# Récupération du vocabulaire d'indexation des estampes
###################################################################################################

# Fichier Excel
fichier_excel = load_workbook(args.vocab_estampes)
vocabulaire = fichier_excel.active

# Dictionnaire concept-UUID
concepts_uuid = {}

for row in vocabulaire:
	# Ignorer la première ligne
	if row[0].value == "uuid SHERLOCK":
		continue

	for colonne in row:
		if colonne.value != None and colonne != row[6] and colonne != row[7] and colonne != row[0]:
			concept = colonne.value.replace(";", "").strip()

			# Ajout du concept dans le dictionnaire UUID-concept
			if concept in concepts_uuid:
				continue
			concepts_uuid[concept] = row[0].value

###################################################################################################
# Traitement des estampes
###################################################################################################

rows = get_xlsx_rows_as_dicts(args.xlsx)
for row in rows:
	if row["ID"] is not None:
		collection = she("759d110d-fd68-47bb-92fd-341bb63dbcae")
		id = row["ID"]

		# L'estampe (E36)
		estampe = she(cache.get_uuid(["estampes", id, "E36", "uuid"], True))
		t(estampe, a, crm("E36_Visual_Item"))
		t(collection, crm("P148_has_component"), estampe)
		t(estampe, crm("P2_has_type"), she("1317e1ac-50c8-4b97-9eac-c4d902b7da10"))

		# Identifiant Mercure Galant de l'estampe (E42)
		estampe_id_MG = she(cache.get_uuid(["estampes", id, "E36", "identifiant MG"], True))
		t(estampe_id_MG, a, crm("E42_Identifier"))
		t(estampe_id_MG, crm("P2_has_type"), she("92c258a0-1e34-437f-9686-e24322b95305"))
		t(estampe_id_MG, RDFS.label, l(id))
		t(estampe, crm("P1_is_identified_by"), estampe_id_MG)

		# Identifiant IIIF de l'estampe (E42)
		estampe_id_iiif = she(cache.get_uuid(["estampes", id, "E36", "identifiant iiif"], True))
		t(estampe_id_iiif, a, crm("E42_Identifier"))
		t(estampe_id_iiif, crm("P2_has_type"), she("19073c4a-0ef7-4ac4-a51a-e0810a596773"))
		t(estampe_id_iiif, RDFS.label,
		  u(f"http://data-iremus.huma-num.fr/iiif/3/mg_estampes--{id.replace(' ', '%20')}.tif/full/max/0/default.jpg"))
		t(estampe, crm("P1_is_identified_by"), estampe_id_iiif)

		# Production (E12) de l'estampe
		if row["[Inventeur] ('Invenit' ou 'Pinxit' ou 'Delineavit') vs. 'fecit'"] or row[
			"[Graveur] 'Sculpsit' ou 'Incidit' vs. 'fecit'"]:
			estampe_E12 = she(cache.get_uuid(["estampes", id, "E36", "E12", "uuid"], True))
			t(estampe_E12, a, crm("E12_Production"))
			t(estampe_E12, crm("P108_has_produced"), estampe)

		# Invenit (concepteur de l'estampe) (sous-E12)
		if row["[Inventeur] ('Invenit' ou 'Pinxit' ou 'Delineavit') vs. 'fecit'"]:
			estampe_invenit = she(cache.get_uuid(["estampes", id, "E36", "E12", "invenit", "uuid"], True))
			t(estampe_invenit, a, crm("E12_Production"))
			t(estampe_invenit, crm("P2_has_type"), she("4d57ac14-247f-4b0e-90ca-0397b6051b8b"))
			t(estampe_E12, crm("P9_consists_of"), estampe_invenit)

			## Lien entre conception de l'estampe et concepteur (E13)
			estampe_invenit_auteur = she(cache.get_uuid(["estampes", id, "E36", "E12", "invenit", "auteur"], True))
			t(estampe_invenit_auteur, a, crm("E21_Person"))
			t(estampe_invenit_auteur, RDFS.label,
			  l(row["[Inventeur] ('Invenit' ou 'Pinxit' ou 'Delineavit') vs. 'fecit'"]))
			estampe_invenit_E13 = she(cache.get_uuid(["estampes", id, "E36", "E12", "invenit", "E13"], True))
			t(estampe_invenit_E13, a, crm("E13_Attribute_Assignement"))
			t(estampe_invenit_E13, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
			t(estampe_invenit_E13, crm("P140_assigned_attribute_to"), estampe_invenit)
			t(estampe_invenit_E13, crm("P141_assigned"), estampe_invenit_auteur)
			t(estampe_invenit_E13, crm("P177_assigned_property_type"), crm("P14_carried_out_by"))

			## Technique de la représentation de l'estampe (E13 sur une E29)
			if row["Technique de la représentation [Avec Maj et au pl.]"]:
				estampe_E29 = she(cache.get_uuid(["estampes", id, "E36", "E12", "E29", "uuid"], True))
				t(estampe_E29, a, crm("E29_Design_or_Procedure"))
				t(estampe_E29, RDFS.label, l(row["Technique de la représentation [Avec Maj et au pl.]"]))
				estampe_E29_E13 = she(cache.get_uuid(["estampes", id, "E36", "E12", "E29", "E13"], True))
				t(estampe_E29_E13, a, crm("E13_Attribute_Assignement"))
				t(estampe_E29_E13, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
				t(estampe_E29_E13, crm("P140_assigned_attribute_to"), estampe_invenit)
				t(estampe_E29_E13, crm("P141_assigned"), estampe_E29)
				t(estampe_E29_E13, crm("P177_assigned_property_type"), crm("P33_used_specific_technique"))

		# Sculpsit (graveur de l'estampe) (sous-E12)
		if row["[Graveur] 'Sculpsit' ou 'Incidit' vs. 'fecit'"]:
			estampe_sculpsit = she(cache.get_uuid(["estampes", id, "E36", "E12", "sculpsit", "uuid"], True))
			t(estampe_sculpsit, a, crm("E12_Production"))
			t(estampe_sculpsit, crm("P2_has_type"), she("f39eb497-5559-486c-b5ce-6a607f615773"))
			t(estampe_E12, crm("P9_consists_of"), estampe_sculpsit)

			## Lien entre la gravure de l'estampe et son graveur (E13)
			estampe_sculpsit_auteur = she(cache.get_uuid(["estampes", id, "E36", "E12", "sculpsit", "auteur"], True))
			t(estampe_sculpsit_auteur, a, crm("E21_Person"))
			t(estampe_sculpsit_auteur, RDFS.label, l(row["[Graveur] 'Sculpsit' ou 'Incidit' vs. 'fecit'"]))
			estampe_sculpsit_E13 = she(cache.get_uuid(["estampes", id, "E36", "E12", "sculpsit", "E13"], True))
			t(estampe_sculpsit_E13, a, crm("E13_Attribute_Assignement"))
			t(estampe_sculpsit_E13, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
			t(estampe_sculpsit_E13, crm("P140_assigned_attribute_to"), estampe_sculpsit)
			t(estampe_sculpsit_E13, crm("P141_assigned"), estampe_sculpsit_auteur)
			t(estampe_sculpsit_E13, crm("P177_assigned_property_type"), crm("P14_carried_out_by"))

			## Technique de la gravure (E13 sur une E55)
			if row["Technique de la gravure [Avec Maj et au pl.]"]:
				estampe_E55 = she(cache.get_uuid(["estampes", id, "E36", "E12", "E55", "uuid"], True))
				t(estampe_E55, a, crm("E55_Type"))
				t(estampe_E55, RDFS.label, l(row["Technique de la gravure [Avec Maj et au pl.]"]))
				estampe_E55_E13 = she(cache.get_uuid(["estampes", id, "E36", "E12", "E55", "E13"], True))
				t(estampe_E55_E13, a, crm("E13_Attribute_Assignement"))
				t(estampe_E55_E13, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
				t(estampe_E55_E13, crm("P140_assigned_attribute_to"), estampe_sculpsit)
				t(estampe_E55_E13, crm("P141_assigned"), estampe_E55)
				t(estampe_E55_E13, crm("P177_assigned_property_type"), crm("P32_used_general_technique"))

		# Identifant BnF (E42)
		if row["Provenance cliché"]:
			estampe_id_BnF = she(cache.get_uuid(["estampes", id, "E36", "identifiant BnF"], True))
			t(estampe_id_BnF, a, crm("E42_Identifier"))
			t(estampe_id_BnF, crm("P2_has_type"), she("15c5867f-f612-4a00-b9f3-17b57e566b8c"))
			t(estampe_id_BnF, RDFS.label, l(row["Provenance cliché"]))
			t(estampe, crm("P1_is_identified_by"), estampe_id_BnF)

		# Rattachement à la livraison ou à l'article OBVIL
		## Si l'article n'est pas précisé:
		if not row["ID article OBVIL"]:
			id_image = id
			id_livraison = id[0:-4]
			if id_livraison.endswith("_"):
				id_livraison = id_livraison[0:-1]
			try:
				# Livraison originale
				livraison_F2_originale = she(
					cache_tei.get_uuid(["Corpus", "Livraisons", id_livraison, "Expression originale", "F2"]))
				t(livraison_F2_originale, crm("P148_has_component"), estampe)

				# Livraison TEI
				livraison_F2_TEI = she(
					cache_tei.get_uuid(["Corpus", "Livraisons", id_livraison, "Expression TEI", "F2"]))
				t(livraison_F2_TEI, crm("P148_has_component"), estampe)
			except:
				print("L'image " + id_image + " n'est reliée à aucune livraison")

		## Si l'article est précisé:
		else:
			id_article = row["ID article OBVIL"][3:]
			id_livraison = id_article[0:11]
			try:
				if id_livraison.endswith("_"):
					id_livraison = id_livraison[0:-1]

					# Article original
					article_F2_original = she(cache_tei.get_uuid(
						["Corpus", "Livraisons", id_livraison, "Expression originale", "Articles", id_article, "F2"]))
					t(article_F2_original, crm("P148_has_component"), estampe)

					### Article TEI
					article_F2_TEI = she(cache_tei.get_uuid(
						["Corpus", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article, "F2"]))
					t(article_F2_TEI, crm("P148_has_component"), estampe)
				else:

					### Article original
					article_F2_original = she(cache_tei.get_uuid(
						["Corpus", "Livraisons", id_livraison, "Expression originale", "Articles", id_article, "F2"]))
					t(article_F2_original, crm("P148_has_component"), estampe)

					### Article TEI
					article_F2_TEI = she(cache_tei.get_uuid(
						["Corpus", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article, "F2"]))
					t(article_F2_TEI, crm("P148_has_component"), estampe)
			except:
				print("Estampe", id, "Article contenant la gravure : l'article " + id_article + " est introuvable dans les fichiers TEI")

		# Article annexe à la gravure
		if row["ID OBVIL article lié"]:
			id_article = row["ID OBVIL article lié"][3:]
			id_livraison = id_article[0:10]
			try:
				article_F2 = she(cache_tei.get_uuid(
					["Corpus", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article, "F2"]))
				estampe_seeAlso_E13 = she(cache.get_uuid(["estampes", id, "E36", "seeAlso", "E13"], True))
				t(estampe_seeAlso_E13, a, crm("E13_Attribute_Assignement"))
				t(estampe_seeAlso_E13, crm("P14_carried_out_by"),
				  she("684b4c1a-be76-474c-810e-0f5984b47921"))
				t(estampe_seeAlso_E13, crm("P140_assigned_attribute_to"), estampe)
				t(estampe_seeAlso_E13, crm("P141_assigned"), article_F2)
				t(estampe_seeAlso_E13, crm("P177_assigned_property_type"), RDFS.seeAlso)

				## Commentaire décrivant le lien entre la gravure et l'article
				if row["Commentaire ID article lié OBVIL"]:
					estampe_seeAlso_P3_E13 = she(
						cache.get_uuid(["estampes", id, "E36", "seeAlso", "note", "E13"], True))
					t(estampe_seeAlso_P3_E13, a, crm("E13_Attribute_Assignement"))
					t(estampe_seeAlso_P3_E13, crm("P14_carried_out_by"),
					  she("684b4c1a-be76-474c-810e-0f5984b47921"))
					t(estampe_seeAlso_P3_E13, crm("P140_assigned_attribute_to"), article_F2)
					t(estampe_seeAlso_P3_E13, crm("P141_assigned"), l(row["Commentaire ID article lié OBVIL"]))
					t(estampe_seeAlso_P3_E13, crm("P177_assigned_property_type"), crm("P3_has_note"))
			except:
				print("Estampe", id, "Article annexe à la gravure : l'article " + id_article + " est introuvable dans les fichiers TEI")

		# Lien Gallica
		# TODO Réparer les URL
		# if row["Lien vers le texte [ou l'image] en ligne"]:
		# 	try:
		# 		lien_gallica = u(row["Lien vers le texte [ou l'image] en ligne"])
		# 		t(lien_gallica, crm("P2_has_type"), she("e73699b0-9638-4a9a-bfdd-ed1715416f02"))
		# 		img_gallica_E13 = she(cache.get_uuid(["estampes", id, "E36", "gallica", "E13"], True))
		# 		t(img_gallica_E13, a, crm("E13_Attribute_Assignement"))
		# 		t(img_gallica_E13, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
		# 		t(img_gallica_E13, crm("P140_assigned_attribute_to"), estampe)
		# 		t(img_gallica_E13, crm("P141_assigned"), lien_gallica)
		# 		t(img_gallica_E13, crm("P177_assigned_property_type"), RDFS.seeAlso)
		# 	except:
		# 		pass
			# print("'Gallica: " + row["Lien au texte [ou à l'image] en ligne"] + "' n'est pas une URL valide")

		# Titre sur l'image (E13)
		if row["Titre sur l'image"]:
			estampe_titre = she(cache.get_uuid(["estampes", id, "E36", "titre sur l'image"], True))
			t(estampe_titre, a, crm("E13_Attribute_Assignement"))
			t(estampe_titre, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
			t(estampe_titre, crm("P140_assigned_attribute_to"), estampe)
			t(estampe_titre, crm("P141_assigned"), l(row["Titre sur l'image"].replace("[", "").replace("]", "").replace("*", "")))
			t(estampe_titre, crm("P177_assigned_property_type"), she("01a07474-f2b9-4afd-bb05-80842ecfb527"))

		# Titre descriptif/forgé (E13)
		if row["[titre descriptif forgé]* (Avec Maj - accentuées]"]:
			estampe_titre = she(cache.get_uuid(["estampes", id, "E36", "titre forgé"], True))
			t(estampe_titre, a, crm("E13_Attribute_Assignement"))
			t(estampe_titre, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
			t(estampe_titre, crm("P140_assigned_attribute_to"), estampe)
			t(estampe_titre, crm("P141_assigned"), l(row["[titre descriptif forgé]* (Avec Maj - accentuées]"].replace("[", "").replace("]", "").replace("*", "")))
			t(estampe_titre, crm("P177_assigned_property_type"), she("58fb99dd-1ffb-4e00-a16f-ef6898902301"))

		# Titre dans le péritexte (E13)
		if row["[Titre dans le péritexte: Avis, article…]"]:
			estampe_titre = she(cache.get_uuid(["estampes", id, "E36", "titre péritexte"], True))
			t(estampe_titre, a, crm("E13_Attribute_Assignement"))
			t(estampe_titre, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
			t(estampe_titre, crm("P140_assigned_attribute_to"), estampe)
			t(estampe_titre, crm("P141_assigned"), l(row["[Titre dans le péritexte: Avis, article…]"].replace("[", "").replace("]", "").replace("*", "")))
			t(estampe_titre, crm("P177_assigned_property_type"), she("ded9ea93-b400-4550-9aa8-e5aac1d627a0"))

		# Lieu représenté
		if row["Lieux"]:

			lieu = row["Lieux"]

			## Zone de l'image comportant la représentation du lieu (E13)
			estampe_zone_img = she(cache.get_uuid(["estampes", id, "E36", lieu, "zone de l'image (E36)", "uuid"], True))
			t(estampe_zone_img, a, crm("E36_Visual_Item"))
			estampe_zone_img_E13 = she(cache.get_uuid(["estampes", id, "E36", lieu, "zone de l'image (E36)", "E13"], True))
			t(estampe_zone_img_E13, a, crm("E13_Attribute_Assignement"))
			t(estampe_zone_img_E13, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
			t(estampe_zone_img_E13, crm("P140_assigned_attribute_to"), estampe)
			t(estampe_zone_img_E13, crm("P141_assigned"), estampe_zone_img)
			t(estampe_zone_img_E13, crm("P177_assigned_property_type"), crm("P106_is_composed_of"))

			## Recherche d'UUID dans le référentiel des lieux
			try:
				lieu_uuid = she(cache_lieux.get_uuid(["lieux", str(lieu), "E93", "uuid"]))
				if lieu_uuid:
					estampe_lieu_E13 = she(
						cache.get_uuid(["estampes", id, "E36", lieu, "zone de l'image (E36)", "lieu représenté"], True))
					t(estampe_lieu_E13, a, crm("E13_Attribute_Assignement"))
					t(estampe_lieu_E13, crm("P14_carried_out_by"),
					  she("684b4c1a-be76-474c-810e-0f5984b47921"))
					t(estampe_lieu_E13, crm("P140_assigned_attribute_to"), estampe_zone_img)
					t(estampe_lieu_E13, crm("P177_assigned_property_type"), crm("P138_represents"))
					t(estampe_lieu_E13, crm("P141_assigned"), lieu_uuid)

			except:
				estampe_lieu_E13 = she(cache.get_uuid(
					["collection", id, "E36", lieu, "zone de l'image (E36)", "lieu représenté"], True))
				t(estampe_lieu_E13, a, crm("E13_Attribute_Assignement"))
				t(estampe_lieu_E13, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
				t(estampe_lieu_E13, crm("P140_assigned_attribute_to"), estampe_zone_img)
				t(estampe_lieu_E13, crm("P177_assigned_property_type"), crm("P138_represents"))
				t(estampe_lieu_E13, crm("P141_assigned"), l(lieu))

		# Objet/Personne représentée (E13)
		if row["objet [en bdc, sg par défaut] / Personne représentés [avec Maj.]"]:

			sujets = row["objet [en bdc, sg par défaut] / Personne représentés [avec Maj.]"].split(";")

			for sujet in sujets:
				sujet = sujet.strip()
				if "/" in sujet:
					sujet = sujet.split("/")
					sujet = sujet[1].strip()

				# Zone de l'image représentant le sujet (E13)
				estampe_zone_img = she(
					cache.get_uuid(["estampes", id, "E36", sujet, "zone de l'image (E36)", "uuid"], True))
				t(estampe_zone_img, a, crm("E36_Visual_Item"))
				estampe_zone_img_E13 = she(
					cache.get_uuid(["estampes", id, "E36", sujet, "zone de l'image (E36)", "E13"], True))
				t(estampe_zone_img_E13, a, crm("E13_Attribute_Assignement"))
				t(estampe_zone_img_E13, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
				t(estampe_zone_img_E13, crm("P140_assigned_attribute_to"), estampe)
				t(estampe_zone_img_E13, crm("P141_assigned"), estampe_zone_img)
				t(estampe_zone_img_E13, crm("P177_assigned_property_type"), crm("P106_is_composed_of"))

				# Si le sujet est une personne, recherche de son UUID
				try:
					personne_uuid = she(cache_personnes.get_uuid(["personnes", sujet, "uuid"]))
					if personne_uuid:
						estampe_personne_E13 = she(cache.get_uuid(
							["collection", id, "E36", sujet, "zone de l'image (E36)", "personne représentée"],
							True))
						t(estampe_personne_E13, a, crm("E13_Attribute_Assignement"))
						t(estampe_personne_E13, crm("P14_carried_out_by"),
						  she("684b4c1a-be76-474c-810e-0f5984b47921"))
						t(estampe_personne_E13, crm("P140_assigned_attribute_to"), estampe_zone_img)
						t(estampe_personne_E13, crm("P177_assigned_property_type"), crm("P138_represents"))
						t(estampe_personne_E13, crm("P141_assigned"), personne_uuid)
				except:

					# Si le sujet est issu du vocabulaire des estampes, recherche de son UUID
					try:
						objet_uuid = she(concepts_uuid[sujet])

						if objet_uuid:
							if sujet != "médaille":
								estampe_objet_E13 = she(cache.get_uuid(
									["collection", id, "E36", sujet, "zone de l'image (E36)", "objet représenté"], True))
								t(estampe_objet_E13, a, crm("E13_Attribute_Assignement"))
								t(estampe_objet_E13, crm("P14_carried_out_by"),
								  she("684b4c1a-be76-474c-810e-0f5984b47921"))
								t(estampe_objet_E13, crm("P140_assigned_attribute_to"), estampe_zone_img)
								t(estampe_objet_E13, crm("P177_assigned_property_type"), crm("P138_represents"))
								t(estampe_objet_E13, crm("P141_assigned"), objet_uuid)

							# Si le sujet représenté est une médaille (E13)
							if sujet == "médaille":

								# Zone d'image imbriquée dans la première zone et correspondant à la médaille
								estampe_zone_médaille = she(
									cache.get_uuid(
										["estampes", id, "E36", sujet, "zone de l'image (E36)", "zone de la médaille (E36)",
										 "uuid"], True))
								t(estampe_zone_médaille, a, crm("E36_Visual_Item"))
								estampe_zone_médaille_E13 = she(
									cache.get_uuid(
										["estampes", id, "E36", sujet, "zone de l'image (E36)", "zone de la médaille (E36)",
										 "E13 zone"], True))
								t(estampe_zone_médaille_E13, a, crm("E13_Attribute_Assignement"))
								t(estampe_zone_médaille_E13, crm("P14_carried_out_by"),
								  she("684b4c1a-be76-474c-810e-0f5984b47921"))
								t(estampe_zone_médaille_E13, crm("P140_assigned_attribute_to"), estampe_zone_img)
								t(estampe_zone_médaille_E13, crm("P141_assigned"), estampe_zone_médaille)
								t(estampe_zone_médaille_E13, crm("P177_assigned_property_type"), crm("P106_is_composed_of"))

								# La médaille (E55)
								t(objet_uuid, a, crm("E55_Type"))

								# La zone d'image représente une médaille
								estampe_médaille_E13 = she(cache.get_uuid(
									["collection", id, "E36", sujet, "zone de l'image (E36)", "zone de la médaille (E36)",
									 "E13 représentation"], True))
								t(estampe_médaille_E13, a, crm("E13_Attribute_Assignement"))
								t(estampe_médaille_E13, crm("P14_carried_out_by"),
								  she("684b4c1a-be76-474c-810e-0f5984b47921"))
								t(estampe_médaille_E13, crm("P140_assigned_attribute_to"), estampe_zone_médaille)
								t(estampe_médaille_E13, crm("P177_assigned_property_type"), crm("P138_represents"))
								t(estampe_médaille_E13, crm("P141_assigned"), objet_uuid)

								# Si la médaille comporte une inscription
								if row["Médailles: légende"] or row["Médailles: exergue"]:
									# La zone d'inscription
									médaille_inscrip_E36 = she(cache.get_uuid(
										["collection", id, "E36", sujet, "zone de l'image (E36)",
										 "zone de la médaille (E36)", "zone d'inscription", "uuid"], True))
									t(médaille_inscrip_E36, a, crm("E36_Visual_Item"))

									# Ce que représente la zone d'inscription
									médaille_inscrip_E13 = she(cache.get_uuid(
										["collection", id, "E36", sujet, "zone de l'image (E36)",
										 "zone de la médaille (E36)", "zone d'inscription", "E13"], True))
									t(médaille_inscrip_E13, a, crm("E13_Attribute_Assignement"))
									t(médaille_inscrip_E13, crm("P14_carried_out_by"),
									  she("684b4c1a-be76-474c-810e-0f5984b47921"))
									t(médaille_inscrip_E13, crm("P140_assigned_attribute_to"), estampe_zone_médaille)
									t(médaille_inscrip_E13, crm("P141_assigned"), médaille_inscrip_E36)
									t(médaille_inscrip_E13, crm("P177_assigned_property_type"),
									  crm("P106_is_composed_of"))

								# Si la médaille comporte une inscription en légende (E13)
								if row["Médailles: légende"]:
									médaille_inscrip_E33 = she(
										cache.get_uuid(
											["collection", id, "E36", sujet, "zone de l'image (E36)",
											 "zone de la médaille (E36)", "zone d'inscription",
											 "inscription en légende", "uuid"], True))
									t(médaille_inscrip_E33, a, crm("E33_Linguistic_Object"))

									médaille_inscrip_E33_E13 = she(
										cache.get_uuid(
											["collection", id, "E36", sujet, "zone de l'image (E36)",
											 "zone de la médaille (E36)", "zone d'inscription",
											 "inscription en légende", "E13"], True))
									t(médaille_inscrip_E33_E13, a, crm("E13_Attribute_Assignement"))
									t(médaille_inscrip_E33_E13, crm("P14_carried_out_by"),
									  she("684b4c1a-be76-474c-810e-0f5984b47921"))
									t(médaille_inscrip_E33_E13, crm("P140_assigned_attribute_to"),
									  médaille_inscrip_E36)
									t(médaille_inscrip_E33_E13, crm("P141_assigned"), médaille_inscrip_E33)
									t(médaille_inscrip_E33_E13, crm("P177_assigned_property_type"),
									  crm("P165_incorporates"))
									t(médaille_inscrip_E33_E13,
									  she_ns("sheP_position_du_texte_par_rapport_à_la_médaille"),
									  she("fc229531-0999-4499-ab0b-b45e18e8196f"))

									# Contenu de l'inscription
									estampe_médaille_inscrip_P190_E13 = she(
										cache.get_uuid(
											["collection", id, "E36", sujet, "zone de l'image (E36)",
											 "zone de la médaille (E36)", "zone d'inscription",
											 "inscription en légende", "contenu"], True))
									t(estampe_médaille_inscrip_P190_E13, a, crm("E13_Attribute_Assignement"))
									t(estampe_médaille_inscrip_P190_E13, crm("P14_carried_out_by"),
									  she("684b4c1a-be76-474c-810e-0f5984b47921"))
									t(estampe_médaille_inscrip_P190_E13, crm("P140_assigned_attribute_to"),
									  médaille_inscrip_E33)
									t(estampe_médaille_inscrip_P190_E13, crm("P141_assigned"),
									  l(row["Médailles: légende"]))
									t(estampe_médaille_inscrip_P190_E13, crm("P177_assigned_property_type"),
									  crm("P190_has_symbolic_content"))

								# Si la médaille comporte une inscription en exergue (E13)
								if row["Médailles: exergue"]:
									médaille_inscrip_E33 = she(
										cache.get_uuid(
											["collection", id, "E36", sujet, "zone de l'image (E36)",
											 "zone de la médaille (E36)", "zone d'inscription",
											 "inscription en exergue", "uuid"], True))
									t(médaille_inscrip_E33, a, crm("E33_Linguistic_Object"))

									médaille_inscrip_E33_E13 = she(
										cache.get_uuid(
											["collection", id, "E36", sujet, "zone de l'image (E36)",
											 "zone de la médaille (E36)", "zone d'inscription",
											 "inscription en exergue", "E13"], True))
									t(médaille_inscrip_E33_E13, a, crm("E13_Attribute_Assignement"))
									t(médaille_inscrip_E33_E13, crm("P14_carried_out_by"),
									  she("684b4c1a-be76-474c-810e-0f5984b47921"))
									t(médaille_inscrip_E33_E13, crm("P140_assigned_attribute_to"),
									  médaille_inscrip_E36)
									t(médaille_inscrip_E33_E13, crm("P141_assigned"), médaille_inscrip_E33)
									t(médaille_inscrip_E33_E13, crm("P177_assigned_property_type"),
									  crm("P165_incorporates"))
									t(médaille_inscrip_E33_E13,
									  she_ns("sheP_position_du_texte_par_rapport_à_la_médaille"),
									  she("357a459f-4f27-4d46-b5ac-709a410bce04"))

									# Contenu de l'inscription
									estampe_médaille_inscrip_P190_E13 = she(
										cache.get_uuid(
											["collection", id, "E36", sujet, "zone de l'image (E36)",
											 "zone de la médaille (E36)", "zone d'inscription",
											 "inscription en exergue", "contenu"], True))
									t(estampe_médaille_inscrip_P190_E13, a, crm("E13_Attribute_Assignement"))
									t(estampe_médaille_inscrip_P190_E13, crm("P14_carried_out_by"),
									  she("684b4c1a-be76-474c-810e-0f5984b47921"))
									t(estampe_médaille_inscrip_P190_E13, crm("P140_assigned_attribute_to"),
									  médaille_inscrip_E33)
									t(estampe_médaille_inscrip_P190_E13, crm("P141_assigned"),
									  l(row["Médailles: exergue"]))
									t(estampe_médaille_inscrip_P190_E13, crm("P177_assigned_property_type"),
									  crm("P190_has_symbolic_content"))

					except:
						estampe_objet_E13 = she(
							cache.get_uuid(["collection", id, "E36", sujet, "zone de l'image (E36)", "objet représenté"],
							               True))
						t(estampe_objet_E13, a, crm("E13_Attribute_Assignement"))
						t(estampe_objet_E13, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
						t(estampe_objet_E13, crm("P140_assigned_attribute_to"), estampe_zone_img)
						t(estampe_objet_E13, crm("P177_assigned_property_type"), crm("P138_represents"))
						t(estampe_objet_E13, crm("P141_assigned"), l(sujet))
						print("Estampe", id, ": L'objet", sujet,
						      "est introuvable dans le vocabulaire d'indexation d'estampes et le référentiel des personnes")

		# Type/Thématique de la gravure
		if row["Type / Thématique [Avec Maj et au pl.]"]:

			type_thématiques = row["Type / Thématique [Avec Maj et au pl.]"].split("/")

			for type_thématique in type_thématiques:
				type_thématique = type_thématique.strip()

				try:
					type_thématique_uuid = she(concepts_uuid[type_thématique])
					estampe_thématique_E13 = she(cache.get_uuid(["collection", id, "E36", "thématique", "E13"], True))
					t(estampe_thématique_E13, a, crm("E13_Attribute_Assignement"))
					t(estampe_thématique_E13, crm("P14_carried_out_by"),
					  she("684b4c1a-be76-474c-810e-0f5984b47921"))
					t(estampe_thématique_E13, crm("P140_assigned_attribute_to"), estampe)
					t(estampe_thématique_E13, crm("P177_assigned_property_type"),
					  she("f2d9b792-2cfd-4265-a2c5-e0a69ce01536"))
					t(estampe_thématique_E13, crm("P141_assigned"), type_thématique_uuid)
				except:
					print("Estampe", id, ": La thématique ou technique", type_thématique,
					      "est introuvable dans le vocabulaire d'indexation d'estampes")

		# Notes sur la provenance de la gravure
		if row["PROVENANCE de l'estampe"]:
			estampe_notes_E13 = she(cache.get_uuid(["estampes", id, "E36", "notes", "E13"], True))
			t(estampe_notes_E13, a, crm("E13_Attribute_Assignement"))
			t(estampe_notes_E13, crm("P14_carried_out_by"), she("684b4c1a-be76-474c-810e-0f5984b47921"))
			t(estampe_notes_E13, crm("P140_assigned_attribute_to"), estampe)
			t(estampe_notes_E13, crm("P141_assigned"), l(row["PROVENANCE de l'estampe"]))
			t(estampe_notes_E13, crm("P177_assigned_property_type"), crm("P3_has_note"))

		# Autres liens externes
		# TODO Réparer les erreurs URL
		"""
		if row["LIENS EXTERNES"]:
			try:
				lien_externe = u(row["LIENS EXTERNES"])
				estampe_lien_externe_E13 = she(
					cache.get_uuid(["estampes", id, "E36", "lien externe", "E13"], True))
				t(estampe_lien_externe_E13, a, crm("E13_Attribute_Assignement"))
				t(estampe_lien_externe_E13, crm("P14_carried_out_by"),
				  she("684b4c1a-be76-474c-810e-0f5984b47921"))
				t(estampe_lien_externe_E13, crm("P140_assigned_attribute_to"), estampe)
				t(estampe_lien_externe_E13, crm("P141_assigned"), lien_externe)
				t(estampe_lien_externe_E13, crm("P177_assigned_property_type"), RDFS.seeAlso)
			except:
				print("Estampe", id, ": 'Liens externes : " + row["LIENS EXTERNES"] + "' n'est pas une URL valide")
		"""

		# Bibliographie relative à la gravure
		if row["BIBLIO relative à la gravure"]:
			biblio = she(cache.get_uuid(["estampes", id, "E36", "bibliographie", "uuid"], True))
			t(biblio, a, crm("E31_Document"))
			t(biblio, RDFS.label, l(row["BIBLIO relative à la gravure"]))
			## E13 Attribute Assignement
			estampe_biblio_E13 = she(cache.get_uuid(["estampes", id, "E36", "bibliographie", "E13"], True))
			t(estampe_biblio_E13, a, crm("E13_Attribute_Assignement"))
			t(estampe_biblio_E13, crm("P14_carried_out_by"),
			  she("684b4c1a-be76-474c-810e-0f5984b47921"))
			t(estampe_biblio_E13, crm("P140_assigned_attribute_to"), estampe)
			t(estampe_biblio_E13, crm("P141_assigned"), biblio)
			t(estampe_biblio_E13, crm("P177_assigned_property_type"), crm("P70_documents"))

###################################################################################################
# Création du graphe et du cache
###################################################################################################

cache.bye()
save_graph(args.ttl)
