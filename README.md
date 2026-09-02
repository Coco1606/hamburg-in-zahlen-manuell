# Hamburg in Zahlen

Aus offenen Daten der Stadt Hamburg werden Instagram-Kacheln: ein Befund pro Kachel, ein Layout, ein nachvollziehbarer Weg von der Rohdatei zum Bild.

Portfolio-Projekt im StackFuel Data Analyst Training, Laufzeit 24.08.–11.09.2026.

## Die Idee

Jede Kachel zeigt einen Befund, keine Zahl. „Hamburg vergab 2025 rund 2,6 Mrd € Zuwendungen" kann jeder abschreiben. „Ein einziger Empfänger bekommt 59 % davon" ist das Ergebnis von Bereinigen, Gruppieren, Sortieren und Kumulieren. Diese Analysearbeit soll sichtbar sein: Wer die Kachel sieht, versteht den Fund in vier Sekunden. Wer ins Repo schaut, sieht den Weg dahin.

Geplant sind vier Kacheln (Sozialwohnungen, Zuwendungen, Straßenbäume, Bäume × Sozialmonitoring). Gebaut wird zuerst Kachel 02.

## Stand: Kachel 02 · Zuwendungen

Frage: Wie verteilt sich das Fördergeld der Stadt auf die Empfänger?

Der Weg von der Datei zur Aussage, alles in `notebooks/01_zuwendungen.ipynb`:

| Schritt | Ergebnis |
|---|---|
| Rohdatei aus dem Transparenzportal | 76.961 Zeilen (einzelne Bescheide, 2015–2025) |
| Pro Vorgang nur den zeitlich letzten Bescheid behalten | 42.085 Förderfälle |
| Fördersumme minus Rückforderungen | 21,0 Mrd € netto über zehn Jahre |
| Auf Erstbescheid-Jahr 2025 eingegrenzt | 3.980 Fälle, 2,62 Mrd € |
| Pro Empfänger summiert, Sammeleintrag „Vereinsregister" aufgelöst | 1.974 Empfänger |

Erster Befund: Die Hamburger Hochbahn AG allein erhält 59,5 %, die 20 größten Empfänger zusammen 82,5 %. Neun der zehn größten sind städtische Unternehmen und Anstalten.

Deshalb wird die Frage geschärft: Wie verteilt sich das Geld unter den **nicht-städtischen** Empfängern? Dafür entsteht gerade eine Trägerliste der Top 50 (städtisch / nicht städtisch, Beleg: Beteiligungsbericht der FHH). Danach folgen die Konzentrationskennzahl für diese Gruppe und das Rendern der Kachel.

## Warum die Daten so roh sind

Bis 2013 legte der Senat der Bürgerschaft alle zwei Jahre einen *empfängerbezogenen Zuwendungsbericht* vor, fertig aufbereitet pro Empfänger (zuletzt Drucksache 20/9850 vom 05.11.2013). Mit dem Hamburgischen Transparenzgesetz (in Kraft seit 06.10.2012) wurden diese Berichte ab 2014 durch die Veröffentlichung der Einzelvorgänge im Transparenzportal ersetzt. Seitdem liegt jeder Bescheid offen, aber niemand fasst mehr zusammen. Die Zusammenfassung, die früher der Senat lieferte, ist Teil dieser Analyse.

Praktische Folgen in der Datei: Ein Förderfall steht bis zu 24 Mal darin (jeder Änderungsbescheid ist eine Zeile, jeweils mit dem aktuellen Gesamtstand), Rückforderungen stehen in einer eigenen Spalte, und in einigen Fällen steht statt des Trägernamens nur „Vereinsregister".

## Aufbau

```
data/raw/        Rohdatei zuwendungen_2025.xlsx (Transparenzportal, Stand Jahresende 2025)
notebooks/       01_zuwendungen.ipynb – die Erkundung, Schritt für Schritt
src/             Paket hamburg_in_zahlen (geplant: fetch / analyse / render)
output/          fertige Kacheln (folgt)
```

Analyse und Gestaltung sollen sich nur an einer Stelle berühren: Ein `Befund` (Überschrift, Kernzahl, Datenreihe, Quelle) geht in eine Renderfunktion, die immer dasselbe 1080 × 1080-Layout füllt.

## Nachbauen

```
uv sync
uv run jupyter lab
```

Python ≥ 3.11, Abhängigkeiten in `pyproject.toml` und `uv.lock`: pandas, matplotlib, seaborn, openpyxl, ipykernel.

## Methodische Regeln

- Pro Vorgang zählt die zeitlich letzte Zeile, nicht die größte. Beträge sinken gelegentlich.
- Fehlende Rückforderung heißt 0, nicht „unbekannt". Sonst fallen 40 % der Fälle aus der Summe.
- Ein Fall zählt mit seinem heutigen Betrag ins Jahr seines ersten Bescheids. Es heißt „bewilligt 2025", nie „ausgegeben 2025".
- Top-Empfänger einzeln prüfen, bevor eine Kachel etwas behauptet. Die Rechtsform verrät die Trägerschaft nicht.
- Jede Zahl auf der Kachel muss zur Quelle rückverfolgbar sein.

## Quellen

- Transparenzportal Hamburg, Zuwendungsvorgänge (INEZ), Stand Jahresende 2025
- Bürgerschaft der FHH, Drucksache 20/9850: Fünfter empfängerbezogener Zuwendungsbericht (05.11.2013)
- Antwort der Finanzbehörde auf die FragDenStaat-Anfrage „Zuwendungsberichte ab 2014"
- Beteiligungsbericht der Freien und Hansestadt Hamburg (für die Einordnung städtisch / nicht städtisch)
