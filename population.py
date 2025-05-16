from playwright.sync_api import sync_playwright
import pandas as pd


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://worldpopulationreview.com/countries", wait_until="domcontentloaded", timeout=60000)

    page.wait_for_timeout(3000)

    content = []
    country_names = page.query_selector_all('//td[@class = "not-prose border-wpr-table_border border-t px-3 py-1.5 text-sm md:px-4 false"]//a//strong')
    rows = page.query_selector_all('table tbody tr')

    for row in rows:
        cells = row.query_selector_all('td')

        if len(cells) >= 8:
            try:
                name = cells[1].query_selector("a strong").inner_text()
            except:
                name = cells[1].inner_text()

            population = cells[2].inner_text()
            area = cells[3].inner_text()
            density = cells[4].inner_text()
            global_pop = cells[6].inner_text()
            rank = cells[7].inner_text()


            content.append({
                            "Name": name,
                            "Population": population,
                            "Area (KM²)": area,
                            "Density": density,
                            "Global Pop": global_pop,
                            "Rank": rank
                        })
    df = pd.DataFrame(content)
    print(df.head(5))
    df.to_csv("country_population_data.csv", index=False)
    browser.close()