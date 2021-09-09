# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Unicode, Integer, Float, String, ForeignKey, MetaData, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import logging
from Utils import JsonTools

import json
import os
from datetime import datetime

engine = create_engine('sqlite:///capivara.db', echo=False)
#engine = create_engine('sqlite://', echo=False)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
connection = engine.connect()
metadata = MetaData(bind=engine, reflect=True)


class CharacterMap(Base):
    __tablename__ = 'characterMap'
    id = Column(Integer(), primary_key=True)
    character_one = Column(Unicode(100))
    character_relationship = Column(Unicode(100))
    character_two = Column(Unicode(100))

    @classmethod
    def insertCharacterMap(cls, character_map):
        s = Session()
        s.add(character_map)
        s.commit()

    @classmethod
    def list(cls):
        s = Session()
        return s.query(CharacterMap).all()

class FileInformation(Base):
    __tablename__ ='file_information'
    id  =  Column(Integer(), primary_key=True)
    versionModel = Column(Unicode(5))
    creator = Column(Unicode(20))
    device =Column(Unicode(100))
    modified =Column(Unicode(30))

    @classmethod
    def get(cls):
        s = Session()
        return s.query(FileInformation).get(1)

class ProjectProperties(Base):
    __tablename__ = 'project_properties'
    id = Column(Integer(), primary_key=True)
    title = Column(Unicode(100))
    authorsFullName = Column(Unicode(100))
    surname = Column(Unicode(100))
    forename = Column(Unicode(100))
    pseudonym = Column(Unicode(100))

    def add(self, projectProperties):
        s = Session
        s.add(projectProperties)

    def update(cls, projectProperties):
        s = Session()
        properties = s.query(ProjectProperties).get(1)
        properties.title = projectProperties.title
        properties.authorsFullName = projectProperties.authorsFullName
        properties.surname = projectProperties.surname
        properties.forename = projectProperties.forename
        properties.pseudonym = projectProperties.pseudonym
        s.commit()

    @classmethod
    def get(cls):
        s = Session()
        return s.query(ProjectProperties).get(1)

class CoreCharacterLink(Base):
    __tablename__ = 'core_character'
    core_id = Column(Integer, ForeignKey('core.id'), primary_key=True)
    character_id = Column(Integer, ForeignKey('character.id'), primary_key=True)

class TagCharacterLink(Base):
    __tablename__ = 'tag_character'
    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)
    character_id = Column(Integer, ForeignKey('character.id'), primary_key=True)

class Biography(Base):
    __tablename__ = 'biography'
    id = Column(Integer(), primary_key=True)
    id_character = Column(Integer())
    year = Column(Integer())
    description = Column(Unicode(100))
    id_character = Column(Integer, ForeignKey('character.id'))

    @classmethod
    def add(cls, biography):
        d = cls()
        d.id_character = int(biography['id_character'])
        d.year = int(biography['year'])
        d.description = biography['description']
        return d

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer(), primary_key=True)
    description = Column(Unicode(100))

    @classmethod
    def add(cls, tag):
        d = cls()
        d.id = tag['id']
        d.description = tag['description']
        return d

    @classmethod
    def get(cls, id):
        s = Session()
        return s.query(Tag).get(id)

    @classmethod
    def dictBuffer(cls):
        s = Session()
        tags = s.query(Tag).all()
        retorno = []
        for tag in tags:
            tagStr = JsonTools.putMap('"id"', str(tag.id)) + ','
            tagStr = tagStr + JsonTools.putMap('"description"', '"' + tag.description + '"')
            retorno.append(JsonTools.putObject(tagStr))

        return JsonTools.putArray(', '.join(retorno))

class SmartGroup(Base):
    __tablename__ = 'smart_group'
    id = Column(Integer(), primary_key=True)
    description = Column(Unicode(100))
    rule = Column(Unicode(100))

    @classmethod
    def add(cls, smartgrupo):
        d = cls()
        d.id = smartgrupo['id']
        d.description = smartgrupo['description']
        d.rule = smartgrupo['rule']
        return d

    @classmethod
    def insertSmartGroup(cls, smartGroup):
        s = Session()
        s.add(smartGroup)
        s.commit()

    @classmethod
    def list(cls):
        s = Session()
        return s.query(SmartGroup).all()

    @classmethod
    def toDict(cls):
        s = Session()
        smartGroups = s.query(SmartGroup).all()
        retorno = []
        for smartGroup in smartGroups:
            smartGroupStr = JsonTools.putMap('"id"', str(smartGroup.id)) + ','
            #smartGroupStr = smartGroupStr + JsonTools.putMap('"description"', '"' + smartGroup.description + '"')
            smartGroupStr = smartGroupStr + JsonTools.putMap('"description"', '"' + smartGroup.description  + '"') + ','
            smartGroupStr = smartGroupStr + JsonTools.putMap('"rule"', '"' + smartGroup.rule  + '"')
            retorno.append(JsonTools.putObject(smartGroupStr))

        return JsonTools.putArray(', '.join(retorno))

class Core(Base):
    __tablename__ = 'core'
    id = Column(Integer(), primary_key=True)
    description = Column(Unicode(100))
    characters = relationship('Character',
                              secondary='core_character')

    @classmethod
    def add(cls, core):
        d = cls()
        d.id = core['id']
        d.description = core['description']
        return d

    @classmethod
    def insertCore(cls, core):
        s = Session()
        s.add(core)
        s.commit()

    @classmethod
    def get(cls, id):
        s = Session()
        return s.query(Core).get(id)

    @classmethod
    def list(cls):
        s = Session()
        return s.query(Core).all()

    @classmethod
    def toDict(cls):
        s = Session()
        cores = s.query(Core).all()
        retorno = []
        for core in cores:
            coresStr = JsonTools.putMap('"id"', str(core.id)) + ','
            coresStr = coresStr + JsonTools.putMap('"description"', '"' + core.description + '"')
            retorno.append(JsonTools.putObject(coresStr))

        return JsonTools.putArray(', '.join(retorno))

class Character(Base):
    __tablename__ = 'character'
    id = Column(Integer(), primary_key=True)
    name = Column(Unicode(200))
    sex = Column(Unicode(1))
    age = Column(Unicode(3))
    local = Column(Unicode(200))
    occupation = Column(Unicode(200))
    position_social = Column(Unicode(1))
    height = Column(Float(1, 2))
    weight = Column(Float(1, 2))
    body_type = Column(Unicode(100))
    appearance = Column(Unicode(100))
    eye_color = Column(Unicode())
    hair_color = Column(Unicode())
    ethnicity = Column(Unicode(1))
    health = Column(Unicode(100))
    standing_features = Column(Unicode(100))
    background = Column(Unicode(1000))
    hobbies = Column(Unicode())
    picture = Column(String(200000))
    notes = Column(Unicode(1000))

    @classmethod
    def set_name(cls, intId, strName):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'name': strName})
        s.commit()

    @classmethod
    def set_image(cls, intId, strBase64Image):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'picture': str(strBase64Image, 'UTF-8')})
        s.commit()

    @classmethod
    def set_height(cls, intId, intHeight):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'height': float(intHeight)})
        s.commit()

    @classmethod
    def set_weight(cls, intId, intWeight):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'weight': float(intWeight)})
        s.commit()

    @classmethod
    def set_local(cls, intId, strLocal):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'local': strLocal})
        s.commit()

    @classmethod
    def add(cls, character):
        d = cls()
        d.id = character['id']
        d.name = character['name']
        d.sex = character['sex']
        d.age = character['age']
        d.local = character['local']
        d.occupation = character['occupation']
        d.position_social = character['position social']
        d.height = character['height']
        d.weight = character['weight']
        d.body_type = character['body type']
        d.appearance = character['appearance']
        d.eye_color = character['eye color']
        d.hair_color = character['hair color']
        d.ethnicity = character['ethnicity']
        d.health = character['health']
        d.standing_features = character['standing features']
        d.background = character['background']
        d.hobbies = character['hobbies']
        d.picture = character['picture']
        d.notes = character['notes']
        return d

    @classmethod
    def insertCharacter(cls, character):
        s = Session()
        s.add(character)
        s.commit()

    @classmethod
    def get(cls, id):
        s = Session()
        return s.query(Character).get(id)

    @classmethod
    def list(cls):
        s = Session()
        return s.query(Character).all()

    @classmethod
    def getBiografia(cls, id):
        s = Session()
        return s.query(Biography).filter_by(id_character=id)

    @classmethod
    def getCores(cls, id):
        s = Session()
        return s.query(CoreCharacterLink).filter_by(character_id=id)

    @classmethod
    def getTags(cls, id):
        s = Session()
        return s.query(TagCharacterLink).filter_by(character_id=id)

    @classmethod
    def toDict(cls):
        s = Session()
        characters = s.query(Character).all()

        retorno = []
        for character in characters:
            characterStr = JsonTools.putMap('"id"', str(character.id)) + ','
            #characterStr = characterStr + JsonTools.putMap('"name"', '"' + str(character.name) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"name"', '"' + str(character.name) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"sex"', '"' + str(character.sex) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"age"', '"' + str(character.age) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"local"', '"' + str(character.local) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"occupation"', '"' + str(character.occupation) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"position social"', '"' + str(character.position_social)  + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"height"', str("{:.2f}".format(character.height))) + ','
            characterStr = characterStr + JsonTools.putMap('"weight"', str("{:.2f}".format(character.weight))) + ','
            characterStr = characterStr + JsonTools.putMap('"body type"', '"' + str(character.body_type) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"appearance"', '"' + str(character.appearance) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"eye color"', '"' + str(character.eye_color) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"hair color"', '"' + str(character.hair_color) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"ethnicity"', '"' + str(character.ethnicity) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"health"', '"' + str(character.health) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"standing features"', '"' + str(character.standing_features) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"background"', '"' + str(character.background) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"hobbies"', '"' + str(character.hobbies) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"picture"', '"' + str(character.picture) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"notes"', '"' + str(character.notes) + '"') + ','

            i = character.id
            strBiografia = ""
            result = s.query(Biography).filter(Biography.id_character == i)

            if result.count() > 0:
                for row in result:
                    strBio = ""
                    strBio = strBio + JsonTools.putMap('"year"', str(row.year)) + ','
                    strBio = strBio + JsonTools.putMap('"description"', '"' + str(row.description) + '"')
                    strBio = JsonTools.putObject(strBio) + ','
                    strBiografia = strBiografia + strBio
                strBiografia = JsonTools.putMap('"biography"', JsonTools.putArray(strBiografia[:-1]))
            else:
                strBiografia = JsonTools.putMap('"biography"', "[]")

            characterStr = characterStr + strBiografia

            # OBTER OS RELACIONAMENTOS
            strDestinationCore = ""
            strDestinationTag = ""
            strRelationship = ""

            result = s.query(CoreCharacterLink).filter(CoreCharacterLink.character_id == i)
            strIdCore = []
            if result.count() > 0:
                for row in result:
                    strIdCore.append(str(row.core_id))
                strIdCore = ",".join(strIdCore)
                strIdCore = JsonTools.putArray(strIdCore.replace("'", ""))
            else:
                strIdCore = ""

            if strIdCore:
                strDestinationCore = JsonTools.putMap('"destination"', '"core"')  + ", "
                strDestinationCore = strDestinationCore + JsonTools.putMap('"idrefs"', strIdCore)
                strDestinationCore = JsonTools.putObject(strDestinationCore)

            # OBTER OS RELACIONAMENTOS COM O TAG
            result = s.query(TagCharacterLink).filter(TagCharacterLink.character_id == i)
            strIdTag = []
            if result.count() > 0:
                for row in result:
                    strIdTag.append(str(row.tag_id))
                strIdTag = ",".join(strIdTag)
                strIdTag = JsonTools.putArray(strIdTag.replace("'", ""))
            else:
                strIdTag  = ""

            if strIdTag:
                strDestinationTag = JsonTools.putMap('"destination"', '"tag"') + ", "
                strDestinationTag = strDestinationTag + JsonTools.putMap('"idrefs"', strIdTag)
                strDestinationTag = JsonTools.putObject(strDestinationTag)

            if strDestinationCore:
                strRelationship = strDestinationCore
                if strDestinationTag:
                    strRelationship +=  ", " + strDestinationTag
            else:
                if strDestinationTag:
                    strRelationship +=  strDestinationTag


            strRelationship = JsonTools.putMap('"relationship"', JsonTools.putArray(strRelationship))

            characterStr = characterStr + ", " + strRelationship


            retorno.append(JsonTools.putObject(characterStr))

        return JsonTools.putArray(', '.join(retorno))


class DataUtils():

    def __init__(self):
        Base.metadata.create_all()

    def clear_data(self, session):
        meta = Base.metadata
        for table in reversed(meta.sorted_tables):
            print('Clear table %s' % table)
            session.execute(table.delete())
        session.commit()

    def drop_table(self, table_name):
        base = declarative_base()
        metadata = MetaData(engine, reflect=True)
        table = metadata.tables.get(table_name)
        if table is not None:
            logging.info(f'Deleting {table_name} table')
            base.metadata.drop_all(engine, [table], checkfirst=True)
