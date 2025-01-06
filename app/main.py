import numpy as np
import pandas as pd
from tqdm import tqdm


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
    df["S"] = df["Str"] - df["Res"]
    return df


def triangle_finder(matchups: pd.DataFrame):
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

    Parameters:
    ----------
    matchups : pd.DataFrame
        A DataFrame containing type interaction data with columns:
        - 'Type1', 'Type2': Types involved in the interaction.
        - 'Res1', 'Res2': Resistance values for dual types.
        - 'Str1', 'Str2': Strength values for dual types.

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing all valid type triangles with columns:
        ['Type1', 'Type2', 'Type3', 'Res Big', 'Res Small', 'Str Big', 'Str Small'].
    """
    df = matchups.copy()
    df['ResB'] = df[['Res1', 'Res2']].min(axis=1)
    df['ResS'] = df[['Res1', 'Res2']].max(axis=1)
    df['StrB'] = df[['Str1', 'Str2']].max(axis=1)
    df['StrS'] = df[['Str1', 'Str2']].min(axis=1)

    df = df[~(
            (df['ResB'] == 1) &
            (df['ResS'] == 1) &
            (df['StrB'] == 1) &
            (df['StrS'] == 1)
    )]

    types = df['Type1'].unique()
    triangles = []
    tri_df = []
    for cur_type in tqdm(types, total=len(types)):
        cur = df[(df['Type1'] == cur_type) & (df['Type2'] != cur_type)]
        for i, next_row in cur.iterrows():
            next = df[
                (df['Type2'] != cur_type) &
                (df['Type1'] == next_row['Type2']) &
                (df['ResB'] == next_row['ResB']) &
                (df['ResS'] == next_row['ResS']) &
                (df['StrB'] == next_row['StrB']) &
                (df['StrS'] == next_row['StrS'])
                ]
            for j, last_row in next.iterrows():
                if (next_row['Type2'] == last_row['Type2']) or (last_row['Type2'] == cur_type): continue
                last = df[
                    (df['Type1'] == last_row['Type2']) &
                    (df['Type2'] == cur_type) &
                    (df['ResB'] == next_row['ResB']) &
                    (df['ResS'] == next_row['ResS']) &
                    (df['StrB'] == next_row['StrB']) &
                    (df['StrS'] == next_row['StrS'])
                    ]
                if not last.empty:
                    new_triangle = {cur_type, next_row['Type2'], last_row['Type2'], next_row['ResB'], next_row['ResS'],
                                    next_row['StrB'], next_row['StrS']}
                    if new_triangle not in triangles:
                        triangles.append(new_triangle)
                        tri_df.append(
                            [cur_type, next_row['Type2'], last_row['Type2'], next_row['ResB'], next_row['ResS'],
                             next_row['StrB'], next_row['StrS']])

        df = df[(df['Type1'] != cur_type) & (df['Type2'] != cur_type)]
    tri_df = pd.DataFrame(columns=['1', '2', '3', 'Res Big', 'Res Small', 'Str Big', 'Str Small'], data=tri_df)
    return tri_df


def best_counter(group: pd.DataFrame, overall: dict) -> None:
    """Updates the 'overall' dict with the values of how well a type counters other types"""
    group["rank"] = group["S"].rank(pct=True)
    for _, row in group.iterrows():
        so_far = overall.get(row["Type1"], [0, 0])
        so_far[0] += row["rank"]
        so_far[1] += 1
        overall[row["Type1"]] = so_far


def team_of_six(matchups: pd.DataFrame) -> list[str]:
    df = matchups[matchups["Str"] >= 2].copy()
    df['1'] = df['Type1'].apply(lambda row: row.split("/")[0])
    df['2'] = df['Type1'].apply(lambda row: row.split("/")[-1])

    found = []
    while len(found) < 6:
        overall = {}
        df.groupby("Type2").apply(lambda group: best_counter(group, overall), include_groups=False)
        scores = pd.DataFrame(overall).T
        #print(scores.sort_values(0, ascending=False).head(10))
        next_best = scores[0].idxmax()
        found.append(next_best)
        #for p_type in next_best.split("/"):
        #    df = df[(df["1"] != p_type) & (df["2"] != p_type)]
        types_already_countered = df[(df["Type1"] == next_best) & (df["S"] >= 1)]["Type2"].unique()
        df = df[~df["Type2"].isin(types_already_countered)]
    return found


def check_team(chart: pd.DataFrame, team: list[str]) -> None:
    left = chart.copy()
    for poke in team:
        for p_type in poke.split("/"):
            a = left.loc[p_type, :]
            left = left[a[(a < 2)].index]
        if len(left.columns) <= 0:
            print("Effective against all types")
            return
    print(f"Warning - team is not effective against {left.columns}")


def find_best_counter(poke: str, team: list[str], matchups: pd.DataFrame) -> pd.DataFrame:
    if poke not in matchups["Type2"].unique():
        poke = poke.split("/")
        poke = "/".join([poke[-1], poke[0]])
    return matchups[(matchups["Type2"]==poke) & (matchups["Type1"].isin(team))].sort_values("S", ascending=False)


def create_charts():
    chart = initialise_chart()
    chart = expand_chart(chart)
    chart.to_csv("chart.csv")

    matchups = matchup_generator(chart)
    matchups.to_csv("matchups.csv", index=False)

    return chart, matchups


def main():
    chart = pd.read_csv("chart.csv", index_col=0)
    matchups = pd.read_csv("matchups.csv")

    #triangles = triangle_finder(matchups)

    team = team_of_six(matchups)
    print(team)

    #team = ['fire/ground', 'rock/steel', 'fighting/dark', 'water/fairy', 'ice/flying', 'grass/ghost']

    check_team(chart, team)

    print(find_best_counter("electric/flying", team, matchups))

if __name__ == '__main__':
    main()
