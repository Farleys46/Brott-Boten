# Way of working - Brott-Boten

## Mål
Bygga en RAG-chatbot som förklarar Brottsbalken på enkel svenska, enligt vår projektplan.
Vi siktar på VG, så bonusdelarna (Docker, Azure, Logfire/evals, CI/CD) ingår i planeringen.

## Team och ansvar
 Alla bidrar överallt. 


## Arbetsflöde
- Vi använder **Kanban** (GitHub Projects) med kolumnerna: Backlog, Ready, In progress, In review, Done.
- Vi försöker utgå från ett **issue**. Ingen kod utan issue.
- Max [2] issues per person i "In progress" samtidigt.
- Vi har [2] korta möten i veckan och en kort avstämning: vad gjorde jag, vad ska jag göra, vad är jag blockerad av.
- Sprintar på 1 vecka. Vi planerar och gör en kort retro vid sprintstart.

## Git
- `main` är alltid fungerande. Ingen pushar direkt till `main eller development`.
- Branchnamn: `feature/`, `fix/`, `docs/`.
- Commits: små, med ett tydligt meddelande i presens (t.ex. `Add paragraph parser`).
- Minst **1 godkännande** från någon annan innan merge. Den som skrivit koden mergar inte själv utan granskning.
- Vi granskar PR:ar inom [24 timmar] på vardagar.

## Definition of done
Ett issue är klart när:
- koden fungerar och har testats (enhetstest där det är rimligt)
- PR är granskad och mergad
- README eller kommentarer är uppdaterade vid behov
- issuet är flyttat till Done

## Kodstandard
- Python, formatering och lint med `ruff`.
- Funktioner är små och gör en sak (DRY). Upprepad kod bryts ut.
- Inga hemligheter i repot. `.env` är gitignorad, och `.env.example` har tomma värden.

## Användning av LLM
- Tillåtet för mindre delar och idéer, inte för att lösa hela delar.
- All LLM-genererad kod **kommenteras** som `# LLM-genererad` och måste kunna förklaras av den som checkar in den.

## Kommunikation
- Kanal: Discord. 
- Är man blockerad mer än [en halvdag] säger man till direkt.

## Beslut och konflikter
- Små beslut tas av den som äger issuet. Större beslut (arkitektur, bibliotek) tas i gruppen.
- Vid oenighet försöker vi först komma överens, annars röstar vi.
- Om någon inte levererar tar vi upp det tidigt i gruppen, och vid behov med läraren.

## Ändringar
Det här dokumentet ändras via PR och kräver att alla godkänner.