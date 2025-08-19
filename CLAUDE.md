# Family Tree Graphviz Project

## Project Location
- Full path: `/Users/lchg5/Library/Mobile Documents/com~apple~CloudDocs/Family history/Family_tree_graphviz`
- Main script: `convert_family.py`
- Data folder: `data/` (contains CSV files)
- Output folder: `output/` (contains generated .dot, .png, .pdf, .svg files)

## Git Commands
```bash
# Add files to git (use absolute path due to directory reset issues)
git -C "/Users/lchg5/Library/Mobile Documents/com~apple~CloudDocs/Family history/Family_tree_graphviz" add convert_family.py data/ output/

# Check status
git -C "/Users/lchg5/Library/Mobile Documents/com~apple~CloudDocs/Family history/Family_tree_graphviz" status
```

## Project Notes
- Script converts CSV family data to Graphviz format
- Generates visual family trees in multiple formats
- Requires Graphviz to be installed for image generation