#!/bin/bash

PYTHONPATH="venv/bin"
$PYTHONPATH/python scraper.py
$PYTHONPATH/python creer_tableau.py
$PYTHONPATH/python sendmail.py
