"""Citation indicators (h, g, i10, m-quotient, e-index) from a publications list."""
from .core import h_index, g_index, i10_index, e_index, m_quotient, summary, read_publications

__version__ = "0.1.0"
__all__ = ["h_index", "g_index", "i10_index", "e_index", "m_quotient", "summary", "read_publications"]
