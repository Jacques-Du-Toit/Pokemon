from bs4 import BeautifulSoup
import requests
import os
from tqdm import tqdm
import pandas as pd


def get_html(url):
    # Step 2: Make a GET request to fetch the raw HTML content
    response = requests.get(url)
    # Step 3: Parse the HTML content with Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_pokedex_soup(game_soup: BeautifulSoup) -> BeautifulSoup:
    # Find the main body so we skip the title
    next_link = game_soup.find('main').find('a')
    while next_link:
        if next_link['href'].startswith('/pokedex/'):
            return get_html(base_url + next_link['href'])
        next_link = next_link.find_next('a')
    raise ValueError("Couldn't find a link to a pokedex")


def extract_stats(pokemon_soup: BeautifulSoup) -> list[str]:
    stats = pokemon_soup.find('div', id='dex-stats')
    all_stats = []
    next_stat = stats.find_next('tr')
    this_stat = next_stat.text.split('\n')
    for _ in range(7):
        all_stats.append(this_stat[2])
        next_stat = next_stat.find_next('tr')
        this_stat = next_stat.text.split('\n')
    return all_stats


def extract_evolution_lines(poke_soup: BeautifulSoup) -> list[str]:
    """
    Extracts all the separate lines of evolutions for a pokemon (if they have different forms or variants).
    """
    evo_tree = [evo.text.strip() for evo in poke_soup.find_all('div', class_='infocard-list-evo')]

    if len(evo_tree) == 1:
        # Only one simple line luckily
        return evo_tree

    # First need to separate any evolutions lines with different starts
    line_starts = []
    all_lines = []
    current_line = -1
    for branch in evo_tree:
        if branch.startswith('#'):
            # this means its an entirely new line
            current_line += 1
            line_starts.append(branch)
            all_lines.append([branch])
        else:
            # this means its continuing on from the last line
            # The start line contains all the evolutions so need to remove that
            line_starts[current_line] = line_starts[current_line].replace(branch, '')
            all_lines[current_line].append(branch)

    # Now need to separate each evolution line that splits
    final_lines = []
    for line in all_lines:
        if len(line) == 1:
            # Line doesn't split
            final_lines += line
            continue
        current_line = []
        for branch in line:
            if branch.startswith('#'):
                # this means its an entirely new line
                line_start = branch
            else:
                # this means its continuing on from the last line
                line_start = line_start.replace(branch,
                                                '')  # Remove it from the start of the line as there are going to be separate lines now
                current_line.append(branch)
        final_lines += [(line_start + line_cont).replace('\n\n', '\n') for line_cont in current_line]

    return final_lines


def clean_evo_line(evo_line: str) -> dict[str, str]:
    split_apart = [a.split('#') for a in evo_line.replace(' · ', '').split('\n')]
    final = {}
    for i, part in enumerate(split_apart):
        name = ' '.join(part[1].split(' ')[1:-1])
        name_split = name.split(' ')
        if len(name_split) > 1 and name_split[0] == name_split[-1]:
            name = ' '.join(name_split[:-1])
        if i != 0:
            final[f'Condition {i+1}'] = part[0]
        final[f'Evolution {i+1}'] = name
    return final


def clean_evolution_lines(raw_evolutions: list, name: str):
    return [clean_evo_line(evo) for evo in raw_evolutions if name in evo]


def prev_next_evo(row) -> pd.Series:
    prev, next = None, None
    evo_line = [row['Evo 1'], row['Evo 2'], row['Evo 3']]

    if evo_line == [None, None, None]:
        return pd.Series([prev, next])

    evo = evo_line.index(row['Name'])

    if evo > 0:
        prev = evo_line[evo - 1]
    if evo < 2:
        next = evo_line[evo + 1]

    return pd.Series([prev, next])


def create_df(pokedex_soup: BeautifulSoup) -> pd.DataFrame:
    pokemon_urls = [poke['href'] for poke in pokedex_soup.find_all('a', class_='ent-name')]


    evolution_cols = ['Evo 1', 'Evo 2', 'Evo 3']
    evolution_data = []
    stats_cols = ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Total']
    stats_data = []

    for poke_url in tqdm(pokemon_urls):
        pokemon_soup = get_html(base_url + poke_url)
        # Find the evolution line of the pokemon
        evolution_data.append(extract_evolutions(pokemon_soup))
        # Find the stats of the pokemon
        stats_data.append(extract_stats(pokemon_soup))

    evolution_df = pd.DataFrame(columns=evolution_cols, data=evolution_data)
    stats_df = pd.DataFrame(columns=stats_cols, data=stats_data)

    full_df = base_df.join(evolution_df)
    full_df[['Prev Evo', 'Next Evo']] = full_df.apply(prev_next_evo, axis=1)
    full_df = full_df.join(stats_df)
    return full_df


def extract_stats(stat_table):
    all_stats = []
    next_link = stat_table.find_next('tr')
    next_stat = next_link.text.split('\n')[1:3]
    while next_stat:
        all_stats.append(next_stat)
        next_link = next_link.find_next('tr')
        next_stat = next_link.text.split('\n')[1:3]
    return all_stats


def extract_pokemon_info(poke_soup):
    name = poke_soup.find('h1').text
    forms = poke_soup.find('div', class_='sv-tabs-tab-list').text.strip().split('\n')
    forms = [form.replace(name, '').strip() for form in forms]

    headers = poke_soup.find_all('th')

    types = [header.find_next('td').text.strip() for header in headers if header.text == 'Type']
    types = [t.split(' ') for t in types[:types.index('1')]]

    abilities = [
        [ability.text for ability in header.find_next('td').find_all('a')]
        for header in headers if header.text == 'Abilities'
    ]

    stats_tables = poke_soup.find_all('div', id='dex-stats')
    stats = [extract_stats(stat_table) for stat_table in stats_tables]

    raw_evolutions = extract_evolution_lines(poke_soup)
    evolutions = clean_evolution_lines(raw_evolutions, name)

    all_forms_info = []
    for evo in evolutions:
        which_form = [form for form in forms if f'{name} {form}'.strip() in evo.values()][0]
        form_i = forms.index(which_form)
        all_forms_info.append({
              'Name': f'{name} {forms[form_i]}'.strip(),
              'Types': types[form_i],
              'Abilities': abilities[form_i]
          } | {
              name: stat for name, stat in stats[form_i]
          } | evo | {
              'Moves': [],
              'Where': [],
          })

    return all_forms_info


if __name__ == "__main__":
    print(clean_evolution_lines([
        '#0906 Sprigatito Grass\n(Level 16)#0907 Floragato Grass\n(Level 36)#0908 Meowscarada Grass · Dark'
    ], 'Floragato'))
    exit(0)

    # Step 1: Define the URL
    base_url = "https://pokemondb.net"
    base_soup = get_html(base_url)

    # Find the <span> with class "main-menu-title-long"
    games_header = [item for item in base_soup.find_all('span', class_='main-menu-title-long') if 'Pokémon games' in item][0]
    list_of_games = [title.text.strip() for title in games_header.find_next('ul').find_all('li') if title.text.strip()]
    links_to_games = [title.find('a')['href'] for title in games_header.find_next('ul').find_all('li') if title.find('a')]

    for game in list_of_games:
        print(game)

    while True:
        game = input('Which game?')
        if game not in list_of_games:
            continue
        break

    df_name = game.lower().replace(
        '&', '').replace(':', '').replace(
        '  ', ' ').replace(' ', '_') + '_pokedex.csv'
    if df_name not in os.listdir("resources/pokedexes"):
        pokedex_soup = get_pokedex_soup(get_html(base_url + links_to_games[list_of_games.index(game)]))
        df = create_df(pokedex_soup)
        if df.empty:
            raise ValueError("No Data Found.")
        df.to_csv(f"resources/pokedexes/{df_name}")
    else:
        df = pd.read_csv(f"resources/pokedexes/{df_name}")

    print(df)