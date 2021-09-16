"""http://www.graphviz.org/content/fsm"""

import graphviz
from DataAccess import CharacterMap, Character, Core, ProjectProperties
import Utils
import tempfile


def GraphMake( chkCharacter, chkCore, mapFile=None):

    c = ProjectProperties()
    c = c.get()

    __title__ = c.title
    __author__ = c.authorsFullName

    if mapFile == None:
        __fileName__ = tempfile.NamedTemporaryFile(suffix='.gv').name
    else:
        __fileName__ = mapFile
        if mapFile.endswith('.pdf'):
            formatOutput = "pdf"
        elif mapFile.endswith('.png'):
            formatOutput = "png"
        elif mapFile.endswith('.svg'):
            formatOutput = "svg"
        elif mapFile.endswith('.jpg'):
            formatOutput = "jpg"


            # .endswith('.xyz')
            # filename += '.xyz'


    #f = graphviz.Digraph('finite_state_machine', filename= __fileName__ + '.gv')
    f = graphviz.Digraph(comment = __title__,  filename=__fileName__)


    f.attr(rankdir='LR', size='8,5')
    f.attr(label="<<TABLE BORDER='0' CELLBORDER='1' CELLSPACING='0' CELLPADDING='4'><TR><TD ROWSPAN='3'>Relationships <BR/> Between Characters  <BR/>in " + __author__ +"'s <BR/>" + __title__  + "</TD></TR></TABLE>>")
    f.attr(fontsize='6')

    cr = Core()
    cores = cr.list()

    c = Character()
    characters = c.list()


    c = CharacterMap()
    relationShips = c.list()


    if chkCore:
        # Criar os Núcleos
        f.attr('node', shape='circle')
        for core in cores:
            f.node(core.description)

    if chkCharacter:
        # Cria os personagens
        f.attr('node', shape='rect')
        for character in characters:
            f.node(character.name)

        if chkCore:
            # Criar os núcleos com personagens
            for character in characters:
                crs = character.getCores(character.id)
                for i in crs:
                    nameCore = cr.get(i.core_id).description
                    f.edge(character.name, nameCore, arrowhead = 'none')


        c = Character()
        # Criar os relacionamentos
        for relationShip in relationShips:
            if relationShip.character_relationship != '':
                f.edge(c.get(relationShip.character_one).name, c.get(relationShip.character_two).name, label=relationShip.character_relationship)

    if mapFile == None:
        f.view()
    else:
        f.format = formatOutput
        f.render(__fileName__, view = True)
