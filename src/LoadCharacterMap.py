from DataAccess import CharacterMap, Character, Core

def loadCharacterMap():
    c = Core()
    cores = c.list()

    c = Character()
    characters = c.list()

    #characterMap = CharacterMap()


    for character in characters:
        characterOne = character.name
        for character2 in characters:
            if characterOne != character2.name:
                c = CharacterMap()
                c.character_one = characterOne
                c.character_relationship = "amigo"
                c.character_two = character2.name
                c.insertCharacterMap(c)
        # incluir os cores
        coreXcaracter = character.getCores(character.id)
        for x in coreXcaracter:
            cm = CharacterMap()
            c = Core()
            cm.character_one = characterOne
            cm.character_relationship = "pertence"
            coreDescription = c.get(x.core_id).description
            cm.character_two = coreDescription
            cm.insertCharacterMap(cm)






