import numpy as np
import pandas as pd
from pandas.core.common import not_none


def initialise_chart() -> pd.DataFrame:
    """
    Creates a 18x18 pandas DataFrame of Pokémon type effectiveness.
       chart.loc[atk_type, def_type] = multiplier
    """
    # Define an ordered list of types (Gen 6+).
    types = [
        "normal", "fire", "water", "electric", "grass", "ice", "fighting",
        "poison", "ground", "flying", "psychic", "bug", "rock", "ghost",
        "dragon", "dark", "steel", "fairy"
    ]

    # Create a DataFrame filled with 1.0 (neutral effectiveness).
    chart = pd.DataFrame(1.0, index=types, columns=types)

    # For readability, we'll just refer to them by name:
    # --- NORMAL attacking ---
    chart.loc["normal", "rock"]   = 0.5
    chart.loc["normal", "ghost"]  = 0.0
    chart.loc["normal", "steel"]  = 0.5

    # --- FIRE attacking ---
    chart.loc["fire", "fire"]     = 0.5
    chart.loc["fire", "water"]    = 0.5
    chart.loc["fire", "grass"]    = 2.0
    chart.loc["fire", "ice"]      = 2.0
    chart.loc["fire", "bug"]      = 2.0
    chart.loc["fire", "rock"]     = 0.5
    chart.loc["fire", "dragon"]   = 0.5
    chart.loc["fire", "steel"]    = 2.0

    # --- WATER attacking ---
    chart.loc["water", "fire"]    = 2.0
    chart.loc["water", "water"]   = 0.5
    chart.loc["water", "grass"]   = 0.5
    chart.loc["water", "ground"]  = 2.0
    chart.loc["water", "rock"]    = 2.0
    chart.loc["water", "dragon"]  = 0.5

    # --- ELECTRIC attacking ---
    chart.loc["electric", "water"]    = 2.0
    chart.loc["electric", "electric"] = 0.5
    chart.loc["electric", "grass"]    = 0.5
    chart.loc["electric", "ground"]   = 0.0
    chart.loc["electric", "flying"]   = 2.0
    chart.loc["electric", "dragon"]   = 0.5

    # --- GRASS attacking ---
    chart.loc["grass", "fire"]     = 0.5
    chart.loc["grass", "water"]    = 2.0
    chart.loc["grass", "grass"]    = 0.5
    chart.loc["grass", "poison"]   = 0.5
    chart.loc["grass", "ground"]   = 2.0
    chart.loc["grass", "flying"]   = 0.5
    chart.loc["grass", "bug"]      = 0.5
    chart.loc["grass", "rock"]     = 2.0
    chart.loc["grass", "dragon"]   = 0.5
    chart.loc["grass", "steel"]    = 0.5

    # --- ICE attacking ---
    chart.loc["ice", "fire"]     = 0.5
    chart.loc["ice", "water"]    = 0.5
    chart.loc["ice", "ice"]      = 0.5
    chart.loc["ice", "grass"]    = 2.0
    chart.loc["ice", "ground"]   = 2.0
    chart.loc["ice", "flying"]   = 2.0
    chart.loc["ice", "dragon"]   = 2.0
    chart.loc["ice", "steel"]    = 0.5

    # --- FIGHTING attacking ---
    chart.loc["fighting", "normal"]  = 2.0
    chart.loc["fighting", "ice"]     = 2.0
    chart.loc["fighting", "poison"]  = 0.5
    chart.loc["fighting", "flying"]  = 0.5
    chart.loc["fighting", "psychic"] = 0.5
    chart.loc["fighting", "bug"]     = 0.5
    chart.loc["fighting", "rock"]    = 2.0
    chart.loc["fighting", "ghost"]   = 0.0
    chart.loc["fighting", "dark"]    = 2.0
    chart.loc["fighting", "steel"]   = 2.0
    chart.loc["fighting", "fairy"]   = 0.5

    # --- POISON attacking ---
    chart.loc["poison", "grass"]  = 2.0
    chart.loc["poison", "poison"] = 0.5
    chart.loc["poison", "ground"] = 0.5
    chart.loc["poison", "rock"]   = 0.5
    chart.loc["poison", "ghost"]  = 0.5
    chart.loc["poison", "steel"]  = 0.0
    chart.loc["poison", "fairy"]  = 2.0

    # --- GROUND attacking ---
    chart.loc["ground", "fire"]     = 2.0
    chart.loc["ground", "electric"] = 2.0
    chart.loc["ground", "grass"]    = 0.5
    chart.loc["ground", "poison"]   = 2.0
    chart.loc["ground", "flying"]   = 0.0
    chart.loc["ground", "bug"]      = 0.5
    chart.loc["ground", "rock"]     = 2.0
    chart.loc["ground", "steel"]    = 2.0

    # --- FLYING attacking ---
    chart.loc["flying", "electric"] = 0.5
    chart.loc["flying", "grass"]    = 2.0
    chart.loc["flying", "fighting"] = 2.0
    chart.loc["flying", "bug"]      = 2.0
    chart.loc["flying", "rock"]     = 0.5
    chart.loc["flying", "steel"]    = 0.5

    # --- PSYCHIC attacking ---
    chart.loc["psychic", "fighting"] = 2.0
    chart.loc["psychic", "poison"]   = 2.0
    chart.loc["psychic", "psychic"]  = 0.5
    chart.loc["psychic", "dark"]     = 0.0
    chart.loc["psychic", "steel"]    = 0.5

    # --- BUG attacking ---
    chart.loc["bug", "fire"]     = 0.5
    chart.loc["bug", "grass"]    = 2.0
    chart.loc["bug", "fighting"] = 0.5
    chart.loc["bug", "poison"]   = 0.5
    chart.loc["bug", "flying"]   = 0.5
    chart.loc["bug", "psychic"]  = 2.0
    chart.loc["bug", "ghost"]    = 0.5
    chart.loc["bug", "dark"]     = 2.0
    chart.loc["bug", "steel"]    = 0.5
    chart.loc["bug", "fairy"]    = 0.5

    # --- ROCK attacking ---
    chart.loc["rock", "fire"]     = 2.0
    chart.loc["rock", "ice"]      = 2.0
    chart.loc["rock", "flying"]   = 2.0
    chart.loc["rock", "bug"]      = 2.0
    chart.loc["rock", "fighting"] = 0.5
    chart.loc["rock", "ground"]   = 0.5
    chart.loc["rock", "steel"]    = 0.5

    # --- GHOST attacking ---
    chart.loc["ghost", "normal"]  = 0.0
    chart.loc["ghost", "psychic"] = 2.0
    chart.loc["ghost", "ghost"]   = 2.0
    chart.loc["ghost", "dark"]    = 0.5

    # --- DRAGON attacking ---
    chart.loc["dragon", "dragon"] = 2.0
    chart.loc["dragon", "steel"]  = 0.5
    chart.loc["dragon", "fairy"]  = 0.0

    # --- DARK attacking ---
    chart.loc["dark", "fighting"] = 0.5
    chart.loc["dark", "dark"]     = 0.5
    chart.loc["dark", "ghost"]    = 2.0
    chart.loc["dark", "psychic"]  = 2.0
    chart.loc["dark", "fairy"]    = 0.5

    # --- STEEL attacking ---
    chart.loc["steel", "fire"]     = 0.5
    chart.loc["steel", "water"]    = 0.5
    chart.loc["steel", "electric"] = 0.5
    chart.loc["steel", "ice"]      = 2.0
    chart.loc["steel", "rock"]     = 2.0
    chart.loc["steel", "steel"]    = 0.5
    chart.loc["steel", "fairy"]    = 2.0

    # --- FAIRY attacking ---
    chart.loc["fairy", "fire"]     = 0.5
    chart.loc["fairy", "fighting"] = 2.0
    chart.loc["fairy", "poison"]   = 0.5
    chart.loc["fairy", "dragon"]   = 2.0
    chart.loc["fairy", "dark"]     = 2.0
    chart.loc["fairy", "steel"]    = 0.5

    return chart


def expand_chart(chart: pd.DataFrame) -> pd.DataFrame:
    """
    Adds double types to the chart.
    """
    types = chart.columns
    new_cols = dict()

    for i, type1 in enumerate(types[:-1]):
        for j, type2 in enumerate(types[i+1:]):
            new_cols[f"{type1}/{type2}"] = chart[type1] * chart[type2]

    new_df = pd.DataFrame.from_dict(new_cols)
    return pd.concat([chart, new_df], axis=1)


def find_matching(input_types: list[str], adv: pd.DataFrame):
    """
    Finds in order the next types needed to be able to be super effective against the most types
    """
    current = adv.copy()
    types = input_types.copy()

    for next_type in types:
        beaten_types = list(current.loc[next_type, current.loc[next_type] == True].index)
        current.drop(beaten_types, axis=1, inplace=True)

    print(f"Remaining types not yet effective against: {current.shape[1]}")

    while not current.empty:
        next_type = current.sum(axis=1).idxmax()
        types.append(next_type)
        print(f"Next best type: {next_type}")
        beaten_types = list(current.loc[next_type, current.loc[next_type] == True].index)
        current.drop(beaten_types, axis=1, inplace=True)
        print(f"Remaining types not yet effective against: {current.shape[1]}")

    print(types)


def matchup_generator(chart: pd.DataFrame) -> pd.DataFrame:
    """
    Generates the matchups between all the different types in the form of a dataframe with columns
    Type1, Type2, Res1, Res2, Str1, Str2, Res, Str

    Where
    - Resi is the resistance of Type1 to the ith type in Type2
    - Stri is the strength of the ith type in Type1 against Type2
    """
    types = list(chart.columns)
    rows = []
    for i, type1 in enumerate(types):
        for j, type2 in enumerate(types):
            resist = [np.nan, np.nan]
            strength = [np.nan, np.nan]

            types_in_one = type1.split("/")
            types_in_two = type2.split("/")

            for t, two_type in enumerate(types_in_two):
                resist[t] = chart.loc[two_type, type1]

            for t, one_type in enumerate(types_in_one):
                strength[t] = chart.loc[one_type, type2]

            new_row = [type1, type2] + resist + strength
            rows.append(new_row)

    df = pd.DataFrame(columns=["Type1", "Type2", "Res1", "Res2", "Str1", "Str2"], data=rows)
    df['Res'] = df[['Res1', 'Res2']].max(axis=1)
    df['Str'] = df[['Str1', 'Str2']].max(axis=1)
    return df


def teams_of_six(chart: pd.DataFrame):
    """
    Generates the different teams of 6 from the different types you could have that cover all types
    """
    pass


def triangle_finder(chart: pd.DataFrame):
    """
    Finds all the perfect type triangles such that each type has the same effectiveness against the next type, and
    same resistance to the previous type
    e.g.
    - Type A -> x4 -> Type B -> x4 -> Type C -> x4 -> Type A
    - Type A -> x0 -> Type C -> x0 -> Type B -> x0 -> Type A

    For dual types - this must be true for both of their types
    e.g.
    - A/B, C/D, E/F
    - (A -> x2 -> C/D) & (B -> x2 -> C/D)
    """
    

def main():
    chart = initialise_chart()
    chart = expand_chart(chart)

    chart.to_csv("chart.csv")


    adv = (chart > 1)
    dis = (chart < 1)
    # Sum across the columns to find how many advantages they have
    strong_against = adv.sum(axis=1).sort_values(ascending=False)
    # Sum across the rows to find how many resistances they have
    resistant_to = dis.sum(axis=0).sort_values(ascending=False)

    # Sums up how effective things are against it - giving types that are overall the most resistant
    general_resistance = chart.sum(axis=0).sort_values()
    #print(general_resistance)

    find_matching([], adv)


if __name__ == '__main__':
    main()
