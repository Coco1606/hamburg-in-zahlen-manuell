import textwrap
from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


@dataclass
class Befund:
    ueberschrift: str
    kernzahl: str
    erlaeuterung: str
    reihe: list
    quelle: str


GROESSE = 1080
DPI = 100
GRUND = "#fcfcfb"
TEXT = "#0b0b0b"
TEXT_LEISE = "#52514e"
SERIE = ["#2a78d6", "#eb6834", "#1baf7a"]

def prozent(wert):
    return f"{wert:.1f}".replace(".", ",") + " %"


def rendern(befund, pfad):
    fig = plt.figure(figsize=(GROESSE / DPI, GROESSE / DPI),
                      dpi=DPI, facecolor=GRUND)

    fig.text(0.08, 0.93, "HAMBURG IN ZAHLEN",
              color=TEXT_LEISE, fontsize=16, fontweight="bold")

    fig.text(0.08, 0.88, textwrap.fill(befund.ueberschrift, 22),
              color=TEXT, fontsize=44, fontweight="bold",
              va="top", linespacing=1.25)

    fig.text(0.08, 0.52, befund.kernzahl, color=SERIE[0],
              fontsize=150, fontweight="bold", va="center")

    fig.text(0.08, 0.40, textwrap.fill(befund.erlaeuterung, 46),
              color=TEXT_LEISE, fontsize=22, va="top", linespacing=1.4)


    ax = fig.add_axes([0.08, 0.22, 0.84, 0.06])
    links = 0.0
    for i, (label, wert) in enumerate(befund.reihe):
        ax.barh(0, wert - 0.4, left=links, height=1, color=SERIE[i])
        links += wert
    ax.set_xlim(0, 100)
    ax.axis("off")

    for i, (label, wert) in enumerate(befund.reihe):
        x = 0.08 + i * 0.30
        fig.add_artist(Rectangle((x, 0.135), 0.018, 0.018, color=SERIE[i]))
        fig.text(x + 0.028, 0.144, f"{label}  {prozent(wert)}",
                 color=TEXT, fontsize=20, va="center")

    fig.text(0.08, 0.06, befund.quelle, color=TEXT_LEISE, fontsize=15)

    fig.savefig(pfad, dpi=DPI, facecolor=GRUND)
    plt.close(fig)
    return pfad



NDR_ROT = "#E1051E"
NDR_BLAU = "#14235A"
WEISS = "#ffffff"
SCHRIFT = "Arial Narrow"
NDR_SERIE = [NDR_ROT, NDR_BLAU, "#9aa3b8"]


FOTO_ANTEIL = 0.33   # oberes Drittel der Kachel

def foto_zuschneiden(pfad, breite, hoehe):
    """Schneidet das Foto mittig auf das Seitenverhältnis des Fotobands zu."""
    from PIL import Image as PilImage
    bild = PilImage.open(pfad).convert("RGB")
    b, h = bild.size
    ziel = breite / hoehe
    if b / h > ziel:                       # zu breit: links und rechts weg
        neu_b = int(h * ziel)
        links = (b - neu_b) // 2
        bild = bild.crop((links, 0, links + neu_b, h))
    else:                                  # zu hoch: oben und unten weg
        neu_h = int(b / ziel)
        oben = (h - neu_h) // 2
        bild = bild.crop((0, oben, b, oben + neu_h))
    return bild.resize((breite, hoehe))



def rendern_ndr(befund, pfad, kicker="Hamburg in Zahlen:", foto=None):
    hoehe = 1350
    fig = plt.figure(figsize=(GROESSE / DPI, hoehe / DPI),
                     dpi=DPI, facecolor=WEISS)
    if foto is not None:
        axf = fig.add_axes([0, 1 - FOTO_ANTEIL, 1, FOTO_ANTEIL], zorder=-1)
        band = foto_zuschneiden(foto, GROESSE, int(hoehe * FOTO_ANTEIL))
        axf.imshow(band, aspect="auto")
        axf.axis("off")
    kasten = dict(edgecolor="none", pad=9)

    fig.text(0.05, 0.945, kicker, color=WEISS, fontsize=30,
             fontweight="bold", family=SCHRIFT, va="top",
             bbox=dict(facecolor=NDR_BLAU, **kasten))

    y = 0.885
    for zeile in textwrap.wrap(befund.ueberschrift.upper(), 24):
        fig.text(0.05, y, zeile, color=WEISS, fontsize=46,
                 fontweight="bold", family=SCHRIFT, va="top",
                 bbox=dict(facecolor=NDR_ROT, **kasten))
        y -= 0.068

    fig.text(0.05, 0.58, befund.kernzahl, color=NDR_ROT, fontsize=150,
             fontweight="bold", family=SCHRIFT, va="center")

    fig.text(0.05, 0.45, textwrap.fill(befund.erlaeuterung, 52),
             color=NDR_BLAU, fontsize=26, family=SCHRIFT,
             va="top", linespacing=1.35)

    ax = fig.add_axes([0.05, 0.30, 0.90, 0.035])
    links = 0.0
    for i, (label, wert) in enumerate(befund.reihe):
        ax.barh(0, wert - 0.4, left=links, height=1, color=NDR_SERIE[i])
        links += wert
    ax.set_xlim(0, 100)
    ax.axis("off")

    for i, (label, wert) in enumerate(befund.reihe):
        x = 0.05 + i * 0.31
        fig.add_artist(Rectangle((x, 0.248), 0.016, 0.013,
                                 color=NDR_SERIE[i]))
        fig.text(x + 0.025, 0.254, f"{label}  {prozent(wert)}",
                 color=NDR_BLAU, fontsize=22, family=SCHRIFT,
                 fontweight="bold", va="center")

    fig.text(0.05, 0.115, befund.quelle, color=NDR_BLAU,
             fontsize=17, family=SCHRIFT)

    fig.add_artist(Rectangle((0.78, 0.04), 0.17, 0.085, color=NDR_ROT))
    fig.text(0.865, 0.082, "NDR HH", color=WEISS, fontsize=34,
             fontweight="bold", family=SCHRIFT, ha="center", va="center")

    fig.savefig(pfad, dpi=DPI, facecolor=WEISS)
    plt.close(fig)
    return pfad


DUNKEL = (0.04, 0.06, 0.12)                       # fast schwarz mit Blaustich
NDR_SERIE_HELL = [NDR_ROT, "#6b83e0", "#c3c9d8"]  # gemischt/frei heller, sonst
                                                  # unsichtbar auf dunklem Grund


def rendern_ndr_voll(befund, pfad, foto, kicker="Hamburg in Zahlen:"):
    hoehe = 1350
    fig = plt.figure(figsize=(GROESSE / DPI, hoehe / DPI),
                     dpi=DPI, facecolor=WEISS)

    # 1. Foto füllt die ganze Kachel, liegt ganz unten
    axf = fig.add_axes([0, 0, 1, 1], zorder=-2)
    axf.imshow(foto_zuschneiden(foto, GROESSE, hoehe), aspect="auto")
    axf.axis("off")

    # 2. Abdunkler darüber: oben durchsichtig, ab 80 % Höhe nach unten dunkler

    axd = fig.add_axes([0, 0, 1, 1], zorder=-1)
    verlauf = np.zeros((hoehe, 1, 4))          # eine Spalte RGBA-Pixel
    verlauf[..., :3] = DUNKEL
    y = np.linspace(1, 0, hoehe)               # 1 = oberer Rand, 0 = unterer
    verlauf[:, 0, 3] = np.clip((0.80 - y) / 0.25, 0, 1) * 0.85
    axd.imshow(verlauf, aspect="auto", extent=(0, 1, 0, 1))
    axd.axis("off")

    # 3. Kicker und Schlagzeile in Kästen
    kasten = dict(edgecolor="none", pad=9)
    fig.text(0.05, 0.945, kicker, color=WEISS, fontsize=30,
             fontweight="bold", family=SCHRIFT, va="top",
             bbox=dict(facecolor=NDR_BLAU, **kasten))
    y_zeile = 0.885
    for zeile in textwrap.wrap(befund.ueberschrift.upper(), 24):
        fig.text(0.05, y_zeile, zeile, color=WEISS, fontsize=46,
                 fontweight="bold", family=SCHRIFT, va="top",
                 bbox=dict(facecolor=NDR_ROT, **kasten))
        y_zeile -= 0.068

    # 4. Kernzahl und Erläuterung in Weiß
    fig.text(0.05, 0.50, befund.kernzahl, color=WEISS, fontsize=150,
             fontweight="bold", family=SCHRIFT, va="center")
    fig.text(0.05, 0.39, textwrap.fill(befund.erlaeuterung, 52),
             color=WEISS, fontsize=26, family=SCHRIFT,
             va="top", linespacing=1.35)

    # 5. Anteilsbalken und Legende
    ax = fig.add_axes([0.05, 0.26, 0.90, 0.035])
    links = 0.0
    for i, (label, wert) in enumerate(befund.reihe):
        ax.barh(0, wert - 0.4, left=links, height=1, color=NDR_SERIE_HELL[i])
        links += wert
    ax.set_xlim(0, 100)
    ax.axis("off")
    for i, (label, wert) in enumerate(befund.reihe):
        x = 0.05 + i * 0.31
        fig.add_artist(Rectangle((x, 0.208), 0.016, 0.013,
                                 color=NDR_SERIE_HELL[i]))
        fig.text(x + 0.025, 0.214, f"{label}  {prozent(wert)}",
                 color=WEISS, fontsize=22, family=SCHRIFT,
                 fontweight="bold", va="center")

    # 6. Quellenzeile und Senderkasten
    fig.text(0.05, 0.115, befund.quelle, color=WEISS,
             fontsize=17, family=SCHRIFT)
    fig.add_artist(Rectangle((0.78, 0.04), 0.17, 0.085, color=NDR_ROT))
    fig.text(0.865, 0.082, "NDR HH", color=WEISS, fontsize=34,
             fontweight="bold", family=SCHRIFT, ha="center", va="center")

    fig.savefig(pfad, dpi=DPI, facecolor=WEISS)
    plt.close(fig)
    return pfad