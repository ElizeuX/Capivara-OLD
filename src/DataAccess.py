# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Unicode, Integer, Float, String, ForeignKey, MetaData, Table, Date
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import logging
from Utils import JsonTools

import json
import os
from datetime import datetime

engine = create_engine('sqlite:///capivara.db', echo=False)
#engine = create_engine('sqlite://', echo=True)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
connection = engine.connect()
metadata = MetaData(bind=engine, reflect=True)


class CharacterMap(Base):
    __tablename__ = 'characterMap'
    id = Column(Integer(), primary_key=True)
    character_one = Column(Integer())
    character_relationship = Column(Unicode(100))
    character_two = Column(Integer())

    @classmethod
    def insertCharacterMap(cls, character_map):
        s = Session()
        s.add(character_map)
        s.commit()

    @classmethod
    def set_relationship(cls, idRelationship, strRelationship):
        s = Session()
        d = cls()
        d = d.get(idRelationship)
        s.query(CharacterMap).filter(CharacterMap.id == d.id).update({'character_relationship': strRelationship})
        s.commit()

    @classmethod
    def get(cls, id):
        s = Session()
        return s.query(CharacterMap).get(id)

    @classmethod
    def list(cls):
        s = Session()
        return s.query(CharacterMap).all()

    @classmethod
    def listCharacterMap(cls, id):
        s = Session()
        return s.query(CharacterMap).filter_by(character_one=id)

    @classmethod
    def toDict(cls):
        s = Session()
        charactersMap = s.query(CharacterMap).all()
        strRelationship = []
        for cm in charactersMap:
            cmStr = JsonTools.putMap('"relationship"', '"' + cm.character_relationship) + '",'
            idRefsStr = JsonTools.putArray(str(cm.character_one) + ',' + str(cm.character_two))
            cmStr = cmStr + JsonTools.putMap('"idrefs"', idRefsStr)
            strRelationship.append(JsonTools.putObject(cmStr))

        strRelationship = ",".join(strRelationship)
        return JsonTools.putArray(strRelationship)


class FileInformation(Base):
    __tablename__ = 'file_information'
    id = Column(Integer(), primary_key=True)
    versionModel = Column(Unicode(5))
    creator = Column(Unicode(20))
    device = Column(Unicode(100))
    modified = Column(Unicode(30))

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
    scrivener_project = Column(Unicode(200))
    aeon_project = Column(Unicode(200))

    def add(self, projectProperties):
        s = Session
        s.add(projectProperties)
        s.commit()

    def update(cls, projectProperties):
        s = Session()
        properties = s.query(ProjectProperties).get(1)
        properties.title = projectProperties.title
        properties.authorsFullName = projectProperties.authorsFullName
        properties.surname = projectProperties.surname
        properties.forename = projectProperties.forename
        properties.pseudonym = projectProperties.pseudonym
        properties.scrivener_project = projectProperties.scrivener_project
        properties.aeon_project = projectProperties.aeon_project
        s.commit()

    @classmethod
    def get(cls):
        s = Session()
        return s.query(ProjectProperties).get(1)


class CoreCharacterLink(Base):
    __tablename__ = 'core_character'
    core_id = Column(Integer, ForeignKey('core.id'), primary_key=True)
    character_id = Column(Integer, ForeignKey('character.id'), primary_key=True)

    @classmethod
    def insertcoreCharacterLink(cls, coreCharacterLink):
        s = Session()
        s.add(coreCharacterLink)
        s.commit()


class TagCharacterLink(Base):
    __tablename__ = 'tag_character'
    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)
    character_id = Column(Integer, ForeignKey('character.id'), primary_key=True)

    @classmethod
    def add(cls, tagcharacterlink):
        d = cls()
        d.character_id = tagcharacterlink['character_id']
        d.tag_id = tagcharacterlink['tag_id']
        return d

    @classmethod
    def get(cls, id):
        s = Session()
        return s.query(TagCharacterLink).get(id)

    @classmethod
    def insertTagCharacterLink(cls, tagcharacterlink):
        s = Session()
        s.add(tagcharacterlink)
        s.commit()


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

    @classmethod
    def insertBiography(cls, biography):
        s = Session()
        s.add(biography)
        s.commit()
        return biography.id

    @classmethod
    def delete(cls, id):
        s = Session()
        s.query(Biography).filter(Biography.id == id).delete()
        s.commit()



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
    def insertTag(cls, tag):
        s = Session()
        s.add(tag)
        s.commit()

    @classmethod
    def hasTag(cls, tag):
        s = Session()
        return s.query(Tag).filter_by(description=tag).count() > 0

    @classmethod
    def getTag(cls, strDescription):
        s = Session()
        ret = s.query(Tag).filter_by(description=strDescription)
        c = cls()
        for tag in ret:
            c = tag
        return c

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
    def delete(cls, id):
        s = Session()
        s.query(SmartGroup).filter(SmartGroup.id == id).delete()
        s.commit()

    @classmethod
    def list(cls):
        s = Session()
        return s.query(SmartGroup).all()

    @classmethod
    def listCharacter(cls, rule):
        # rule = ( sex ==[cd] \"Male\" )
        s = Session()
        strRule = rule.replace("(", "").replace(")", "").replace('[cd]', "")
        lstRule = strRule.split()
        moreRule = ""
        isContains = False
        isBeginsWith = False
        isEndWith = False
        for i in lstRule:
            if isContains:
                moreRule = moreRule + ' "%' + i.replace('"','') + '%"'
                isContains = False
                continue

            if isBeginsWith:
                moreRule = moreRule + '"' + i.replace('"', '') + '%"'
                isBeginsWith = False
                continue

            if isEndWith:
                moreRule = moreRule + ' "%' + i.replace('"','') + '"'
                isEndWith = False
                continue

            elif i == "CONTAINS":
                moreRule = moreRule + ' ' + "LIKE"
                isContains = True

            elif i == "BEGINSWITH":
                moreRule = moreRule + ' ' + "LIKE"
                isBeginsWith = True

            elif i == "ENDWITH":
                moreRule = moreRule + ' ' + "LIKE"
                isEndWith = True

            else:
                moreRule = moreRule +  ' ' + i


        rs = s.execute('SELECT * FROM character WHERE ' + moreRule + ';')

        return rs


    @classmethod
    def toDict(cls):
        s = Session()
        smartGroups = s.query(SmartGroup).all()
        retorno = []
        for smartGroup in smartGroups:
            smartGroupStr = JsonTools.putMap('"id"', str(smartGroup.id)) + ','
            # smartGroupStr = smartGroupStr + JsonTools.putMap('"description"', '"' + smartGroup.description + '"')
            smartGroupStr = smartGroupStr + JsonTools.putMap('"description"', '"' + smartGroup.description + '"') + ','
            smartGroupStr = smartGroupStr + JsonTools.putMap('"rule"', '"' + smartGroup.rule.replace('"', '\\"')  + '"')
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
    def update(cls, core):
        s = Session()
        s.query(Core).filter(Core.id == core.id).update({'description': core.description})
        s.commit()

    @classmethod
    def delete(cls, id):
        s = Session()
        # deletar link character-core
        s.query(CoreCharacterLink).filter(CoreCharacterLink.core_id == id).delete()
        s.query(Core).filter(Core.id == id).delete()
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
    def listCharacters(cls, id):
        s = Session()
        return s.query(CoreCharacterLink).filter_by(core_id=id)
        s.commit()

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
    uuid = Column(Unicode(40))
    created = Column(Unicode(30))
    modified = Column(Unicode(30))
    name = Column(Unicode(200))
    archtype = Column(Unicode(30))
    date_of_birth = Column(Date())
    sex = Column(Unicode(5))
    age = Column(Unicode(3))
    local = Column(Unicode(200))
    imperfections = Column(Unicode(100))
    height = Column(Float(1, 2))
    weight = Column(Float(1, 2))
    body_type = Column(Unicode(100))
    month = Column(Unicode(50))
    eye_color = Column(Unicode(20))
    hair_color = Column(Unicode(20))
    arms = Column(Unicode(50))
    legs = Column(Unicode(50))
    face = Column(Unicode(100))
    background = Column(Unicode(1000))
    hobbies = Column(Unicode(500))
    picture = Column(String(200000))
    why = Column(Unicode(50))
    habits = Column(Unicode(500))
    costume = Column(Unicode(100))
    shoes = Column(Unicode(50))
    hands_gestures = Column(Unicode(100))
    feet_legs = Column(Unicode(100))
    trunk_head = Column(Unicode(100))
    home = Column(Unicode(100))
    favorite_room = Column(Unicode(100))
    view_from_the_window = Column(Unicode(100))
    vehicles = Column(Unicode(100))
    notes = Column(Unicode(1000))

    @classmethod
    def set_name(cls, intId, strName):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'name': strName.strip().upper()})
        s.commit()

    @classmethod
    def set_archtype(cls, intId, strArchtype):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'archtype': strArchtype})
        s.commit()

    @classmethod
    def set_age(cls, intId, strAge):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'age': strAge})
        s.commit()

    @classmethod
    def set_sex(cls, intId, strSex):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'sex': strSex})
        s.commit()

    @classmethod
    def set_dateOfBirth(cls, intId, datDate):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'date_of_birth': datDate})
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
    def set_bodyType(cls, intId, strBodyType):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'body_type': strBodyType.strip().upper()})
        s.commit()

    @classmethod
    def set_eyeColor(cls, intId, strEyeColor):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'eye_color': strEyeColor.strip().upper()})
        s.commit()

    @classmethod
    def set_hairColor(cls, intId, strHairColor):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'hair_color': strHairColor.strip().upper()})
        s.commit()

    @classmethod
    def set_ethinicity(cls, intId, strEthinicity):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'ethnicity': strEthinicity.strip().upper()})
        s.commit()

    @classmethod
    def set_health(cls, intId, strHealth):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'health': strHealth.strip().upper()})
        s.commit()

    @classmethod
    def set_background(cls, intId, strBackground):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'background': strBackground})
        s.commit()

    @classmethod
    def set_local(cls, intId, strLocal):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'local': strLocal.strip().upper()})
        s.commit()

    @classmethod
    def set_face(cls, intId, value):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'face': value.strip().upper()})
        s.commit()

    @classmethod
    def set_month(cls, intId, value):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'month': value.strip().upper()})
        s.commit()

    @classmethod
    def set_arms(cls, intId, value):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'arms': value.strip().upper()})
        s.commit()

    @classmethod
    def set_legs(cls, intId, value):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'legs': value.strip().upper()})
        s.commit()

    @classmethod
    def set_imperfections(cls, intId, value):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'imperfections': value.strip().upper()})
        s.commit()

    @classmethod
    def set_why(cls, intId, value):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'why': value.strip().upper()})
        s.commit()

    @classmethod
    def set_habits(cls, intId, value):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'habits': value.strip().upper()})
        s.commit()

    @classmethod
    def set_costume(cls, intId, value):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'costume': value.strip().upper()})
        s.commit()

    @classmethod
    def set_shoes(cls, intId, value):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'shoes': value.strip().upper()})
        s.commit()

    @classmethod
    def set_hands_gestures(cls, intId, value):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'hands_gestures': value.strip().upper()})
        s.commit()

    @classmethod
    def set_feet_legs(cls, intId, value):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'feet_legs': value.strip().upper()})
        s.commit()


    @classmethod
    def set_trunk_head(cls, intId, value):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'trunk_head': value.strip().upper()})
        s.commit()

    @classmethod
    def set_home(cls, intId, value):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'home': value.strip().upper()})
        s.commit()



    @classmethod
    def set_favorite_room(cls, intId, value):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'favorite_room': value.strip().upper()})
        s.commit()



    @classmethod
    def set_view_from_the_window(cls, intId, value):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'view_from_the_window': value.strip().upper()})
        s.commit()

    @classmethod
    def set_vehicles(cls, intId, value):
        s = Session()
        d = cls()
        d = d.get(intId)
        s.query(Character).filter(Character.id == d.id).update({'vehicles': value.strip().upper()})
        s.commit()

    @classmethod
    def add(cls, character):
        d = cls()
        dateformat = "%Y-%m-%d"
        d.id = character['id']
        d.uuid = character['uuid']
        d.created = character['created']
        d.modified = character['modified']
        d.name = character['name'].strip().upper().replace('\"', '"')
        d.archtype = character['archtype']
        if character['date of birth'] and character['date of birth'] != "":
            d.date_of_birth = datetime.strptime(character['date of birth'], dateformat)
        d.sex = character['sex']
        d.age = character['age'].strip()
        d.local = character['local'].strip().upper()
        d.face = character['face'].strip().upper()
        d.month = character['month']
        d.height = character['height']
        d.weight = character['weight']
        d.body_type = character['body type'].strip().upper()
        d.imperfections = character['imperfections'].strip().upper()
        d.eye_color = character['eye color'].strip().upper()
        d.hair_color = character['hair color'].strip().upper()
        d.arms = character['arms'].strip().upper()
        d.legs = character['legs'].strip().upper()
        d.background = character['background']
        d.hobbies = character['hobbies']
        d.picture = character['picture']
        d.why = character['why']
        d.habits = character['habits']
        d.costume = character['costume']
        d.shoes = character['shoes']
        d.hands_gestures = character['hands gestures']
        d.feet_legs =  character['feet legs']
        d.trunk_head = character['trunk head']
        d.home = character['home']
        d.favorite_room = character['favorite room']
        d.view_from_the_window = character['view from the window']
        d.vehicles = character['vehicles']
        d.notes = character['notes']
        return d

    @classmethod
    def delete(cls, id):
        s = Session()
        s.query(CoreCharacterLink).filter(CoreCharacterLink.character_id == id).delete()
        s.query(TagCharacterLink).filter(TagCharacterLink.character_id == id).delete()
        s.query(Character).filter(Character.id == id).delete()
        s.commit()

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
    def removeCharacterOfCore(cls, id):
        s = Session()
        s.query(CoreCharacterLink).filter(CoreCharacterLink.character_id == id).delete()
        s.commit()

    @classmethod
    def hasTag(cls, intCharacter, strTag):
        s = Session()
        t = Tag()
        t = t.getTag(strTag)
        return s.query(TagCharacterLink).filter_by(tag_id=t.id, character_id=intCharacter).count() > 0

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
    def getGuid(cls, uuid):
        s = Session()
        return s.query(Character).filter_by(uuid=uuid)


    @classmethod
    def toDict(cls):
        s = Session()
        characters = s.query(Character).all()

        retorno = []
        for character in characters:
            characterStr = JsonTools.putMap('"id"', str(character.id)) + ','
            characterStr = characterStr + JsonTools.putMap('"uuid"', '"' + character.uuid + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"created"', '"' + character.created + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"modified"', '"' + character.modified + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"name"', '"' + str(character.name).replace('"', '\\"') + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"sex"', '"' + str(character.sex) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"archtype"', '"' + str(character.archtype) + '"') + ','
            if character.date_of_birth != None:
                characterStr = characterStr + JsonTools.putMap('"date of birth"','"' + str(character.date_of_birth) + '"') + ','
            else:
                characterStr = characterStr + JsonTools.putMap('"date of birth"', '""') + ','
            characterStr = characterStr + JsonTools.putMap('"age"', '"' + str(character.age) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"local"', '"' + str(character.local) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"face"', '"' + str(character.face) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"month"','"' + str(character.month) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"height"', str("{:.2f}".format(character.height))) + ','
            characterStr = characterStr + JsonTools.putMap('"weight"', str("{:.2f}".format(character.weight))) + ','
            characterStr = characterStr + JsonTools.putMap('"body type"', '"' + str(character.body_type) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"imperfections"', '"' + str(character.imperfections) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"eye color"', '"' + str(character.eye_color) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"hair color"', '"' + str(character.hair_color) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"arms"', '"' + str(character.arms) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"legs"', '"' + str(character.legs) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"background"', '"' + str(character.background) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"hobbies"', '"' + str(character.hobbies) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"picture"', '"' + str(character.picture) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"why"', '"' + str(character.why) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"habits"', '"' + str(character.habits) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"costume"', '"' + str(character.costume) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"shoes"', '"' + str(character.shoes) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"hands gestures"', '"' + str(character.hands_gestures) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"feet legs"', '"' + str(character.feet_legs) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"trunk head"', '"' + str(character.trunk_head) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"home"', '"' + str(character.home) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"favorite room"', '"' + str(character.favorite_room) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"view from the window"', '"' + str(character.view_from_the_window) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"vehicles"', '"' + str(character.vehicles) + '"') + ','
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
                strDestinationCore = JsonTools.putMap('"destination"', '"core"') + ", "
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
                strIdTag = ""

            if strIdTag:
                strDestinationTag = JsonTools.putMap('"destination"', '"tag"') + ", "
                strDestinationTag = strDestinationTag + JsonTools.putMap('"idrefs"', strIdTag)
                strDestinationTag = JsonTools.putObject(strDestinationTag)

            if strDestinationCore:
                strRelationship = strDestinationCore
                if strDestinationTag:
                    strRelationship += ", " + strDestinationTag
            else:
                if strDestinationTag:
                    strRelationship += strDestinationTag

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
            session.execute(table.delete())
        session.commit()

    def drop_table(self, table_name):
        base = declarative_base()
        metadata = MetaData(engine, reflect=True)
        table = metadata.tables.get(table_name)
        if table is not None:
            logging.info(f'Deleting {table_name} table')
            base.metadata.drop_all(engine, [table], checkfirst=True)
