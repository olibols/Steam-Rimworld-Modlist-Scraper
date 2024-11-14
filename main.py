from gooey import Gooey, GooeyParser
import os
import requests
from bs4 import BeautifulSoup
import winreg
import xml.etree.ElementTree as ET
import string
import ctypes
import re

rimworld_id = "294100"
rimworld_version = ""
rimworld_package_id = "ludeon.rimworld"
rimworld_install_path = ""
steam_install_path = ""
steam_workshop_content_path = ""
modlist_title = "RimWorld_Modlist"
modlist_save_path = ""

def getValidPath(prompt, default_path):
    path = input(prompt) or default_path
    while not os.path.exists(path):
        print(f"ERROR: The given path does not exist: {path}")
        path = input(prompt) or default_path
    return path

def get_steam_path():
    try:
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\Valve\\Steam")
        return os.path.join(winreg.QueryValueEx(hkey, "InstallPath")[0])
    except:
        return "*CANNOT RESOLVE STEAM PATH*"

def list_drives():
    drives = []
    bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(f"{letter}:\\")
        bitmask >>= 1
    return drives

def get_steam_library_folders():
    steam_path = get_steam_path()
    library_vdf_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
    library_folders = []

    if os.path.exists(library_vdf_path):
        with open(library_vdf_path, 'r') as file:
            content = file.read()
            # Use regex to find all paths in the VDF file
            matches = re.findall(r'"path"\s+"([^"]+)"', content)
            library_folders = [match.replace('\\\\', '\\') for match in matches]

    # Add the default Steam path
    library_folders.append(steam_path)
    return library_folders

def auto_detect_rimworld_install_path():
    library_folders = get_steam_library_folders()
    for folder in library_folders:
        potential_path = os.path.join(folder, "steamapps\\common\\RimWorld")
        if os.path.exists(potential_path):
            return potential_path
    return "CANNOT RESOLVE RIMWORLD INSTALL PATH"

def auto_detect_workshop_content_path():
    library_folders = get_steam_library_folders()
    for folder in library_folders:
        potential_path = os.path.join(folder, "steamapps\\workshop\\content", rimworld_id)
        if os.path.exists(potential_path):
            return potential_path
    return "CANNOT RESOLVE WORKSHOP CONTENT PATH"

@Gooey(program_name="RimWorld Modlist Creator", default_size=(800, 600))
def main():
    parser = GooeyParser(description="Create a modlist for RimWorld")
    parser.add_argument("collection_url", help="Enter RimWorld Steam workshop collection URL")
    parser.add_argument("modlist_save_path", help="Enter modlist save location path", widget="DirChooser")
    parser.add_argument("rimworld_install_path", help="Enter RimWorld install path", default=auto_detect_rimworld_install_path(), widget="DirChooser")
    parser.add_argument("steam_workshop_content_path", help="Enter Steam workshop content path (point to 294100 folder)", default=auto_detect_workshop_content_path(), widget="DirChooser")
    parser.add_argument("--add_dlc", help="Include DLCs in the modlist", action="store_true")
    args = parser.parse_args()

    global modlist_save_path, steam_workshop_content_path, rimworld_install_path
    modlist_save_path = args.modlist_save_path.rstrip("\\/")
    steam_workshop_content_path = args.steam_workshop_content_path.rstrip("\\/")
    rimworld_install_path = args.rimworld_install_path.rstrip("\\/")

    response = requests.get(args.collection_url)
    if response.status_code == 200:
        mod_ids = parse(response.content)
        package_ids = findModPackageIds(mod_ids)
        if args.add_dlc:
            package_ids.extend(get_dlc_package_ids())
        buildXMLModlist(package_ids)
        print(f"\nModList: {modlist_title} , created in: {modlist_save_path}")
    else:
        print("ERROR: Can't fetch URL content. Please make sure the URL is correct and you are connected to a network.")

def parse(content):
    soup = BeautifulSoup(content, "html.parser")
    id_nodes = soup.find_all("div", class_="collectionItem")
    ids = [node.get("id")[11:] for node in id_nodes if node.has_attr("id")]
    if not ids:
        print("ERROR: No mod collection could be found at provided URL")
    return ids

def findModPackageIds(ids):
    dir_path = steam_workshop_content_path
    dir_contents = os.listdir(dir_path)
    packages = []

    for item in ids:
        if item in dir_contents:
            about_path = os.path.join(dir_path, item, "About\\About.xml")
            if os.path.isfile(about_path):
                try:
                    tree = ET.parse(about_path)
                    root = tree.getroot()
                    packages.append(root.find("packageId").text.lower())
                except ET.ParseError:
                    print(f"Error parsing 'About.xml' for mod id: {item}")
            else:
                print(f"Mod {item} is missing an 'About.xml' or is not downloaded, skipping...")
    return packages

def get_dlc_package_ids():
    return [
        "ludeon.rimworld",
        "ludeon.rimworld.royalty",
        "ludeon.rimworld.ideology",
        "ludeon.rimworld.biotech",
        "ludeon.rimworld.anomaly"
    ]

def buildXMLModlist(package_ids):
    root = ET.Element("ModsConfigData")
    version = ET.Element("version")
    version.text = "1.5.4243 rev947" 
    root.append(version)

    active_mods = ET.Element('activeMods')
    for id in package_ids:
        li = ET.Element("li")
        li.text = id
        active_mods.append(li)
    root.append(active_mods)

    known_expansions = ET.Element('knownExpansions')
    for dlc in get_dlc_package_ids():
        li = ET.Element("li")
        li.text = dlc
        known_expansions.append(li)
    root.append(known_expansions)

    tree = ET.ElementTree(root)
    
    # Use 4 spaces for indentation
    ET.indent(tree, space="    ", level=0)
    
    save_path = os.path.join(modlist_save_path, modlist_title) + ".xml"
    tree.write(save_path, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    main()