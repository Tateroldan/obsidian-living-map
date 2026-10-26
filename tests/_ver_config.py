"""Imprime la bóveda que resuelve config.py (lo usa test_validar_config en un proceso aparte)."""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import BOVEDA  # noqa: E402

print(BOVEDA)
