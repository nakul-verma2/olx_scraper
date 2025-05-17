import requests
from bs4 import BeautifulSoup
import subprocess
import json
import csv

def scrape_via_requests(url="https://www.olx.in/items/q-car-cover", output_csv="olx_data_via_requests.csv"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve page. Status code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    ul = soup.find("ul", class_="_266Ly _10aCo")

    def is_item_box(tag):
        return tag.get("data-aut-id", "").startswith("itemBox")

    data = []
    
    if ul:
        items = [item for item in ul.find_all("li") if is_item_box(item)]

        for item in items:
            title_tag = item.find("span", {"data-aut-id": "itemTitle"})
            price_tag = item.find("span", {"data-aut-id": "itemPrice"})
            location_tag = item.find("span", {"data-aut-id": "item-location"})
            link_tag = item.find("a", href=True)

            title = title_tag.text.strip() if title_tag else ""
            price = price_tag.text.strip() if price_tag else ""
            location = location_tag.text.strip() if location_tag else ""
            link = "https://www.olx.in" + link_tag['href'] if link_tag else ""

            data.append([title, price, location, link])

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Title", "Price", "Location", "Link"])
        writer.writerows(data)

    print(f"Extracted {len(data)} items and saved to {output_csv}")



def scrape_via_curl():
    base_url = (
        "https://www.olx.in/api/relevance/v4/search?"
        "lang=en-IN&location=1000001&platform=web-desktop&pttEnabled=true"
        "&query=car%20cover&relaxedFilters=true&spellcheck=true"
    )
    
    pages = input("How many pages do you want to parse? ")
    try:
        pages = int(pages)
        if pages < 1:
            raise ValueError
    except ValueError:
        print("Please enter a valid positive integer for pages.")
        return

    csv_file = "olx_data_via_curl.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            "Title", "Username", "Price", "Description",
            "Address", "Latitude", "Longitude",
            "Google Maps Link", "Direct OLX Link"
        ])

        for page in range(1, pages + 1):
            print(f"Fetching page {page}...")
            url = f"{base_url}&page={page}"
            curl_command = ["curl", url]
            result = subprocess.run(curl_command, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"Curl failed on page {page}:", result.stderr)
                continue

            try:
                data = json.loads(result.stdout)
                ads = data.get("data", [])
            except json.JSONDecodeError as e:
                print(f"Failed to parse JSON on page {page}:", e)
                continue

            for ad in ads:
                title = ad.get("title", "")
                username = ad.get("user_name", "")
                description = ad.get("description", "")
                price = ad.get("price", {}).get("value", {}).get("display", "")

                loc = ad.get("locations_resolved", {})
                address = ", ".join([
                    loc.get("SUBLOCALITY_LEVEL_1_name", ""),
                    loc.get("ADMIN_LEVEL_3_name", ""),
                    loc.get("ADMIN_LEVEL_1_name", ""),
                    loc.get("COUNTRY_name", "")
                ]).strip(", ")

                lat, lon, maps_link = "", "", ""
                if ad.get("locations"):
                    location_data = ad["locations"][0]
                    lat = location_data.get("lat", "")
                    lon = location_data.get("lon", "")
                    if lat and lon:
                        maps_link = f"https://www.google.com/maps?q={lat},{lon}"

                ad_id = ad.get("ad_id", "")
                direct_link = f"https://www.olx.in/item/iid-{ad_id}" if ad_id else ""

                writer.writerow([
                    title, username, price, description,
                    address, lat, lon, maps_link, direct_link
                ])

    print(f"Data from {pages} page(s) saved to {csv_file}")

def main():
    print("Choose a method to scrape OLX data:")
    print("1. Scrape via requests (Less Results)")
    print("2. Fetch via Curl (More Results)")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        scrape_via_requests()
    elif choice == "2":
        scrape_via_curl()
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()



