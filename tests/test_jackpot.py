from jackpot import roll_dice, poss_moves, gen_ltr_images
import pytest


def test_roll_dice():
    r = roll_dice()
    assert type(r[0]) == int


@pytest.mark.parametrize(
    "input, expected",
    [((3, 4), [3, 4, 7]), ((2, 4), [2, 4, 6]), ((4, 6), [4, 6]), ((3, 6,), [3, 6, 9])],
)
def test_poss_moves(input, expected):
    assert poss_moves(input) == expected


def test_gen_letter_images():
    assert len(gen_ltr_images()) == 9
