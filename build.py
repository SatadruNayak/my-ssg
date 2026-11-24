import shutil
from pathlib import Path

# Directory paths
CONTENT_DIR = Path("content")
TEMPLATE_FILE = Path("templates/base.html")
STATIC_DIR = Path("static")
PUBLIC_DIR = Path("public")


def parse_markdown(text: str) -> tuple[str, str]:
    """Converts basic Markdown (#, ##, ###, paragraphs) to HTML and extracts the title."""
    lines = text.strip().splitlines()
    html_lines = []
    title = "Untitled Page"

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("### "):
            html_lines.append(f"<h3>{stripped[4:]}</h3>")
        elif stripped.startswith("## "):
            html_lines.append(f"<h2>{stripped[3:]}</h2>")
        elif stripped.startswith("# "):
            heading = stripped[2:]
            if title == "Untitled Page":
                title = heading
            html_lines.append(f"<h1>{heading}</h1>")
        else:
            html_lines.append(f"<p>{stripped}</p>")

    return title, "\n        ".join(html_lines)


def build_site() -> None:
    # 1. Ensure the public/ directory exists
    PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Copy static assets (CSS, images) into public/
    if STATIC_DIR.exists():
        for asset in STATIC_DIR.iterdir():
            if asset.is_file():
                shutil.copy(asset, PUBLIC_DIR / asset.name)

    # 3. Load the base HTML template
    template = TEMPLATE_FILE.read_text(encoding="utf-8")
    pages = []

    # 4. Process every .md file in content/
    for md_file in sorted(CONTENT_DIR.glob("*.md")):
        raw_text = md_file.read_text(encoding="utf-8")
        title, html_body = parse_markdown(raw_text)

        output_html = template.replace("{{ title }}", title).replace("{{ content }}", html_body)
        output_filename = f"{md_file.stem}.html"
        (PUBLIC_DIR / output_filename).write_text(output_html, encoding="utf-8")

        pages.append((title, output_filename))
        print(f"Built: public/{output_filename}")

    # 5. Auto-generate public/index.html
    links_html = "\n        ".join(
        f'<li><a href="{filename}">{title}</a></li>' for title, filename in pages
    )
    index_body = f"<h1>My Site</h1>\n        <ul>\n        {links_html}\n        </ul>"
    index_html = template.replace("{{ title }}", "Home").replace("{{ content }}", index_body)
    (PUBLIC_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print("Built: public/index.html")


if __name__ == "__main__":
    build_site()