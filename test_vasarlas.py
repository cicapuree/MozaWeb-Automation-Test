import random
import time
from playwright.sync_api import sync_playwright

def test_vasarlas():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        #random adatok generalasa
        keresztnevek = ["Emma", "Richard", "Szabolcs", "Eszter", "Ödön", "Mia"]
        vezeteknevek = ["Kovács", "Nagy", "Kis", "Toth", "Smith", "Wilson"]
        szam = random.randint(1000, 9999)
        kereszt = random.choice(keresztnevek)
        vezetek = random.choice(vezeteknevek)
        felhasznalonev = f"{kereszt.lower()}_{szam}"
        email = f"testmail{szam}@example.com"
        jelszo = "RandomJelszo@123"


        #regisztracio
        page.goto("https://automationteststore.com/index.php?rt=account/create")
        page.fill("#AccountFrm_firstname", kereszt)
        page.fill("#AccountFrm_lastname", vezetek)
        page.fill("#AccountFrm_email", email)
        page.fill("#AccountFrm_address_1", "Random utca 10.")
        page.fill("#AccountFrm_city", "Szeged")
        page.select_option("#AccountFrm_zone_id", label="Angus")
        page.fill("#AccountFrm_postcode", "1234")
        page.fill("#AccountFrm_loginname", felhasznalonev)
        page.fill("#AccountFrm_password", jelszo)
        page.fill("#AccountFrm_confirm", jelszo)
        page.check("#AccountFrm_agree")
        page.click("button[title='Continue']")

        #polok vizsgalata
        page.goto("https://automationteststore.com/index.php?rt=product/category&path=68_70")
        
        page.wait_for_selector(".thumbnail")
        items = page.query_selector_all(".thumbnail")
        product_list = []

        for item in items:
            try:
                name_el = item.query_selector(".prdocutname")
                if name_el:
                    name = name_el.inner_text().strip()
                    url = name_el.get_attribute("href")
                    price_el = item.query_selector(".oneprice, .pricenew")
                    if price_el:
                        price = float(price_el.inner_text().replace('$', '').strip())
                        product_list.append({"name": name, "price": price, "url": url})
            except: continue

        product_list.sort(key=lambda x: x['price'], reverse=True)

        #kosarba tetel
        kosarban_van = 0
        for target in product_list:
            if kosarban_van >= 2: break
            
            print(f"{target['name']} ({target['price']}$)")
            page.goto(target['url'])
            
            cart_button = page.query_selector(".cart")
            if cart_button:
                cart_button.click()
                kosarban_van += 1
                print(f"Sikerült kosárba tenni!")
            else:
                print(f"Termék kihagyása.")
            
            page.goto("https://automationteststore.com/index.php?rt=product/category&path=68_70")

        #fizetes
        page.goto("https://automationteststore.com/index.php?rt=checkout/cart")
        page.click("#cart_checkout1")
        page.wait_for_timeout(3000)
        page.wait_for_selector("#checkout_btn", state="visible")
        page.click("#checkout_btn")

        time.sleep(2)

        #ellenorzes
        page.wait_for_load_state("networkidle")
        content = page.content()
        if "Your Order Has Been Processed!" in content:
            print("\n"+"*"*40)
            print("Sikeres vásárlás!")
            print("*"*40)
        else:
            print("A vásárlás sikertelen.")

        time.sleep(2)
        browser.close()

if __name__ == "__main__":
    test_vasarlas()