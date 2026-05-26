import csv
import json
import os
import re

def genera_planning():
    # Carica dati e gestisci le intestazioni (assumendo i nomi corretti dai CSV)
    try:
        dati = {
            "articoli": list(csv.DictReader(open('data/articoli.csv', encoding='utf-8'))),
            "presse": list(csv.DictReader(open('data/presse.csv', encoding='utf-8'))),
            "ordini": list(csv.DictReader(open('data/ordini.csv', encoding='utf-8')))
        }
    except Exception as e:
        print(f"Errore nella lettura dei CSV: {e}")
        return

    # Leggi il template
    with open('docs/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Prepara il blocco JS - assicurati che i nomi dei campi corrispondano ai tuoi CSV
    # Esempio: se nel CSV la colonna è 'ID_Ordine', nel JS useremo ordine.ID_Ordine
    dati_js = f"<script>const APP_DATA = {json.dumps(dati, ensure_ascii=False)};</script>"
    
    # PULIZIA: Rimuovi il vecchio blocco
    html_pulito = re.sub(r'<script>const APP_DATA = .*?</script>', '', html, flags=re.DOTALL)

    # Inserimento sicuro
    if "<!-- DATA_READY -->" in html_pulito:
        nuovo_html = html_pulito.replace("<!-- DATA_READY -->", f"<!-- DATA_READY -->\n{dati_js}")
    else:
        print("Errore: Segnaposto <!-- DATA_READY --> non trovato")
        return

    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(nuovo_html)

if __name__ == "__main__":
    genera_planning()
