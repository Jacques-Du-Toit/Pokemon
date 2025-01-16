import numpy as np
import pandas as pd
from tqdm import tqdm
from tabulate import tabulate


def dmg_calc(atk: float, defs: float, type_mult: float) -> float:
    return ((84 * atk / defs) + 2) * 1.5 * type_mult


def one_vs_one(poke1: pd.Series, poke2: pd.Series, chart: pd.DataFrame) -> float:
    """
    Returns a score that shows how much faster one pokemon would beat the other

    > 0 -> pokemon 1 wins
    < 0 -> pokemon 2 wins
    = 0 0> draw
    """
    t1 = poke1['Types'].split('/')
    t1_mult = max(
        chart.loc[t1[0], poke2['Types'].replace(' ', '/')],
        chart.loc[t1[-1], poke2['Types'].replace(' ', '/')]
    )
    dmg1 = dmg_calc(poke1['ATK'], poke2[poke1['ATK.T']], t1_mult)

    t2 = poke2['Types'].split('/')
    t2_mult = max(
        chart.loc[t2[0], poke1['Types']],
        chart.loc[t2[-1], poke1['Types']]
    )
    dmg2 = dmg_calc(poke2['ATK'], poke1[poke2['ATK.T']], t2_mult)

    hits_to_kill_2 = int((poke2['HP'] / dmg1) + 1) if dmg1 != 0 else 5
    hits_to_kill_1 = int((poke1['HP'] / dmg2) + 1) if dmg2 != 0 else 5

    if poke1['Speed'] > poke2['Speed']:
        hits_to_kill_1 += 1
    elif poke1['Speed'] < poke2['Speed']:
        hits_to_kill_2 += 1

    return (hits_to_kill_1 - hits_to_kill_2) / min(hits_to_kill_1, hits_to_kill_2)


def battle_pokemon(pokedex: pd.DataFrame):
    df = pokedex[['Name', 'Form', 'Types', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Total']].copy()
    chart = pd.read_csv('resources/type_charts/chart.csv', index_col=0)

    df = df[(df['Form']!='Mega')&(df['Total'].notnull())]

    df['Types'] = df['Types'].str.lower().str.replace(' ', '/')
    wrong_order_types = [t for t in df['Types'].unique() if t not in chart.columns]
    for typ in wrong_order_types:
        df.loc[df['Types'] == typ, 'Types'] = '/'.join(typ.split('/')[::-1])

    df.drop_duplicates(inplace=True)

    df['ATK'] = df[['Attack', 'Sp. Atk']].max(axis=1)
    df['ATK.T'] = df[['Attack', 'Sp. Atk']].idxmax(axis=1).replace('Attack', 'Defense').replace('Atk', 'Def')

    df['Score'] = 0.0

    matchups = []
    for i, poke1 in tqdm(df.iloc[:-1].iterrows(), total=len(df)-1):
        for j, poke2 in df.iloc[i+1:].iterrows():
            score = one_vs_one(poke1, poke2, chart)
            df.loc[df['Name'] == poke1['Name'], 'Score'] += score
            df.loc[df['Name'] == poke2['Name'], 'Score'] -= score
            matchups.append([poke1['Name'], poke2['Name'], score])
            matchups.append([poke2['Name'], poke1['Name'], -score])

    matchups = pd.DataFrame(columns=['Name 1', 'Name 2', 'Score'], data=matchups)
    matchups.to_csv('resources/poke_matchups.csv', index=False)

    print(tabulate(df.sort_values(by=['Score'], ascending=False), headers='keys'))


def best_team(matchups: pd.DataFrame, team: list[str] = None, exclude: list[str] = None, min_score: int = 3) -> list[str]:
    df = matchups.copy()

    if not team:
        team = []
    if exclude:
        df = df[~df['Name 1'].isin(exclude)]

    # We only care about counters
    df = df[df['Score'] > 0]

    for poke in team:
        counters = df.loc[(df['Name 1'] == poke) & (df['Score'] >= min_score), 'Name 2'].unique()
        df = df[(df['Name 1'] != poke) & (~df['Name 2'].isin(counters))]

    while len(team) < 6:

        num_counters = df.loc[df['Score'] >= 2, 'Name 1'].value_counts()
        pokes_with_most = num_counters[num_counters == num_counters.max()]
        if len(pokes_with_most) == 1:
            next_best = pokes_with_most.index[0]
        else:
            next_best = df[df['Name 1'].isin(pokes_with_most.index)].groupby('Name 1')['Score'].mean().idxmax()

        team.append(next_best)

        counters = df.loc[(df['Name 1'] == next_best) & (df['Score'] >= min_score), 'Name 2'].unique()
        df = df[(df['Name 1'] != next_best) & (~df['Name 2'].isin(counters))]

    return team


def latest_evolution(pokemon: str, pokedex: pd.DataFrame) -> str:
    """Finds the latest evolution of the pokemon given."""
    evo_line = pokedex[pokedex['Name'] == pokemon].dropna(axis=1)
    if evo_line.empty:
        # TODO - Forms and variants need to be sorted out
        return pokemon

    latest_evo = [col for col in evo_line.columns if 'Evo' in col]
    if not latest_evo:
        # It doesn't evolve
        return pokemon
    else:
        return evo_line[latest_evo[-1]].iloc[0]


def eval_team(team: list[str], matchups: pd.DataFrame, pokedex: pd.DataFrame):
    """Returns what % of pokemon the team can beat, their median score and mean score, and the pokemon they lose to"""
    # We care about the team at it's strongest -> fully evolved
    evo_team = [latest_evolution(poke, pokedex) for poke in team]
    team_df = matchups[matchups['Name 1'].isin(evo_team)].copy()
    # What & of pokemon we can beat
    ratio_beats = team_df[team_df['Score'] > 0]['Name 2'].nunique() / matchups['Name 2'].nunique()
    # What pokemon we lose to
    loses_to = set(matchups['Name 2'].unique()) - set(team_df[team_df['Score'] > 0]['Name 2'].unique())
    return round(ratio_beats, 2), round(team_df['Score'].median(), 2), round(team_df['Score'].mean(), 2), ' '.join(loses_to)


def poke_replace(team: list[str], new_poke: str, matchups: pd.DataFrame, pokedex: pd.DataFrame) -> pd.DataFrame:
    """
    Evaluates replacing each Pokémon in the team with a new Pokémon
    and prints the changes in the ratio if it's an improvement.

    Parameters:
        team (list[str]): Current team of Pokémon.
        new_poke (str): The Pokémon to potentially add to the team.
        matchups (pd.DataFrame): DataFrame containing Pokémon matchups data.
        pokedex (pd.DataFrame): DataFrame containing Pokémon stats and info.

    Returns:
        None
    """
    # Evaluate the current team's performance
    ratio, median, mean, loses_to = eval_team(team, matchups, pokedex)

    data = [[None, ratio, median, mean, loses_to]]

    # Iterate over each Pokémon in the team
    for poke in team:
        # Create a new team by replacing the current Pokémon with the new Pokémon
        new_team = [p for p in team if p != poke] + [new_poke]

        # Evaluate the new team's performance
        ratio, median, mean, loses_to = eval_team(new_team, matchups, pokedex)

        data.append([poke, ratio, median, mean, loses_to])

    df = pd.DataFrame(
        columns=['Poke', 'Ratio', 'Median', 'Mean', 'Loses To'], data=data
    )
    return df.sort_values(by=['Ratio', 'Median', 'Mean'], ascending=False)


def display(df: pd.DataFrame) -> None:
    print(tabulate(df, headers='keys'))


def main():
    pokedex = pd.read_csv('resources/pokedexes/platinum_pokedex.csv')
    matchups = pd.read_csv('resources/poke_matchups.csv')

    display(poke_replace(['Turtwig', 'Bidoof', 'Starly', 'Zubat', 'Graveler', 'Psyduck'],
                 'shinx', matchups, pokedex))




if __name__ == "__main__":
    main()