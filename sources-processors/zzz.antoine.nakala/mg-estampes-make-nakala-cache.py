import argparse
import dload
from pathlib import Path
from pprint import pprint
from sherlockcachemanagement import Cache

parser = argparse.ArgumentParser()
parser.add_argument("--cache_estampes")
parser.add_argument("--cache_nakala")
args = parser.parse_args()

cache_estampes = Cache(args.cache_estampes)
cache_nakala = Cache(args.cache_nakala)

# print(cache_estampes.get_uuid(["estampes", "1678-01_000", "E36_uuid"]))
# print(cache_nakala.get_uuid(["1678-01_000", "E36_uuid"]))

url = 'https://api.github.com/repos/sherlock-iremus/mercure-galant-estampes/git/trees/main?recursive=1'
j = dload.json(url)
for file in j["tree"]:
    if file["path"] != ".gitattributes":
        clef_métier = Path(file["path"]).stem
        try:
            existing_e36_uuid = cache_estampes.get_uuid(["estampes", clef_métier, "E36_uuid"], True)
            cache_nakala.set_kv([clef_métier, "E36_uuid"], existing_e36_uuid)
        except:
            print(f"[WARNING] Fichier non référencé dans le classeur d'analyse des estampes : {file['path']}")

cache_nakala.bye()
cache_estampes.bye()
