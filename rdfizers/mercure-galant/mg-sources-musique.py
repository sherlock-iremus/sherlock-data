import argparse
from rdflib import Literal as l, RDF, RDFS, URIRef as u
import sys, os
from sherlockcachemanagement import Cache
import glob
import ntpath

# Helpers
sys.path.append(os.path.abspath(os.path.join('rdfizers/', '')))
from helpers_rdf import *
sys.path.append(os.path.abspath(os.path.join('python_packages/helpers_excel', '')))
from helpers_excel import *

parser = argparse.ArgumentParser()
parser.add_argument("--ttl")
parser.add_argument("--xlsx")
parser.add_argument("--cache")
parser.add_argument("--cache_tei")
parser.add_argument("--dossier_coll")
args = parser.parse_args()

cache = Cache(args.cache)
if args.cache_tei:
	cache_tei = Cache(args.cache_tei)

init_graph()

for img in glob.glob(args.dossier_coll + '/*.JPG', recursive=False):

	id = ntpath.basename(img[:-4])

	collection = she("3a0fcd6a-c226-49f4-ac11-5eff8448ee55")

	# E36 Visual Item
	gravure = she(cache.get_uuid(["collection", id, "gravure (E36)", "uuid"], True))
	t(gravure, a, crm("E36_Visual_Item"))
	t(collection, crm("P106_is_composed_of"), gravure)
	t(gravure, crm("P2_has_type"), she("e2f6219a-2a40-4724-b4f9-1cf45a4f2849"))

	# Identifiant Mercure Galant
	gravure_id_MG = she(cache.get_uuid(["collection", id, "gravure (E36)", "Identifiant MG"], True))
	t(gravure_id_MG, a, crm("E42_Identifier"))
	t(gravure_id_MG, crm("P2_has_type"), she("92c258a0-1e34-437f-9686-e24322b95305"))
	t(gravure_id_MG, RDFS.label, l(id))
	t(gravure, crm("P1_is_identified_by"), gravure_id_MG)

	# Identifiant IIIF
	gravure_D1 = she(cache.get_uuid(["collection", id, "gravure (E36)", "D1", "uuid"], True))
	t(gravure_D1, a, crmdig("D1_Digital_Object"))
	t(gravure_D1, crm("P130_shows_features_of"), gravure)
	gravure_D1_E42 = she(cache.get_uuid(["collection", id, "gravure (E36)", "D1", "E42", "uuid"], True))
	t(gravure_D1_E42, a, crm("E42_Identifier"))
	t(gravure_D1_E42, crm("P2_has_type"), she("19073c4a-0ef7-4ac4-a51a-e0810a596773"))
	t(gravure_D1, crm("P1_is_identified_by"), gravure_D1_E42)
	t(gravure_D1_E42, crm("P190_has_symbolic_content"), u(f"https://ceres.huma-num.fr/iiif/3/mercure-galant-gravures--{id.replace(' ', '%20')}/full/max/0/default.jpg"))

	# # Identifiant GitHub
	# gravure_id_github = she(
	# 	cache.get_uuid(["collection", id, "gravure (E36)", "Identifiant GitHub"], True))
	# t(gravure_id_github, a, crm("E42_Identifier"))
	# t(gravure_id_github, crm("P2_has_type"), she("cdbec0af-a5c4-49e2-8a71-4a6fc43dd3ea"))
	# t(gravure_id_github, RDFS.label,
	#   u(f"https://github.com/OBVIL/mercure-galant/blob/0ba4cfdbb66ccf7ed6af0a92bf1490a998e95b3c/images/{id.replace(' ', '%20')}.JPG"))
	# t(gravure, crm("P1_is_identified_by"), gravure_id_github)

	# Rattachement ?? l'article
	if "copyOf" in id:
		parties_de_l_id = id.split(" ")

		id_article = parties_de_l_id[0]
		if id_article.endswith("w") or id_article.endswith("x") or id_article.endswith("y") or id_article.endswith("z"):
			id_article = id_article[:-1]

		id_livraison = id_article[:-4]
		if id_livraison.endswith("_"):
			id_livraison = id_livraison[:-1]

		try:
			## Article original
			article_F2_original = she(cache_tei.get_uuid(
				["Corpus", "Livraisons", id_livraison, "Expression originale", "Articles", id_article, "F2"]))
			t(article_F2_original, crm("P106_is_composed_of"), gravure)
			## Article TEI
			article_F2_TEI = she(
				cache_tei.get_uuid(
					["Corpus", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article, "F2"]))
			t(article_F2_TEI, crm("P106_is_composed_of"), gravure)
		except:
			print("Impossible de retrouver l'article de la gravure", id_article, "(livraison " + id_livraison + ")")

	else:
		id_article = id
		if id_article.endswith("w") or id_article.endswith("x") or id_article.endswith("y") or id_article.endswith("z"):
			id_article = id_article[:-1]

		id_livraison = id_article[:-4]
		if id_livraison.endswith("_"):
			id_livraison = id_livraison[:-1]

		try:
			## Article original
			article_F2_original = she(cache_tei.get_uuid(
				["Corpus", "Livraisons", id_livraison, "Expression originale", "Articles", id_article, "F2"]))
			t(article_F2_original, crm("P106_is_composed_of"), gravure)
			## Article TEI
			article_F2_TEI = she(
				cache_tei.get_uuid(
					["Corpus", "Livraisons", id_livraison, "Expression TEI", "Articles", id_article, "F2"]))
			t(article_F2_TEI, crm("P106_is_composed_of"), gravure)

		except:
			print("Impossible de retrouver l'article de la gravure", id_article, "(livraison " + id_livraison + ")")

###################################################################################################
# Cr??ation du graphe et du cache
###################################################################################################

cache.bye()
save_graph(args.ttl)
