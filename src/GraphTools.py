"""http://www.graphviz.org/content/fsm"""

import graphviz
from DataAccess import CharacterMap, Character, Core

def GraphMake(mapFile=None):

    f = graphviz.Digraph('finite_state_machine', filename='fsm.gv')
    f.attr(rankdir='LR', size='8,5')

    c = Core()
    cores = c.list()

    c = Character()
    characters = c.list()

    c = CharacterMap()
    relationShips = c.list()


    # Criar os Núcleos
    f.attr('node', shape='circle')
    for core in cores:
        f.node(core.description)

    # Cria os personagens
    f.attr('node', shape='rect')
    for character in characters:
        f.node(character.name)

    # Criar os relacionamentos
    for relationShip in relationShips:
        f.edge(relationShip.character_one, relationShip.character_two, label=relationShip.character_relationship, arrowhead = 'none')






    # f.attr('node', shape='rect')
    # f.edge('Elizabeth Bennet', 'Mr Fitzwilliam Darcy', label='falls in love with')
    # f.edge('Elizabeth Bennet', 'Jane Bennet', label='confidante of')
    # f.edge('Elizabeth Bennet', 'Colonel Fitzwilliam', label='atractted to')
    # f.edge('Elizabeth Bennet', 'Core 1',  arrowhead = 'none' )
    # f.edge('Jane Bennet', 'Core 1',  arrowhead = 'none')
    # f.edge('Colonel Fitzwilliam', 'Core 1',  arrowhead = 'none')
    # f.edge('Charles Bingley', 'Jane Bennet', label='Loves')
    # f.edge('Charles Bingley', 'Core 2',  arrowhead = 'none')

    f.view()