import textwrap
from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


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

    fig.text(0.08, 0.88, textwrap.fill(befund.ueberschrift, 30),
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




