from DataAccess import Character


class CharacterControl():

    def __init__(self, characterId):
        c = Character()
        characters = c.get(characterId)

        for character in characters:
            print(character.name)






