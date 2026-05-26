import csv
import json
import os

def leggi_csv(nome_file):
    percorso = os.path.join('data', nome_file)
    if not os.path.exists(percorso):
        print(f"Attenzione: {percorso} non trovato.")
        return []
    with open(percorso, mode='r', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))

def genera_planning():
    # Caricamento dei dati dai file CSV
    articoli = leggi_csv('articoli.csv')
    presse = leggi_csv('presse.csv')
    ordini = leggi_csv('ordini.csv')

    # Verifica la presenza del file HTML
    html_path = os.path.join('docs', 'index.html')
    if not os.path.exists(html_path):
        print("Errore: docs/index.html non trovato.")
        return

    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Prepara le stringhe JSON dei dati
    json_articoli = json.dumps(articoli, ensure_ascii=False)
    json_presse = json.dumps(presse, ensure_ascii=False)
    json_ordini = json.dumps(ordini, ensure_ascii=False)

    # Costruisci il blocco dati JavaScript sostitutivo
    nuovo_blocco_dati = (
        "// DATA_START\n"
        f"        const ARTICOLI_SORGENTE = {json_articoli};\n"
        f"        const PRESSE_SORGENTE = {json_presse};\n"
        f"        const ORDINI_SORGENTE = {json_ordini};\n"
        "        // DATA_END"
    )

    # Cerca i marcatori di inizio e fine dati nell'HTML e sostituisci il contenuto
    marker_start = "// DATA_START"
    marker_end = "// DATA_END"

    if marker_start in html_content and marker_end in html_content:
        parte_iniziale = html_content.split(marker_start)[0]
        parte_finale = html_content.split(marker_end)[1]
        html_aggiornato = parte_iniziale + nuovo_blocco_dati + parte_finale
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_aggiornato)
        print("Planning rigenerato con successo!")
    else:
        print("Errore: Marcatori di iniezione dati non trovati nel file HTML.")

if __name__ == "__main__":
    genera_planning()
