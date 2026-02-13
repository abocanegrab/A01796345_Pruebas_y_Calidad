"""Compute sales totals from a product catalogue and sales records."""

import json
import sys
import time


def load_json(filepath):
    """Load a JSON file and return its contents."""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {filepath}")
        sys.exit(1)
    except json.JSONDecodeError as err:
        print(f"Error: Invalid JSON in {filepath} - {err}")
        sys.exit(1)
    return data


def build_price_catalogue(products):
    """Build a dictionary mapping product title to price."""
    catalogue = {}
    for product in products:
        title = product.get("title")
        price = product.get("price")
        if title is not None and price is not None:
            catalogue[title] = price
    return catalogue


def compute_sales(catalogue, sales):
    """Compute total cost for each sale record.

    Returns a list of result dicts and the grand total.
    Negative quantities are included in the calculation.
    Products not found in the catalogue are skipped with a warning.
    """
    results = []
    grand_total = 0.0

    for record in sales:
        product = record.get("Product", "")
        quantity = record.get("Quantity", 0)
        sale_id = record.get("SALE_ID", "N/A")

        if product not in catalogue:
            print(f"Warning: Product '{product}' not found in catalogue "
                  f"(SALE_ID: {sale_id}). Skipping.")
            continue

        price = catalogue[product]
        subtotal = round(price * quantity, 2)
        grand_total += subtotal

        results.append({
            "sale_id": sale_id,
            "product": product,
            "quantity": quantity,
            "price": price,
            "subtotal": subtotal,
        })

    grand_total = round(grand_total, 2)
    return results, grand_total


def format_results(results, grand_total, elapsed_time):
    """Format the computation results as a readable string."""
    lines = []
    lines.append(f"{'SALE_ID':<10} {'Product':<35} {'Qty':>5} "
                 f"{'Price':>10} {'Subtotal':>12}")
    lines.append("-" * 75)

    for item in results:
        lines.append(
            f"{item['sale_id']:<10} "
            f"{item['product']:<35} "
            f"{item['quantity']:>5} "
            f"{item['price']:>10.2f} "
            f"{item['subtotal']:>12.2f}"
        )

    lines.append("-" * 75)
    lines.append(f"{'TOTAL':>62} {grand_total:>12.2f}")
    lines.append(f"\nTime elapsed: {elapsed_time:.4f} seconds")

    return "\n".join(lines)


def main():
    """Orchestrate: parse args, load files, compute, output results."""
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py <ProductList.json> <Sales.json>")
        sys.exit(1)

    product_file = sys.argv[1]
    sales_file = sys.argv[2]

    start_time = time.time()

    products = load_json(product_file)
    sales = load_json(sales_file)

    catalogue = build_price_catalogue(products)
    results, grand_total = compute_sales(catalogue, sales)

    elapsed_time = time.time() - start_time

    output = format_results(results, grand_total, elapsed_time)

    print(output)

    with open("SalesResults.txt", "w", encoding="utf-8") as file:
        file.write(output + "\n")

    print(f"\nResults saved to SalesResults.txt")


if __name__ == "__main__":
    main()
