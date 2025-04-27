import requests

# Clear the console using ANSI escape code (works in most terminals)
print("\033c", end="")

# Fetch the latest Libreddit instances JSON from GitHub
session = requests.session()
json_url = 'https://github.com/libreddit/libreddit-instances/raw/refs/heads/master/instances.json'
request = session.get(json_url)
updated = request.json()["updated"]
instances = request.json()["instances"]
print(f"Last updated: {updated}\n")
# Dynamically collect address keys (excluding 'country', 'version', 'description')
address_keys = set()
countries = set()
for item in instances:
    # Collect all unique countries
    if "country" in item:
        countries.add(item["country"])
    # Collect only relevant address keys
    for key in item.keys():
        if key not in ("country", "version", "description"):
            address_keys.add(key)
address_keys = sorted(address_keys)
countries = sorted(countries)

# Prompt user to select address type (url, onion, i2p, etc.)
print("Select address type:")
for idx, key in enumerate(address_keys, 1):
    print(f"{idx}. {key}".upper())
key_choice = input("Enter number: ").strip()
try:
    selected_key = address_keys[int(key_choice) - 1]
except (ValueError, IndexError):
    print("Invalid selection. Defaulting to first option.")
    selected_key = address_keys[0]

# Prompt user to select country (or all countries)
print("\nAvailable countries:")
print("0. All countries")
for idx, country in enumerate(countries, 1):
    print(f"{idx}. {country}")
country_choice = input("Select country by number: ").strip()
try:
    if country_choice == "0":
        selected_country = None
    else:
        selected_country = countries[int(country_choice) - 1]
except (ValueError, IndexError):
    print("Invalid selection. Showing all countries.")
    selected_country = None

# Clear the console again before displaying results
print("\033c", end="")

# Show selected options
print(f"Selected {selected_key.upper()} for address type.")
print("\nAvailable instances:")
print(f"0. All countries")
for idx, country in enumerate(countries, 1):
    print(f"{idx}. {country}")

# Display filtered instances based on user selection
print(f"\nInstances", end="")
if selected_country:
    print(f" in {selected_country}", end="")
else:
    print(" in all countries:\n", end="")
print(f" in {selected_key.upper()} format:\n")
for item in instances:
    if selected_key in item and item[selected_key]:
        if selected_country is None or item.get("country") == selected_country:
            print(item[selected_key])

# Pause at the end until user presses Enter
input("\nPress Enter to exit...")
