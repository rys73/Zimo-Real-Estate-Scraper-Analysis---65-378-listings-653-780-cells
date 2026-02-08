from playwright.async_api import async_playwright
import asyncio, json, re, csv, os

JSON_PATH = r"C:\Users\ighik\OneDrive\Escritorio\html\PORTFOLIO_LINKEDIN\PORTOFOLIO_4_2\WEB_SCRAPING_PROJET_3_\JSON\urls_zimo.json"
CSV_PATH = r"C:\Users\ighik\OneDrive\Escritorio\html\PORTFOLIO_LINKEDIN\PORTOFOLIO_4_2\WEB_SCRAPING_PROJET_3_\CSV"
CSV_PATH_ALL = r"C:\Users\ighik\OneDrive\Escritorio\html\PORTFOLIO_LINKEDIN\PORTOFOLIO_4_2\WEB_SCRAPING_PROJET_3_\CSV\Global\zimo_all_villes.csv"

# Fonction pour extraire le m² depuis le titre
def extract_surface(title: str):
    if not title:
        return None
    match = re.search(r"(\d{1,3})\s*m²", title)
    return int(match.group(1)) if match else None


# Fonction pour nettoyer le prix en format numérique
def clean_price(text: str):
    return int(re.sub(r"[^\d]", "", text)) if text else None

# Fonction pour sauvegarder les résultats dans un fichier CSV
def write_to_csv(data, filename):
    if not data:
        print(f"Aucune donnée à écrire dans le fichier {filename}")
        return
    with open(filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Fonction pour accepter les cookies (si non ça bloque la page)
async def accept_cookies(page):
    try:
        button = page.locator("button:has-text('Continuer sans accepter')").first
        await button.wait_for(timeout=8000)
        if await button.is_visible():
            await button.click()
            print("Cookies ignorés.")
    except:
        pass

# Fonction principale pour récupérer les annonces d'une ville et d'un type de bien
async def scrape_city_type(page, ville, type_bien, base_url, cookies_done):
    results = []

    await page.goto(base_url)
    await page.wait_for_selector("app-thumb-ann", timeout=20000)

       # Accepter les cookies
    if not cookies_done:
       await accept_cookies(page)
       cookies_done = True
       # 2 -> On détermine le nombre total de pages
    try:
        pages = await page.locator("nav a").all_inner_texts()
        pages = [int(p) for p in pages if p.isdigit()]
        total_pages = max(pages) if pages else 1
    except:
        total_pages = 1 
    
    print(f"{ville} | {type_bien} | {total_pages} pages à scraper")

       # 3 -> On crée une boucle sur chaque page
    for page_num in range(1, total_pages + 1):
        await page.goto(f"{base_url}?page={page_num}")
        await page.wait_for_selector("app-thumb-ann", timeout=20000)
        await page.wait_for_timeout(1000)

        annonces = await page.locator("app-thumb-ann").all()
        print(f"{ville} -> {type_bien} : page {page_num} -> {len(annonces)} annonces")

        for ann in annonces:
               # init Safe
            titre = prix = prix_m2 = surface_m2 = None
            pro_ou_part = date_annonce = url_annonce = description = None
               # Prix
            try:
                main_link = ann.locator("div a.font-semibold")
                await main_link.wait_for(state="visible", timeout=45000)
                titre = (await main_link.inner_text()).strip()

                prix = None 
                prices = ann.locator(":text-matches('€', 'i')")
                if await prices.count() > 0:
                   prix_text = await prices.first.inner_text()
                   prix = clean_price(prix_text)

                badges = await ann.locator("div.badge-primary").all_inner_texts()
                pro_ou_part = badges[0] if badges else "Particulier"

                dates = await ann.locator("time").all_inner_texts()
                date_annonce = dates[0] if dates else None

                url_annonce = None
                links = ann.locator("a.absolute[href]")

                if await links.count() > 0:
                   href = await links.first.get_attribute("href")
                   if href:
                      if href.startswith("/"):
                         url_annonce = f"https://www.zimo.fr{href}"
                      else:
                         url_annonce = href

                desc = await ann.locator("div.text-sm").nth(1).all_inner_texts()
                description = desc[0] if desc else None

                surface_m2 = extract_surface(titre)
                prix_m2 = prix / surface_m2 if prix and surface_m2 else None

            except Exception as e:
               print(f"[{ville}-{type_bien}] erreur annonce : {e}")

            results.append({
                "Ville": ville,
                "Type_de_Bien": type_bien,
                "Titre": titre,
                "Prix": prix,
                "Prix_m2": prix_m2,
                "Surface_m2": surface_m2,
                "Pro_ou_Part": pro_ou_part,
                "Date_Annonce": date_annonce,
                "URL": url_annonce,
                "Description": description
            })

    return results, cookies_done

# Fonction principale
async def main():
    all_results = [] # On le met avant la boucle pour éviter l'erreur d'UnboundLocalError

    # Lire le JSON ou il y a les liens (pour aller plus vite)
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        urls = json.load(f)
    
       # Démarrage de Playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=0, args=["--disable-blink-features=AutomationControlled"])
        context = await browser.new_context(
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"),
            locale="fr-FR",
            timezone_id="Europe/Paris")
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")
        page = await context.new_page()

        cookies_done = False

        # Boucle sur les villes et types de biens
        for ville, types in urls.items():
            for type_bien, url in types.items():
                results, cookies_done = await scrape_city_type(
                    page, ville, type_bien, url, cookies_done
                )
                all_results.extend(results)
                # Sauvegarde CSV par ville/type
                csv_name = os.path.join(
                    CSV_PATH, f"{ville}/zimo_{ville}_{type_bien}.csv"
                ).replace(" ", "_")

                write_to_csv(results, csv_name)
                print(f"CSV généré : {csv_name}")
        # Sauvegarde du CSV Global
        if all_results:
            write_to_csv(all_results, CSV_PATH_ALL)
            print(f"CSV global généré ({len(all_results)} lignes)")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())