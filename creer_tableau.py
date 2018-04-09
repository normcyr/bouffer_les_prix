#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime
from json2html import *
from tabulate import tabulate
import csv

def faire_tableau_html(fichier_json, fichier_html):

    with open(fichier_json, 'r') as f:
        texte_json = json.load(f)
        tableau_html = json2html.convert(json = texte_json)

    with open(fichier_html, 'w') as f2:
        f2.write(tableau_html)

    return(tableau_html)

def faire_tableau_texte(fichier_json, fichier_texte):

    with open(fichier_json, 'r') as f:
        texte_json = json.load(f)

    tableau_texte = tabulate(texte_json, headers = 'keys')

    print(tableau_texte)

    return(tableau_texte)

def main():

    ajd = datetime.now().strftime("%Y%m%d")

    fichier_json = 'liste_speciaux_' + ajd + '.json'
    fichier_html = 'liste_speciaux_' + ajd + '.html'
    fichier_texte = 'liste_speciaux_' + ajd + '.txt'

    #tableau_html = faire_tableau_html(fichier_json, fichier_html)

    tableau_texte = faire_tableau_texte(fichier_json, fichier_texte)

if __name__ == '__main__':
    main()
