#!/usr/bin/env python3
"""Generiert ../plz-bundesland.js aus den GeoNames-Postleitzahldaten (CC-BY 4.0).

Nutzung:
    curl -sL -o /tmp/DE.zip https://download.geonames.org/export/zip/DE.zip
    unzip -o -q /tmp/DE.zip -d /tmp
    python3 tools/build-plz-bundesland.py /tmp/DE.txt

Bei mehrdeutigen PLZs (mehrere Bundeslaender, z. B. Grossempfaenger-PLZs)
gewinnt die Mehrheit der GeoNames-Eintraege. Luecken zwischen bekannten PLZs
innerhalb eines Bundesland-Blocks werden dem Block zugerechnet; Luecken an
Bundesland-Grenzen ergeben '' (unbekannt).
"""
import csv
import json
import os
import sys
from collections import Counter, defaultdict

BL_NAMES = ["Baden-Württemberg", "Bayern", "Berlin", "Brandenburg", "Bremen", "Hamburg",
            "Hessen", "Mecklenburg-Vorpommern", "Niedersachsen", "Nordrhein-Westfalen",
            "Rheinland-Pfalz", "Saarland", "Sachsen", "Sachsen-Anhalt",
            "Schleswig-Holstein", "Thüringen"]

def main(src: str) -> None:
    idx = {n: i for i, n in enumerate(BL_NAMES)}
    votes = defaultdict(Counter)
    with open(src, encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            plz, bl = row[1].strip(), row[3].strip()
            if len(plz) == 5 and plz.isdigit() and bl in idx:
                votes[plz][bl] += 1

    resolved = {plz: idx[c.most_common(1)[0][0]] for plz, c in votes.items()}
    ambiguous = sum(1 for c in votes.values() if len(c) > 1)

    items = sorted((int(p), b) for p, b in resolved.items())
    ranges = []
    for n, b in items:
        if ranges and ranges[-1][2] == b and n > ranges[-1][1]:
            ranges[-1][1] = n
        else:
            ranges.append([n, n, b])
    flat = [x for r in ranges for x in r]

    js = f"""// PLZ -> Bundesland Aufloesung (generiert aus GeoNames.org Postal-Daten, CC-BY 4.0)
// Format: flaches Array [von, bis, blIndex, ...] ueber aufsteigend sortierte PLZ-Bereiche.
// Luecken innerhalb eines Bereichs werden dem Bereich zugerechnet.
// Regenerieren: siehe tools/build-plz-bundesland.py
(function() {{
    var BL = {json.dumps(BL_NAMES, ensure_ascii=False)};
    var R = {json.dumps(flat)};
    window.resolveBundesland = function(plz) {{
        var n = parseInt(String(plz || '').replace(/\\D/g, ''), 10);
        if (isNaN(n) || String(plz).replace(/\\D/g, '').length !== 5) return '';
        var lo = 0, hi = R.length / 3 - 1;
        while (lo <= hi) {{
            var mid = (lo + hi) >> 1;
            if (n < R[mid * 3]) hi = mid - 1;
            else if (n > R[mid * 3 + 1]) lo = mid + 1;
            else return BL[R[mid * 3 + 2]];
        }}
        return '';
    }};
}})();
"""
    out = os.path.join(os.path.dirname(__file__), "..", "plz-bundesland.js")
    with open(out, "w", encoding="utf-8") as f:
        f.write(js)
    print(f"{len(resolved)} PLZs ({ambiguous} mehrdeutig, Mehrheit gewinnt) -> "
          f"{len(ranges)} Ranges -> {out} ({os.path.getsize(out) / 1024:.1f} KB)")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "/tmp/DE.txt")
