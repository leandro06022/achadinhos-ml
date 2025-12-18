import requests
import json
import random

URL = "https://api.mercadolibre.com/sites/MLB/search"

PARAMS = {
    "category": "MLB1055",  # Eletrônicos (ajustamos depois)
    "condition": "new",
    "limit": 50,
    "sort": "price_asc"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def buscar_ofertas():
    r = requests.get(URL, params=PARAMS, headers=HEADERS, timeout=20)
    r.raise_for_status()
    data = r.json()

    ofertas = []

    for item in data.get("results", []):
        price = item.get("price", 0)
        original = item.get("original_price")

        if not original or original <= price:
            continue

        desconto = int(100 - (price / original * 100))

        if desconto < 25:
            continue

        installments = item.get("installments")
        parcelas = None

        if installments:
            parcelas = f"{installments['quantity']}x de R$ {installments['amount']:.2f}"

        ofertas.append({
            "titulo": item["title"],
            "preco": price,
            "preco_original": original,
            "desconto": desconto,
            "parcelas": parcelas,
            "link": item["permalink"],
            "imagem": item["thumbnail"]
        })

    return random.sample(ofertas, min(3, len(ofertas)))


if __name__ == "__main__":
    ofertas = buscar_ofertas()

    with open("ofertas.json", "w", encoding="utf-8") as f:
        json.dump(ofertas, f, ensure_ascii=False, indent=2)
