# Stinnett Family Tree Project

## Project Location
- Full path: `/Users/lchg5/Library/Mobile Documents/com~apple~CloudDocs/Family history/Stinnett_tree`
- Main script: `convert_family.py`
- Data folder: `data/` (contains CSV files)
- Output folder: `output/` (contains generated .dot, .png, .pdf, .svg, .html files)
- Quarto document: `Stinnett_tree.qmd` (renders to HTML and PDF)

## Git Commands
```bash
# Add files to git (use absolute path due to directory reset issues)
git -C "/Users/lchg5/Library/Mobile Documents/com~apple~CloudDocs/Family history/Stinnett_tree" add convert_family.py data/ output/

# Check status
git -C "/Users/lchg5/Library/Mobile Documents/com~apple~CloudDocs/Family history/Stinnett_tree" status
```

## Usage Commands
```bash
# Generate family tree visualizations
python convert_family.py

# Render Quarto document (HTML and PDF)
quarto render Stinnett_tree.qmd
```

## Project Notes
- Script converts CSV family data to Graphviz format
- Generates visual family trees in multiple formats
- Requires Graphviz and Quarto to be installed