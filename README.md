# Python Static Site Generator

A lightweight Static Site Generator built from scratch using Python's standard library (`pathlib`, `shutil`), HTML, and CSS. It converts Markdown files into a styled, multi-page static website with an auto-generated homepage.

## Features
- Parses Markdown headings (`#`, `##`, `###`) and paragraphs into semantic HTML
- Injects content into a reusable HTML5 template (`base.html`)
- Automatically copies static CSS assets and generates an `index.html` navigation list
- Zero external dependencies

## How to Run
1. Add `.md` files to the `content/` folder.
2. Run the build script:
   ```bash
   py build.py
