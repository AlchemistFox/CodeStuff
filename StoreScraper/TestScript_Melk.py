from scrapers.meny import get_prices

if __name__ == "__main__":
    results = get_prices("melk")
    for r in results:
        print(r)
