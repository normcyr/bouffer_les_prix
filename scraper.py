#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aller chercher les prix via http://www.supermarches.ca/epicerie.asp
"""

import json
import yaml
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime


def faire_soupe(url_recherche):

    requete = requests.get(url_recherche)

    if requete.status_code == requests.codes.ok:
        # crée la soupe
        soupe = BeautifulSoup(requete.text, "html.parser")
    else:
        # pleure parce que la page n'est pas disponible
        requete.raise_for_status()

    """
    # pour effectuer les tests hors-ligne
    with open('exemple.html', 'r', encoding='utf-8') as fichier_html:
        soupe = BeautifulSoup(fichier_html, 'html.parser')
    """

    return soupe


def trouver_si_resultats(soupe):

    # trouver section nombre de résultats et extraire le chiffre
    section_nb_produits = soupe.find("table", {"id": "table89"})

    # vérifier s'il y a des spéciaux
    try:
        nb_produits = int(section_nb_produits.find("b").text)
        if nb_produits >= 1:
            speciaux = True
    except AttributeError:
        speciaux = False

    return speciaux


def trouver_resultats(soupe):

    # trouver section liste des résultats
    soupe_resultats = soupe.find_all("tr", {"onmouseover": "this.bgColor = '#FFFFD9'"})

    return soupe_resultats


def creer_liste(soupe_resultats, mot):

    # initialiser liste de résultats
    liste_speciaux = []

    # extraire l'information
    for resultat in soupe_resultats:
        nom_produit = (
            resultat.find("td", {"width": "297"}).text.strip().replace("\n", " ")
        )
        origine_produit = resultat.find("td", {"width": "93"}).text.strip()
        prix_produit = (
            resultat.find("td", {"width": "78"}).text.strip().replace(" / ch.", "")
        )
        periode_special_produit = resultat.find("td", {"width": "74"}).text.strip()
        magasin_produit = resultat.find("td", {"width": "72"}).text.strip()
        format_produit = resultat.find("td", {"width": "86"}).text.strip()

        # créer dictionnaire des résultats
        details_produit = {
            "nom": nom_produit[:40],
            "format": format_produit,
            "origine": origine_produit,
            "prix": str("{}".format(prix_produit)) + " $",
            "période spécial": periode_special_produit,
            "magasin": magasin_produit,
        }

        # ajouter le dictionnaire à la liste de résultats
        liste_speciaux.append(details_produit)

    return liste_speciaux


def sortie_json(liste_speciaux, fichier_sortie):

    with open(fichier_sortie, "a", encoding="utf-8") as outfile:
        json.dump(liste_speciaux, outfile, indent=4, sort_keys=True)


def main():

    # variables
    recherche_url_base = (
        "http://www.supermarches.ca/pages/default.asp?t=&tr=&vd=&ig=&q=rech&cid=&query="
    )
    ajd = datetime.now().strftime("%Y-%m-%d")

    basepath = Path(__file__).parent.resolve()
    fichier_mots = str(Path(basepath / "mots_recherche.yml"))

    # extraire les mots clé à chercher
    with open(fichier_mots, "r") as f_yml:
        mots_recherche = yaml.safe_load(f_yml)

    # mots_recherche = 'Beurre+d\'arachide'
    for mot in mots_recherche:
        mot = mot.replace(" ", "+")
        url_recherche = recherche_url_base + mot
        soupe = faire_soupe(url_recherche)
        speciaux = trouver_si_resultats(soupe)

        if speciaux is True:
            soupe_resultats = trouver_resultats(soupe)

            # faire liste des spéciaux et sortir en json
            fichier_sortie = (
                str(Path(basepath / "liste_speciaux_")) + mot[:6] + ajd + ".json"
            )
            liste_speciaux = creer_liste(soupe_resultats, mot)
            sortie_json(liste_speciaux, fichier_sortie)

        else:
            print("Pas de spéciaux pour {}".format(mot).replace("+", " "))


if __name__ == "__main__":
    main()
