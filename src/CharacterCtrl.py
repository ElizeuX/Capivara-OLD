# -*- coding: utf-8 -*-

import gi

gi.require_version(namespace='Gtk', version='3.0')

from gi.repository import Gtk
from DataAccess import Character, Biography, Tag
from collections import namedtuple
import Utils
import re
from datetime import datetime
from Utils import Date

class CharacterControl:
    characterId = ""
    voCharacter = namedtuple('voCharacter',
                             ['id', 'name', 'archtype', 'date_of_birth','sex', 'height', 'weight', 'body_type', 'eye_color', 'hair_color', 'ethinicity',
                              'health', 'tag', 'local',
                              'background',
                              'picture', 'biography'])

    def __init__(self, characterId, voCharacter):
        self.strCharacterId = characterId
        __NOIMAGE = '''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oooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAK2oX1vpmnXN/dyBLe2iaWRj2VRk/wAq+SPiV8SNQ8a6ttAe302E5t7Y+n95vViP0r1b9oLxcNP0S28N28uJ70iW4CnkRKflB+rDP/AfevmtmLMSepoATqaKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigDrfAnjnU/BetpeWLGRHwlxbM2EuE9D6MOzDkE9wSD9e+HdfsfE+g2usaezG3uV3BXGGQg4KsPUEEV8K17t+zx4uEOo3Xhe5k+W6BuLYH/noo+cD6qAf+AH1oA+iaKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKrahfW+l6bdaheSeXbWsTzTPgnaigknA5PA7VZrzb4465/ZHw3urZH2zai62y4PO37zfouP8AgVAHzN4x8S3Hi7xVfazcZAnkPlIf+WcY4VfwGPxzWFRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABV/RNTudG1q01KzcJc20qyxsem4HIz6jjBHeqFFAH3Z4e1u28R+H7HWLQ/ubuISBc5KHoyn3BBB9xWnXjP7O+ufa/DGoaPI2Xs51mTJ/gkHIA9mUn/gVezUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAV82ftGa8bjxLp2ixP8lnAZJB/tydv++VB/wCBV9J18S+P9YfXfHWsXzMWV7pxGc5+QHao/wC+QKAOaooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA9N+BuvDSfiLZ2zuI4r6N7V8ngk/Mn47lUfjX1lXwZpWoS6VqltfwErNbyrLG3oysGB/MV912V3Ff2FveQHMVxEsqH1VgCP0NAFiiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAyfE2pDR/C+q6iW2m2tZJFP+0FOP1xXwxISZXJOSWO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zAa1fqdhB5gi5Bk+uRhffJ/hwfk+gAooooAKKKKACiiigAooooAKKKKACiiigArt/hFp51H4oaJGBlY5vPJ9NgL/APstcRXsf7O1ibnxpd3bZKWlo5X2Zyq/yDflQB9OUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQB5l8eNKOpfDOeZRlrG4iuBgc4zsP4fPn8K+Ta+5/FeknXfCWraWqgvc2skcef7+07T/31ivhuUETOGBBDHIPWgBlFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFAH2h8LNMXSfhh4et1cv5lotySfWXMuPw34/Cul1LULfStMu9Ru3KW1rC88rAZIRQSeO/AqS0tYLGygs7aNY7eCNYokUYCqowAPoBXmfx+1l9L+Gz2kRAfUbmO3bDYIQZdiPX7gU+zUAfNXinxHe+LPEd5rN87GS4kJRC2REn8KDpwBx79epNY9FFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABX0r+znpgi8OarqmwL9onSAf8ATJP4mT9K+aq+yfhNpLaR8NdIjljKTTo1zJnqd7FlP8A3ztoA7aiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACvj/4w+G/+Ed+IOoBI9lvdv9qgwMAq+S35MGH4V9gV5N8fPDEer+Cl1iNP9K0twcgdYnIVh+B2n2Ab1oA+WaKKKACiiigAooooAKKKKACiiigAooooAK2/BkEd1458P28q7o5dStkceoMqg1iVr+FL630vxjoeoXb+XbWuoQTzPtJ2osisxwOTwD0oA+6K+d/2l72F9R8O2KsPPhinmdfRXKBT+cbflXpH/C7fh5/0MP8A5JXH/wAbrwf41eKtG8XeM7W/0O7N1axWCQNIYmT5xJIxGGAPRh2oA84ooooAKKKKACiiigAooooAKKKKACiiigAooooA3/BXh+TxR4w03SIwcTzDzCP4UHLH8FBr7dijSGJIo1CRooVVA4AHQV4R+zp4WRLfUPE86ZlZvslvkfdAwXP45Ufga96oAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKxvFiW8ng7W0uhm3NjP5g/2dhzj3rZrlfiSzr8N/EBj6/Y3B+h6/pmgD4qooooAKKKKACiiigAooooAKKKKACiiigAorS0DQ77xLrtpo+mxh7u6fYgY4A4yWJ9AASfYV9c+B/hloHgiyi+z28d1qQX97fzIDIzd9vXYvsPxJPNAHxpRX3/VLVNI03W7NrTVLG3vLdusc8YcfUZ6H3FAHwbRXpvxc+F3/CC3seo6azSaHdybIw5y9vJgnyyf4gQCVPXAIPIy3mVABRRRQAUUUUAFFFFABRRRQAUUUUAFKpwwPoaSigD7G+D6W6/CzRGtgNrpIzH1bzG3fqP0rua80+BMkj/C+0DklVnlCZ7DOePxJr0ugAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigArn/HUZl8AeIkAyf7NuCPwjY10FRXNvDd2sttcRrJDMhjkRujKRgg/hQB8C9Dg0+SJo8bu9e/XX7Okkmvu1tq0MelGTcrOC0yp/d24Ckjn5s+nFcJ8aPD1v4b8aQWVpHstzYQGP1IVfLyff5KAPOaKKKACiiigAooooAKKKKACiiigD2/8AZs0qOfxBreqsfntLaOBFI/56sST9f3WPxNfSFfOv7NN/BHqviHTmJ8+eCGdBjjbGzK36yrX0VQAUUUUAcn8TtNg1X4Z+IYJx8sdlJcKR1DRDzF/VRXxZX2x8RryCx+G3iSW4cIjadNECf7zoUUfizAfjXxPQAUUUUAFFFFABRRRQAUUUUAFFFFAD4VV540YsFZgCVGTjPYU0jBIPauu+FumrqvxL0K2aMSKLkSsrAEEIC5yD7LXqWofs6ynXN+n6tENNZw375T5sS55GAMMQOhyPpQB3/wAFofJ+Feknj940z4Hb96w/pXf1n6Jo9n4f0W10mwQpa2ybEBOSe5J9yST+NaFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAV86ftLWqJq/h+7AG+WCaMnvhWUj/0M19F18/ftMgbvC7dyLof+iaAPAaKKKACiiigAooooAKKKKACiiigDc8IeKLzwd4ntNbshveAkSRFiFlQjDKfqOnXBAPavsfwr4u0bxjpEeo6RdCRSB5kLYEkLf3XXsf0PYkV8OVZsdQvdMulutPvLi0uFGBLbytG4/EEGgD72prukUbSSMqIoLMzHAAHUk18Rf8J34w/6GvXP/BjN/wDFVU1DxPr+r2/2fUtc1O9gzny7m7kkXPrhiRQB6f8AGv4pW3iZl8OaFKZNMt5Q9xdKxC3Eg6Kvqg65PU4I4AJ8boooAKKKKACiiigAooooAKKKKACiiigD1T9n62Sf4lrK3WCzldfqcL/JjX1XXzJ+zjEreONQkIyV05wPb95HX03QAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABRRRQAUUUUAFFFFABXz/+01/zK/8A29/+0a+gK8p/aA01rz4ex3KDDWl4js2OisGQ/hlloA+VqKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAPbf2blB8T6u+ORZ4z9XX/CvpKvBf2atOxZa9qbL96SKBG+gLN/Na96oAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigArlfiTp39qfDjXrULuItGlCjuY8OP1WuqqK5gjuraW3lXdHKhRx6gjBoA+CJWLTOzHJLEk0yrWpWM2mapd2FwMT20zQyD0ZSQf1FVaACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKOpop0f+sX6igD61+Bunmy+GtvOVAa9uJZ+BjjOwf8AoFekVh+DdMOjeDNG09l2vBaRq4x/HtBb9Sa3KACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKAPmL4/+Ev7L8VRa9bRkW+ppmXHQTKAD9MrtPud1eO19p/EjwsPF/ge/01EDXSr59qe4lXoB9Rlf+BV8WsjIxV1KsOoIwaAEooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACvQfg54U/4Sfx7ameLfZWP+lT7hkHaflX3y2PwzXn4G5gB34r60+CfhU+HvA0V5cR7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'''

        c = Character()
        character = c.get(characterId)

        # m = self.voCharacter
        # teste = m


        voCharacter.id.set_text("#" + str(character.id).zfill(5))

        voCharacter.name.set_text(character.name)

        if character.height == None:
            voCharacter.height.set_text('0.00')
        else:
            voCharacter.height.set_text(str("{:.2f}".format(character.height)))

        if not character.archtype:
            voCharacter.archtype.set_active(-1)
        else:
            sem_espacos_a_mais = re.sub(' {2,}', ' ', str(character.archtype)).strip(' ')
            voCharacter.archtype.set_active_id(sem_espacos_a_mais)

        dateBirth = character.date_of_birth
        if dateBirth != None:
            #dateBirth = "{}/{}/{}".format(dateBirth.day, dateBirth.month, dateBirth.year)
            dateBirth = dateBirth.strftime('%m/%d/%Y')
            voCharacter.date_of_birth.set_text(dateBirth)
        else:
            voCharacter.date_of_birth.set_text("")


        if not character.sex:
            voCharacter.sex.set_active(-1)
        else:
            sem_espacos_a_mais = re.sub(' {2,}', ' ', str(character.sex)).strip(' ')
            voCharacter.sex.set_active_id(sem_espacos_a_mais)

        if character.weight==None:
            voCharacter.weight.set_text('0.00')
        else:
            voCharacter.weight.set_text(str("{:.2f}".format(character.weight)))

        if character.eye_color == None:
            voCharacter.eye_color.set_text('')
        else:
            voCharacter.eye_color.set_text(character.eye_color)

        if character.hair_color == None:
            voCharacter.hair_color.set_text('')
        else:
            voCharacter.hair_color.set_text(character.hair_color)

        voCharacter.local.set_text(character.local)
        voCharacter.body_type.set_text(character.body_type)
        voCharacter.ethinicity.set_text(character.ethnicity)
        voCharacter.health.set_text(character.health)

        if  voCharacter.background == None:
            print("sem background")
        else:
            textbuffer = voCharacter.background.get_buffer()
            textbuffer.set_text(character.background)

        if not character.picture:
            pixbuf = Utils.get_pixbuf_from_base64string(__NOIMAGE)
            pixbuf = pixbuf.scale_simple(170, 200, 2)
        else:
            pixbuf = Utils.get_pixbuf_from_base64string(character.picture)
            pixbuf = pixbuf.scale_simple(170, 200, 2)

        voCharacter.picture.set_from_pixbuf(pixbuf)


        biography = c.getBiografia(character.id)
        voCharacter.biography.clear()
        bioTupla = ()
        for bio in biography:
            bioTupla = (bio.year, bio.description)
            voCharacter.biography.append(row=bioTupla)

        #Carregando as tags
        t = Tag()
        tags = character.getTags(character.id)
        strTag = ""
        for tag in tags:
            c =t.get(tag.tag_id)
            strTag += c.description + ' '

        voCharacter.tag.set_text(strTag)



















