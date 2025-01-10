from app.pokedex_scraping import *


def test_that_extract_evolution_lines_works():
    assert extract_evolution_lines(get_html("https://pokemondb.net/pokedex/sprigatito")) == [
        '#0906 Sprigatito Grass\n(Level 16)#0907 Floragato Grass\n(Level 36)#0908 Meowscarada Grass · Dark']
    assert extract_evolution_lines(get_html("https://pokemondb.net/pokedex/typhlosion")) == [
        '#0155 Cyndaquil Fire\n(Level 14, or Level 17 in Legends: Arceus)#0156 Quilava Fire\n(Level 36)#0157 Typhlosion Fire',
        '#0155 Cyndaquil Fire\n(Level 14, or Level 17 in Legends: Arceus)#0156 Quilava Fire\n(Level 36, in Legends: Arceus)#0157 Typhlosion Hisuian Typhlosion Fire · Ghost']
    assert extract_evolution_lines(get_html("https://pokemondb.net/pokedex/cascoon")) == [
        '#0265 Wurmple Bug\n(Level 7, random based on personality)#0266 Silcoon Bug\n(Level 10)#0267 Beautifly Bug · Flying',
        '#0265 Wurmple Bug\n(Level 7, random based on personality)#0268 Cascoon Bug\n(Level 10)#0269 Dustox Bug · Poison']
    assert extract_evolution_lines(get_html("https://pokemondb.net/pokedex/lycanroc")) == [
        '#0744 Rockruff Rock\n(Level 25, Daytime)#0745 Lycanroc Midday Form Rock',
        '#0744 Rockruff Rock\n(Level 25, Nighttime)#0745 Lycanroc Midnight Form Rock',
        '#0744 Rockruff Own Tempo Rockruff Rock\n(Level 25, Dusk)#0745 Lycanroc Dusk Form Rock']
    assert extract_evolution_lines(get_html("https://pokemondb.net/pokedex/clodsire")) == [
        '#0194 Wooper Water · Ground\n(Level 20)#0195 Quagsire Water · Ground',
        '#0194 Wooper Paldean Wooper Poison · Ground\n(Level 20)#0980 Clodsire Poison · Ground']


def test_that_clean_evolution_lines_works():
    assert clean_evolution_lines([
        '#0906 Sprigatito Grass\n(Level 16)#0907 Floragato Grass\n(Level 36)#0908 Meowscarada Grass · Dark'
    ], 'Floragato') == [{
        'Evolution 1': 'Sprigatito',
        'Condition 2': 'Level 16',
        'Evolution 2': 'Floragato',
        'Condition 3': 'Level 36',
        'Evolution 3': 'Meowscarada'
    }]
    assert clean_evolution_lines([
        '#0155 Cyndaquil Fire\n(Level 14, or Level 17 in Legends: Arceus)#0156 Quilava Fire\n(Level 36)#0157 Typhlosion Fire',
        '#0155 Cyndaquil Fire\n(Level 14, or Level 17 in Legends: Arceus)#0156 Quilava Fire\n(Level 36, in Legends: Arceus)#0157 Typhlosion Hisuian Typhlosion Fire · Ghost'
    ], 'Typhlosion') == [{
                'Evolution 1': 'Cyndaquil',
                'Condition 2': 'Level 14, or Level 17 in Legends: Arceus',
                'Evolution 2': 'Quilava',
                'Condition 3': 'Level 36',
                'Evolution 3': 'Typhlosion'
            },
           {
               'Evolution 1': 'Cyndaquil',
               'Condition 2': 'Level 14, or Level 17 in Legends: Arceus',
               'Evolution 2': 'Quilava',
               'Condition 3': 'Level 36, in Legends: Arceus',
               'Evolution 3': 'Hisuian Typhlosion'
           }]
    assert clean_evolution_lines([
        '#0265 Wurmple Bug\n(Level 7, random based on personality)#0266 Silcoon Bug\n(Level 10)#0267 Beautifly Bug · Flying',
        '#0265 Wurmple Bug\n(Level 7, random based on personality)#0268 Cascoon Bug\n(Level 10)#0269 Dustox Bug · Poison'
    ], 'Wurmple') == [{
        'Evolution 1': 'Wurmple',
        'Condition 2': 'Level 7, random based on personality',
        'Evolution 2': 'Silcoon',
        'Condition 3': 'Level 10',
        'Evolution 3': 'Beautifly'
    },
               {
                   'Evolution 1': 'Wurmple',
                   'Condition 2': 'Level 7, random based on personality',
                   'Evolution 2': 'Cascoon',
                   'Condition 3': 'Level 10',
                   'Evolution 3': 'Dustox'
               }]
    assert clean_evolution_lines([
        '#0265 Wurmple Bug\n(Level 7, random based on personality)#0266 Silcoon Bug\n(Level 10)#0267 Beautifly Bug · Flying',
        '#0265 Wurmple Bug\n(Level 7, random based on personality)#0268 Cascoon Bug\n(Level 10)#0269 Dustox Bug · Poison'
    ], 'Dustox') == [{
        'Evolution 1': 'Wurmple',
        'Condition 2': 'Level 7, random based on personality',
        'Evolution 2': 'Cascoon',
        'Condition 3': 'Level 10',
        'Evolution 3': 'Dustox'
    }]
    assert clean_evolution_lines([
                '#0744 Rockruff Rock\n(Level 25, Daytime)#0745 Lycanroc Midday Form Rock',
                '#0744 Rockruff Rock\n(Level 25, Nighttime)#0745 Lycanroc Midnight Form Rock',
                '#0744 Rockruff Own Tempo Rockruff Rock\n(Level 25, Dusk)#0745 Lycanroc Dusk Form Rock'
            ], 'Lycanroc') == [{
                'Evolution 1': 'Rockruff',
                'Condition 2': 'Level 25, Daytime',
                'Evolution 2': 'Lycanroc Midday Form'
            },
           {
               'Evolution 1': 'Rockruff',
               'Condition 2': 'Level 25, Nighttime',
               'Evolution 2': 'Lycanroc Midnight Form'
           },
           {
               'Evolution 1': 'Own Tempo Rockruff',
               'Condition 2': 'Level 25, Dusk',
               'Evolution 2': 'Lycanroc Dusk Form'
           }]
    assert clean_evolution_lines([
        '#0194 Wooper Water · Ground\n(Level 20)#0195 Quagsire Water · Ground',
        '#0194 Wooper Paldean Wooper Poison · Ground\n(Level 20)#0980 Clodsire Poison · Ground'
    ], 'Clodsire') == [
               {
                   'Evolution 1': 'Paldean Wooper',
                   'Condition 2': 'Level 20',
                   'Evolution 2': 'Clodsire'
               }]

