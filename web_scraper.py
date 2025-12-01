import requests
from bs4 import BeautifulSoup
import json

def scrape_allrecipes(soup):
    title_tag = soup.find("h1", class_="article-heading text-headline-400")
    title = title_tag.get_text(strip=True) if title_tag else "No title found"
    ingredients, steps = [], []

    ingredient_list = soup.find("ul", class_="mm-recipes-structured-ingredients__list")
    step_list = soup.find("div", class_="mm-recipes-steps__content")

    if ingredient_list:
        for item in ingredient_list.find_all("li"):
            quantity = item.find("span", {"data-ingredient-quantity": True})
            unit = item.find("span", {"data-ingredient-unit": True})
            name = item.find("span", {"data-ingredient-name": True})

            if name:
                ingredients.append({
                    "quantity": quantity.get_text(strip=True) if quantity else "",
                    "unit": unit.get_text(strip=True) if unit else "",
                    "name": name.get_text(strip=True)
                })

    if step_list:
        for li in step_list.find_all("li"):
            p_tag = li.find("p")
            if p_tag:
                steps.append(p_tag.get_text(strip=True))

    ingredient_text = ""
    step_text = ""
    for ing in ingredients:
        ingredient_text += f"{ing['quantity']} {ing['unit']} {ing['name']}, "
    for i, step in enumerate(steps, start=1):
        step_text += f"Step {i}: {step}\n"
        
    return title, ingredient_text, step_text

# Serious Eats
def scrape_seriouseats(soup):
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "No title found"
    ingredients, steps = [], []

    # ingredients
    ingredient_list = soup.find("ul", class_="structured-ingredients__list")
    if ingredient_list:
        for item in ingredient_list.find_all("li", class_="structured-ingredients__list-item"):
            quantity = item.find("span", {"data-ingredient-quantity": True})
            unit = item.find("span", {"data-ingredient-unit": True})
            name = item.find("span", {"data-ingredient-name": True})

            if name:
                ingredients.append({
                    "quantity": quantity.get_text(strip=True) if quantity else "",
                    "unit": unit.get_text(strip=True) if unit else "",
                    "name": name.get_text(strip=True)
                })

    # steps
    instructions_section = soup.find("section", id=lambda x: x and x.startswith("section--instructions"))
    if instructions_section:
        for li in instructions_section.find_all("li"):
            p_tag = li.find("p")
            if p_tag:
                text = p_tag.get_text(strip=True)
                if len(text.split()) > 3:
                    steps.append(text)

    return title, ingredients, steps

# Bon Appetit
def scrape_bonappetit(soup):
    title, ingredients, steps = "No title found", [], []

    # try json-ld first 
    json_block = soup.find("script", type="application/ld+json")
    if json_block:
        try:
            data = json.loads(json_block.string)
            if isinstance(data, list):
                for entry in data:
                    if entry.get("@type") == "Recipe":
                        data = entry
                        break
            if data.get("@type") == "Recipe":
                title = data.get("name", title)
                ingredients = [{"quantity": "", "unit": "", "name": ing} for ing in data.get("recipeIngredient", [])]
                steps_data = data.get("recipeInstructions", [])
                for s in steps_data:
                    if isinstance(s, dict):
                        steps.append(s.get("text", "").strip())
                    elif isinstance(s, str):
                        steps.append(s.strip())
                return title, ingredients, steps
        except Exception as e:
            print("JSON-LD parsing failed:", e)

    # fallback to static html
    title_tag = soup.find("h1")
    if title_tag:
        title = title_tag.get_text(strip=True)

    # ingredients
    for item in soup.select("div.List-jjjUFK div.BaseWrap-sc-gzm6lz"):
        text = item.get_text(strip=True)
        if text:
            ingredients.append({"quantity": "", "unit": "", "name": text})

    # steps
    for step_tag in soup.select("div.InstructionListWrapper-dhIood p"):
        text = step_tag.get_text(strip=True)
        if text and len(text.split()) > 3:
            steps.append(text)

    return title, ingredients, steps

# Delish
def scrape_delish(soup):
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "No title found"
    ingredients, steps = [], []

    # ingredients
    for li in soup.select("ul.ingredient-lists li.css-1kiufme"):
        strong = li.find("strong")
        p_tag = li.find("p")
        text_parts = []
        if strong:
            text_parts.append(strong.get_text(strip=True))
        if p_tag:
            text_parts.append(p_tag.get_text(strip=True))
        text = " ".join(text_parts).strip()
        if text:
            ingredients.append({"quantity": "", "unit": "", "name": text})

    # steps
    steps_section = soup.select_one("ul.directions.css-j01fd6.e1241r8m4")
    if steps_section:
        for li in steps_section.find_all("li", class_="direction"):
            text = li.get_text(" ", strip=True)
            if text and len(text.split()) > 3:
                # remove redundant step # prefix
                if text.lower().startswith("step "):
                    parts = text.split(" ", 2)
                    if len(parts) == 3 and parts[1].isdigit():
                        text = parts[2].strip()
                steps.append(text)

    return title, ingredients, steps

# Food Network scraper skipped — site blocks scraping with 403 errors
def scrape_foodnetwork(soup):
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "No title found"
    ingredients, steps = [], []

    # ingredients
    for label in soup.select("label.checkbox-text"):
        text = label.get_text(strip=True)
        if text:
            ingredients.append({
                "quantity": "",
                "unit": "",
                "name": text
            })

    # steps
    for step_tag in soup.select("li.o-Method__m-Step"):
        text = step_tag.get_text(strip=True)
        if text and len(text.split()) > 3:
            steps.append(text)

    return title, ingredients, steps

# Epicurious scraper skipped — paywall + inconsistent class naming and dynamic structure
def scrape_epicurious(soup):
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "No title found"
    ingredients, steps = [], []

    # ingredients
    for div in soup.select('div[class*="List"] div[class*="Description"]'):
        text = div.get_text(strip=True)
        if text:
            ingredients.append({"quantity": "", "unit": "", "name": text})

    # steps
    for p in soup.select('ol[class*="InstructionGroupWrapper"] li[class*="InstructionListWrapper"] p'):
        text = p.get_text(" ", strip=True)
        if text and len(text.split()) > 3:
            steps.append(text)

    return title, ingredients, steps

def scrape_generic(soup):
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "No title found"
    ingredients, steps = [], []

    # generic ingredients
    for li in soup.find_all("li"):
        if li.find_parent(attrs={"class": lambda x: x and "ingredient" in x.lower()}) or \
           li.get("class") and any("ingredient" in c.lower() for c in li.get("class", [])):
            text = li.get_text(strip=True)
            if text and len(text.split()) > 2:
                ingredients.append({"quantity": "", "unit": "", "name": text})

    # generic steps
    for p in soup.find_all("p"):
        if p.find_parent(attrs={"class": lambda x: x and ("instruction" in x.lower() or "direction" in x.lower())}):
            text = p.get_text(strip=True)
            if len(text.split()) > 3:
                steps.append(text)

    return title, ingredients, steps


def fetch(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    if "allrecipes.com" in url:
        return scrape_allrecipes(soup)
    elif "seriouseats.com" in url:
        return scrape_seriouseats(soup)
    elif "bonappetit.com" in url:
        return scrape_bonappetit(soup)
    elif "delish.com" in url:
        return scrape_delish(soup)
    elif any(site in url for site in ["seriouseats.com", "bonappetit.com", "delish.com", "allrecipes.com"]):
        print(f"Using generic scraper for {url}")
        return scrape_generic(soup)
    else:
        print("Unsupported website.")
        return "Unknown", [], []


if __name__ == "__main__":
    # url = "https://www.allrecipes.com/recipe/6701/persimmon-bread-i/"
    # url = "https://www.bonappetit.com/recipe/parker-house-rolls-recipe"
    # url = "https://www.bonappetit.com/recipe/smoky-brown-butter-pasta"
    # url = "https://www.seriouseats.com/pasta-carbonara-sauce-recipe"
    # url = "https://www.foodnetwork.com/recipes/robert-irvine/french-toast-recipe-1951408" -- doesnt work
    # url = "https://www.delish.com/cooking/recipe-ideas/recipes/a52456/breakfast-crunchwrap-supreme-recipe/"
    # url = "https://www.delish.com/cooking/recipe-ideas/a25636180/shrimp-stir-fry-recipe/"
    url = "https://www.epicurious.com/recipes/food/views/simple-one-skillet-chicken-alfredo-pasta"
    title, ingredients, steps = fetch(url)

    print("Title:", title)
    print("Ingredients:")
    for ing in ingredients:
        print(f"- {ing['quantity']} {ing['unit']} {ing['name']}")
    print("\nSteps:")
    for i, step in enumerate(steps, start=1):
        print(f"Step {i}: {step}")