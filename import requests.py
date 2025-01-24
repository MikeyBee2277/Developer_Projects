import requests
from bs4 import BeautifulSoup

def fetch_and_print_unicode_grid(doc_url):
    try:
        # Step 1: Fetch the document content
        response = requests.get(doc_url)
        response.raise_for_status()
        content = response.text

        # Step 2: Parse the HTML content to extract table data
        soup = BeautifulSoup(content, 'lxml')
        table = soup.find('table')
        if not table:
            print("No table found in the document.")
            return

        character_data = []
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) == 3:
                try:
                    x = int(cols[0].get_text(strip=True))
                    char = cols[1].get_text(strip=True)
                    y = int(cols[2].get_text(strip=True))
                    character_data.append((x, char, y))
                except ValueError:
                    print(f"Skipping invalid row: {[col.get_text(strip=True) for col in cols]}")

        # Step 3: Determine grid dimensions
        if not character_data:
            print("No valid character data found.")
            return

        max_x = max(data[0] for data in character_data) + 1
        max_y = max(data[2] for data in character_data) + 1

        # Step 4: Create a grid filled with spaces
        grid = [[' ' for _ in range(max_x)] for _ in range(max_y)]

        # Step 5: Populate the grid with characters
        for x, char, y in character_data:
            grid[y][x] = char

        # Step 6: Print the grid row by row
        for row in grid:
            print(''.join(row))

    except requests.RequestException as e:
        print(f"Error fetching document: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
doc_url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
fetch_and_print_unicode_grid(doc_url)