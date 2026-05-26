import csv
import json
import os

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

    # Carica il template originale
    with open('docs/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Prepara il blocco dati con il segnaposto incluso per il prossimo giro
    dati_js = f"<script>const APP_DATA = {json.dumps(dati, ensure_ascii=False)};</script>"
    segnaposto = "<!-- DATA_READY -->"
    
    # Sostituisce il segnaposto con i dati + il segnaposto stesso
    nuovo_html = html.split(segnaposto)[0] + segnaposto + "\n" + dati_js + "\n" + html.split(segnaposto)[1]

    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(nuovo_html)

if __name__ == "__main__":
    genera_planning()
