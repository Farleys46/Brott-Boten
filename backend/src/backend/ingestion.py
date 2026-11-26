import re
from pathlib import Path
from pydantic import BaseModel


class BBalkenChunk(BaseModel):
    chunk_id: str
    kapitel_nr: int
    kapitel_titel: str
    paragraf: str
    raw_text: str
    context_text: str


def clean_markdown(text: str) -> str:
    """Tvättar unicode, normaliserar avvikande paragrafer i 26 kap. och klipper bort header/övergångsbestämmelser."""
    text = text.replace("\xa0", " ").replace("\xad", "").replace("\u200b", "")

    # Hoppa över metadata och innehållsförteckning fram till första kapitlets brödtext
    start_match = re.search(r"(?m)^###\s+1\s*kap\.", text)
    if start_match:
        text = text[start_match.start():]

    # Klipp bort övergångsbestämmelser i slutet av dokumentet
    end_match = re.search(r"(?m)^###\s+Övergångsbestämmelser", text)
    if end_match:
        text = text[:end_match.start()]

    # Normalisera 26 kap. 4 c § och 4 d § där "§" hamnat på raden under
    text = re.sub(
        r"(?m)^(\d+\s*[a-z]?)\s+(_/Träder i kraft[^/\n]+/_)\s*\n§\s+",
        r"**\1 §** \2\n",
        text,
    )

    # Normalisera 26 kap. 1 § och 2 a § som saknar fetstil framför "/Rubriken..."
    text = re.sub(
        r"(?m)^(\d+\s*[a-z]?\s*§)\s+(/Rubriken\s+)",
        r"**\1** \2",
        text,
    )

    # Ta bort Firecrawls escape-tecken i numrerade listor ("1\." -> "1.")
    text = re.sub(r"(?m)^(\s*\d+)\\\.", r"\1.", text)

    return text.strip()


def clean_paragraph_tail(text: str) -> str:
    """Tar bort avdelnings-, kapitel- och underrubriker som råkat hamna sist i en paragraf."""
    lines = text.splitlines()
    while lines:
        last = lines[-1].strip()
        if (
            not last
            or last.startswith(("####", "##", "/Kapitlet", "_/Kapitlet", "/Rubriken", "_/Rubriken"))
        ):
            lines.pop()
        else:
            break
    return "\n".join(lines).strip()


def chunk_brottsbalken(md_path: Path) -> list[BBalkenChunk]:
    """Läser brottsbalken.md och delar upp den i en chunk per paragraf (§)."""
    raw_md = md_path.read_text(encoding="utf-8")
    cleaned_md = clean_markdown(raw_md)

    # Splitta på kapitelrubriker ("### 3 kap. Om brott mot liv och hälsa")
    kapitel_parts = re.split(r"(?m)^###\s+(\d+\s*kap\.[^\n]+)$", cleaned_md)

    chunks: list[BBalkenChunk] = []
    seen_ids: dict[str, int] = {}

    for i in range(1, len(kapitel_parts), 2):
        kapitel_titel = kapitel_parts[i].strip()
        kapitel_body = kapitel_parts[i + 1]

        kap_nr_match = re.match(r"(\d+)\s*kap\.", kapitel_titel)
        kapitel_nr = int(kap_nr_match.group(1)) if kap_nr_match else 0

        # Splitta enbart på fetstilta paragrafer i början av rad ("**1 §**", "**4 a §**")
        paragraf_parts = re.split(r"(?m)^\*\*(\d+\s*[a-z]?\s*§)\*\*\s*", kapitel_body)

        for j in range(1, len(paragraf_parts), 2):
            paragraf_nr = re.sub(r"\s+", " ", paragraf_parts[j]).strip()
            paragraf_text = clean_paragraph_tail(paragraf_parts[j + 1])

            if not paragraf_text:
                continue

            base_id = f"{kapitel_nr}_kap_{paragraf_nr.replace(' ', '_')}"
            seen_ids[base_id] = seen_ids.get(base_id, 0) + 1
            chunk_id = (
                base_id
                if seen_ids[base_id] == 1
                else f"{base_id}_v{seen_ids[base_id]}"
            )

            context_text = (
                f"Brottsbalken (1962:700) | {kapitel_titel} | {paragraf_nr}\n"
                f"{paragraf_text}"
            )

            chunks.append(
                BBalkenChunk(
                    chunk_id=chunk_id,
                    kapitel_nr=kapitel_nr,
                    kapitel_titel=kapitel_titel,
                    paragraf=paragraf_nr,
                    raw_text=paragraf_text,
                    context_text=context_text,
                )
            )

    return chunks


if __name__ == "__main__":
    md_file = Path(__file__).parent / "brottsbalken.md"
    chunks = chunk_brottsbalken(md_file)

    print(f"Totalt antal chunks: {len(chunks)}")
    print(f"Antal unika chunk_id: {len({c.chunk_id for c in chunks})}")
