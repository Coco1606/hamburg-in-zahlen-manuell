Ich schaue welche Hamburger Fördergelder wo gelandet sind

Ergebnis 80 bleiben bei der Stadt

1. Frage und Ergebnis

- Frage: Wohin geht Hamburgs Fördergeld 2025, und wie viel davon an die Stadt selbst?
- 2,62 Mrd € bewilligt 2025: 80,3 % städtisch, 1,3 % gemischt-öffentlich, 18,4 % frei (481 Mio €)
- Hochbahn allein 59,5 %, die Top 20 zusammen 82,5 %
- Freier Sektor: 1.884 Empfänger, deren Top 20 = 38,0 %, 43 Empfänger ergeben die Hälfte
- Ergebnis: Kachel output/kachel_02_zuwendungen.png plus NDR-Variante

2. Daten

- Transparenzportal Hamburg, INEZ-Zuwendungen, Bescheide 2015–2025, Stand Jahresende 2025
- data/raw/zuwendungen_2025.xlsx, 76.961 Zeilen
- 1 Zeile = 1 Bescheid, kein Förderfall, bis zu 24 Zeilen je Fall
- Befund der anderen Sitzung von heute, von mir nicht nachgeprüft: Die Datei ist ein Bestand und keine vollständige 10-Jahres-Liste. Deshalb die 21 Mrd nicht als „alles Fördergeld seit 2015“ darstellen.

3. 
- Rohdatei                                      76.961 Zeilen            
- letzter Bescheid je Fall      42.085 Fälle, 21,09 Mrd brutto                   
- minus Rückforderungen                        21,00 Mrd netto (−93Mio)                     
- Erstbescheid 2025                            3.980 Fälle, 2,62 Mrd    
- Vereinsregister aufgelöst, Schreibweisen      1.913 Empfänger zusammengeführt                                                  
- Top 50 von Hand eingeordnet                  3 Gruppen                

4. Entscheidungen (je: was, warum, Beleg)

- a. Letzter Bescheid je Fall: Jede Zeile enthält den Gesamtstand, eine Summe über alle Zeilen würde mehrfach zählen. Gleichstand am selben Tag: 154 Fälle, 32 mit abweichenden Beträgen, davon 1 im 2025-Datensatz mit 13.425 € (0,0005 %). (Entscheidungsdatei Nr. 3)
- b. Erstbescheid-Jahr statt Zuwendungszeitraum: Deshalb „bewilligt 2025“, nie „ausgegeben 2025“.
- c. Rückforderungen: Leer heißt „noch nicht festgesetzt“, gerechnet als 0. Für 2025 sind 94,9 % leer und es gibt 0 € Rückforderungen. Über alle Jahre 93 Mio €, zu 98 % aus 2015–2022. Die alte Angabe „40 %“ war falsch (22,8 / 30,3 / 94,9 %). Die 0 € und die Verteilung nach Jahren fehlen noch als Zelle im Notebook.
- d. Vereinsregister: 5 Fälle (nicht 2), 9,4 Mio €, 0,36 %. Jeder bekommt seine INEZ-Nummer und bleibt einzeln. Die zwei großen stehen auf Rang 35 und 48 (0,34 %).
- e. Schreibweisen: Schlüssel = klein und nur a-z0-9. 114 Namen in 53 Gruppen, 1.974 → 1.913 Empfänger. Angezeigt wird die Schreibweise mit der höchsten Summe. Verworfen: die längste Schreibweise, weil die Trägerliste sie nicht mehr gefunden hätte. Die Anteile bleiben gleich. Schwächen: Umlaute fallen weg, „AG“ und „Aktiengesellschaft“ werden nicht zusammengeführt (für die 10 größten städtischen Empfänger geprüft). (Entscheidungsdatei Nr. 1)
- f. Regel A, städtisch: zwei Äste, bei privatrechtlichen Formen zählt die Beteiligung, bei öffentlich-rechtlichen der Träger. Kammern zählen nicht. Verworfen: Aufsichtsrat (zu aufwendig), „Konzern Stadt“ (zu unscharf). Gegenprobe: crosstab Rechtsform × Einstufung. (Nr. 6)
- g. Nur Top 50 geprüft: Der Rest zählt als frei, also 80,3 % = Untergrenze und 18,4 % = Obergrenze. Wie viel Geld auf die Top 50 entfällt, ist im Notebook noch nicht berechnet.
- h. Belege ohne Seitenzahlen (Beteiligungsbericht): bewusst so, für eine Veröffentlichung nachzuholen.

5. Grenzen und Offenes

- „gemischt-öffentlich“ (3 Fälle: FFHSH, Hamburg Tourismus, HIW) ist noch nicht abgegrenzt
- wer hinter „Vereinsregister“ steckt, bleibt unbekannt
- Datei als Bestand statt Vollständigkeit (siehe 2.)

6. Nachbauen

- uv sync, dann uv run jupyter lab. JupyterLab
- notebooks/01_zuwendungen.ipynb → Restart & Run All