# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Unicode, Integer, Float, ForeignKey, MetaData, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from logger import Logs
import os
from datetime import datetime

from Utils import JsonTools
from DataAccess import DataUtils, FileInformation, ProjectProperties, Character, Core, SmartGroup, Tag, Biography, \
    CoreCharacterLink, TagCharacterLink, CharacterMap

engine = create_engine('sqlite:///capivara.db', echo=False)
# engine = create_engine('sqlite://', echo=False)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
connection = engine.connect()
metadata = MetaData(bind=engine, reflect=True)


def loadCapivaraFile(fileOpen=None):
    # TODO: Colocar o loadcapivarafile em uma transaction
    logs = Logs(filename="capivara.log")

    if fileOpen == None:
        capivara = {
            "version model": "0.1.0",
            "creator": "Capivara 0.1.0",
            "device": "",
            "modified": "",
            "project properties": {
                "title": "Untitled",
                "abbreviated title": "",
                "authors full name": "",
                "surname": "",
                "forename": "",
                "pseudonym": ""
            },
            "character": [
                {
                    "id": 1,
                    "name": "unnamed",
                    "archtype" : "",
                    "date of birth" : "",
                    "sex": "",
                    "age": "",
                    "local": "",
                    "occupation": "",
                    "position social": "",
                    "height": 0,
                    "weight": 0,
                    "body type": "",
                    "appearance": "",
                    "eye color": "",
                    "hair color": "",
                    "ethnicity": "",
                    "health": "",
                    "standing features": "",
                    "background": "",
                    "hobbies": "",
                    "picture": "",
                    "notes": "NOTAS",
                    "biography": [],
                    "relationship": []
                }
            ],
            "core": [],
            "smart group": [],
            "tag": [],
            "Relationship map": []
        }

    else:
        capivara = JsonTools.loadFile(fileOpen)

    if not capivara:
        logs.record("O arquivo " + fileOpen + " está vazio.")
        raise CapivaraEmptyError(10, "O arquivo " + fileOpen + " está vazio")

    logs.record("Gravando os dados na base do Capivara", type="info")

    dataUtils = DataUtils()

    s = Session()
    dataUtils.clear_data(s)

    try:
        registro = "FileInformation"
        __InsertFileInformationOnBase(s, capivara)

        registro = "Project properties"
        __InsertProjectPropertiesOnBase(s, capivara)

        registro = "Character"
        __InsertCharaterOnBase(s, capivara)

        registro = "Core"
        __InsertCoreOnBase(s, capivara)

        registro = "SmartGroup"
        __InsertSmartGroupOnBase(s, capivara)

        registro = "Tag"
        __InsertTagOnBase(s, capivara)

        registro = "Biografia"
        __IncludeBiographyOnBase(s, capivara)

        registro = "Relationships"
        __CreateAllRelationships(s, capivara)

        __CreateRelationshipMap(s, capivara)

        s.commit()

    except:
        s.rollback()
        # TODO: Obter o código da exception
        logs.record("Não foi possível gravar o registro " + registro)
        raise WritingRecordError(20, "Não foi possível gravar o registro" + registro)

    finally:
        s.close()
        engine.dispose()


class CapivaraEmptyError(Exception):
    def __init__(self, error_code, *args, **kwargs):
        super(CapivaraEmptyError, self).__init__(*args, **kwargs)
        self.error_code = error_code


class WritingRecordError(Exception):
    def __init__(self, error_code, *args, **kwargs):
        super(WritingRecordError, self).__init__(*args, **kwargs)
        self.error_code = error_code


def __CreateAllRelationships(s, capivara):
    for character_um in capivara['character']:
        characterId = character_um['id']
        for relationship in character_um['relationship']:
            if relationship['destination'] == 'core':
                for i in relationship['idrefs']:
                    c = CoreCharacterLink()
                    c.character_id = characterId
                    c.core_id = i
                    s.add(c)
                    s.commit()

            elif relationship['destination'] == 'tag':
                for i in relationship['idrefs']:
                    c = TagCharacterLink()
                    c.character_id = characterId
                    c.tag_id = i
                    s.add(c)
                    s.commit()


def __IncludeBiographyOnBase(s, capivara):
    for character in capivara['character']:
        for bio in character['biography']:
            bioDict = {}
            bioDict['id_character'] = character['id']
            bioDict['year'] = bio['year']
            bioDict['description'] = bio['description']
            c = Biography.add(bioDict)
            s.add(c)
            s.commit()


def __InsertTagOnBase(s, capivara):
    for tag in capivara['tag']:
        c = Tag.add(tag)
        s.add(c)
        s.commit()


def __InsertSmartGroupOnBase(s, capivara):
    for smart_group in capivara['smart group']:
        c = SmartGroup.add(smart_group)
        s.add(c)
        s.commit()


def __InsertCoreOnBase(s, capivara):
    for core in capivara['core']:
        c = Core.add(core)
        s.add(c)
        s.commit()


def __InsertCharaterOnBase(s, capivara):
    for character in capivara['character']:
        c = Character.add(character)
        s.add(c)
        s.commit()


def __InsertProjectPropertiesOnBase(s, capivara):
    c = ProjectProperties()
    c.title = capivara['project properties']['title']
    c.authorsFullName = capivara['project properties']['authors full name']
    c.surname = capivara['project properties']['surname']
    c.forename = capivara['project properties']['forename']
    c.pseudonym = capivara['project properties']['pseudonym']
    s.add(c)
    s.commit()


def __InsertFileInformationOnBase(s, capivara):
    device = os.environ['COMPUTERNAME']
    now = datetime.now()
    modified = str(now.today())

    c = FileInformation()
    c.versionModel = capivara['version model']
    c.creator = capivara['creator']
    c.device = device
    c.modified = modified
    s.add(c)
    s.commit()

def __CreateRelationshipMap(s, capivara):
    for relationship in capivara['Relationship map']:
        c = Character()
        mp = CharacterMap()
        mp.character_relationship = relationship['relationship']
        c = c.get(relationship['idrefs'][0])
        mp.character_one = c.id
        c = c.get(relationship['idrefs'][1])
        mp.character_two = c.id
        s.add(mp)
        s.commit()







        


