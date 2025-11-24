# Genealogy to Graphviz Converter

import pandas as pd
import os
import glob

import subprocess

def create_family_tree(csv_file, output_dir="output"):
    """
    Convert CSV family data to Graphviz format
    """
    
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file)
        
    except FileNotFoundError:
        print(f"Error: Could not find file '{csv_file}'")
        return False
    except Exception as e:
        
        print(f"Error reading file: {e}")
        return False
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Get base filename without extension
    base_name = os.path.splitext(os.path.basename(csv_file))[0]
    
    # Create output filename
    dot_file = os.path.join(output_dir, f"{base_name}.dot")
    
    
    # Generation colors
    colors = {
        0: "gold",           # Focus person
        1: "lightcoral",     # Parents
        2: "lightsteelblue", # Grandparents
        3: "lightgreen",     # Great-grandparents
        4: "wheat",          # 2nd great-grandparents
        5: "plum",           # 3rd great-grandparents
        6: "lightyellow",    # 4th+ great-grandparents
        7: "lightcyan",
        8: "mistyrose",
        9: "lavender",
        10: "lightgray"
    }
    
    with open(dot_file, 'w', encoding='utf-8') as f:
        # Write header
        f.write('digraph family_tree {\n')
        f.write('    rankdir=TB;\n')
        f.write('    bgcolor=white;\n')
        f.write('    margin=0.1;\n')
        f.write('    pad=0.1;\n')
        f.write('    ranksep=0.3;\n')
        f.write('    nodesep=0.2;\n')
        f.write('    node [shape=box, style="filled,rounded", fontname="Arial", fontsize=10, fixedsize=false, margin=0.1];\n')
        f.write('    edge [color=black, penwidth=1.5];\n')
        f.write('    \n')
        
        # No title in image (controlled by qmd file)
        f.write('    \n')
        
        # Process each person
        for _, person in df.iterrows():
            if pd.isna(person["Person_ID"]):
                continue
            
            person_id = str(person["Person_ID"]).strip()
            
            # Get display name (use Chart_Display_Name if available, otherwise Full_Name)
            if "Chart_Display_Name" in person and pd.notna(person["Chart_Display_Name"]):
                name = str(person["Chart_Display_Name"]).strip().replace('"', '\\"')
            else:
                name = str(person["Full_Name"]).strip().replace('"', '\\"')
            
            # Get birth info
            if "Chart_Birth_Info" in person and pd.notna(person["Chart_Birth_Info"]):
                birth_info = str(person["Chart_Birth_Info"]).strip().replace('"', '\\"')
            elif "Birth_Info" in person and pd.notna(person["Birth_Info"]):
                birth_info = str(person["Birth_Info"]).strip().replace('"', '\\"')
            else:
                birth_info = "Unknown"
            
            birth_line = f"{birth_info}" if birth_info != "Unknown" else "Birth: Unknown"
            
            # Get death info
            death_line = ""
            if "Chart_Death_Info" in person and pd.notna(person["Chart_Death_Info"]):
                death_info = str(person["Chart_Death_Info"]).strip().replace('"', '\\"')
                if death_info:
                    death_line = f"{death_info}"
            elif "Death_Info" in person and pd.notna(person["Death_Info"]):
                death_info = str(person["Death_Info"]).strip().replace('"', '\\"')
                if death_info:
                    death_line = f"{death_info}"
            
            # Check for tree connections to apply bold formatting
            has_tree_connection = False
            if "Tree_Connection" in person and pd.notna(person["Tree_Connection"]):
                has_tree_connection = True
            elif "Related_Tree" in person and pd.notna(person["Related_Tree"]):
                has_tree_connection = True
            
            # Build label (no HTML formatting)
            if death_line:
                label = f"{name}\\n{birth_line}\\n{death_line}"
            else:
                label = f"{name}\\n{birth_line}"
            
            # Get generation for color
            gen = person.get("Generation", 0)
            if pd.isna(gen):
                gen = 0
            color = colors.get(int(gen), "lightgray")
            
            
            # Special styling for focus person (generation 0)
            if gen == 0:
                if has_tree_connection:
                    style = f'fillcolor="{color}", style="filled,rounded", peripheries=3, fontname="Arial Bold"'
                else:
                    style = f'fillcolor="{color}", style="filled,rounded"'
            else:
                if has_tree_connection:
                    style = f'fillcolor="{color}", style="filled,rounded", peripheries=3, fontname="Arial Bold"'
                else:
                    style = f'fillcolor="{color}", style="filled,rounded"'
            
            # Add URL if available (check both Primary_URL and Secondary_URL)
            url_attr = ""
            url = ""
            if "Primary_URL" in person and pd.notna(person["Primary_URL"]):
                url = str(person["Primary_URL"]).strip()
            elif "Secondary_URL" in person and pd.notna(person["Secondary_URL"]):
                url = str(person["Secondary_URL"]).strip()
            
            if url:
                url_attr = f', URL="{url}", target="_blank"'
                # Add visual indicator for clickable names right after the name
                if "🔗" not in name:
                    name_with_link = name + " 🔗"
                    # Rebuild the label with the linked name
                    if death_line:
                        label = f"{name_with_link}\\n{birth_line}\\n{death_line}"
                    else:
                        label = f"{name_with_link}\\n{birth_line}"
            
            # Add CSS class for tree connections
            css_class = ""
            if has_tree_connection:
                css_class = ', class="tree-connection"'
            
            # Write the person with empty tooltip to suppress node ID display
            f.write(f'    "{person_id}" [label="{label}", {style}{url_attr}, tooltip=""{css_class}];\n')
        
        f.write('    \n')
        
        # Tree navigation connection boxes (disabled)
        f.write('    // Tree navigation connection boxes\n')
        
        f.write('    \n')
        
        # Track marriages to avoid duplicates and collect spouse pairs
        marriages = set()
        spouse_pairs = []
        
        f.write('    // Marriage relationships and rank constraints\n')
        for _, person in df.iterrows():
            if pd.isna(person["Person_ID"]) or pd.isna(person.get("Spouse_ID")):
                continue
                
            person_id = str(person["Person_ID"]).strip()
            spouse_id = str(person["Spouse_ID"]).strip()
            
            # Create unique marriage key (sorted to avoid duplicates)
            marriage_key = tuple(sorted([person_id, spouse_id]))
            
            if marriage_key not in marriages:
                marriages.add(marriage_key)
                spouse_pairs.append((person_id, spouse_id))
                
                # Build marriage label from available fields
                marriage_info = []
                if "Chart_Marriage_Info" in person and pd.notna(person["Chart_Marriage_Info"]):
                    marriage_info.append(str(person["Chart_Marriage_Info"]).strip().replace('"', '\\"'))
                elif "Marriage_Date" in person and pd.notna(person["Marriage_Date"]):
                    marriage_info.append(str(person["Marriage_Date"]).strip().replace('"', '\\"'))
                if "Marriage_Location" in person and pd.notna(person["Marriage_Location"]):
                    marriage_info.append(str(person["Marriage_Location"]).strip().replace('"', '\\"'))
                
                marriage_label = "\\n".join(marriage_info) if marriage_info else ""
                
                # Keep spouses on same rank (horizontal line)
                f.write(f'    {{rank=same; "{person_id}"; "{spouse_id}"}};\n')
                
                # Connect spouses with a direct line and marriage info label
                if marriage_label:
                    f.write(f'    "{person_id}" -> "{spouse_id}" [dir=none, color=black, style=dashed, constraint=false, label="{marriage_label}", fontsize=10, fontcolor=black];\n')
                else:
                    f.write(f'    "{person_id}" -> "{spouse_id}" [dir=none, color=black, style=dashed, constraint=false];\n')
        
        f.write('    \n')
        
        # Write parent-child relationships
        f.write('    // Parent-child relationships\n')
        for _, person in df.iterrows():
            if pd.isna(person["Person_ID"]):
                continue
            
            person_id = str(person["Person_ID"]).strip()
            
            # Get parent IDs
            father_id = None
            mother_id = None
            if "Father_ID" in person and pd.notna(person["Father_ID"]):
                father_id = str(person["Father_ID"]).strip()
            if "Mother_ID" in person and pd.notna(person["Mother_ID"]):
                mother_id = str(person["Mother_ID"]).strip()
            
            # Connect parents to children
            if father_id:
                f.write(f'    "{father_id}" -> "{person_id}";\n')
            if mother_id:
                f.write(f'    "{mother_id}" -> "{person_id}";\n')
        
        f.write('}\n')
    
    
    # Generate output files
    
    formats = [
        ("png", "PNG image"),
        ("svg", "SVG vector"),
        ("svg", "HTML interactive")
    ]
    
    print(f"\nGenerating visual outputs...")
    
    for fmt, description in formats:
        if description == "HTML interactive":
            # Generate HTML file with embedded SVG
            output_file = os.path.join(output_dir, f"{base_name}.html")
            svg_file = os.path.join(output_dir, f"{base_name}_temp.svg")
            
            try:
                # First generate SVG
                cmd = ["dot", "-Tsvg", dot_file, "-o", svg_file]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                
                # Read the SVG content
                with open(svg_file, 'r', encoding='utf-8') as f:
                    svg_content = f.read()
                
                # Create HTML wrapper
                html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{base_name.replace('_', ' ').title()} - Family Tree</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 100%;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }}
        .svg-container {{
            text-align: center;
            overflow: auto;
        }}
        svg {{
            max-width: 100%;
            height: auto;
        }}
        
        /* Interactive hover effects only for tree connections */
        .tree-connection {{
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .tree-connection:hover {{
        }}
        
        .tree-connection:hover path {{
            stroke-width: 3 !important;
        }}
        
        .tree-connection:hover text {{
            font-weight: bold;
            font-size: 11px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="svg-container">
            {svg_content}
        </div>
    </div>
</body>
</html>"""
                
                # Write HTML file
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                # Clean up temporary SVG file
                os.remove(svg_file)
                
                print(f"{description} created: {output_file}")
                
            except subprocess.CalledProcessError as e:
                print(f"Failed to create {description}: {e}")
                print(f"   Make sure Graphviz is installed: https://graphviz.org/download/")
                return False
            except FileNotFoundError:
                print(f"Graphviz not found. Please install it from: https://graphviz.org/download/")
                return False
        else:
            output_file = os.path.join(output_dir, f"{base_name}.{fmt}")
            
            # For PDF, use cairo renderer to enable clickable links
            if fmt == "pdf":
                cmd = ["dot", "-Tpdf:cairo", dot_file, "-o", output_file]
            else:
                cmd = ["dot", f"-T{fmt}", dot_file, "-o", output_file]
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"{description} created: {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to create {description}: {e}")
                print(f"   Make sure Graphviz is installed: https://graphviz.org/download/")
                return False
            except FileNotFoundError:
                print(f"Graphviz not found. Please install it from: https://graphviz.org/download/")
                print(f"   Then manually run: dot -T{fmt} {dot_file} -o {output_file}")
                return False
    
    return True

# Main execution
if __name__ == "__main__":
    print("GENEALOGY TO GRAPHVIZ CONVERTER")
    print("=" * 40)
    
    # Process all CSV files in the data folder
    data_folder = "data"
    output_folder = "output"
    
    # Check if data folder exists
    if not os.path.exists(data_folder):
        print(f"Data folder not found: {data_folder}")
        print("   Please create a 'data' folder and put your CSV files in it.")
        exit(1)
    
    # Find all CSV files in data folder
    csv_files = glob.glob(os.path.join(data_folder, "*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {data_folder} folder")
        print("   Please add CSV files to the data folder.")
        exit(1)
    
    print(f"Found {len(csv_files)} CSV file(s) in {data_folder} folder:")
    for csv_file in csv_files:
        print(f"   - {os.path.basename(csv_file)}")
    
    print(f"\nProcessing files...")
    
    success_count = 0
    for csv_file in csv_files:
        print(f"\n{'='*50}")
        print(f"Processing: {os.path.basename(csv_file)}")
        print(f"{'='*50}")
        
        if create_family_tree(csv_file, output_folder):
            success_count += 1
        else:
            print(f"Failed to process {os.path.basename(csv_file)}")
    
    print(f"\nScript completed!")
    print(f"Successfully processed {success_count}/{len(csv_files)} files")
    print(f"Output files saved to: {output_folder}/")