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


def extract_stats(stat_table):
    all_stats = []
    next_link = stat_table.find_next('tr')
    next_stat = next_link.text.split('\n')[1:3]
    while next_stat:
        all_stats.append(next_stat)
        next_link = next_link.find_next('tr')
        next_stat = next_link.text.split('\n')[1:3]
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
    split_apart = [part for part in split_apart if part != ['']]
    final = {}
    for i, part in enumerate(split_apart):
        if part == ['']:
            continue
        name = ' '.join(part[1].split(' ')[1:-1])
        name_split = name.split(' ')
        if len(name_split) > 1 and name_split[0] == name_split[-1]:
            name = ' '.join(name_split[1:])
        if i != 0:
            final[f'Condition {i + 1}'] = part[0].replace('(', '').replace(')', '')
        final[f'Evolution {i + 1}'] = name
    return final


def clean_evolution_lines(raw_evolutions: list, name: str):
    return [clean_evo_line(evo) for evo in raw_evolutions if name in evo]


def extract_pokemon_info(poke_soup):
    name = poke_soup.find('h1').text
    forms = poke_soup.find('div', class_='sv-tabs-tab-list').text.strip().split('\n')
    forms = [form.strip() for form in forms]

    headers = poke_soup.find_all('th')

    types = [header.find_next('td').text.strip() for header in headers if header.text == 'Type']
    types = types[:types.index('1')]

    abilities = [
        ', '.join([ability.text for ability in header.find_next('td').find_all('a')])
        for header in headers if header.text == 'Abilities'
    ]

    stats_tables = poke_soup.find_all('div', id='dex-stats')
    stats = [extract_stats(stat_table) for stat_table in stats_tables]

    raw_evolutions = extract_evolution_lines(poke_soup)
    evolutions = clean_evolution_lines(raw_evolutions, name)

    return name, forms, types, abilities, stats, evolutions


def find_form(name: str, forms: list[str], evo: dict[str, str]) -> str:
    if name in evo.values():
        return name
    else:
        remaining_forms = [form for form in forms if form != name]
        valid_forms = [form for form in remaining_forms if any([form in e for k, e in evo.items() if 'Evolution' in k])]
        if len(valid_forms) == 1:
            form = valid_forms[0]
            return form
        elif len(valid_forms) == 0:
            return None
        else:
            raise ValueError(f"Found multiple matching forms for {name} {forms} {evo} - Valid Forms: {valid_forms}")


def build_pokemon_entry(poke_soup):
    name, forms, types, abilities, stats, evolutions = extract_pokemon_info(poke_soup)

    mega = False
    if evolutions and len(evolutions) < len(forms):
        if len(evolutions) == 1:
            evolutions *= len(forms)
            mega = True

    all_forms_info = []
    if evolutions:
        for i, evo in enumerate(evolutions):
            which_form = find_form(name, forms, evo)

            if which_form:
                if mega:
                    form_i = i
                else:
                    form_i = forms.index(which_form)
                this_form = forms[form_i].replace(name, '').strip()
                this_type = types[form_i]
                this_ability = abilities[form_i]
                this_stat = stats[form_i]
            else:
                this_form = None
                this_type = None
                this_ability = None
                this_stat = {}

            all_forms_info.append({
                  'Name': name,
                  'Form': this_form,
                  'Types': this_type,
                  'Abilities': this_ability
              } | {
                  name: stat for name, stat in this_stat
              } | evo | {
                  # 'Moves': [],
                  # 'Where': [],
              })
    else:
        all_forms_info.append({
              'Name': name.strip(),
              'Form': None,
              'Types': types[0],
              'Abilities': abilities[0]
          } | {
              name: stat for name, stat in stats[0]
          } | {
              # 'Moves': [],
              # 'Where': [],
          })

    return all_forms_info


def create_df(pokedex_soup):
    pokemon_urls = [poke['href'] for poke in pokedex_soup.find_all('a', class_='ent-name')]
    all_pokemon_info = []
    for poke_url in tqdm(pokemon_urls):
        try:
            all_pokemon_info += build_pokemon_entry(get_html(base_url + poke_url))
        except:
            print(poke_url)
    return pd.DataFrame(all_pokemon_info).drop_duplicates().replace('', None)


def create_all_pokedexes() -> None:
    for game in list_of_games:
        print(game)
        try:
            df_name = game.lower().replace(
                '&', '').replace(':', '').replace(
                '  ', ' ').replace(' ', '_') + '_pokedex.csv'
            pokedex_soup = get_pokedex_soup(get_html(base_url + links_to_games[list_of_games.index(game)]))
            df = create_df(pokedex_soup)
            if df.empty:
                raise ValueError("No Data Found.")
            df.to_csv(f"resources/pokedexes/{df_name}")
        except:
            print(f"No luck on {game}")


if __name__ == "__main__":
    # Step 1: Define the URL
    base_url = "https://pokemondb.net"
    base_soup = get_html(base_url)

    # Find the <span> with class "main-menu-title-long"
    games_header = [item for item in base_soup.find_all('span', class_='main-menu-title-long') if 'Pokémon games' in item][0]
    list_of_games = [title.text.strip() for title in games_header.find_next('ul').find_all('li') if title.text.strip()]
    links_to_games = [title.find('a')['href'] for title in games_header.find_next('ul').find_all('li') if title.find('a')]

    create_all_pokedexes()


