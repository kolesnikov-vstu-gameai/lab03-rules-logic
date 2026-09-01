"""Вариант C: вызов SWI-Prolog через pyswip. Требует установленный swipl."""

from pathlib import Path

KB = Path(__file__).resolve().parents[3] / "prolog" / "guard.pl"


def query_state(guard: str) -> list[str]:
    from pyswip import Prolog

    p = Prolog()
    p.consult(str(KB))
    return [r["S"] for r in p.query(f"next_state({guard}, S)")]
