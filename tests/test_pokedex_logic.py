import pytest
from app.pokedex_logic import *


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