import requests
import json

def get_prices(query):
    url = "https://platform-rest-prod.ngdata.no/api/episearch/1300/products"
    params = {
        "search": query,
        "page_size": 21,
        "suggest": "true",
        "page": 1,
        "types": "suggest,products,recipes,stores,articles",
        "store_id": "7080001150488",
        "popularity": "true",
        "sort": "",
        "facet": "",
        "full_response": "true",
        "showNotForSale": "true"
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    # Optional: save for inspection
    with open("meny_api_response.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    products = data.get("hits", {}).get("hits", [])
    prices = []

    for item in products:
        source = item.get("contentData", {}).get("_source", {})
        name = source.get("title", "Unknown")
        price = source.get("pricePerUnit", None)
        ean = source.get("ean", "Unknown")
        vendor = source.get("vendor", "Unknown")
        is_for_sale = source.get("isForSale", False)
        is_out_of_stock = source.get("isOutOfStock", False)

        # ✅ This is inside the loop
        if not is_for_sale or is_out_of_stock:
            continue

        prices.append({
            "store": "Meny",
            "name": name,
            "price": price,
            "ean": ean,
            "vendor": vendor
        })

    return prices

# Test it
if __name__ == "__main__":
    results = get_prices("melk")
    for r in results:
        print(r)
