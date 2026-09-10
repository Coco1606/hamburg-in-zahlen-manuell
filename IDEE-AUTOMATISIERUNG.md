# Idee: Hamburg in Zahlen als automatische Kachel-Pipeline

die Lösung bietet der SciCAR-Workshops (18.9.2026: restatis
11:30, n8n 14:30).  Die Stopp-Regel im FAHRPLAN-2026-H2
gilt: kein neues Projekt vor der ersten bezahlten Rechnung. Der Zusatz „manuell" im
Ordnernamen bleibt Programm, solange das StackFuel-Portfolio läuft (Selbstleistung).

## Die Frage

Kann ich eine Zielfrage eingeben („Wie viele Menschen ziehen jedes Jahr nach Hamburg?"),
und die Kette holt die amtliche Zahl automatisch und rendert daraus eine Instagram-Kachel?

## Antwort: ja, in vier Schritten

1. **Zielfrage rein.** Freitext.
2. **Tabelle finden.** Ein Sprachmodell übersetzt die Frage in eine Katalogsuche bei
   Destatis/Regionaldatenbank/Zensus und schlägt die passende Tabelle vor. Einziger
   Schritt mit KI. Der „Bibliothekar", der das Regal zeigt.
3. **Zahl holen.** Skript ruft die Tabelle über die amtliche Schnittstelle ab.
   Die Zahl kommt aus der Datenbank, nie aus dem Sprachmodell. Tabellennummer und
   Stand kommen mit, damit ist die Quellenpflicht automatisch erfüllt.
4. **Kachel rendern.** `Befund` (Überschrift, Kernzahl, Datenreihe, Quelle) geht in die
   Renderfunktion, 1080 × 1080. Mensch sieht, gibt frei, dann Instagram.

## Was schon existiert

- **Renderer**: `src/hamburg_in_zahlen/render.py` hier, plus die Kachel-Engine in
  miri-social (rendert täglich PNGs, Maskottchen-Automatik).
- **Instagram-Versand**: miri-social (Meta-Token noch offen, wird dort gelöst).
- **Methodische Regeln**: README hier (Rückverfolgbarkeit, Dedup-Regeln).

## Was neu wäre

- **Datenabruf über die amtlichen Schnittstellen.** Vorbild: R-Paket `restatis`
  (CorrelAid, MIT-Lizenz, 7 GENESIS-Datenbanken: Destatis, Regionaldatenbank, Zensus
  2022, Kommunale Bildungsdatenbank, Landesämter NRW/BY/ST). Python-Pendant: `pystatis`.
  Kostenlose Konten je Datenbank nötig. Grob 100 Zeilen.
- **Frage → Tabelle** (Sprachmodell + Katalogsuche), mit Freigabe-Schritt.

## Der Haken: Hamburg ist in diesen Datenbanken ein einziger Kreis

Destatis/Regionaldatenbank kennen Hamburg als Land und als Kreis 02000. **Keine Bezirke,
keine Stadtteile.** Für Landesebene (Einwohner, Mieten, Inflation, Unfälle, Pendler)
reicht das. Für Wilhelmsburg oder Eimsbüttel braucht es:
- Statistikamt Nord (Stadtteilprofile, Excel, keine bequeme Schnittstelle),
- Transparenzportal Hamburg (CKAN-API, aus dem Ratsmonitor bekannt),
- Zensus 2022 (geht bis auf 100-m-Gitterzellen, spannend für Karten-Kacheln).

## Empfehlung für den Bau (wenn es so weit ist)

Nicht von der freien Frage ausgehen. Destatis hat tausende Tabellen mit kryptischen
Namen, die Übersetzung trifft nicht immer. Stattdessen: eine **gepflegte Liste von
30–50 Tabellen**, einmal von Hand geprüft. Die Kette zieht täglich eine, holt den
aktuellen Stand, rendert. Die freie Frage bleibt Werkzeug für neue Kachel-Ideen.
Immer Freigabe durch einen Menschen vor dem Posten.

## Aufwand

Wenige Tage, weil Renderer und Versand aus miri-social kommen. Neu ist nur der
Statistik-Abruf.

## Quellen

- restatis: https://github.com/CorrelAid/restatis
- Workshop-Code SciCAR 2026 (M. Neutze, Destatis): https://github.com/wahlatlas/SciCAR26
- SciCAR-Workshop „Datenjournalismus im Flow – Mit n8n redaktionelle Workflows
  automatisieren" (L. Dreesbach, SMC), 18.9.2026 14:30

---

# Bauplan (Stand 10.9.2026)

Ergebnis des Gesprächs vom 10.9. Zielbild: journalistischer Instagram-Account
„Hamburg in Zahlen", ausbaufähig zu SH / MV („Nord in Zahlen"). Frage rein
(bestenfalls im Dashboard), Pipeline findet passende Kennzahl, zieht die Daten,
bringt sie in eine feste Form, rendert eine Kachel. Mensch gibt frei.

## Grundentscheidung: nicht putzen, sondern normalisieren

Eine Regel, die jeden beliebigen Datensatz bereinigt, gibt es nicht. Stattdessen:
**jede Quelle wird einmal in eine feste Zielform übersetzt** (Adapter), danach
sieht alles gleich aus. Putzen passiert einmal pro Quelle, nie pro Frage.

**Zielform** (eine schmale Tabelle, immer dieselben 7 Spalten):

| Spalte | Beispiel |
|---|---|
| region | 02000 (Hamburg), 02103 (Stadtteil), 01 (SH), 13 (MV) |
| zeit | 2025 oder 2025-03 |
| merkmal | Bevölkerung insgesamt |
| wert | 1.964.021 |
| einheit | Personen |
| quelle | Regionaldatenbank 12411-01-01-5-B |
| stand | 2026-06-30 |

Quelle und Stand stehen in **jeder Zeile**. Damit ist die Grundregel
(jede Zahl rückverfolgbar) technisch eingebaut.

## Drei Quellen-Klassen

| Klasse | Quellen | Aufwand |
|---|---|---|
| **A Schnittstelle** | Destatis GENESIS, Regionaldatenbank, Zensus 2022, Landesämter | **ein** Adapter für alle (gleiches Format „ffcsv"), danach 0 Handarbeit |
| **B strukturierte Datei** | Transparenzportal HH (Stadtteil-CSV/GeoJSON, CKAN-API), Stadtteil-Profile-Excel (Statistikamt Nord) | ein kleiner Adapter je Dateityp, danach 0 Handarbeit |
| **C PDF / krumme Excel** | Bürgerschaftsdrucksachen, Sonderauswertungen | bleibt Handarbeit, im Katalog als C markiert |

Vorhandene Adapter: `K:\projekte\statistik\scripts\stadtteilprofile.py` (Klasse B,
trennt Stadtteil/Bezirk/Gesamt), `regionalstatistik.py` (Klasse A, nur Regio, Login
per HTTP-Header gelöst).

## Fünf Bausteine

1. **Katalog** (Herz der Pipeline). Gepflegte Liste von Kennzahlen, Start 30–50.
   Je Eintrag: Klartext-Name, 2–3 Beispielfragen, Quelle, Tabellennummer, Filter,
   Regionsebene, Klasse A/B/C, Adapter-Name. Ersetzt die Suche in tausenden
   Destatis-Tabellen durch die Suche im eigenen Regal. Wächst mit jeder Frage,
   die nicht trifft.
2. **Abruf.** `regionalstatistik.py` erweitern: Datenbank wählbar (genesis / regio /
   zensus / Landesämter, gleiche Software, andere Adresse), Merkmalsfilter und
   Regionalschlüssel durchreichen. Plus Transparenzportal-Abruf (CKAN
   `package_search` → neueste CSV). Vorbild für Filter: SciCAR26-Skripte 00 und 041.
3. **Normalisierung.** Adapter A / B → Zielform. Feste Prüfungen: Ebenen getrennt?
   Bruchjahre markiert (Stadtteilprofile 2013)? Einheit vorhanden? Stand vorhanden?
4. **Frage → Kennzahl.** Sprachmodell liest Frage + Katalogtexte, schlägt 3
   Kandidaten vor, Mensch wählt. Modell sieht **nie Zahlen**, nur Katalogtexte.
   Kein Treffer → ehrliche Antwort „nicht im Katalog / nicht in den Datenbanken"
   plus Vorschlag für neuen Katalogeintrag.
5. **Kachel + Freigabe.** Zielform → Renderer (`src/hamburg_in_zahlen/render.py`
   hier oder Kachel-Engine miri-social), 1080×1080, Quellenzeile Pflicht.
   Dashboard = kleine lokale Webseite (Streamlit, ~100 Zeilen, StackFuel-Stoff):
   Frage, Kandidaten, Zahl, Vorschau, Freigabe-Knopf.

## Ausbau SH / MV

Region ist eine **Spalte im Katalog**, nicht im Code. Flächenländer sind sogar
leichter als Hamburg: Regionaldatenbank kennt dort jeden Kreis und jede Gemeinde
(siehe SciCAR26 `041_MV.R`). Statistikamt Nord ist für SH ohnehin zuständig.

## Etappen (jede für sich nutzbar)

| Etappe | Ergebnis | Aufwand |
|---|---|---|
| 1 | Katalog mit 10 Einträgen, Abruf erweitert, Adapter A, erste Kachel per Kommandozeile | 2–3 Tage |
| 2 | Transparenzportal-Adapter (Klasse B), Stadtteile funktionieren | 1 Tag |
| 3 | Frage → Kennzahl mit Sprachmodell, Streamlit-Dashboard mit Freigabe | 2 Tage |
| 4 | Zeitplan (täglich eine Katalog-Kennzahl), Versand über miri-social | 1 Tag + Meta-Token |

Nach Etappe 1 existiert der Sparfall: Frage manuell, Zahl + Kachel automatisch.

## Voraussetzungen

- Konten: Regionaldatenbank vorhanden (`statistik/.env`). **Destatis und Zensus
  fehlen** (kostenlos anlegen).
- **Neuer Ordner**, getrennt von `hamburg-in-zahlen-manuell` (bleibt
  StackFuel-Portfolio = Selbstleistung). Vorschlag: `K:\projekte\nord-in-zahlen`.
- `statistik` vorher unter Git stellen (`.env` prüfen, siehe Repo-Analyse 12.7.).

## Risiken

- **Freie Frage ist der schwächste Schritt**: viele Fragen haben keine amtliche
  Zahl (Beispiel Kita-Mindestflächen). Dashboard muss das ehrlich sagen.
- **Stopp-Regel** FAHRPLAN-2026-H2: kein neues Projekt vor der ersten Rechnung.
  Etappe 1 wäre als StackFuel-Übung (Abruf, pandas, Visualisierung) vertretbar.
  Entscheidung liegt bei Coco.

## Offene Prüfpunkte

- Transparenzportal-CSV einmal öffnen: steckt dort dieselbe Ebenen-Falle wie in
  der Excel?
- SciCAR 18.9.: restatis-Workshop 11:30 (M. Neutze, Destatis), DDJ-Meetup 12:45,
  n8n-Workshop 14:30. Frage für Neutze: Landesamt-Datenbanken Nord geplant?
