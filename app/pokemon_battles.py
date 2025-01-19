import numpy as np
import pandas as pd
from tqdm import tqdm
from tabulate import tabulate
import os


def dmg_calc(atk: float, defs: float, type_mult: float) -> float:
    return ((44 * atk / defs) + 2) * 1.5 * type_mult


def turns_won_by(hits_to_kill_1: int, hits_to_kill_2: int, speed_1: int, speed_2: int) -> float:
    """Calculates the number of turns one pokemon would beat the other one by"""
    if (hits_to_kill_1 == hits_to_kill_2) and (speed_1 == speed_2):
        return 0

    hits_to_kill = [hits_to_kill_1, hits_to_kill_2]
    speed = [speed_1, speed_2]
    stronger_index = hits_to_kill.index(max(hits_to_kill))
    weaker_index = stronger_index - 1
    faster_index = speed.index(max(speed))

    if hits_to_kill_1 == hits_to_kill_2:
        hits_to_kill[faster_index] += 1
    elif speed[weaker_index] > speed[stronger_index]:
        pass
    elif speed[weaker_index] < speed[stronger_index]:
        hits_to_kill[stronger_index] += 1
    else:
        hits_to_kill[stronger_index] += 0.5

    return (hits_to_kill[0] - hits_to_kill[1]) / min(hits_to_kill)


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

    hits_to_kill_2 = int(((poke2['HP'] + 60) / dmg1) + 1) if dmg1 != 0 else np.inf
    hits_to_kill_1 = int(((poke1['HP'] + 60) / dmg2) + 1) if dmg2 != 0 else np.inf

    if (hits_to_kill_1 == np.inf) and (hits_to_kill_2 == np.inf):
        if poke1['Total'] > poke2['Total']:
            return 1
        elif poke1['Total'] < poke2['Total']:
            return -1
        else:
            return 0

    # Set them to take 3 turns longer to kill instead
    if hits_to_kill_2 == np.inf:
        hits_to_kill_2 = hits_to_kill_1 + 3
    elif hits_to_kill_1 == np.inf:
        hits_to_kill_1 = hits_to_kill_2 + 3

    return turns_won_by(hits_to_kill_1, hits_to_kill_2, poke1['Speed'], poke2['Speed'])


def battle_pokemon(pokedex: pd.DataFrame, path: str):
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
    df.reset_index(drop=True, inplace=True)

    matchups = []
    for i, poke1 in tqdm(df.iloc[:-1].iterrows(), total=len(df)-1):
        for j, poke2 in df.iloc[i+1:].iterrows():
            score = one_vs_one(poke1, poke2, chart)
            df.loc[df['Name'] == poke1['Name'], 'Score'] += score
            df.loc[df['Name'] == poke2['Name'], 'Score'] -= score
            matchups.append([poke1['Name'], poke2['Name'], score])
            matchups.append([poke2['Name'], poke1['Name'], -score])

    matchups = pd.DataFrame(columns=['Name 1', 'Name 2', 'Score'], data=matchups)
    matchups.to_csv(path, index=False)
    return matchups


def find_next_best(matchups: pd.DataFrame, min_score: int) -> str:
    """Returns the next best pokemon by adding scores of how uniquely good a pokemon is against other pokemon"""
    beaten_by = matchups.groupby('Name 2')['Name 1'].nunique().reset_index(name='beaten by')
    df = matchups.loc[matchups['Score'] > 0, ['Name 1', 'Name 2']].merge(beaten_by, how='outer')
    df['score'] =  1/ df['beaten by']
    return df.groupby('Name 1')['score'].sum().idxmax()


def best_team(matchups: pd.DataFrame, team: list[str] = None, exclude: list[str] = None, min_score: int = 1) -> list[str]:
    df = matchups.copy()

    if not team:
        team = []
    if exclude:
        df = df[~df['Name 1'].isin(exclude)]

    # We only care about counters
    df = df[df['Score'] > min_score]

    for poke in team:
        counters = df.loc[(df['Name 1'] == poke) & (df['Score'] > min_score), 'Name 2'].unique()
        df = df[(df['Name 1'] != poke) & (~df['Name 2'].isin(counters))]

    while len(team) < 6:
        next_best = find_next_best(df, min_score)
        team.append(next_best)
        counters = df.loc[(df['Name 1'] == next_best) & (df['Score'] > min_score), 'Name 2'].unique()
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
    possible_pokes = matchups['Name 1'].unique()
    if new_poke not in possible_pokes:
        raise ValueError(f'{new_poke} not a valid pokemon - right spelling/captialisation/game?')

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


def find_counters(team: list[str], pokemon: str, matchups: pd.DataFrame) -> pd.DataFrame:
    display(matchups[(matchups['Name 1'].isin(team)) & (matchups['Name 2'] == pokemon)].sort_values(by='Score', ascending=False))


def display(df: pd.DataFrame) -> None:
    print(tabulate(df, headers='keys'))


def main():
    game = 'heartgold_soulsilver'
    pokedex = pd.read_csv(f'resources/pokedexes/{game}_pokedex.csv')

    matchup_path = f'resources/poke_matchups/{game}_matchups.csv'
    if os.path.isfile(matchup_path):
        matchups = pd.read_csv(matchup_path)
    else:
        matchups = battle_pokemon(pokedex, matchup_path)

    team = ['Totodile', 'Sentret', 'Pidgey', 'Rattata', 'Hoothoot', 'Bellsprout']

    find_counters(team, 'Caterpie', matchups)

    display(poke_replace(team,'Onix', matchups, pokedex))


if __name__ == "__main__":
    main()