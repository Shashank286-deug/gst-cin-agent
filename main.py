import pandas as pd
from playwright.sync_api import sync_playwright
import time
import os

# Function to search GST and CIN using Playwright
def search_gst_and_cin(company_name):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Visit KnowYourGST search page
            page.goto("https://www.knowyourgst.com/gst-number-search/", timeout=60000)

            # Type company name into the search bar
            page.fill("input[name='gst']", company_name)
            page.keyboard.press("Enter")
            page.wait_for_timeout(3000)

            # Extract first result (you may need to inspect the correct selectors)
            result = page.locator(".panel-body")
            text = result.inner_text()

            gstin = ""
            cin = ""

            if "GSTIN:" in text:
                gstin = text.split("GSTIN:")[1].split("\n")[0].strip()
            if "CIN:" in text:
                cin = text.split("CIN:")[1].split("\n")[0].strip()

            return gstin, cin

        except Exception as e:
            print(f"Error for {company_name}: {e}")
            return "", ""

        finally:
            browser.close()

# Main function to read Excel and write results
def main():
    input_file = "input_companies.xlsx"
    output_file = "output_with_gst_cin.xlsx"

    if not os.path.exists(input_file):
        print(f"File '{input_file}' not found.")
        return

    df = pd.read_excel(input_file)
    df["GST"] = ""
    df["CIN"] = ""

    for idx, row in df.iterrows():
        name = row["Legal Name"]
        print(f"Processing: {name}")
        gst, cin = search_gst_and_cin(name)
        df.at[idx, "GST"] = gst
        df.at[idx, "CIN"] = cin
        time.sleep(2)  # Be nice to the server

    df.to_excel(output_file, index=False)
    print(f"Saved results to {output_file}")

if __name__ == "__main__":
    main()
