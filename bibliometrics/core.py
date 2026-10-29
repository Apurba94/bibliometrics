"""Standard bibliometric indicators, computed transparently from citation counts."""
import csv
import math
import statistics


def h_index(cites):
    """Largest h such that h papers have at least h citations each (Hirsch, 2005)."""
    s = sorted(cites, reverse=True)
    return sum(1 for i, c in enumerate(s, 1) if c >= i)


def g_index(cites):
    """Largest g such that the top g papers together have at least g^2 citations (Egghe, 2006); g <= n."""
    s = sorted(cites, reverse=True)
    total, g = 0, 0
    for i, c in enumerate(s, 1):
        total += c
        if total >= i * i:
            g = i
    return g


def i10_index(cites):
    return sum(1 for c in cites if c >= 10)


def e_index(cites):
    """Square root of the excess citations in the h-core beyond h^2 (Zhang, 2009)."""
    h = h_index(cites)
    core = sorted(cites, reverse=True)[:h]
    return math.sqrt(max(0, sum(core) - h * h))


def m_quotient(cites, first_year, current_year):
    """h divided by academic age in years (Hirsch's m)."""
    age = max(1, current_year - first_year + 1)
    return h_index(cites) / age


def read_publications(path):
    """CSV with at least 'citations'; optional 'year', 'title', 'venue', 'first_author' (yes/no)."""
    pubs = []
    with open(path, encoding="utf-8-sig", newline="") as fh:
        for i, r in enumerate(csv.DictReader(fh), start=2):
            try:
                c = int(float((r.get("citations") or r.get("cited_by") or "0").strip() or 0))
            except ValueError:
                raise ValueError("row %d: citations must be a number" % i)
            year = (r.get("year") or "").strip()
            pubs.append({"title": (r.get("title") or "").strip(), "year": int(year) if year.isdigit() else None,
                         "venue": (r.get("venue") or r.get("journal") or "").strip(), "citations": c,
                         "first_author": (r.get("first_author") or "").strip().lower() in ("yes", "y", "1", "true", "x")})
    return pubs


def summary(pubs, current_year, window=5):
    cites = [p["citations"] for p in pubs]
    years = [p["year"] for p in pubs if p["year"]]
    recent = [p["citations"] for p in pubs if p["year"] and p["year"] > current_year - window]
    res = {"papers": len(pubs), "citations": sum(cites), "h": h_index(cites), "g": g_index(cites),
           "i10": i10_index(cites), "e": round(e_index(cites), 2),
           "mean": round(statistics.fmean(cites), 2) if cites else 0, "median": statistics.median(cites) if cites else 0,
           "uncited": sum(1 for c in cites if c == 0), "h_recent_%dy" % window: h_index(recent)}
    if years:
        res["first_year"] = min(years)
        res["m"] = round(m_quotient(cites, min(years), current_year), 2)
        per_year = {}
        for p in pubs:
            if p["year"]:
                per_year.setdefault(p["year"], [0, 0])
                per_year[p["year"]][0] += 1
                per_year[p["year"]][1] += p["citations"]
        res["by_year"] = {y: {"papers": v[0], "citations": v[1]} for y, v in sorted(per_year.items())}
    fa = [p["citations"] for p in pubs if p["first_author"]]
    if fa:
        res["h_first_author"] = h_index(fa)
    res["top"] = sorted(pubs, key=lambda p: -p["citations"])[:5]
    return res
