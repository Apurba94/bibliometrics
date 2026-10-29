# bibliometrics

**Compute h-index, g-index, i10-index, e-index, m-quotient, recent and first-author h-index, and
citations per year from a simple publications CSV, transparently and offline.**

Part of the *Research Automation Toolkit*: 100 open tools for daily research work.

## Why

Grant, promotion and fellowship applications ask for citation indicators, and different databases
(Google Scholar, Scopus, Web of Science) give different numbers. Computing them yourself from an exported
list makes clear which database and which papers were used, lets you report field-appropriate variants
(recent h-index, first-author h-index), and documents the definitions.

## Indicators

| Indicator | Definition |
|-----------|------------|
| h-index | largest h with h papers cited at least h times (Hirsch, 2005) |
| g-index | largest g with the top g papers cited at least g^2 times in total (Egghe, 2006) |
| i10-index | papers with at least 10 citations |
| e-index | sqrt of excess citations in the h-core (Zhang, 2009) |
| m-quotient | h / years since first publication |
| recent h | h-index of papers from the last N years |

## Usage

```bash
pip install .
bibliometrics my_publications.csv --year 2026
bibliometrics scopus_export.csv --window 10 --json
```

CSV columns: `citations` (or `cited_by`), optional `title`, `year`, `venue`/`journal`, `first_author`.

Indicators summarize citation counts, not research quality; follow the DORA and Leiden Manifesto
recommendations when using them.

## Testing

```bash
python -m unittest discover -s tests -t .
```

## License

MIT (c) JANIN A APURBA
