import glob
from pathlib import Path
import shutil

files = glob.glob("/Users/amleth/Google Drive/Mon Drive/IReMus/Estampes fichiers d'images/*/**")
for file in files:
    parent_dir = Path(file).parent
    if len(parent_dir.stem) == 4:
        print(file)
        id = Path(file).stem.split(" ")[0]
        ext = Path(file).suffix.lower()
        shutil.copy2(file, f"/Users/amleth/Xobpord/Xobpord3/Dropbox/CNRS/iremus/data-iremus/in/mercure-galant-estampes-github/{id}{ext}")
