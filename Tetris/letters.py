from arcade import color
from random import choice

# T betű.
letter_T = {
    1: [[1, 1, 1],
        [0, 1, 0]],

    2: [[0, 0, 1],
        [0, 1, 1],
        [0, 0, 1]],

    3: [[0, 0, 0],
        [0, 1, 0],
        [1, 1, 1]],

    4: [[1, 0],
        [1, 1],
        [1, 0]],

    "color": color.RED,
    "num_rotations": 4,
    "settled_letter": 11
}

# I betű.
letter_I = {
    1: [[0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0]],

    2: [[0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0]],

    "color": color.BLUE,
    "num_rotations": 2,
    "settled_letter": 12
}

# O betű.
letter_O = {
    1: [[1, 1],
        [1, 1]],

    "color": color.GREEN,
    "num_rotations": 1,
    "settled_letter": 13
}

# Z betű.
letter_Z = {
    1: [[1, 1, 0],
        [0, 1, 1]],

    2: [[0, 0, 1],
        [0, 1, 1],
        [0, 1, 0]],

    "color": color.JASMINE,
    "num_rotations": 2,
    "settled_letter": 14
}

# S betű.
letter_S = {
    1: [[0, 1, 1],
        [1, 1, 0]],

    2: [[1, 0, 0],
        [1, 1, 0],
        [0, 1, 0]],

    "color": color.AFRICAN_VIOLET,
    "num_rotations": 2,
    "settled_letter": 15
}

# L betű.
letter_L = {
    1: [[0, 1, 0],
        [0, 1, 0],
        [0, 1, 1]],

    2: [[0, 0, 0],
        [1, 1, 1],
        [1, 0, 0]],

    3: [[1, 1, 0],
        [0, 1, 0],
        [0, 1, 0]],

    4: [[0, 0, 1],
        [1, 1, 1],
        [0, 0, 0]],

    "color": color.ALLOY_ORANGE,
    "num_rotations": 4,
    "settled_letter": 16
}

# J betű.
letter_J = {
    1: [[0, 1, 0],
        [0, 1, 0],
        [1, 1, 0]],

    2: [[1, 0, 0],
        [1, 1, 1],
        [0, 0, 0]],

    3: [[0, 1, 1],
        [0, 1, 0],
        [0, 1, 0]],

    4: [[0, 0, 0],
        [1, 1, 1],
        [0, 0, 1]],

    "color": color.AMETHYST,
    "num_rotations": 4,
    "settled_letter": 17
}

all_letters = [letter_T, letter_I, letter_O, letter_Z, letter_S, letter_L, letter_J]


# Véletlenszerűen visszaad egy betűt az all_letters listából.
def choose_random_letter():
    return choice(all_letters)
