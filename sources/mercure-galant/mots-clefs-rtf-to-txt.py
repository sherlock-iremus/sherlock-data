import glob
import sys, os
from pathlib import Path
from striprtf.striprtf import rtf_to_text
from urlextract import URLExtract
import aspose.words as aw
import re

# !! Ignorer les messages d'erreur automatiques d'aspose.words !! #

# Conversion des fichiers RTF en TXT
for file in glob.glob('indexations-stagiaires/**/*.rtf', recursive = True): 
    text = aw.Document(file)
    text.save(f'{file[:-4]}.txt')

    # Correction des variations de clé
    with open(f'{file[:-4]}.txt', "r") as f:
        text = f.read()
        text = text.replace("Evaluation Only. Created with Aspose.Words. Copyright 2003-2022 Aspose Pty Ltd.", "")
        text = text.replace("Created with an evaluation copy of Aspose.Words. To discover the full versions of our APIs please visit: https://products.aspose.com/words/", "")
        text = text.replace("mot clé ", "mots-clés ")
        text = text.replace("mot-clé ", "mots-clés ")
        text = text.replace("mots clés", "mots-clés")
        text = text.replace("mots  clés", "mots-clés")
        text = text.replace("mots        clés", "mots-clés")
        text = text.replace("mot clés", "mots-clés")
        text = text.replace("Mots clés", "mots-clés")
        text = text.replace("Mot clé ", "mots-clés ")
        text = text.replace("Personnes", "personnes")
        text = text.replace("Personne ", "personnes  ")
        text = text.replace("personne ", "personnes ")
        text = text.replace("persones", "personnes")
        text = text.replace("personnages", "personnes")
        text = text.replace("personnage ", "personnes")
        text = text.replace("oeuvre citée\t", "oeuvres citées ")
        text = text.replace("oeuvre citée ", "oeuvres citées ")
        text = text.replace("Oeuvre citée ", "oeuvres citées ")
        text = text.replace("Oeuvres citées", "oeuvres citées")
        text = text.replace("œuvre citée", "oeuvres citées")
        text = text.replace("Lieu ", "lieux ")
        text = text.replace("lieu ", "lieux ")
        text = text.replace("Lieux", "lieux")
        text = text.replace("Institutions", "institutions")
        text = text.replace("Institution ", "institutions ")
        text = text.replace("institution ", "institutions ")
        text = text.replace("congrégation ", "congrégations ")
        text = text.replace("Congrégation ", "congrégations ")
        text = text.replace("Congrégations", "congrégations")
        text = text.replace("Corporations", "corporations") 
        text = text.replace("Corporation ", "corporations ")
        text = text.replace("corporation ", "corporations ")
        text = re.sub(r'(^\n)|(^\s+)', '', text)

    with open(f'{file[:-4]}.txt', "w") as f:
        f.write(text)