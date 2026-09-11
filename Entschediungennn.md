# Entscheidungen und Befunde

Pro Entscheidung drei Felder: was ich getan habe, warum genau so, welche Alternative es gab und
warum nicht. Dieselbe Idee wie das Logbuch zum Churn-Projekt, nur kürzer.

**Selbstleistungs-Regel:** Das Feld *„Meine Begründung"* formuliere **ich**. Der Trainer liefert
Faktenbasis, Kanon-Alternativen und Gegenproben, und prüft, ob meine Logik trägt.

Stand: 07.09.2026

---

## 1. Schreibweisen der Empfängernamen zusammengeführt

### Was ich getan habe

Vor dem Gruppieren bekommt jede Zeile einen bereinigten Vergleichsschlüssel: alles klein, alles
außer Buchstaben und Ziffern entfernt. Gruppiert wird über diesen Schlüssel. Als Anzeigename
gewinnt die Schreibweise mit der höchsten Fördersumme.

### Der Fund

Geprüft mit `duplicated(keep=False)` auf dem bereinigten Schlüssel. Ergebnis: **114 Namen in
53 Gruppen**, alle echt.

Größter Fall, Basis & Woge:

| Schreibweise | netto |
|---|---|
| Basis & Woge e.V. | 5.002.815,04 |
| BASIS & WOGE e. V. | 983.582,31 |
| BASIS & WOGE e. V | 227.041,71 |
| BASIS & WOGE e.V | 75.320,91 |
| **zusammen** | **6.288.759,97** |

Vier Zeilen für einen Träger, unterschieden nur durch Groß-/Kleinschreibung, ein Leerzeichen und
einen Punkt.

### Verworfene Alternative

Als Anzeigename die **längste** Schreibweise zu nehmen. Hätte hier `BASIS & WOGE e. V.` gewählt,
weil sie ein Zeichen länger ist. Zwei Nachteile: Die Kachel zeigt eine Schreibweise, die wie
Geschrei aussieht, und die Trägerliste ist mit `Basis & Woge e.V.` verschlüsselt, hätte den
Eintrag also nicht mehr gefunden und den Träger still in die falsche Kategorie geschoben.

### Folgen

| | vorher | nachher |
|---|---|---|
| Empfänger | 1.974 | **1.913** |
| Dubletten-Check | 114 Treffer | leer |
| Trägerliste gefunden | — | 50 von 50 |
| Kategorien | 80,31 / 1,29 / 18,40 | **unverändert** |

Die Kachel-Kernzahlen bleiben stehen, weil das Geld nur innerhalb der nicht-städtischen Gruppe
umverteilt wird. Was sich ändert, ist die Rangfolge innerhalb dieser Gruppe, und dort steigt
Basis & Woge mit 1,3 % der nicht-städtischen Summe deutlich auf.

### Zweite Prüfung: Rechtsform-Varianten

Der Schlüssel führt `Aktiengesellschaft` und `AG` **nicht** zusammen. Deshalb ein gezielter Check
auf die zehn größten städtischen Namen (Hochbahn, SAGA, Sprinkenhof, Elbkinder, Port Authority,
Staatsoper, Thalia, Kampnagel, UKE, Studierendenwerk). Jedes Stichwort liefert genau einen
Treffer. `HHW Hamburger Hochbahn-Wache GmbH` steht zu Recht neben der Hochbahn, das ist eine
eigenständige Tochterfirma.

Die 59,5 % der Hochbahn und damit die städtische Seite der Kachel sind sauber.

### Meine Begründung

*(von mir zu formulieren)*

### IPB-Nachsprech-Antwort

*(von mir zu formulieren, 2–3 Sätze)*

---

## 2. Die 40-Prozent-Angabe im README ist nicht belegbar

### Was im README steht

> Fehlende Rückforderung heißt 0, nicht „unbekannt". Sonst fallen **40 %** der Fälle aus der
> Summe.

### Gemessen

| Ebene | fehlende Rückforderungen |
|---|---|
| Rohzeilen (76.961) | 17.540 = **22,8 %** |
| Vorgänge nach Dedup (42.085) | 12.734 = **30,3 %** |
| nur Erstjahr 2025 (3.980) | 3.777 = **94,9 %** |

Auf keiner Ebene sind es 40 %.

### Warum das die Regel wichtiger macht, nicht unwichtiger

In dem Datensatz, den die Kachel benutzt, fehlt die Rückforderung bei 94,9 % der Fälle. Ohne
`fillna(0)` würde `netto` bei fast allen 2025-Fällen zu `NaN`, und die 2,62 Mrd € gäbe es
überhaupt nicht. Die Angabe im README verkauft die eigene Methodenentscheidung unter Wert.

### Zu tun

README-Zahl ersetzen. Vorschlag: die 94,9 %, weil der Satz von den Fällen spricht, die aus der
Summe fallen würden.

### Meine Begründung

*(von mir zu formulieren)*

---

## 3. Mehrere Bescheide am selben Tag

Die Regel lautet: pro Vorgang zählt die zeitlich letzte Zeile. Offen war, was bei Gleichstand
passiert, denn dann entscheidet die zufällige Zeilenreihenfolge der Datei.

| Prüfschritt | Ergebnis |
|---|---|
| Vorgänge mit mehreren Bescheiden am spätesten Datum | 154 von 42.085 (0,37 %) |
| davon mit **abweichenden** Beträgen | 32 |
| davon im 2025-Datensatz | **1 Vorgang** |
| dessen Betrag | 13.425 € von 2.616.008.624,65 € (0,0005 %) |

Kein zweites Sortierkriterium nötig. Geprüft, beziffert, ohne Einfluss auf das Ergebnis.

---

## 4. Fehlende Werte in den Schlüsselspalten

| Spalte | fehlend von 76.961 |
|---|---|
| INEZ-Nummer | 0 |
| Zuwendungsempfänger | 0 |
| Summe von Zuwendungssumme | 0 |
| Bescheiddatum | 0 |

Die Spalten, die Gruppierung, Summe und Zeitzuordnung tragen, sind vollständig. Fehlende Werte
gibt es nur bei den Rückforderungen, siehe Punkt 2.

---

## 5. README-Anleitung „Nachbauen" war kaputt

`uv run jupyter lab` lief nicht, weil JupyterLab nicht in den Abhängigkeiten stand. Aufgefallen
beim Einrichten des zweiten Rechners am 07.09. Behoben mit `uv add jupyterlab`.

Ein Fremder, der dem README folgt, wäre an derselben Stelle gescheitert. Der Test hat nur
funktioniert, weil das Projekt einmal auf einem frischen Rechner aufgesetzt wurde.

---

## 6. Regel für die Trägerschaft (Regel A) und die Belege

### Die Regel

> Städtisch ist, wer der FHH mehrheitlich gehört, oder wer eine Anstalt, Körperschaft oder
> Stiftung öffentlichen Rechts ist, deren Träger die FHH oder eine ihrer Körperschaften ist.
> Selbstverwaltungskörperschaften wie Kammern zählen nicht, auch wenn sie öffentlich-rechtlich
> sind.

Die Regel hat zwei Äste. Bei **öffentlich-rechtlichen** Formen entscheidet die Trägerschaft, bei
**privatrechtlichen** Formen die Beteiligung. Verworfen wurden eine steuerungsrechtliche Regel
(Aufsichtsrat mehrheitlich FHH) als pro Fall zu aufwendig und eine zuwendungsrechtliche
(„Konzern Stadt") als zu unscharf.

### Die Gegenprobe

Alle 50 Träger wurden mit ihrer Rechtsform erfasst (`data/traeger_top50.csv`) und die Einstufung
je Rechtsform gegengeprüft:

| Rechtsform | gemischt | nicht städtisch | städtisch |
|---|---|---|---|
| AG | 0 | 0 | 2 |
| AöR | 0 | 0 | 2 |
| KöR | 0 | 1 | 1 |
| Stiftung öffentlichen Rechts | 0 | 0 | 6 |
| Stiftung bürgerlichen Rechts | 0 | 2 | 0 |
| e.V. | 0 | 12 | 0 |
| GmbH | 3 | 4 | 13 |
| gGmbH | 0 | 2 | 2 |

Eindeutig sind alle öffentlich-rechtlichen Formen und die Vereine. Uneindeutig sind `GmbH`,
`gGmbH` und `KöR`, und zwar zu Recht: Eine GmbH sagt nichts darüber, wem sie gehört. Der Fall
`KöR` (UKE städtisch, Handwerkskammer nicht) ist derselbe Mechanismus eine Ebene tiefer und in
den Notizen der beiden Zeilen begründet.

### Belege: bewusst ohne Seitenzahlen

Eingetragen ist die Art des Nachweises, nicht die Fundstelle:

| Beleg | Zeilen |
|---|---|
| Rechtsform (öffentlich-rechtlich oder e.V.) | 21 |
| Beteiligungsbericht FHH | 20 |
| nicht im Beteiligungsbericht FHH | 6 |
| Feldwert im Transparenzportal | 2 |
| shmh.de/organisationsstruktur/ | 1 |

Die Prüfung gegen den Beteiligungsbericht hat am 05.09. stattgefunden, seitengenaue Fundstellen
wurden dabei nicht mitgeschrieben. Sie nachzutragen hätte den Nachmittag gekostet, an dem die
Kachel entstehen musste. Für eine Veröffentlichung wären sie nachzuholen, für ein
Portfolio-Stück ist die Art des Nachweises ausreichend.

### Zwei Träger ohne Namen

Das Transparenzportal nennt in zwei Fällen statt des Trägers nur „Vereinsregister". Beide sind
als `e.V. (aus dem Feldwert abgeleitet)` geführt.

| | |
|---|---|
| Rang 35, ZUW-2025-00367 | 5.500.290,66 € = 0,21 % |
| Rang 48, ZUW-2025-00986 | 3.500.000,00 € = 0,13 % |
| zusammen | **0,34 %** |

Selbst wenn beide städtisch wären, ginge die Kachelzahl von 80,31 % auf 80,65 %. Statt zu raten
ist die Größe des Nichtwissens beziffert.

### Offen: die dritte Kategorie

`gemischt_oeffentlich` ist dreimal vergeben (FFHSH, Hamburg Tourismus, HIW). Was sie von
„städtisch" unterscheidet, ist noch nicht definiert.

*(Satz von mir zu formulieren)*

---

## Noch zu dokumentieren (Donnerstag)

- [ ] Dedup pro Vorgang statt Summe über alle Zeilen
- [ ] Erstbescheid-Jahr statt Zuwendungszeitraum
- [ ] Vereinsregister als Sammeleintrag aufgelöst
- [ ] Top 50 geprüft, der Rest per `fillna` als nicht-städtisch gewertet
      (80,3 % ist damit eine Untergrenze, 18,4 % eine Obergrenze)
- [ ] Die Regel, nach der Grenzfälle entschieden werden (Bücherhallen, Handwerkskammer,
      Klimarechenzentrum, Studierendenwerk)

## Zahlen, die im README nachgezogen werden müssen

- 1.974 Empfänger → **1.913**
- 40 % fehlende Rückforderungen → **94,9 %** (bezogen auf die 2025-Fälle)
- eine Zeile für das Zusammenführen der Schreibweisen in der Schritt-Tabelle
