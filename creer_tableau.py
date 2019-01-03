#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime
from json2html import *
from tabulate import tabulate

def faire_tableau_html(texte_json, fichier_html):

    tableau_html = json2html.convert(json = texte_json)
    with open(fichier_html, 'w') as f2:
        f2.write(tableau_html)

    return(tableau_html)

def faire_tableau_texte(texte_json, fichier_texte, ajd):

    # créer le tableau texte avec le module tabulate
    tableau_texte = tabulate(texte_json, headers = 'keys')

    # enregistrer en fichier TXT
    with open(fichier_texte, 'w') as f:
        f.write('<html>\n<body>\n<pre style="font: monospace">\n')
        f.write('Spéciaux sur le beurre d\'arachide.\n')
        f.write('Généré le {}.\n'.format(ajd))
        f.write('\n')
        f.write(tableau_texte+'\n')
        f.write('</pre>\n</body>\n</html>\n')

    return(tableau_texte)

def main():

    ajd = datetime.now().strftime("%Y%m%d")

    # je dois changer ceci pour une variable
    produit = 'Beurre'

    fichier_json = 'liste_speciaux_' + produit + ajd + '.json'
    fichier_html = 'liste_speciaux_' + ajd + '.html'
    fichier_texte = 'liste_speciaux_' + ajd + '.txt'

    # lire les données JSON
    with open(fichier_json, 'r') as f:
        texte_json = json.load(f)
        tableau_texte = faire_tableau_texte(texte_json, fichier_texte, ajd)
        #print(tableau_texte)

    #tableau_html = faire_tableau_html(texte_json, fichier_html)

    return(tableau_texte)

if __name__ == '__main__':
    main()
