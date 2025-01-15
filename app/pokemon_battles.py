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

    hits_to_kill_2 = int((poke2['HP'] / dmg1) + 1) if dmg1 != 0 else 10
    hits_to_kill_1 = int((poke1['HP'] / dmg2) + 1) if dmg2 != 0 else 10

    if poke1['Speed'] > poke2['Speed']:
        hits_to_kill_1 += 1
    elif poke1['Speed'] < poke2['Speed']:
        hits_to_kill_2 += 1

    return (hits_to_kill_1 - hits_to_kill_2) / min(hits_to_kill_1, hits_to_kill_2)


def battle_pokemon(pokedex: str):
    df = pd.read_csv(f'resources/pokedexes/{pokedex}.csv', usecols=['Name', 'Form', 'Types', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Total'])
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


def main():
    battle_pokemon('platinum_pokedex')


if __name__ == "__main__":
    main()