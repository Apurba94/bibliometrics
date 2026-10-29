"""Command-line interface for bibliometrics."""
import argparse
import datetime as dt
import json

from .core import read_publications, summary


def main(argv=None):
    ap = argparse.ArgumentParser(prog="bibliometrics", description="Citation indicators from a publications CSV.")
    ap.add_argument("csvfile", help="columns: title, year, venue, citations, first_author")
    ap.add_argument("--year", type=int, default=dt.date.today().year, help="current year for m-quotient")
    ap.add_argument("--window", type=int, default=5, help="years for the recent h-index")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        pubs = read_publications(args.csvfile)
    except ValueError as exc:
        print("error: %s" % exc)
        return 1
    s = summary(pubs, args.year, args.window)
    if args.json:
        print(json.dumps(s, indent=2, default=str))
        return 0
    print("%d papers, %d citations (mean %.1f, median %g, %d uncited)" % (s["papers"], s["citations"], s["mean"],
                                                                       s["median"], s["uncited"]))
    print("h-index %d | g-index %d | i10 %d | e-index %.1f | h (last %dy) %d%s%s" % (
        s["h"], s["g"], s["i10"], s["e"], args.window, s["h_recent_%dy" % args.window],
        " | m %.2f (since %d)" % (s["m"], s["first_year"]) if "m" in s else "",
        " | h first-author %d" % s["h_first_author"] if "h_first_author" in s else ""))
    if "by_year" in s:
        print("\nyear  papers citations")
        for y, v in s["by_year"].items():
            print("%d  %6d %9d %s" % (y, v["papers"], v["citations"], "#" * min(60, v["citations"] // 10)))
    print("\nMost cited:")
    for p in s["top"]:
        print("  %5d  %s (%s)" % (p["citations"], p["title"][:70], p["year"] or "-"))
    print("\nIndicators depend on the citation database used; never compare across fields or career stages naively.")
    return 0
