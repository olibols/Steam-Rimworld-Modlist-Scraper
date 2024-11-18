import os
import json
import xml.etree.ElementTree as ET
from main import auto_detect_workshop_content_path

def generate_mod_json():
    workshop_content_path = auto_detect_workshop_content_path()
    mod_json = {}

    if os.path.exists(workshop_content_path):
        for mod_id in os.listdir(workshop_content_path):
            mod_path = os.path.join(workshop_content_path, mod_id)
            about_path = os.path.join(mod_path, "About", "About.xml")
            if os.path.isfile(about_path):
                try:
                    tree = ET.parse(about_path)
                    root = tree.getroot()
                    package_id_element = root.find("packageId")
                    if package_id_element is not None:
                        package_id = package_id_element.text.lower()
                        steam_url = f"https://steamcommunity.com/sharedfiles/filedetails/?id={mod_id}"
                        mod_json[steam_url] = package_id
                    else:
                        print(f"'packageId' not found in 'About.xml' for mod id: {mod_id}")
                except ET.ParseError:
                    print(f"Error parsing 'About.xml' for mod id: {mod_id}")
            else:
                print(f"Mod {mod_id} is missing an 'About.xml' or is not downloaded, skipping...")

        # Write the JSON data to a file
        with open("mod_steam_mapping.json", "w") as json_file:
            json.dump(mod_json, json_file, indent=4)
        print("JSON file 'mod_steam_mapping.json' created successfully.")
    else:
        print(f"ERROR: The workshop content path does not exist: {workshop_content_path}")

if __name__ == "__main__":
    generate_mod_json()
