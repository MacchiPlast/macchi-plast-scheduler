import csv
import json
import os

# Legge i file CSV dalla cartella data/
def leggi_csv(nome_file):
    percorso = os.path.join('data', nome_file)
    if not os.path.exists(percorso):
        return []
    with open(percorso, mode='r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def genera_planning():
    dati = {
        "articoli": leggi_csv('articoli.csv'),
        "presse": leggi_csv('presse.csv'),
        "ordini": leggi_csv('ordini.csv')
    }

    # Apre l'HTML template
    with open('docs/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Inietta i dati come costante JavaScript
    dati_js = f"const APP_DATA = {json.dumps(dati, ensure_ascii=False)};"
    
    # Sostituisce il commento segnaposto con il blocco script dei dati
    nuovo_html = html.replace('<!-- DATA_READY -->', f'<script>{dati_js}</script>')

    # Salva il file aggiornato
    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(nuovo_html)

if __name__ == "__main__":
    genera_planning()
