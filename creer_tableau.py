#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime
from json2html import *
from tabulate import tabulate

def faire_tableau_html(fichier_json, fichier_html):

    with open(fichier_json, 'r', encoding='utf-8') as f:
        texte_json = json.load(f)
        tableau_html = json2html.convert(json = texte_json)

    with open(fichier_html, 'w') as f2:
        f2.write(tableau_html)

    return(tableau_html)

def faire_tableau_texte(fichier_json, fichier_texte, ajd):

    # lire les données JSON
    with open(fichier_json, 'r', encoding='utf-8') as f:
        texte_json = json.load(f)

    # créer le tableau texte avec le module tabulate
    tableau_texte = tabulate(texte_json, headers = 'keys')

    # enregistrer en fichier TXT
    with open(fichier_texte, 'w', encoding='utf-8') as f:
        f.write('Spéciaux sur le beurre d\'arachide.\n')
        f.write('Généré le {}.\n'.format(ajd))
        f.write('\n')
        f.write(tableau_texte+'\n')

    return(tableau_texte)

def main():

    ajd = datetime.now().strftime("%Y%m%d")

    fichier_json = 'liste_speciaux_' + ajd + '.json'
    fichier_html = 'liste_speciaux_' + ajd + '.html'
    fichier_texte = 'liste_speciaux_' + ajd + '.txt'

    #tableau_html = faire_tableau_html(fichier_json, fichier_html)
    tableau_texte = faire_tableau_texte(fichier_json, fichier_texte, ajd)

if __name__ == '__main__':
    main()
