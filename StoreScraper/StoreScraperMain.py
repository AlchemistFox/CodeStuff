import os
import streamlit as st
from scrapers import meny, kiwi  # import your new scraper here
from utils.formatters import format_price

def load_css(file_path: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, file_path)
    with open(full_path, encoding="utf-8") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Grocery Price Checker", layout="centered")
    load_css("styles/style.css")
    st.title("Grocery Price Checker")

    query = st.text_input("Search product by name:")

    if query:
        st.write(f"Searching stores for: **{query}**")

        all_prices = []
        # Try to get prices from Meny
        try:
            meny_prices = meny.get_prices(query)
            all_prices.extend(meny_prices)
        except Exception as e:
            st.error(f"Error fetching prices from Meny: {e}")

        # Try to get prices from Kiwi
        try:
            kiwi_prices = kiwi.get_prices(query)
            all_prices.extend(kiwi_prices)
        except Exception as e:
            st.error(f"Error fetching prices from Kiwi: {e}")

        if all_prices:
            # Sort combined list by price ascending, None prices go last
            all_prices = sorted(all_prices, key=lambda x: x["price"] if x["price"] is not None else float("inf"))

            rows = ""
            for item in all_prices:
                price_str = format_price(item["price"]) if item["price"] else "N/A"
                vendor = item.get("vendor", "N/A")
                ean = item.get("ean", "N/A")
                rows += (
                    "<tr>"
                    f"<td style='border:1px solid black; padding:6px 12px; font-family: monospace; text-align:center;'>{item['store']}</td>"
                    f"<td style='border:1px solid black; padding:6px 12px; font-family: monospace; text-align:center;'>{item['name']}</td>"
                    f"<td style='border:1px solid black; padding:6px 12px; font-family: monospace; text-align:center;'>{vendor}</td>"
                    f"<td style='border:1px solid black; padding:6px 12px; font-family: monospace; text-align:center;'>{ean}</td>"
                    f"<td style='border:1px solid black; padding:6px 12px; font-family: monospace; text-align:center;'>{price_str}</td>"
                    "</tr>"
                )

            table_html = (
                "<div style='display:flex; justify-content:center; margin-top:20px;'>"
                "<table style='border-collapse: collapse; border: 1px solid black; background-color: white;'>"
                "<thead>"
                "<tr>"
                "<th style='border:1px solid black; padding:6px 12px; font-family: monospace; text-align:center;'>Store</th>"
                "<th style='border:1px solid black; padding:6px 12px; font-family: monospace; text-align:center;'>Product</th>"
                "<th style='border:1px solid black; padding:6px 12px; font-family: monospace; text-align:center;'>Vendor</th>"
                "<th style='border:1px solid black; padding:6px 12px; font-family: monospace; text-align:center;'>EAN</th>"
                "<th style='border:1px solid black; padding:6px 12px; font-family: monospace; text-align:center;'>Price</th>"
                "</tr>"
                "</thead>"
                "<tbody>"
                f"{rows}"
                "</tbody>"
                "</table>"
                "</div>"
            )

            st.markdown(table_html, unsafe_allow_html=True)
        else:
            st.info("No prices found for this product.")

if __name__ == "__main__":
    main()
