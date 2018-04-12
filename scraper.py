#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Aller chercher les prix via http://www.supermarches.ca/epicerie.asp
'''

from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime
import csv

def faire_soupe(url_recherche):

    requete = requests.get(url_recherche)

    if requete.status_code == requests.codes.ok:
        # crée la soupe
        soupe = BeautifulSoup(requete.text, 'html.parser')
    else:
        # pleure parce que la page n'est pas disponible
        requete.raise_for_status()

    '''
    # pour effectuer les tests hors-ligne
    with open('exemple.html', 'r', encoding='utf-8') as fichier_html:
        soupe = BeautifulSoup(fichier_html, 'html.parser')
    '''

    return(soupe)

def trouver_si_resultats(soupe):

    # trouver section nombre de résultats et extraire le chiffre
    section_nb_produits = soupe.find('table', {'id': 'table89'})

    # vérifier s'il y a des spéciaux
    try:
        nb_produits = int(section_nb_produits.find('b').text)
        speciaux = True
    except AttributeError:
        speciaux = False

    return(speciaux)

def trouver_resultats(soupe):

    # trouver section liste des résultats
    soupe_resultats = soupe.find_all('tr', {'onmouseover': 'this.bgColor = \'#FFFFD9\''})

    return(soupe_resultats)


def creer_liste(soupe_resultats, fichier_sortie_csv):

    # initialiser liste de résultats
    liste_speciaux = []

    # extraire l'information
    for resultat in soupe_resultats:
        nom_produit = resultat.find('td', {'width': '297'}).text.strip().replace('\n', ' ')
        origine_produit = resultat.find('td', {'width': '93'}).text.strip()
        prix_produit = float(resultat.find('td', {'width': '78'}).text.strip().replace(' / ch.', ''))
        periode_special_produit = resultat.find('td', {'width': '74'}).text.strip()
        magasin_produit = resultat.find('td', {'width': '72'}).text.strip()

        # enlever la mention de l'unité de mesure et mettre format sur même unité (ici: gramme)
        format_produit = resultat.find('td', {'width': '86'}).text.strip()
        if format_produit[-2:] == 'kg':
            format_produit_grammes = int(format_produit[:-2]) * 1000
        else:
            format_produit_grammes = int(format_produit[:-2])

        # calculer coût par 100 g
        cout_100g_produit = prix_produit / (format_produit_grammes / 100)

        # créer dictionnaire des résultats
        details_produit = {'nom': nom_produit, 'format': format_produit, 'origine': origine_produit, 'prix': str('{:.2f}'.format(prix_produit)) + ' $', 'prix / 100 g': str('{:.2f}'.format(cout_100g_produit)) + ' $', 'période spécial': periode_special_produit, 'magasin': magasin_produit}

        # ajouter le dictionnaire à la liste de résultats
        liste_speciaux.append(details_produit)

        # création fichier CSV
        rangee = [nom_produit, format_produit, origine_produit, prix_produit, periode_special_produit, magasin_produit]
        with open(fichier_sortie_csv, 'a', encoding='utf-8') as csv_sortie:
            writer = csv.writer(csv_sortie, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(rangee)

    return(liste_speciaux)

def extraire_json(liste_speciaux, fichier_sortie):

    with open(fichier_sortie, 'w', encoding='utf-8') as outfile:
        json.dump(liste_speciaux, outfile, indent = 4, sort_keys = True)

def main():

    # variables
    recherche_url_base = 'http://www.supermarches.ca/pages/default.asp?t=&tr=&vd=&ig=&q=rech&cid=&query='
    mots_recherche = 'Beurre+d\'arachide+Croquant+Kraft'
    url_recherche = recherche_url_base + mots_recherche
    ajd = datetime.now().strftime("%Y%m%d")
    fichier_sortie = 'liste_speciaux_' + ajd + '.json'
    fichier_sortie_csv = 'liste_speciaux_' + ajd + '.csv'

    soupe = faire_soupe(url_recherche)
    speciaux = trouver_si_resultats(soupe)

    if speciaux == True:
        soupe_resultats = trouver_resultats(soupe)

        # écrire entêtes du fichier csv
        with open(fichier_sortie_csv, 'w', encoding='utf-8') as csv_sortie:
            writer = csv.writer(csv_sortie, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(['Nom', 'Format', 'Origine', 'Prix', 'Période du spécial', 'Magasin'])

        # faire liste des spéciaux et sortir en csv et json
        liste_speciaux = creer_liste(soupe_resultats, fichier_sortie_csv)
        extraire_json(liste_speciaux, fichier_sortie)

    else:
        print('Pas de spéciaux pour {}'.format(mots_recherche).replace('+', ' '))

if __name__ == '__main__':
    main()
