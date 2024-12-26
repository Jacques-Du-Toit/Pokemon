import numpy as np


def initialise_chart() -> np.ndarray:
    """Creates a 2D matrix (18x18) of Pokémon type effectiveness.
       chart[atk][def] = multiplier
    """
    # Create an 18x18 matrix of 1.0 (neutral effectiveness).
    chart = np.ones((18, 18), dtype=float)

    # Define indices for each type for readability:
    normal   = 0
    fire     = 1
    water    = 2
    electric = 3
    grass    = 4
    ice      = 5
    fighting = 6
    poison   = 7
    ground   = 8
    flying   = 9
    psychic  = 10
    bug      = 11
    rock     = 12
    ghost    = 13
    dragon   = 14
    dark     = 15
    steel    = 16
    fairy    = 17

    # --- NORMAL attacking ---
    chart[normal][rock]  = 0.5
    chart[normal][ghost] = 0.0
    chart[normal][steel] = 0.5

    # --- FIRE attacking ---
    chart[fire][fire]    = 0.5
    chart[fire][water]   = 0.5
    chart[fire][grass]   = 2.0
    chart[fire][ice]     = 2.0
    chart[fire][bug]     = 2.0
    chart[fire][rock]    = 0.5
    chart[fire][dragon]  = 0.5
    chart[fire][steel]   = 2.0

    # --- WATER attacking ---
    chart[water][fire]   = 2.0
    chart[water][water]  = 0.5
    chart[water][grass]  = 0.5
    chart[water][ground] = 2.0
    chart[water][rock]   = 2.0
    chart[water][dragon] = 0.5

    # --- ELECTRIC attacking ---
    chart[electric][water]   = 2.0
    chart[electric][electric] = 0.5
    chart[electric][grass]   = 0.5
    chart[electric][ground]  = 0.0
    chart[electric][flying]  = 2.0
    chart[electric][dragon]  = 0.5

    # --- GRASS attacking ---
    chart[grass][fire]    = 0.5
    chart[grass][water]   = 2.0
    chart[grass][grass]   = 0.5
    chart[grass][poison]  = 0.5
    chart[grass][ground]  = 2.0
    chart[grass][flying]  = 0.5
    chart[grass][bug]     = 0.5
    chart[grass][rock]    = 2.0
    chart[grass][dragon]  = 0.5
    chart[grass][steel]   = 0.5

    # --- ICE attacking ---
    chart[ice][fire]     = 0.5
    chart[ice][water]    = 0.5
    chart[ice][ice]      = 0.5
    chart[ice][grass]    = 2.0
    chart[ice][ground]   = 2.0
    chart[ice][flying]   = 2.0
    chart[ice][dragon]   = 2.0
    chart[ice][steel]    = 0.5
    # (Rock, Fighting, etc. stay at 1.0 by default)

    # --- FIGHTING attacking ---
    chart[fighting][normal]  = 2.0
    chart[fighting][ice]     = 2.0
    chart[fighting][poison]  = 0.5
    chart[fighting][flying]  = 0.5
    chart[fighting][psychic] = 0.5
    chart[fighting][bug]     = 0.5
    chart[fighting][rock]    = 2.0
    chart[fighting][ghost]   = 0.0
    chart[fighting][dark]    = 2.0
    chart[fighting][steel]   = 2.0
    chart[fighting][fairy]   = 0.5

    # --- POISON attacking ---
    chart[poison][grass]  = 2.0
    chart[poison][poison] = 0.5
    chart[poison][ground] = 0.5
    chart[poison][rock]   = 0.5
    chart[poison][ghost]  = 0.5
    chart[poison][steel]  = 0.0
    chart[poison][fairy]  = 2.0

    # --- GROUND attacking ---
    chart[ground][fire]    = 2.0
    chart[ground][electric] = 2.0
    chart[ground][grass]   = 0.5
    chart[ground][poison]  = 2.0
    chart[ground][flying]  = 0.0
    chart[ground][bug]     = 0.5
    chart[ground][rock]    = 2.0
    chart[ground][steel]   = 2.0

    # --- FLYING attacking ---
    chart[flying][electric] = 0.5
    chart[flying][grass]    = 2.0
    chart[flying][fighting] = 2.0
    chart[flying][bug]      = 2.0
    chart[flying][rock]     = 0.5
    chart[flying][steel]    = 0.5

    # --- PSYCHIC attacking ---
    chart[psychic][fighting] = 2.0
    chart[psychic][poison]   = 2.0
    chart[psychic][psychic]  = 0.5
    chart[psychic][dark]     = 0.0
    chart[psychic][steel]    = 0.5

    # --- BUG attacking ---
    chart[bug][fire]     = 0.5
    chart[bug][grass]    = 2.0
    chart[bug][fighting] = 0.5
    chart[bug][poison]   = 0.5
    chart[bug][flying]   = 0.5
    chart[bug][psychic]  = 2.0
    chart[bug][ghost]    = 0.5
    chart[bug][dark]     = 2.0
    chart[bug][steel]    = 0.5
    chart[bug][fairy]    = 0.5

    # --- ROCK attacking ---
    chart[rock][fire]    = 2.0
    chart[rock][ice]     = 2.0
    chart[rock][flying]  = 2.0
    chart[rock][bug]     = 2.0
    chart[rock][fighting] = 0.5
    chart[rock][ground]  = 0.5
    chart[rock][steel]   = 0.5

    # --- GHOST attacking ---
    chart[ghost][normal]  = 0.0
    chart[ghost][psychic] = 2.0
    chart[ghost][ghost]   = 2.0
    chart[ghost][dark]    = 0.5

    # --- DRAGON attacking ---
    chart[dragon][dragon] = 2.0
    chart[dragon][steel]  = 0.5
    chart[dragon][fairy]  = 0.0

    # --- DARK attacking ---
    chart[dark][fighting] = 0.5
    chart[dark][dark]     = 0.5
    chart[dark][ghost]    = 2.0
    chart[dark][psychic]  = 2.0
    chart[dark][fairy]    = 0.5

    # --- STEEL attacking ---
    chart[steel][fire]    = 0.5
    chart[steel][water]   = 0.5
    chart[steel][electric] = 0.5
    chart[steel][ice]     = 2.0
    chart[steel][rock]    = 2.0
    chart[steel][steel]   = 0.5
    chart[steel][fairy]   = 2.0

    # --- FAIRY attacking ---
    chart[fairy][fire]    = 0.5
    chart[fairy][fighting] = 2.0
    chart[fairy][poison]  = 0.5
    chart[fairy][dragon]  = 2.0
    chart[fairy][dark]    = 2.0
    chart[fairy][steel]   = 0.5

    return chart


