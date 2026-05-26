import csv
import json
import os

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
    
    # Inserimento sicuro: cerchiamo <!-- DATA_READY --> e lo sostituiamo con segnaposto + dati
    if "<!-- DATA_READY -->" in html:
        nuovo_html = html.replace("<!-- DATA_READY -->", f"<!-- DATA_READY -->\n{dati_js}")
    else:
        # Se il segnaposto manca, non può funzionare
        print("Errore: Segnaposto <!-- DATA_READY --> non trovato in docs/index.html")
        return

    with open('docs/index.html', 'w', encoding='utf-8') as f:
        f.write(nuovo_html)

if __name__ == "__main__":
    genera_planning()
```

### 2. Verifica `docs/index.html`
Assicurati che il tuo file `docs/index.html` contenga esattamente questa riga di commento, senza spazi aggiuntivi tra i tag:

```html
<!-- DATA_READY -->
