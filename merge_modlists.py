from gooey import Gooey, GooeyParser
import xml.etree.ElementTree as ET
import os

@Gooey(program_name="RimWorld Modlist Merger", default_size=(600, 400))
def main():
    parser = GooeyParser(description="Merge two RimWorld modlist XML files")
    parser.add_argument("file1", help="Select the first modlist XML file", widget="FileChooser")
    parser.add_argument("file2", help="Select the second modlist XML file", widget="FileChooser")
    parser.add_argument("output_file", help="Select the output file location", widget="FileSaver")
    args = parser.parse_args()

    if os.path.exists(args.file1) and os.path.exists(args.file2):
        merge_modlists(args.file1, args.file2, args.output_file)
    else:
        print("One or both input files do not exist.")

def merge_modlists(file1, file2, output_file):
    # Parse the XML files
    tree1 = ET.parse(file1)
    root1 = tree1.getroot()
    
    tree2 = ET.parse(file2)
    root2 = tree2.getroot()
    
    # Find the activeMods elements
    active_mods1 = root1.find('activeMods')
    active_mods2 = root2.find('activeMods')
    
    # Create a set to store unique mod IDs
    mod_ids = set()
    
    # Add mod IDs from the first file
    for mod in active_mods1.findall('li'):
        mod_ids.add(mod.text)
    
    # Add mod IDs from the second file
    for mod in active_mods2.findall('li'):
        mod_ids.add(mod.text)
    
    # Create a new root element for the merged modlist
    new_root = ET.Element("ModsConfigData")
    
    # Add version element (assuming version from the first file)
    version = root1.find('version')
    new_root.append(version)
    
    # Create a new activeMods element
    new_active_mods = ET.Element('activeMods')
    for mod_id in sorted(mod_ids):  # Sort for consistency
        li = ET.Element('li')
        li.text = mod_id
        new_active_mods.append(li)
    
    new_root.append(new_active_mods)
    
    # Add knownExpansions from the first file (assuming they are the same)
    known_expansions = root1.find('knownExpansions')
    new_root.append(known_expansions)
    
    # Write the merged XML to the output file
    new_tree = ET.ElementTree(new_root)
    ET.indent(new_tree, space="    ", level=0)  # Pretty print
    new_tree.write(output_file, encoding='utf-8', xml_declaration=True)
    print(f"Merged modlist saved to {output_file}")

if __name__ == '__main__':
    main()