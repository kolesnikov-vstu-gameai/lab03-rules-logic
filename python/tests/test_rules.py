from rules.guard_rules import build


def test_see_player_triggers_chase_and_alarm():
    e = build()
    e.assert_fact("sees", "g1", "player")
    fired = e.run()
    assert ("state", "g1", "chase") in e.facts
    assert ("alarm",) in e.facts
    assert ("state", "g2", "search") in e.facts
    assert "see_player_g1" in fired
