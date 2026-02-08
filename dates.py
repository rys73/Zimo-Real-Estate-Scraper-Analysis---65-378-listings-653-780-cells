from datetime import datetime, timedelta
import pandas as pd
import json, re, os

# Date de référence
REFERENCE_DATE = datetime(2026, 2, 7, 21, 30, 0)
JSON_PATH = r"C:\Users\ighik\OneDrive\Escritorio\html\PORTFOLIO_LINKEDIN\PORTOFOLIO_4_2\PANDAS_PROJET_2_\JSON\csv_path.json"

# 1 -> Conversion
def parse_relative_date(text):
    # On transforme "Il y a X minutes/heures/jours/mois/années" en datetime réel
    if not isinstance(text, str):
        return None
    
    text = text.lower().strip()

    # Minutes
    match = re.match(r"il y a (\d+)\s*minute", text)
    if match:
        minutes = int(match.group(1))
        return REFERENCE_DATE - timedelta(minutes=minutes)
    
    # Heures
    match = re.match(r"il y a (\d+)\s*heure", text)
    if match:
        hours = int(match.group(1))
        return REFERENCE_DATE - timedelta(hours=hours)
    
    # Jours
    match = re.match(r"il y a (\d+)\s*jour", text)
    if match:
        days = int(match.group(1))
        return REFERENCE_DATE - timedelta(days=days)
    
    # Mois (approximation : 30 jours)
    match = re.match(r"il y a (\d+)\s*mois", text)
    if match:
        months = int(match.group(1))
        return REFERENCE_DATE - timedelta(days=30*months)
    
    return None

# 2 -> Fonction pout traiter tous les PATH_CSV du JSON
def update_dates_in_csv(JSON_PATH):
    # On ouvre le JSON avec tout les chemins CSV
    # On modifier la colonne Date_Annonce par la date réelle dans chaque CSV

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        csv_paths = json.load(f)

    for ville, types in csv_paths.items():
        for type_bien, path in types.items():
            if not os.path.exists(path):
                print(f"Erreur Fichier non trouvé : {path}")
                continue

            df = pd.read_csv(path)

            if "Date_Annonce" in df.columns:
                df["Date_Annonce"] = df["Date_Annonce"].apply(parse_relative_date)
            
            df.to_csv(path, index=False)
            print(f"{ville} | {type_bien} : Date_Annonce mise à jour ({len(df)} lignes)")

if __name__ == "__main__":
    update_dates_in_csv(JSON_PATH)
