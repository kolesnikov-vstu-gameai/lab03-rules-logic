"""База знаний стражника. Предикаты: (sees, guard, player), (hears, guard, noise), (at, guard, zone),
(state, guard, s), (alarm,), (light_on, zone), (door_open, zone) ..."""

from .engine import Engine, Rule


def has(facts, *pat):
    return tuple(pat) in facts


def set_state(facts, guard, new):
    for f in [f for f in facts if f[0] == "state" and f[1] == guard]:
        facts.discard(f)
    facts.add(("state", guard, new))


def build(guards=("g1", "g2")) -> Engine:
    e = Engine()
    for g in guards:
        e.assert_fact("state", g, "patrol")
        e.add(Rule(f"see_player_{g}", lambda f, g=g: has(f, "sees", g, "player") and not has(f, "state", g, "chase"),
                   lambda f, g=g: set_state(f, g, "chase"), priority=10))
        e.add(Rule(f"hear_noise_{g}", lambda f, g=g: has(f, "hears", g, "noise") and has(f, "state", g, "patrol"),
                   lambda f, g=g: set_state(f, g, "investigate"), priority=5))
        e.add(Rule(f"raise_alarm_{g}", lambda f, g=g: has(f, "state", g, "chase") and not has(f, "alarm"),
                   lambda f: f.add(("alarm",)), priority=8))
        e.add(Rule(f"alarm_join_{g}", lambda f, g=g: has(f, "alarm") and has(f, "state", g, "patrol"),
                   lambda f, g=g: set_state(f, g, "search"), priority=7))
    # TODO: добавьте правила до 10+: освещение, двери, потеря цели, возврат на пост, память о последней позиции
    return e
