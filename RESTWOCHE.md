# Restwoche — eine fertige Kachel bis Freitag

**Zeitraum:** Mo 07.09. bis Fr 11.09.2026 · **Ziel:** Kachel 02 „Zuwendungen" abgeschlossen,
Notebook läuft durch, Bild liegt in `output/`.

Stand dieses Plans: Commit `dedbb75` („Top 50", 05.09.). Angenommen sind rund vier Stunden
Projektzeit pro Tag.

---

## Der Zuschnitt

Drei der vier geplanten Kacheln fallen weg. Sozialwohnungen, Straßenbäume und die Kreuzung
Bäume × Sozialmonitoring bleiben im README als Ausblick stehen, damit sichtbar ist, dass die
Reihe angelegt ist.

**Der Befund der Kachel steht schon.** Du hast ihn am Samstag selbst formuliert: 80,3 % der
2,62 Mrd € gehen an städtische Empfänger, 18,4 % (481 Mio €) an nicht-städtische, und innerhalb
dieser Gruppe ist das Geld breit gestreut. 45 Empfänger brauchen für die Hälfte statt einer
einzigen AG. Die Woche dient jetzt dazu, diesen Befund zu belegen, zu erzählen und zu rendern.

---

## Was seit Freitag schon erledigt ist

Der Samstags-Commit hat den kompletten Dienstag aus dem alten Plan vorweggenommen, und zwar
größer als ich ihn zugeschnitten hatte:

- Trägerliste über **50** Empfänger statt der von mir vorgeschlagenen 20
- eine dritte Kategorie `gemischt_oeffentlich`, die im alten Plan fehlte
- die Konzentrationsrechnung innerhalb der nicht-städtischen Gruppe
- ein ausformulierter Befund als Markdown-Zelle am Notebook-Ende

Damit ist die eigentliche Analyse fertig. Offen sind Belege, Reproduzierbarkeit, Erzählung und
Bild.

---

## Regel für die zwei Rechner

Gearbeitet wird auf dem PC und auf dem Laptop, und beide gehen über
`Coco1606/hamburg-in-zahlen-manuell`. Bei einem Notebook ist das gefährlicher als bei normalen
Dateien, weil die Ausgaben mit in der Datei stehen. Schon ein erneuter Durchlauf ohne jede
Code-Änderung erzeugt eine Änderung, die git sieht.

Zwei Sätze genügen als Disziplin:

1. **`git pull` bevor du anfängst.** Jedes Mal, auch wenn du sicher bist.
2. **`git push` wenn du aufhörst.** Auch bei halbfertigen Ständen, lieber ein Commit
   „Zwischenstand" als eine Kollision.

Falls es doch einmal kollidiert: Ein Konflikt in einer `.ipynb` wird **nicht** von Hand
aufgelöst. Das ist JSON mit eingebetteten Ausgaben und in einem Editor unlesbar. Nimm eine der
beiden Fassungen komplett (`git checkout --ours` oder `--theirs`, dann `git add` und `commit`)
und tipp die Arbeit der anderen nach. Das dauert zwanzig Minuten. Ein Handmerge dauert einen Tag
und geht schief.

Weil diese Woche knapp ist, gilt zusätzlich: Die Reinschrift `02_kachel_zuwendungen.ipynb`
entsteht auf **einem** Rechner. Such dir einen aus.

---

## Montag 07.09. — Fundament sichern

**Ziel:** Ein Notebook, das von oben nach unten durchläuft, und drei beantwortete Datenfragen.

### 1. Reinschrift anlegen

Das Notebook hat inzwischen 43 Zellen und genau eine Markdown-Zelle, die Befund-Zelle am Ende.
Leg `notebooks/02_kachel_zuwendungen.ipynb` als Reinschrift an. Das alte `01_zuwendungen.ipynb`
bleibt unverändert liegen und wird im README als Erkundung gekennzeichnet.

Der Grund: Die 43 Zellen zu entwirren kostet mehr Zeit, als die tragenden Schritte in eine
lineare Erzählung zu übertragen. Und zwei Notebooks zeigen den Prozess ehrlicher als eines, dem
man die Suche weggeputzt hat.

In die Reinschrift kommen nur die Schritte, die im Ergebnis stehen: Einlesen, Bestandsaufnahme,
Dedup pro Vorgang, Netto rechnen, Erstjahr zuordnen, auf 2025 eingrenzen, Vereinsregister
auflösen, pro Empfänger summieren, Trägerschaft zuordnen, Konzentration. Vor jedem Block eine
Markdown-Zelle mit zwei bis drei Sätzen: was passiert hier und warum so.

Beim Übertragen fällt der Namenskonflikt weg: `anteil` heißt in Zelle [14] die
Rückforderungsquote und in Zelle [26] den Empfängeranteil. Gib den beiden verschiedene Namen.
Die Zellen [28] bis [33] zeigen viermal dasselbe `anteil.head(50)`, davon bleibt eine.

### 2. Die drei Datenfragen beantworten

Jede bekommt eine eigene Zelle plus Markdown-Antwort in der Reinschrift.

**a) Schreibweisen der Empfängernamen.** Du gruppierst über rohe Strings, und die Trägerliste
matcht ebenfalls über exakte Strings. Wenn ein Empfänger unter zwei Schreibweisen in den Daten
steht, wird er doppelt gezählt **und** die zweite Variante rutscht per `fillna` in die falsche
Kategorie. Der Punkt trifft jetzt zweimal.

**b) Mehrere Bescheide am selben Tag.** Dein `drop_duplicates(keep="last")` sortiert nach Datum
und nimmt den letzten. Bei zwei Bescheiden am selben Tag entscheidet die zufällige
Zeilenreihenfolge der Datei. Zähl, wie oft das vorkommt. Wenn es selten ist, reicht ein Satz im
Notebook.

**c) Fehlende Werte in den Schlüsselspalten.** `df.info()` zeigt sie, aber du kommentierst sie
nirgends. Je ein Satz zu `Zuwendungsempfänger`, `Summe von Zuwendungssumme` und `Bescheiddatum`.

**Fertig wenn:** `Kernel → Restart & Run All` läuft ohne Fehler durch und die drei Kennzahlen
kommen wieder heraus: 2,62 Mrd € bei 3.980 Fällen, 80,3 / 1,3 / 18,4 Prozent, 45 Empfänger für
die Hälfte der nicht-städtischen Summe.

---

## Dienstag 08.09. — Belege und Grenzfälle

Die Trägerliste steht, ihre Begründung fehlt noch. Das ist der Tag, an dem aus 50 Zuordnungen
50 belegte Zuordnungen werden.

### 1. Das `fillna` sauber benennen

`kategorie = empfaenger.index.map(traeger).fillna('nicht_staedtisch')` steckt alle 1.895 nicht
geprüften Empfänger in die nicht-städtische Gruppe. Deine Markdown-Zelle nennt das „unklare Fälle
vorsichtshalber als nicht-städtisch gewertet", was den Umfang untertreibt. Geprüft sind 50 von
1.945.

In Geld ist der Effekt klein, weil die geprüften 50 rund 82,5 % der Summe abdecken. Der saubere
Satz dafür lautet sinngemäß: 80,3 % ist eine **Untergrenze** für den städtischen Anteil und
18,4 % eine **Obergrenze** für den nicht-städtischen. Und die 1.945 sind genau genommen
„Empfänger, die nicht als städtisch belegt sind".

Diese Formulierung ist kein Eingeständnis einer Schwäche. Sie ist der Unterschied zwischen einer
Zahl und einer belegten Zahl, und sie gehört auf die Kachel-Quellenzeile und in die IPB-Antwort.

### 2. Belege nachtragen

Zieh das dict aus Zelle [38] nach `data/traeger_top50.csv` mit vier Spalten:

| Spalte | Inhalt |
|---|---|
| `empfaenger` | Name exakt wie in den Daten |
| `traegerschaft` | `staedtisch`, `gemischt_oeffentlich` oder `nicht_staedtisch` |
| `beleg` | Fundstelle, etwa „Beteiligungsbericht FHH 2025, S. 44" |
| `notiz` | Grenzfälle und offene Fragen |

Damit wandert die Liste aus dem Code in die Daten, wo sie hingehört, und jede Zeile bekommt ihre
Quelle. Deine journalistische Grundregel verlangt genau das.

### 3. Die Grenzfälle entscheiden

Ein paar Zuordnungen tragen den Befund stärker als andere, und bei denen lohnt der zweite Blick:

- **Stiftung Hamburger Öffentliche Bücherhallen** steht mit 7,81 % an der **Spitze** der
  nicht-städtischen Liste. Wenn diese eine Einstufung kippt, ändert sich die Spitze der Kachel.
- **Handwerkskammer Hamburg** ist eine Körperschaft öffentlichen Rechts mit Selbstverwaltung.
- **Deutsches Klimarechenzentrum GmbH** hat staatliche Gesellschafter.
- **Studierendenwerk Hamburg AöR** hast du als städtisch geführt, die Bücherhallen als
  nicht-städtisch. Beide sind öffentlich-rechtlich organisiert.

Ich entscheide diese Fälle nicht für dich. Was du brauchst, ist eine **Regel**, nach der du
entscheidest, in einem Satz, und dann alle Grenzfälle konsequent daran gemessen. Die Regel kommt
in `ENTSCHEIDUNGEN.md`, die Einordnung je Fall in die `notiz`-Spalte.

**Fertig wenn:** Die CSV ist eingelesen, das dict aus dem Notebook verschwunden, die Zahlen sind
unverändert, und du kannst zu jeder der 50 Zeilen sagen, woher die Einstufung kommt.

---

## Mittwoch 09.09. — Renderfunktion und Bild

**Ziel:** `output/kachel_02_zuwendungen.png` existiert, 1080 × 1080.

Bau die Trennung, die im README steht: ein `Befund` mit Überschrift, Kernzahl, Datenreihe und
Quelle geht hinein, ein immer gleiches Layout kommt heraus. In `src/hamburg_in_zahlen/render.py`,
damit das Notebook die Funktion importiert und nicht selbst zeichnet.

Für 1080 × 1080 in matplotlib: `figsize=(10.8, 10.8)` bei `dpi=100`.

Zeitfalle: Die Feingestaltung frisst den ganzen Tag, wenn man sie lässt. Setz dir eine Grenze bei
drei Stunden. Ein schlichtes, sauber beschriftetes Bild schlägt ein halbfertiges schönes.

Ersetz bei der Gelegenheit das `print("Hello from hamburg-in-zahlen!")` in
`src/hamburg_in_zahlen/__init__.py`, es ist noch der uv-Rohling. Entweder der Eintrag
`[project.scripts]` in `pyproject.toml` zeigt auf etwas Echtes, oder er fliegt raus.

**Fertig wenn:** Das PNG liegt in `output/`, und ein zweiter Aufruf mit anderen Werten erzeugt
dasselbe Layout mit anderem Inhalt.

---

## Donnerstag 10.09. — Erzählung

**Ziel:** README aktuell, Entscheidungen begründet.

### 1. README nachziehen

Der Abschnitt „Stand: Kachel 02" endet noch mit „Dafür entsteht gerade eine Trägerliste der
Top 50". Die ist fertig, der Befund steht. Zieh den Abschnitt auf das Ergebnis nach, ergänz die
Kachel als Bild und schreib in einem Satz, warum es bei einer Kachel geblieben ist. Der Ausblick
auf die drei anderen bleibt stehen.

Der Ordner `output/` fehlt bisher tatsächlich, obwohl er in der Aufbau-Übersicht beschrieben ist.

### 2. Begründungen festhalten

Leg `ENTSCHEIDUNGEN.md` an, dieselbe Idee wie das Churn-Logbuch, nur kürzer. Pro Entscheidung
drei Felder: was ich getan habe, warum genau so, welche Alternative es gab und warum nicht.

Mindestens diese sieben: Dedup pro Vorgang statt Summe über alle Zeilen, `fillna(0)` bei
Rückforderungen, Erstbescheid-Jahr statt Zuwendungszeitraum, Vereinsregister aufgelöst, Top 50
geprüft und der Rest als nicht-städtisch gewertet, die Regel für die Grenzfälle, und der Umgang
mit den Schreibweisen aus Montag.

Diese Datei formulierst du selbst. Ich liefere Faktenbasis und prüfe, ob deine Logik trägt, aber
die Begründungen sind der Teil, der dich von jemandem unterscheidet, der `groupby` tippen kann.

**Fertig wenn:** Jemand, der nur README und ENTSCHEIDUNGEN.md liest, versteht Befund und Weg
dorthin, ohne das Notebook zu öffnen.

---

## Freitag 11.09. — Abnahme

Vormittag, in dieser Reihenfolge:

1. `Kernel → Restart & Run All` auf der Reinschrift, ohne Fehler
2. Jede Zahl auf der Kachel gegen die Notebook-Ausgabe prüfen, Ziffer für Ziffer
3. `01_zuwendungen.ipynb` im README als Erkundung gekennzeichnet
4. Alle vier Quellen aus dem README auf Erreichbarkeit prüfen
5. `git status` sauber, alles committet **und gepusht**

Nachmittag ist Puffer. Er ist eingeplant und kein Luxus.

---

## Wenn ein Tag kippt

Die Reihenfolge ist nach Wichtigkeit gebaut. Montag und Dienstag tragen den Befund und dürfen
nicht wegfallen. Mittwoch ist kürzbar bis auf ein sehr schlichtes Layout. Donnerstag ist kürzbar
auf README plus vier statt sieben Entscheidungen. Freitagvormittag ist unantastbar.

Was zuerst gestrichen wird, wenn es eng wird: die Feingestaltung der Kachel, dann die
zusätzlichen Einträge in ENTSCHEIDUNGEN.md. Nicht gestrichen wird der Restart-&-Run-All-Lauf,
nicht die Prüfung der Schreibweisen und nicht die Belegspalte in der Trägerliste.
