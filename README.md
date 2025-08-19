# Stinnett Family Tree Project

A comprehensive family tree visualization project documenting the Stinnett lineage, with interactive web displays and multiple output formats. Created by [Leslie Hodges Gallagher](https://lchogal.github.io/cv/), granddaughter of Sidney William Stinnett (1911-1971).

## Project Overview

This project combines genealogical research with modern visualization tools to create interactive family tree diagrams. The main Python script converts CSV family data into visual family tree diagrams using Graphviz, with additional Quarto-based web rendering for interactive displays.

## Features

- Converts CSV genealogy data to Graphviz DOT format
- Generates family trees in multiple formats (PNG, PDF, SVG, HTML)
- Interactive web display with clickable hyperlinks to genealogy sources
- Color-coded generations for easy visualization (10 generation support)
- Optimized layout with improved spacing and readability
- Supports custom display names and birth/death information
- Clickable web links with visual indicators (🔗)
- Tree navigation connection boxes for complex family trees
- Handles multiple CSV files in batch processing
- Special highlighting for focus person (bold border)
- Flexible node sizing for better text display
- Quarto-based webpage compilation with iframe embeds for full interactivity

## Methodology

Genealogy data was collected through online searches with assistance from AI tools (ChatGPT 5 and Claude Opus 4.1). Research relied heavily on crowd-sourced information from:
- [Geni.com](https://geni.com)
- [FamilySearch.org](https://familysearch.org) 
- [FindAGrave.com](https://findagrave.com)

**Important Note**: Recorded data was rarely independently verified against primary historical sources. Low-confidence connections were included in the trees; errors should be expected.

## Technical Requirements

- Python 3.12.11+
- pandas
- Graphviz 13.0.1+ (for image generation)
- Quarto 1.6.42+ (for interactive webpage generation)

## Installation

1. Install Python dependencies:
   ```bash
   pip install pandas
   ```

2. Install Graphviz:
   - Visit: https://graphviz.org/download/
   - Or use package manager (e.g., `brew install graphviz` on macOS)

3. Install Quarto (for interactive webpage generation):
   - Visit: https://quarto.org/docs/get-started/
   - Or use package manager (e.g., `brew install quarto` on macOS)

## Usage

### Generate Family Tree Diagrams

1. Place your CSV family data files in the `data/` folder
2. Run the conversion script:
   ```bash
   python convert_family.py
   ```
3. Generated files will appear in the `output/` folder

### Create Interactive Webpage

1. After generating diagrams, render the interactive webpage:
   ```bash
   quarto render Stinnett_tree.qmd
   ```
2. Open `Stinnett_tree.html` in your browser for the interactive experience

## CSV Format

Your CSV should include these columns:

### Required Columns
- `Person_ID` - Unique identifier for each person
- `Full_Name` or `Chart_Display_Name` - Person's display name
- `Father_ID` - Father's Person_ID (for parent-child relationships)
- `Mother_ID` - Mother's Person_ID (for parent-child relationships)
- `Generation` - Generation number (0 for focus person, 1 for parents, 2 for grandparents, etc.)

### Optional Columns
- `Birth_Info` or `Chart_Birth_Info` - Birth details (date, location)
- `Death_Info` or `Chart_Death_Info` - Death details (date, location)
- `Primary_URL` or `Secondary_URL` - Web links for additional information
- Additional location/origin information will be displayed automatically

## Output

For each CSV file, the script generates:
- `.dot` file - Graphviz source code
- `.png` file - High-resolution PNG image
- `.pdf` file - Vector PDF document
- `.svg` file - Scalable SVG vector graphic
- `.html` file - Interactive HTML with embedded SVG and clickable links

The main project also includes:
- `Stinnett_tree.qmd` - Quarto markdown source for comprehensive webpage
- `Stinnett_tree.html` - Final interactive webpage with iframe-embedded family trees

## Color Coding

- **Gold** - Focus person (Generation 0)
- **Light Coral** - Parents (Generation 1)
- **Light Steel Blue** - Grandparents (Generation 2)  
- **Light Green** - Great-grandparents (Generation 3)
- **Wheat** - 2nd Great-grandparents (Generation 4)
- **Plum** - 3rd Great-grandparents (Generation 5)
- And so on through 10 generations...

## Technical Attribution

Family tree diagrams were generated using:
- **Python 3.12.11** with Graphviz 13.0.1
- **Coding support**: Claude Code 1.0.83 (Anthropic)
- **Webpage rendering**: Quarto 1.6.42 (Posit)
- **Research assistance**: ChatGPT 5 (OpenAI) and Claude Opus 4.1 (Anthropic)

## Contact & Corrections

Send corrections, suggestions, and privacy concerns to [hodges.gallagher@gmail.com](mailto:hodges.gallagher@gmail.com).

Supporting files and project repository: [https://github.com/lchogal/Stinnett_line](https://github.com/lchogal/Stinnett_line)