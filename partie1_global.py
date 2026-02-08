import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns
import os

# 1 -> Charger le CSV global 
CSV_ALL_PATH = r"C:\Users\ighik\OneDrive\Escritorio\html\PORTFOLIO_LINKEDIN\PORTOFOLIO_4_2\WEB_SCRAPING_PROJET_3_\CSV\Global\zimo_all_villes.csv"
df = pd.read_csv(CSV_ALL_PATH, parse_dates=["Date_Annonce"])

# On crée un dossier pour les graphiques
OUTPUT_DIR = r"C:\Users\ighik\OneDrive\Escritorio\html\PORTFOLIO_LINKEDIN\PORTOFOLIO_4_2\PANDAS_PROJET_2_\PDF\PDF_partie1_graphiques_global"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2 -> Graphiques globaux

sns.set_style("whitegrid")

   # 2.1 -> Prix moyen au m² par ville
plt.figure(figsize=(10,6))
df.groupby("Ville")["Prix_m2"].mean().sort_values(ascending=False).plot(kind="bar", color="skyblue")
plt.title("Prix moyen au m² par ville")
plt.ylabel("Prix moyen (€ / m²)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/01_prix_moyen_par_ville.pdf")
plt.close()

   # 2.2 -> Prix médian au m² par ville
plt.figure(figsize=(10,6))
df.groupby("Ville")["Prix_m2"].median().sort_values(ascending=False).plot(kind="bar", color="orange")
plt.title("Prix médian au m² par ville")
plt.ylabel("Prix médian (€ / m²)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/02_prix_median_par_ville.pdf")
plt.close()

   # 2.3 -> Prix moyen au m² par type de bien et par ville
plt.figure(figsize=(12,6))
df_grouped = df.groupby(["Ville","Type_de_Bien"])["Prix_m2"].mean().unstack()
df_grouped.plot(kind="bar", figsize=(12,6))
plt.title("Prix moyen au m² par type de bien et par ville")
plt.ylabel("Prix moyen (€ / m²)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/03_prix_moyen_par_type_et_ville.pdf")
plt.close()

   # 2.4 -> Écart de prix moyen Maison vs Appartement par ville
plt.figure(figsize=(14,7))
df_grouped = df.groupby(["Ville","Type_de_Bien"])["Prix_m2"].mean().unstack()
df_grouped["Ecart_Appartement_Maison"] = df_grouped["Appartement"] - df_grouped["Maison"]
# Barres colorées selon positif ou négatif
colors = ["green" if x >= 0 else "red" for x in df_grouped["Ecart_Appartement_Maison"]]
bars = plt.bar(df_grouped.index, df_grouped["Ecart_Appartement_Maison"], color=colors)
# On ajoute des valeurs sur chaque barre
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f"{height:.0f}", ha="center", va="bottom" if height>=0 else "top")
plt.title("Écart de prix moyen (Appartement - Maison) par ville")
plt.ylabel("Écart (€ / m²)")
plt.xticks(rotation=45)
plt.axhline(0, color="black", linewidth=0.8)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/04_ecart_prix_maison_appartement.pdf")
plt.close()

   # 2.5 -> Nombre d'annonces par ville
plt.figure(figsize=(10,6))
df["Ville"].value_counts().plot(kind="bar", color="purple")
plt.title("Nombre d'annonces par ville")
plt.ylabel("Nombre d'annonces")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/05_nb_annonces_par_ville.pdf")
plt.close()

   # 2.6 Répartition Maison vs Appartement (global)
plt.figure(figsize=(6,6))
df["Type_de_Bien"].value_counts().plot(kind="pie", autopct="%1.1f%%", colors=["skyblue","salmon"])
plt.title("Répartition Maison vs Appartement (global)")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/06_repartition_type_bien.pdf")
plt.close()

   # 2.7 Prix moyen Maison vs Appartement (global)
plt.figure(figsize=(8,6))
df.groupby("Type_de_Bien")["Prix_m2"].mean().plot(kind="bar", color=["skyblue","salmon"])
plt.title("Prix moyen au m² : Maison vs Appartement")
plt.ylabel("Prix moyen (€ / m²)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/07_prix_moyen_maison_vs_appartement.pdf")
plt.close()

   # 2.8 Pro vs Particulier (global)
plt.figure(figsize=(6,6))
df["Pro_ou_Part"].value_counts().plot(kind="bar", color=["orange","lightgreen"])
plt.title("Pro vs Particulier (global)")
plt.ylabel("Nombre d'annonces")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/08_pro_vs_part.pdf")
plt.close()

   # 2.9 -> Prix moyen au m² par tranche de surface (global)
plt.figure(figsize=(12,6))
bins = [0,40,60,80,100,120,150,200,1000]
labels = ["<40","40-60","60-80","80-100","100-120","120-150","150-200",">200"]
df["Surface_bin"] = pd.cut(df["Surface_m2"], bins=bins, labels=labels)
df.groupby("Surface_bin", observed=True)["Prix_m2"].mean().plot(kind="bar", color="teal")
plt.title("Prix moyen au m² par tranche de surface (global)")
plt.ylabel("Prix moyen (€ / m²)")
plt.xlabel("Tranche de surface (m²)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/09_prix_moyen_par_tranche_surface.pdf")
plt.close()

   # 2.10 -> (Scatter plot) Prix total vs Surface (toutes les villes)
plt.figure(figsize=(10,6))
sns.scatterplot(x="Surface_m2", y="Prix", hue="Type_de_Bien", data=df, alpha=0.6)
plt.title("Prix total vs Surface (toutes les villes)")
plt.xlabel("Surface (m²)")
plt.ylabel("Prix (€)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/10_scatter_prix_vs_surface.pdf")
plt.close()

print("Tous les graphiques globaux ont été générés !")



