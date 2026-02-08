import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

CSV_GLOBAL = r"C:\Users\ighik\OneDrive\Escritorio\html\PORTFOLIO_LINKEDIN\PORTOFOLIO_4_2\WEB_SCRAPING_PROJET_3_\CSV\Global\zimo_all_villes.csv"
OUTPUT_DIR = r"C:\Users\ighik\OneDrive\Escritorio\html\PORTFOLIO_LINKEDIN\PORTOFOLIO_4_2\PANDAS_PROJET_2_\PDF\PDF_partie2_graphiques_par_ville"

# 1 -> On crée le dossier de sortie et on lit le CSV
os.makedirs(OUTPUT_DIR, exist_ok=True)
df = pd.read_csv(CSV_GLOBAL)

# 2 -> On s'assure que Date_Annonce est en datetime
df["Date_Annonce"] = pd.to_datetime(df["Date_Annonce"])


# 3 -> On crée une boucle pour chaque ville
for ville in df["Ville"].unique():
    df_ville = df[df["Ville"] == ville].copy()
    ville_dir = os.path.join(OUTPUT_DIR, ville)
    os.makedirs(ville_dir, exist_ok=True)

    # 3.1 -> Prix moyen et médian
    prix_moyen = df_ville["Prix_m2"].mean()
    prix_median = df_ville["Prix_m2"].median()
    print(f"{ville} -> Prix moyen: {prix_moyen:.2f} €/m² | Prix médian: {prix_median:.2f} €/m² ")
    # Graphique 1 : Bar prix moyen / médian
    plt.figure(figsize=(6,4))
    plt.bar(["Moyen","Médian"], [prix_moyen, prix_median], color=["teal","orange"])
    plt.ylabel("Prix €/m²")
    plt.title(f"{ville} - Prix moyen et médian au m²")
    plt.tight_layout()
    plt.savefig(f"{ville_dir}/01_prix_moyen_median.pdf")
    plt.close()

    # 3.2 -> Écart au prix médian
    df_ville["Ecart_median"] = df_ville["Prix_m2"] - prix_median
    # Graphique 2 : histogramme écart au prix médian
    plt.figure(figsize=(8,4))
    plt.hist(df_ville["Ecart_median"], bins=20, color="purple", edgecolor="black")
    plt.axvline(0, color="red", linestyle="--")
    plt.title(f"{ville} - Écart au prix médian")
    plt.xlabel("Écart €/m²")
    plt.ylabel("Nombre d'annonces")
    plt.tight_layout()
    plt.savefig(f"{ville_dir}/02_ecart_median.pdf")
    plt.close()

    # 3.3 -> Top 10 meilleures opportunités (plus grand écart négatif)
    top10 = df_ville.nsmallest(10, "Ecart_median")
    plt.figure(figsize=(8,5))
    plt.barh(top10["Titre"], top10["Ecart_median"], color="red")
    plt.xlabel("Écart €/m²")
    plt.title(f"{ville} - Top 10 opportunités")
    plt.tight_layout()
    plt.savefig(f"{ville_dir}/03_top10_opportunites.pdf")
    plt.close()

    # 3.4 -> Prix au m² par type de bien
    prix_type = df_ville.groupby("Type_de_Bien")["Prix_m2"].mean()
    plt.figure(figsize=(6,4))
    prix_type.plot(kind="bar", color=["skyblue","orange"])
    plt.ylabel("Prix €/m²")
    plt.title(f"{ville} - Prix moyen au m² par type de bien")
    plt.tight_layout()
    plt.savefig(f"{ville_dir}/04_prix_type.pdf")
    plt.close()

    # 3.5 -> Prix au m² par tranche de surface
    bins = [0,40,60,80,100,1000]
    labels = ["<40","40-60","60-80","80-100","100+"]
    df_ville["Surface_bin"] = pd.cut(df_ville["Surface_m2"], bins=bins, labels=labels)
    prix_surface = df_ville.groupby("Surface_bin", observed=True)["Prix_m2"].mean()
    plt.figure(figsize=(6,4))
    prix_surface.plot(kind="bar", color="green")
    plt.ylabel("Prix €/m²")
    plt.title(f"{ville} - Prix moyen par tranche de surface")
    plt.tight_layout()
    plt.savefig(f"{ville_dir}/05_prix_surface.pdf")
    plt.close()

    # 3.6 -> Analyse Pro vs Particulier
    prix_pro_part = df_ville.groupby("Pro_ou_Part")["Prix_m2"].mean()
    plt.figure(figsize=(6,4))
    prix_pro_part.plot(kind="bar", color=["orange","purple"])
    plt.ylabel("Prix €/m²")
    plt.title(f"{ville} - Prix moyen Pro vs Particulier")
    plt.tight_layout()
    plt.savefig(f"{ville_dir}/06_pro_part.pdf")
    plt.close()

    # 3.7 -> Surface moyenne par type de bien
    surface_type = df_ville.groupby("Type_de_Bien")["Surface_m2"].mean()
    plt.figure(figsize=(6,4))
    surface_type.plot(kind="bar", color=["skyblue","orange"])
    plt.ylabel("Surface moyenne m²")
    plt.title(f"{ville} - Surface moyenne par type de bien")
    plt.tight_layout()
    plt.savefig(f"{ville_dir}/07_surface_type.pdf")
    plt.close()

    # 3.8 -> Annonces récentes vs anciennes
    today = df_ville["Date_Annonce"].max()
    df_ville["Age_jours"] = (today - df_ville["Date_Annonce"]).dt.days
    bins_age = [0,7,30,1000]
    labels_age = ["<7 jours","7-30 jours",">30 jours"]
    df_ville["Age_bin"] = pd.cut(df_ville["Age_jours"], bins=bins_age, labels=labels_age)
    age_counts = df_ville["Age_bin"].value_counts().reindex(labels_age)
    plt.figure(figsize=(6,4))
    age_counts.plot(kind="bar", color="teal")
    plt.ylabel("Nombre d'annonces")
    plt.title(f"{ville} - Ancienneté des annonces")
    plt.tight_layout()
    plt.savefig(f"{ville_dir}/08_age_annonces.pdf")
    plt.close()

    # 3.9 ->  Prix au m² des annonces récentes (<30 jours)
    df_recent = df_ville[df_ville["Age_jours"] <= 30]
    plt.figure(figsize=(6,4))
    plt.hist(df_recent["Prix_m2"], bins=15, color="purple", edgecolor="black")
    plt.xlabel("Prix €/m²")
    plt.ylabel("Nombre d'annonces")
    plt.title(f"{ville} - Prix au m² annonces récentes (<30 jours)")
    plt.tight_layout()
    plt.savefig(f"{ville_dir}/09_prix_recent.pdf")
    plt.close()

    # 3.10 -> Carte mentale du marché
    sous_cotes_pct = (df_ville["Ecart_median"]<0).mean()*100
    part_particuliers = (df_ville["Pro_ou_Part"]=="Particulier").mean()*100
    carte_mentale = (
        f"Prix médian : {prix_median:.0f} €/m²\n"
        f"% sous-cotés : {sous_cotes_pct:.1f} %\n"
        f"% particuliers : {part_particuliers:.1f} %\n"
        f"Marché {'tendu' if sous_cotes_pct<20 else 'opportunités intéressantes'}"
    )
    with open(f"{ville_dir}/10_carte_mentale.txt","w", encoding="utf-8") as f:
        f.write(carte_mentale)

print("Partie 2 terminée !")







