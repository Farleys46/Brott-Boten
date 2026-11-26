from dotenv import load_dotenv
import json
from firecrawl import Firecrawl

load_dotenv()

app = Firecrawl()

data = app.scrape(
    "https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/brottsbalk-1962700_sfs-1962-700/",
    only_main_content=True,
    formats=["markdown"],
)

markdown_text = data.markdown if hasattr(data, "markdown") else data["markdown"]

with open("brottsbalken.md", "w", encoding="utf-8") as f:
    f.write(markdown_text)

print(f"Klar! Sparade {len(markdown_text)} tecken till brottsbalken.md")