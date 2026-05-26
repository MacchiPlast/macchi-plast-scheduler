import csv
import json
import os
import re

def genera_planning():
    # Carica dati
    dati = {
        "articoli": list(csv.DictReader(open('data/articoli.csv', encoding='utf-8'))),
        "presse": list(csv.DictReader(open('data/presse.csv', encoding='utf-8'))),
        "ordini": list(csv.DictReader(open('data/ordini.csv', encoding='utf-8')))
    }

    # Leggi il template
    with open('docs/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Prepara il blocco JS
    dati_js = f"<script>const APP_DATA = {json.dumps(dati, ensure_ascii=False)};</script>"
    
    # PULIZIA: Rimuovi qualsiasi precedente blocco <script> che contiene APP_DATA
    # Questo cerca il tag script che contiene APP_DATA e lo rimuove
    html_pulito = re.sub(r'<script>const APP_DATA = .*?</script>', '', html, flags=re.DOTALL)

    # Inserimento sicuro
    if "<!-- DATA_READY -->" in html_pulito:
        nuovo_html = html_pulito.replace("<!-- DATA_READY -->", f"<!-- DATA_READY -->\n{dati_js}")
    else:
        print("Errore: Segnaposto <!-- DATA_READY --> non trovato in docs/index.html")
        return

    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(nuovo_html)

if __name__ == "__main__":
    genera_planning()
