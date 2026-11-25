
import pandas as pd
from urllib.parse import quote_plus


def load_products():
    products = pd.read_csv("products.csv")

    def generate_links(row):
        product_name = f"{row['brand']} {row['name']}"
        query = quote_plus(product_name)

        return pd.Series({
            "Amazon": f"https://www.amazon.in/s?k={query}",
            "Flipkart": f"https://www.flipkart.com/search?q={query}",
            "Google Shopping": f"https://www.google.com/search?tbm=shop&q={query}"
        })

    links = products.apply(generate_links, axis=1)

    products = pd.concat([products, links], axis=1)

    return products


def search_products(category, budget, min_ram=0, min_storage=0):

    products = load_products()

    products = products[
        products["category"].str.lower() == category.lower()
    ]

    products = products[products["price"] <= budget]

    products = products[
        products["ram_gb"].fillna(0) >= min_ram
    ]

    products = products[
        products["storage_gb"].fillna(0) >= min_storage
    ]

    products = products.sort_values(
        by="rating",
        ascending=False
    )

    return products
