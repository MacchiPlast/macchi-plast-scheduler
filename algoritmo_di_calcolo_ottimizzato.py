import os
import csv
from datetime import datetime, timedelta

# Data di riferimento: Lunedì 25 Maggio 2026 alle 06:00
DATA_CORRENTE = datetime(2026, 5, 25, 6, 0)

# 11 Presse dell'officina
PRESSE_DEFAULT = [
    {"ID_Pressa": "P01", "Modello": "Arburg 50t", "Tonnellaggio": 50, "Stato": "Attiva"},
    {"ID_Pressa": "P02", "Modello": "Negri Bossi 100t", "Tonnellaggio": 100, "Stato": "Attiva"},
    {"ID_Pressa": "P03", "Modello": "Engel 100t", "Tonnellaggio": 100, "Stato": "Attiva"},
    {"ID_Pressa": "P04", "Modello": "BMB 150t", "Tonnellaggio": 150, "Stato": "Attiva"},
    {"ID_Pressa": "P05", "Modello": "Negri Bossi 150t", "Tonnellaggio": 150, "Stato": "Attiva"},
    {"ID_Pressa": "P06", "Modello": "Engel 180t", "Tonnellaggio": 180, "Stato": "Attiva"},
    {"ID_Pressa": "P07", "Modello": "Arburg 200t", "Tonnellaggio": 200, "Stato": "Attiva"},
    {"ID_Pressa": "P08", "Modello": "BMB 250t", "Tonnellaggio": 250, "Stato": "Attiva"},
    {"ID_Pressa": "P09", "Modello": "Krauss Maffei 300t", "Tonnellaggio": 300, "Stato": "Attiva"},
    {"ID_Pressa": "P10", "Modello": "Negri Bossi 350t", "Tonnellaggio": 350, "Stato": "Attiva"},
    {"ID_Pressa": "P11", "Modello": "Engel 400t", "Tonnellaggio": 400, "Stato": "Attiva"},
]

# Database degli Articoli con Vincoli Macchina Rigidi
ARTICOLI_DEFAULT = [
    {"ID_Articolo": "ART-001", "Descrizione": "Scatola PP Nera", "Codice_Stampo": "ST-001", "Impronte": 2, "Tempo_Ciclo": 25, "Materiale": "PP", "Colore": "Nero", "Tonnellaggio_Min": 100, "Pressa_Vincolata": ""},
    {"ID_Articolo": "ART-022", "Descrizione": "Coperchio ABS Grigio", "Codice_Stampo": "ST-022", "Impronte": 1, "Tempo_Ciclo": 30, "Materiale": "ABS", "Colore": "Grigio", "Tonnellaggio_Min": 150, "Pressa_Vincolata": "P05"}, # Vincolo rigido P05
    {"ID_Articolo": "ART-045", "Descrizione": "Connettore PA6 Naturale", "Codice_Stampo": "ST-045", "Impronte": 4, "Tempo_Ciclo": 20, "Materiale": "PA6", "Colore": "Naturale", "Tonnellaggio_Min": 50, "Pressa_Vincolata": ""},
    {"ID_Articolo": "ART-089", "Descrizione": "Filtro PC Trasparente", "Codice_Stampo": "ST-089", "Impronte": 1, "Tempo_Ciclo": 40, "Materiale": "PC", "Colore": "Trasparente", "Tonnellaggio_Min": 100, "Pressa_Vincolata": ""},
    {"ID_Articolo": "ART-112", "Descrizione": "Contenitore HDPE Blu", "Codice_Stampo": "ST-112", "Impronte": 1, "Tempo_Ciclo": 45, "Materiale": "HDPE", "Colore": "Blu", "Tonnellaggio_Min": 250, "Pressa_Vincolata": ""},
]

ORDINI_DEFAULT = [
    {"ID_Ordine": "ORD-2026-001", "Articolo": "ART-022", "Quantita_Richiesta": 950, "Data_Scadenza": "2026-05-29", "Priorita": "Alta"},
    {"ID_Ordine": "ORD-2026-002", "Articolo": "ART-001", "Quantita_Richiesta": 5000, "Data_Scadenza": "2026-05-30", "Priorita": "Normale"},
    {"ID_Ordine": "ORD-2026-003", "Articolo": "ART-045", "Quantita_Richiesta": 6000, "Data_Scadenza": "2026-05-28", "Priorita": "Alta"},
]

def get_grado_colore(colore):
    c = colore.lower()
    if any(x in c for x in ["trasparente", "naturale", "bianco", "giallo"]):
        return 1  # Chiaro
    if any(x in c for x in ["nero", "marrone"]):
        return 3  # Scuro
    return 2  # Medio

def aggiungi_ore_lavorative(data_partenza, ore):
    """Calcola il tempo reale di produzione saltando i fine settimana (Venerdì 22:00 -> Lunedì 06:00)."""
    corrente = datetime.fromtimestamp(data_partenza.timestamp())
    minuti_rimanenti = int(round(ore * 60))

    while minuti_rimanenti > 0:
        corrente += timedelta(minutes=1)
        wd = corrente.weekday() # 0=Lun, 4=Ven, 5=Sab, 6=Dom
        ora = corrente.hour

        is_weekend = False
        if wd == 4 and ora >= 22:
            is_weekend = True
        elif wd in [5, 6]:
            is_weekend = True
        elif wd == 0 and ora < 6:
            is_weekend = True

        if is_weekend:
            # Salta a Lunedì ore 06:00
            giorni_da_aggiungere = (0 - wd + 7) % 7
            if giorni_da_aggiungere == 0 and (wd == 0 and ora < 6):
                corrente = corrente.replace(hour=6, minute=0, second=0, microsecond=0)
            else:
                if giorni_da_aggiungere == 0:
                    giorni_da_aggiungere = 7
                corrente += timedelta(days=giorni_da_aggiungere)
                corrente = corrente.replace(hour=6, minute=0, second=0, microsecond=0)
        else:
            minuti_rimanenti -= 1
            
    return corrente

def calcola_tempo_attrezzaggio(art_prec, art_succ):
    """Calcola lo spurgo in base alla matrice di cambio colore."""
    if not art_prec:
        return 2.0

    stesso_stampo = art_prec["Codice_Stampo"] == art_succ["Codice_Stampo"]
    stesso_mat = art_prec["Materiale"] == art_succ["Materiale"]
    stesso_col = art_prec["Colore"] == art_succ["Colore"]

    if stesso_stampo and stesso_mat and stesso_col:
        return 0.0

    if not stesso_mat:
        return 3.5  # Cambio completo materiale/stampo

    grado_prec = get_grado_colore(art_prec["Colore"])
    grado_succ = get_grado_colore(art_succ["Colore"])

    if grado_prec < grado_succ:
        return 1.0  # Da Chiaro a Scuro: Facile (1.0 ora)
    elif grado_prec > grado_succ:
        return 5.0  # Da Scuro a Chiaro: Difficile / Purging pesante (5.0 ore!)
    else:
        return 2.5  # Stesso livello (2.5 ore)

def calcola_pianificazione():
    # Caricamento CSV o inizializzazione valori di default
    presse = PRESSE_DEFAULT
    articoli = {a["ID_Articolo"]: a for a in ARTICOLI_DEFAULT}
    ordini = ORDINI_DEFAULT

    # Ordinamento coda per Priorità (Alta prima) e Scadenza (EDD)
    ordini.sort(key=lambda x: (0 if x["Priorita"] == "Alta" else 1, x["Data_Scadenza"]))

    planning_presse = {p["ID_Pressa"]: [] for p in presse if p["Stato"] == "Attiva"}
    timeline_presse = {p["ID_Pressa"]: DATA_CORRENTE for p in presse}
    ultimo_articolo_su_pressa = {p["ID_Pressa"]: None for p in presse}

    for ordine in ordini:
        id_art = ordine["Articolo"]
        if id_art not in articoli:
            continue
        art = articoli[id_art]

        # Filtro compatibilità presse e vincolo macchina rigido
        if art["Pressa_Vincolata"]:
            presse_compatibili = [p for p in presse if p["Stato"] == "Attiva" and p["ID_Pressa"] == art["Pressa_Vincolata"]]
        else:
            presse_compatibili = [p for p in presse if p["Stato"] == "Attiva" and int(p["Tonnellaggio"]) >= int(art["Tonnellaggio_Min"])]

        if not presse_compatibili:
            continue

        # Calcolo preventivo durata produzione
        qta = int(ordine["Quantita_Richiesta"])
        tempo_ciclo = int(art["Tempo_Ciclo"])
        impronte = int(art["Impronte"])
        secondi_teorici = (qta / impronte) * tempo_ciclo
        ore_produzione = (secondi_teorici / 3600) / 0.85

        # Algoritmo Earliest Completion Time (ECT)
        pressa_scelta = None
        data_fine_minima = None
        setup_scelto = 2.0

        for p in presse_compatibili:
            p_id = p["ID_Pressa"]
            ora_inizio_test = timeline_presse[p_id]
            ultimo_art_test = ultimo_articolo_su_pressa[p_id]

            setup_test = calcola_tempo_attrezzaggio(ultimo_art_test, art)
            inizio_prod_test = aggiungi_ore_lavorative(ora_inizio_test, setup_test)
            fine_prod_test = aggiungi_ore_lavorative(inizio_prod_test, ore_produzione)

            if data_fine_minima is None or fine_prod_test < data_fine_minima:
                data_fine_minima = fine_prod_test
                pressa_scelta = p
                setup_scelto = setup_test

        if not pressa_scelta:
            continue

        p_id = pressa_scelta["ID_Pressa"]
        ora_inizio = timeline_presse[p_id]

        # Scrive il setup
        if setup_scelto > 0:
            fine_setup = aggiungi_ore_lavorative(ora_inizio, setup_scelto)
            planning_presse[p_id].append({
                "tipo": "setup",
                "inizio": ora_inizio,
                "fine": fine_setup,
                "durata": setup_scelto,
                "articoloSucc": art["ID_Articolo"]
            })
            ora_inizio = fine_setup

        # Scrive la produzione
        ora_fine = aggiungi_ore_lavorative(ora_inizio, ore_produzione)
        planning_presse[p_id].append({
            "tipo": "produzione",
            "id": ordine["ID_Ordine"],
            "articolo": art["ID_Articolo"],
            "qta": qta,
            "inizio": ora_inizio,
            "fine": ora_fine,
            "durata": ore_produzione
        })

        timeline_presse[p_id] = ora_fine
        ultimo_articolo_su_pressa[p_id] = art

    print("Pianificazione ECT Completata con Successo!")

if __name__ == "__main__":
    calcola_pianificazione()