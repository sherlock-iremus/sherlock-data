import argparse
from rdflib import Literal as l, RDF, RDFS, URIRef as u
import sys, os
from openpyxl import load_workbook
from pprint import pprint
import requests
import yaml

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

def make_E13(path, subject, predicate, object):
  E13_uri = she(cache.get_uuid(path, True))
  t(E13_uri, a, crm("E13_Attribute_Assignement"))
  t(E13_uri, crm("P14_carried_out_by"), she("846ef057-41d5-48e1-bd7f-2299b2faaf00"))
  t(E13_uri, crm("P140_assigned_attribute_to"), subject)
  t(E13_uri, crm("P141_assigned"), object)
  t(E13_uri, crm("P177_assigned_property_type"), predicate)

###################################################################################################
# Récupération du vocabulaire d'indexation des estampes
###################################################################################################

with open(args.vocab_estampes, "r+") as f:
    concepts_uuid = yaml.safe_load(f)

###################################################################################################
# Traitement des estampes
###################################################################################################

rows = get_xlsx_rows_as_dicts(args.xlsx)
for row in rows:
	if row["ID estampe"] is not None:
		collection = she("759d110d-fd68-47bb-92fd-341bb63dbcae")
		id = row["ID estampe"]

		# L'estampe (E36)
		estampe = she(cache.get_uuid(["estampes", id, "E36", "uuid"], True))
		t(estampe, a, crm("E36_Visual_Item"))
		t(collection, crm("P165_has_component"), estampe)
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
		  u(f"https://ceres.huma-num.fr/iiif/3/mercure-galant-estampes--{id.replace(' ', '%20')}/full/max/0/default.jpg"))
		t(estampe, crm("P1_is_identified_by"), estampe_id_iiif)

		# Production (E12) de l'estampe
		if row["Inventeur (du sujet) ['Invenit' ou 'Pinxit' ou 'Delineavit']"] or row[
			"Graveur ['Sculpsit' ou 'Incidit' ou 'fecit']"]:
			estampe_E12 = she(cache.get_uuid(["estampes", id, "E36", "E12", "uuid"], True))
			t(estampe_E12, a, crm("E12_Production"))
			t(estampe_E12, crm("P108_has_produced"), estampe)

		# Invenit (concepteur de l'estampe) (sous-E12)
		if row["Inventeur (du sujet) ['Invenit' ou 'Pinxit' ou 'Delineavit']"]:
			estampe_invenit = she(cache.get_uuid(["estampes", id, "E36", "E12", "invenit", "uuid"], True))
			t(estampe_invenit, a, crm("E12_Production"))
			t(estampe_invenit, crm("P2_has_type"), she("4d57ac14-247f-4b0e-90ca-0397b6051b8b"))
			t(estampe_E12, crm("P9_consists_of"), estampe_invenit)

			## Lien entre conception de l'estampe et concepteur (E13)
			estampe_invenit_auteur = she(cache.get_uuid(["estampes", id, "E36", "E12", "invenit", "auteur"], True))
			t(estampe_invenit_auteur, a, crm("E21_Person"))
			t(estampe_invenit_auteur, RDFS.label,
			  l(row["Inventeur (du sujet) ['Invenit' ou 'Pinxit' ou 'Delineavit']"]))
			make_E13(["estampes", id, "E36", "E12", "invenit", "E13"], estampe_invenit, crm("P14_carried_out_by"), estampe_invenit_auteur)

			## Technique de la représentation de l'estampe (E13 sur une E29)
			if row["Technique de la représentation [Avec Maj et au pl.]"]:
				estampe_E29 = she(cache.get_uuid(["estampes", id, "E36", "E12", "E29", "uuid"], True))
				t(estampe_E29, a, crm("E29_Design_or_Procedure"))
				t(estampe_E29, RDFS.label, l(row["Technique de la représentation [Avec Maj et au pl.]"]))
				make_E13(["estampes", id, "E36", "E12", "E29", "E13"], estampe_invenit, crm("P33_used_specific_technique"), estampe_E29)

		# Sculpsit (graveur de l'estampe) (sous-E12)
		if row["Graveur ['Sculpsit' ou 'Incidit' ou 'fecit']"]:
			estampe_sculpsit = she(cache.get_uuid(["estampes", id, "E36", "E12", "sculpsit", "uuid"], True))
			t(estampe_sculpsit, a, crm("E12_Production"))
			t(estampe_sculpsit, crm("P2_has_type"), she("f39eb497-5559-486c-b5ce-6a607f615773"))
			t(estampe_E12, crm("P9_consists_of"), estampe_sculpsit)

			## Lien entre la gravure de l'estampe et son graveur (E13)
			estampe_sculpsit_auteur = she(cache.get_uuid(["estampes", id, "E36", "E12", "sculpsit", "auteur"], True))
			t(estampe_sculpsit_auteur, a, crm("E21_Person"))
			t(estampe_sculpsit_auteur, RDFS.label, l(row["Graveur ['Sculpsit' ou 'Incidit' ou 'fecit']"]))
			make_E13(["estampes", id, "E36", "E12", "sculpsit", "E13"], estampe_sculpsit, crm("P14_carried_out_by"), estampe_sculpsit_auteur)

			## Technique de la gravure (E13 sur une E55)
			if row["Technique de la gravure [Avec Maj et au pl.]"]:
				estampe_E55 = she(cache.get_uuid(["estampes", id, "E36", "E12", "E55", "uuid"], True))
				t(estampe_E55, a, crm("E55_Type"))
				t(estampe_E55, RDFS.label, l(row["Technique de la gravure [Avec Maj et au pl.]"]))
				make_E13(["estampes", id, "E36", "E12", "E55", "E13"], estampe_sculpsit, crm("P32_used_general_technique"), estampe_E55)

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
				t(livraison_F2_originale, crm("P165_has_component"), estampe)

				# Livraison TEI
				livraison_F2_TEI = she(
					cache_tei.get_uuid(["Corpus", "Livraisons", id_livraison, "Expression TEI", "F2"]))
				t(livraison_F2_TEI, crm("P165_has_component"), estampe)
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
					t(article_F2_original, crm("P165_has_component"), estampe)

					### Article TEI
					article_F2_TEI = she(cache_tei.get_uuid(
						["Corpus", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article, "F2"]))
					t(article_F2_TEI, crm("P165_has_component"), estampe)
				else:

					### Article original
					article_F2_original = she(cache_tei.get_uuid(
						["Corpus", "Livraisons", id_livraison, "Expression originale", "Articles", id_article, "F2"]))
					t(article_F2_original, crm("P165_has_component"), estampe)

					### Article TEI
					article_F2_TEI = she(cache_tei.get_uuid(
						["Corpus", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article, "F2"]))
					t(article_F2_TEI, crm("P165_has_component"), estampe)
			except:
				print("Estampe", id, "Article contenant la gravure : l'article " + id_article + " est introuvable dans les fichiers TEI")

		# Article annexe à la gravure
		if row["ID OBVIL article lié"]:
			id_article = row["ID OBVIL article lié"][3:]
			id_livraison = id_article[0:10]
			try:
				article_F2 = she(cache_tei.get_uuid(
					["Corpus", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article, "F2"]))
				make_E13(["estampes", id, "E36", "seeAlso", "E13"], estampe, RDFS.seeAlso, article_F2)

				## Commentaire décrivant le lien entre la gravure et l'article
				if row["Commentaire ID article lié OBVIL"]:
					make_E13(["estampes", id, "E36", "seeAlso", "note", "E13"], article_F2, crm("P3_has_note"), l(row["Commentaire ID article lié OBVIL"]))
			except:
				print("Estampe", id, "Article annexe à la gravure : l'article " + id_article + " est introuvable dans les fichiers TEI")

		# Lien Gallica
		# TODO Réparer les URL
		# if row["Lien vers le texte [ou l'image] en ligne"]:
		# 	try:
		# 		lien_gallica = u(row["Lien vers le texte [ou l'image] en ligne"])
		# 		t(lien_gallica, crm("P2_has_type"), she("e73699b0-9638-4a9a-bfdd-ed1715416f02"))
		# 		make_E13(["estampes", id, "E36", "gallica", "E13"], estampe, RDFS.seeAlso, lien_gallica)
		# 	except:
		# 		pass
			# print("'Gallica: " + row["Lien au texte [ou à l'image] en ligne"] + "' n'est pas une URL valide")

		# Titre sur l'image (E13)
		if row["Titre sur l'image"]:
			titre = row["Titre sur l'image"].replace("[", "").replace("]", "").replace("*", ""))
			make_E13(["estampes", id, "E36", "titre sur l'image", "E13"], estampe, she("01a07474-f2b9-4afd-bb05-80842ecfb527"), l(titre))

		# Titre descriptif/forgé (E13)
		if row["[titre descriptif forgé]* (Avec Maj - accentuées]"]:
			titre = row["[titre descriptif forgé]* (Avec Maj - accentuées]"].replace("[", "").replace("]", "").replace("*", ""))
			make_E13(["estampes", id, "E36", "titre forgé"], estampe, she("58fb99dd-1ffb-4e00-a16f-ef6898902301"), l(titre))

		# Titre dans le péritexte (E13)
		if row["[Titre dans le péritexte: Avis, article…]"]:
			titre = row["[Titre dans le péritexte: Avis, article…]"].replace("[", "").replace("]", "").replace("*", "")
			make_E13(["estampes", id, "E36", "titre péritexte"], estampe, she("ded9ea93-b400-4550-9aa8-e5aac1d627a0"), l(titre))
			
		# Lieu représenté
		if row["Lieux représentés"]:

			lieu = row["Lieux représentés"]

			## Zone de l'image comportant la représentation du lieu (E13)
			estampe_zone_img = she(cache.get_uuid(["estampes", id, "E36", lieu, "zone de l'image (E36)", "uuid"], True))
			t(estampe_zone_img, a, crm("E36_Visual_Item"))
			make_E13(["estampes", id, "E36", lieu, "zone de l'image (E36)", "E13"], estampe, crm("P106_is_composed_of"), estampe_zone_img)

			## Recherche d'UUID dans le référentiel des lieux
			try:
				lieu_uuid = she(cache_lieux.get_uuid(["lieux", str(lieu), "E93", "uuid"]))
				if lieu_uuid:
					make_E13(["estampes", id, "E36", lieu, "zone de l'image (E36)", "lieu représenté"], estampe_zone_img, crm("P138_represents"), lieu_uuid))

			except:
				make_E13(["collection", id, "E36", lieu, "zone de l'image (E36)", "lieu représenté"], estampe_zone_img, crm("P138_represents"), l(lieu))

		# Objet représenté (E13)
		if row["Objets représentés"]:
			objets = row["Objets représentés"].split(";")
			for objet in objets:
				objet = objet.strip()
				# Zone de l'image représentant l'objet (E13)
				make_E13(["estampes", id, "E36", objet, "zone de l'image (E36)", "uuid"], estampe, crm("P106_is_composed_of"), estampe_zone_img)
					# Si l'objet est issu du vocabulaire des estampes, recherche de son UUID
					try:
						objet_uuid = she(concepts_uuid[objet])
						# Si l'objet représenté n'est pas une médaille
						if objet_uuid != "24aee532-c740-4232-bb6c-c66cf1f3f432":
							make_E13(["collection", id, "E36", sujet, "zone de l'image (E36)", "objet représenté"], estampe_zone_img, crm("P138_represents"), objet_uuid)
						# Si l'objet représenté est une médaille (E13)
						if objet == "médaille":
							# Zone d'image imbriquée dans la première zone et correspondant à la médaille
							estampe_zone_médaille = she(
								cache.get_uuid(
									["estampes", id, "E36", objet, "zone de l'image (E36)", "zone de la médaille (E36)",
										"uuid"], True))
							t(estampe_zone_médaille, a, crm("E36_Visual_Item"))
							make_E13(["estampes", id, "E36", objet, "zone de l'image (E36)", "zone de la médaille (E36)",
										"E13 zone"], estampe_zone_img, crm("P106_is_composed_of"), estampe_zone_médaille)
							# La zone d'image représente une médaille
							make_E13(["collection", id, "E36", objet, "zone de l'image (E36)", "zone de la médaille (E36)",
									"E13 représentation"], estampe_zone_médaille, crm("P138_represents"), objet_uuid)
							# Si la médaille comporte une inscription
							if row["Médailles: avers"] or row["Médailles: revers"]:
								# La zone d'inscription
								médaille_inscrip_E36 = she(cache.get_uuid(
									["collection", id, "E36", objet, "zone de l'image (E36)",
										"zone de la médaille (E36)", "zone d'inscription", "uuid"], True))
								t(médaille_inscrip_E36, a, crm("E36_Visual_Item"))

								# Ce que représente la zone d'inscription
								make_E13(["collection", id, "E36", objet, "zone de l'image (E36)",
										"zone de la médaille (E36)", "zone d'inscription", "E13"], estampe_zone_médaille, crm("P106_is_composed_of"), médaille_inscrip_E36)

							# Si la médaille comporte une inscription sur son avers (E13)
							if row["Médailles: avers"]:
								médaille_inscrip_E33 = she(
									cache.get_uuid(
										["collection", id, "E36", objet, "zone de l'image (E36)",
											"zone de la médaille (E36)", "zone d'inscription",
											"avers", "uuid"], True))
								t(médaille_inscrip_E33, a, crm("E33_Linguistic_Object"))

								make_E13(["collection", id, "E36", objet, "zone de l'image (E36)",
											"zone de la médaille (E36)", "zone d'inscription",
											"avers", "E13"], médaille_inscrip_E36, crm("P165_incorporates"), médaille_inscrip_E33)
								t(E13_uri,
									she_ns("sheP_position_du_texte_par_rapport_à_la_médaille"),
									she("fc229531-0999-4499-ab0b-b45e18e8196f"))

								# Contenu de l'inscription
								make_E13(["collection", id, "E36", objet, "zone de l'image (E36)",
											"zone de la médaille (E36)", "zone d'inscription",
											"avers", "contenu", "E13"], médaille_inscrip_E33, crm("P190_has_symbolic_content"), l(row["Médailles: avers"])

							# Si la médaille comporte une inscription sur son revers (E13)
							if row["Médailles: revers"]:
								médaille_inscrip_E33 = she(
									cache.get_uuid(
										["collection", id, "E36", objet, "zone de l'image (E36)",
											"zone de la médaille (E36)", "zone d'inscription",
											"revers", "uuid"], True))
								t(médaille_inscrip_E33, a, crm("E33_Linguistic_Object"))

								make_E13(["collection", id, "E36", objet, "zone de l'image (E36)",
											"zone de la médaille (E36)", "zone d'inscription",
											"revers", "E13"], médaille_inscrip_E36, crm("P165_incorporates"), médaille_inscrip_E33, )
								t(E13_uri,
									she_ns("sheP_position_du_texte_par_rapport_à_la_médaille"),
									she("357a459f-4f27-4d46-b5ac-709a410bce04"))

								# Contenu de l'inscription
								make_E13(["collection", id, "E36", objet, "zone de l'image (E36)",
											"zone de la médaille (E36)", "zone d'inscription",
											"revers", "contenu", "E13"], médaille_inscrip_E33, crm("P190_has_symbolic_content"), l(row["Médailles: revers"]))
					except:
						make_E13(["collection", id, "E36", objet, "zone de l'image (E36)", "objet représenté"], estampe_zone_img, crm("P138_represents"), l(objet))
						print("Estampe", id, ": L'objet", objet,
						      "est introuvable dans le vocabulaire d'indexation d'estampes et le référentiel des personnes")


		# Personnes représentées
		if row["Personnes représentées"]:
			personnes = row["Personnes représentés"].split(";")
			for personne in personnes:
				personne = personne.strip()
				make_E13(["collection", id, "E36", objet, "zone de l'image (E36)", "personne représentée"], estampe_zone_img, crm("P138_represents"), she(personne))


		# Type/Thématique de la gravure
		if row["Thématique [Avec Maj et au pl.]"]:
			thématiques = row["Thématique [Avec Maj et au pl.]"].split(";")
			for thématique in thématiques:
				thématique = thématique.strip()
				try:
					thématique_uuid = she(concepts_uuid[thématique])
					make_E13(["collection", id, "E36", "thématique", "E13"], estampe, she("f2d9b792-2cfd-4265-a2c5-e0a69ce01536"), thématique_uuid)
				except:
					print("Estampe", id, ": La thématique", thématique,
					      "est introuvable dans le vocabulaire d'indexation d'estampes")

		# TODO institutions associées
		# TODO lieux associés
		# TODO personnes associées

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
