import csv
import json
import os

def leggi_csv(nome_file):
    percorso = os.path.join('data', nome_file)
    if not os.path.exists(percorso):
        print(f"Errore: {percorso} non trovato.")
        return []
    
    # Legge il file CSV gestendo l'eventuale BOM iniziale (utf-8-sig)
    with open(percorso, mode='r', encoding='utf-8-sig') as f:
        # Usa il DictReader per mappare le colonne come chiavi dell'oggetto
        lettore = csv.DictReader(f)
        dati = []
        for riga in lettore:
            # Pulisce eventuali spazi bianchi intorno alle chiavi e ai valori
            riga_pulita = {k.strip(): v.strip() for k, v in riga.items() if k is not None}
            dati.append(riga_pulita)
        return dati

def genera_file_dati():
    # Legge i file CSV originali
    articoli = leggi_csv('articoli.csv')
    presse = leggi_csv('presse.csv')
    ordini = leggi_csv('ordini.csv')

    # Se la cartella docs non esiste, la crea
    if not os.path.exists('docs'):
        os.makedirs('docs')

    # Costruisce il contenuto del file JavaScript contenente solo le variabili pure
    contenuto_js = (
        "// FILE GENERATO AUTOMATICAMENTE - NON MODIFICARE A MANO\n"
        f"const ARTICOLI_SORGENTE = {json.dumps(articoli, ensure_ascii=False)};\n"
        f"const PRESSE_SORGENTE = {json.dumps(presse, ensure_ascii=False)};\n"
        f"const ORDINI_SORGENTE = {json.dumps(ordini, ensure_ascii=False)};\n"
    )

    # Scrive il file js caricabile dall'HTML
    with open('docs/pianificazione.js', 'w', encoding='utf-8') as f:
        f.write(contenuto_js)
    
    print("Sincronizzazione completata! Generato docs/pianificazione.js")

if __name__ == "__main__":
    genera_file_dati()
