from jackpot import roll_dice


def test_roll_dice():
    r = roll_dice()
    assert type(r) == tuple
