#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from datetime import datetime
from tabulate import tabulate
from jinja2 import Environment, FileSystemLoader


def faire_tableau_html(texte_json, fichier_html, ajd):

    file_loader = FileSystemLoader("gabarits")
    env = Environment(loader=file_loader)
    template = env.get_template("tableau.html")

    with open(fichier_html, "w") as f:
        f.write(
            template.render(
                info_speciaux=texte_json, fichier_html=fichier_html, date_genere=ajd
            )
        )


def faire_tableau_texte(texte_json, fichier_texte, ajd):

    # créer le tableau texte avec le module tabulate
    tableau_texte = tabulate(texte_json, headers="keys")

    # enregistrer en fichier TXT
    with open(fichier_texte, "w") as f:
        f.write('<html>\n<body>\n<pre style="font: monospace">\n')
        f.write("Spéciaux sur le beurre d'arachide.\n")
        f.write("Généré le {}.\n".format(ajd))
        f.write("\n")
        f.write(tableau_texte + "\n")
        f.write("</pre>\n</body>\n</html>\n")

    return tableau_texte


def main():

    ajd = datetime.now().strftime("%Y-%m-%d")

    # je dois changer ceci pour une variable
    produit = "Beurre"
    # produit = "Yogour"

    basepath = Path(__file__).parent.resolve()
    fichier_json = str(Path(basepath / "liste_speciaux_")) + produit + ajd + ".json"
    fichier_html = str(Path(basepath / "liste_speciaux_")) + ajd + ".html"
    fichier_texte = str(Path(basepath / "announcement")) + ".txt"

    # lire les données JSON
    with open(fichier_json, "r") as f:
        texte_json = json.load(f)
        tableau_texte = faire_tableau_texte(texte_json, fichier_texte, ajd)
        faire_tableau_html(texte_json, fichier_html, ajd)

    return tableau_texte


if __name__ == "__main__":
    main()
