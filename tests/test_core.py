import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from bibliometrics.cli import main
from bibliometrics.core import e_index, g_index, h_index, i10_index, m_quotient, read_publications, summary


class IndexTests(unittest.TestCase):
    def test_h(self):
        self.assertEqual(h_index([10, 8, 5, 4, 3]), 4)
        self.assertEqual(h_index([25, 8, 5, 3, 3]), 3)
        self.assertEqual(h_index([0, 0]), 0)
        self.assertEqual(h_index([]), 0)
        self.assertEqual(h_index([100]), 1)

    def test_g(self):
        self.assertEqual(g_index([10, 8, 5, 4, 3]), 5)       # 30 >= 25
        self.assertEqual(g_index([3, 0, 0]), 1)
        self.assertEqual(g_index([25, 8, 5, 3, 3]), 5)       # 44 >= 25

    def test_i10_e_m(self):
        self.assertEqual(i10_index([10, 9, 50]), 2)
        self.assertAlmostEqual(e_index([10, 8, 5, 4, 3]), (27 - 16) ** 0.5)
        self.assertAlmostEqual(m_quotient([10, 8, 5, 4, 3], 2017, 2026), 0.4)


class SummaryTests(unittest.TestCase):
    CSV = ("title,year,venue,citations,first_author\nA,2018,J1,40,yes\nB,2020,J2,12,no\nC,2024,J1,3,yes\n"
           "D,2025,J3,0,no\nE,2025,J3,5,yes\n")

    def test_summary_and_cli(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "pubs.csv")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(self.CSV)
            pubs = read_publications(p)
            s = summary(pubs, 2026, window=5)
            self.assertEqual((s["papers"], s["citations"], s["h"], s["i10"], s["uncited"]), (5, 60, 3, 2, 1))
            self.assertEqual(s["h_recent_5y"], 2)          # 2022-2026: [3, 0, 5]
            self.assertEqual(s["h_first_author"], 3)
            self.assertEqual(s["by_year"][2025], {"papers": 2, "citations": 5})
            self.assertEqual(s["top"][0]["title"], "A")
            with redirect_stdout(io.StringIO()) as buf:
                main([p, "--year", "2026"])
            self.assertIn("h-index 3 | g-index 5 | i10 2", buf.getvalue())

    def test_bad_csv(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "bad.csv")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write("title,citations\nA,many\n")
            with self.assertRaises(ValueError):
                read_publications(p)


if __name__ == "__main__":
    unittest.main()
