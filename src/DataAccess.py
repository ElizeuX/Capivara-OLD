from sqlalchemy import create_engine, Column, Unicode, Integer, Float, ForeignKey, MetaData, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import logging
from Utils import JsonTools

import json
import os
from datetime import datetime

#engine = create_engine('sqlite:///capivara.db', echo=False)
engine = create_engine('sqlite://', echo=False)
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)
connection = engine.connect()
metadata = MetaData(bind=engine, reflect=True)


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
    abbreviatedTitle = Column(Unicode(100))
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
    def dictBuffer(cls):
        s = Session()
        smartGroups = s.query(SmartGroup).all()
        retorno = []
        for smartGroup in smartGroups:
            smartGroupStr = JsonTools.putMap('"id"', str(smartGroup.id)) + ','
            smartGroupStr = smartGroupStr + JsonTools.putMap('"description"', '"' + smartGroup.description + '"')
            #smartGroupStr = smartGroupStr + JsonTools.putMap('"description"', '"' + smartGroup.description  + '"') + ','
            #smartGroupStr = smartGroupStr + JsonTools.putMap('"rule"', '"' + smartGroup.rule  + '"')
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
    def list(cls):
        s = Session()
        return s.query(Core).all()

    @classmethod
    def dictBuffer(cls):
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
    picture = Column(Unicode(200000))
    notes = Column(Unicode(1000))
    tag = Column(Unicode(50))
    biography = relationship("Biography")

    @classmethod
    def add(cls, character):
        d = cls()
        d.id = character['id']
        d.name = character['name']
        d.sex = character['sex']
        d.local = character['local']
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
    def getBiografia(cls):
        s = Session()
        result = s.query(Character, Biography).filter_by(id).all()

    @classmethod
    def dictBuffer(cls):
        s = Session()
        characters = s.query(Character).all()

        retorno = []
        for character in characters:
            characterStr = JsonTools.putMap('"id"', str(character.id)) + ','
            #characterStr = characterStr + JsonTools.putMap('"name"', '"' + str(character.name) + '"') + ','
            characterStr = characterStr + JsonTools.putMap('"name"', '"' + str(character.name) + '"')
            # characterStr = characterStr + JsonTools.putMap('"sex"', '"' + str(character.sex) + '"') + ','
            # characterStr = characterStr + JsonTools.putMap('"local"', '"' + str(character.local) + '"') + ','
            # characterStr = characterStr + JsonTools.putMap('"occupation"', '"' + str(character.occupation) + '"') + ','
            # characterStr = characterStr + JsonTools.putMap('"position social"', '"' + str(character.position_social)  + '"') + ','
            # characterStr = characterStr + JsonTools.putMap('"height"', '"' + str(character.height) + '"') + ','
            # characterStr = characterStr + JsonTools.putMap('"weight"', '"' + str(character.weight) + '"') + ','
            # characterStr = characterStr + JsonTools.putMap('"body type"', '"' + str(character.body_type) + '"') + ','
            # characterStr = characterStr + JsonTools.putMap('"appearance"', '"' + str(character.appearance) + '"') + ','
            # characterStr = characterStr + JsonTools.putMap('"eye color"', '"' + str(character.eye_color) + '"') + ','
            # characterStr = characterStr + JsonTools.putMap('"hair color"', '"' + str(character.hair_color) + '"') + ','
            # characterStr = characterStr + JsonTools.putMap('"ethnicity"', '"' + str(character.ethnicity) + '"') + ','
            # characterStr = characterStr + JsonTools.putMap('"health"', '"' + str(character.health) + '"') + ','
            # characterStr = characterStr + JsonTools.putMap('"standing features"', '"' + str(character.standing_features) + '"') + ','
            # characterStr = characterStr + JsonTools.putMap('"background"', '"' + str(character.background) + '"') + ','
            # characterStr = characterStr + JsonTools.putMap('"hobbies"', '"' + str(character.hobbies) + '"') + ','
            # characterStr = characterStr + JsonTools.putMap('"picture"', '"' + str(character.picture) + '"') + ','
            # # characterStr = characterStr + JsonTools.putMap('"notes"', '"' + str(character.notes) + '"') + ','
            # characterStr = characterStr + JsonTools.putMap('"notes"', '"' + str(character.notes) + '"')

            # i = character.id
            # strBiografia = ""
            # result = s.query(Biography).filter(Biography.id_character == i)
            #
            # if result.count() > 0:
            #     for row in result:
            #         strBio = ""
            #         strBio = strBio + JsonTools.putMap('"year"', str(row.year)) + ','
            #         strBio = strBio + JsonTools.putMap('"description"', '"' + str(row.description) + '"')
            #         strBio = JsonTools.putObject(strBio) + ','
            #         strBiografia = strBiografia + strBio
            #     strBiografia = JsonTools.putMap('"biography"', JsonTools.putArray(strBiografia[:-1]))
            # else:
            #     strBiografia = JsonTools.putMap('"biography"', "[]")
            #
            # characterStr = characterStr + strBiografia
            #
            # # OBTER OS RELACIONAMENTOS COM O CORE
            # result = s.query(CoreCharacterLink).filter(CoreCharacterLink.character_id == i)
            # strIdCore = []
            # if result.count() > 0:
            #     for row in result:
            #         strIdCore.append(str(row.core_id))
            #     strIdCore = ",".join(strIdCore)
            #     strIdCore = JsonTools.putArray(strIdCore.replace("'", ""))
            # else:
            #     strIdCore = JsonTools.putMap("[]")
            #
            # strDestinationCore = JsonTools.putMap('"destination"', '"core"')  + ", "
            # strDestinationCore = strDestinationCore + JsonTools.putMap('"idrefs"', strIdCore)
            # strDestinationCore = JsonTools.putObject(strDestinationCore)
            #
            # # OBTER OS RELACIONAMENTOS COM O TAG
            # result = s.query(TagCharacterLink).filter(TagCharacterLink.character_id == i)
            # strIdTag = []
            # if result.count() > 0:
            #     for row in result:
            #         strIdTag.append(str(row.tag_id))
            #     strIdTag = ",".join(strIdTag)
            #     strIdTag = JsonTools.putArray(strIdTag.replace("'", ""))
            # else:
            #     strIdTag  = JsonTools.putMap("[]")
            #
            # strDestinationTag = JsonTools.putMap('"destination"', '"tag"') + ", "
            # strDestinationTag = strDestinationTag + JsonTools.putMap('"idrefs"', strIdTag)
            # strDestinationTag = JsonTools.putObject(strDestinationTag)
            #
            # strRelationship = strDestinationCore + ", " + strDestinationTag
            # strRelationship = JsonTools.putMap('"relationship"', JsonTools.putArray(strRelationship))
            #
            # characterStr = characterStr + ", " + strRelationship
            #

            retorno.append(JsonTools.putObject(characterStr))

        return JsonTools.putArray(', '.join(retorno))


class DataUtils():

    def __init__(self):
        pass
        # self.drop_table('character')
        # self.drop_table('group')
        # self.drop_table('smart_group')
        # self.drop_table('tag')
        # self.drop_table('biography')

    def truncate_db(self):
        # delete all table data (but keep tables)
        # we do cleanup before test 'cause if previous test errored,
        # DB can contain dust
        #meta = MetaData(bind=engine, reflect=True)
        # trans = connection.begin()
        # connection.execute('SET FOREIGN_KEY_CHECKS = 0;')
        # for table in metadata.sorted_tables:
        #     connection.execute(table.delete())
        # connection.execute('SET FOREIGN_KEY_CHECKS = 1;')
        # trans.commit()
        # meta = Base.metadata
        # s = Session()
        # for table in reversed(meta.sorted_tables):
        #     print('Clear table %s' % table)
        #     s.execute(table.delete())
        # s.commit()
        # for all records
        s = Session()
        s.query(CoreCharacterLink).delete()
        s.query(TagCharacterLink).delete()
        s.query(Biography).delete()
        s.query(Character).delete()
        s.query(Core).delete()
        s.query(SmartGroup).delete()
        s.query(Tag).delete()
        s.query(FileInformation).delete()
        s.query(ProjectProperties).delete()
        s.commit()



    def drop_table(self, table_name):
        base = declarative_base()
        metadata = MetaData(engine, reflect=True)
        table = metadata.tables.get(table_name)
        if table is not None:
            logging.info(f'Deleting {table_name} table')
            base.metadata.drop_all(engine, [table], checkfirst=True)

    def LoadCapivaraFileEmpty(self, propertiesProject):
        logging.info("Gravando objetos na base de dados.")

        Base.metadata.create_all()
        self.truncate_db()
        now = datetime.now()

        s = Session()
        # Incluir dados do arquivo
        c = FileInformation()
        c.versionModel = "0.1.0"
        c.creator = "Capivara 0.1.0"
        c.device = os.environ['COMPUTERNAME']
        c.modified = str(now.today())
        s.add(c)
        s.commit()

        # Incluir propriedades do projeto
        c = ProjectProperties()
        c.title = propertiesProject['title']
        c.authorsFullName = propertiesProject['authors full name']
        c.surname = propertiesProject['surname']
        c.forename = propertiesProject['forename']
        c.pseudonym = propertiesProject['pseudonym']
        s.add(c)
        s.commit()

        c = Character()
        c.name = "unnamed"
        s.add(c)
        s.commit()

        # Retornar o dict com os dados carregados no banco de dados
        c = SmartGroup()
        __smartgroups__ = '"smart group":' + c.dictBuffer()
        dictReturn = __smartgroups__ + ','
        c = Core()
        __cores__ = '"core" :' + c.dictBuffer()
        dictReturn = dictReturn + __cores__ + ','

        c = Character()
        __charaters__ = '"character":' + c.dictBuffer()
        dictReturn = '{' + dictReturn + __charaters__ + '}'

        json_acceptable_string = dictReturn.replace("'", "\"")
        dict_object = json.loads(json_acceptable_string)

        return dict_object

    def loadCapivaraFile(self, fileOpen):
        capivara = JsonTools.loadFile(fileOpen)
        logging.info("Gravando objetos na base de dados.")

        Base.metadata.create_all()

        self.truncate_db()

        s = Session()
        # Incluir dados do arquivo
        c = FileInformation()
        c.versionModel = capivara['version model']
        c.creator = capivara['creator']
        c.device = capivara['device']
        c.modified = capivara['modified']
        s.add(c)
        s.commit()

        #Incluir propriedades do projeto
        c = ProjectProperties()
        c.title = capivara['project properties']['title']
        c.abbreviatedTitle = capivara['project properties']['abbreviated title']
        c.authorsFullName = capivara['project properties']['authors full name']
        c.surname = capivara['project properties']['surname']
        c.forename = capivara['project properties']['forename']
        c.pseudonym = capivara['project properties']['pseudonym']
        s.add(c)
        s.commit()

        # INCLUIR TODOS OS OBJETOS DO ARQUIVO JSON
        for character in capivara['character']:
            c = Character.add(character)
            s.add(c)
            s.commit()

        for core in capivara['core']:
            c = Core.add(core)
            s.add(c)
            s.commit()

        for smart_group in capivara['smart group']:
            c = SmartGroup.add(smart_group)
            s.add(c)
            s.commit()

        for tag in capivara['tag']:
            c = Tag.add(tag)
            s.add(c)
            s.commit()

        for character in capivara['character']:
            for bio in character['biography']:
                bioDict = {}
                bioDict['id_character'] = character['id']
                bioDict['year'] = bio['year']
                bioDict['description'] = bio['description']
                c = Biography.add(bioDict)
                s.add(c)
                s.commit()

        # MARCAR OS RELACIONAMENTOS
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

        # Retornar o dict com os dados carregados no banco de dados
        c = SmartGroup()
        __smartgroups__ =  '"smart group":' + c.dictBuffer()
        dictReturn = __smartgroups__ + ','
        c = Core()
        __cores__ = '"core" :' +c.dictBuffer()
        dictReturn = dictReturn + __cores__ + ','

        c = Character()
        __charaters__ = '"character":' + c.dictBuffer()
        dictReturn = '{' + dictReturn + __charaters__ +'}'

        json_acceptable_string = dictReturn.replace("'", "\"")
        dict_object = json.loads(json_acceptable_string)

        return dict_object

    def saveCapivaraFile(self, capivaraFile):

        logging.info("Salvando arquivo " + capivaraFile)

        jsonTools = JsonTools()
        dataUtils = DataUtils()
        now = datetime.now()

        versionModel = "0.1.0"
        creator = "Capivara 0.1.0"
        device = os.environ['COMPUTERNAME']
        modified = str(now.today())

        # DADOS GERAIS DO ARQUIVO
        arquivo = JsonTools.putMap('"version model"', '"' + versionModel + '"') + ','
        arquivo = arquivo + JsonTools.putMap('"creator"',  '"' + creator + '"') + ','
        arquivo = arquivo + JsonTools.putMap('"device"', '"' + device + '"') + ','
        arquivo = arquivo + JsonTools.putMap('"modified"', '"' + modified + '"')
        logging.info(arquivo)

        # PEGAR PROPRIEDADES DO PROJETO
        projectProperties = ProjectProperties.get()
        abbreviatedTitle = "TSCF"
        title = projectProperties.title
        authorsFullName = projectProperties.authorsFullName
        surname = projectProperties.surname
        forename = projectProperties.forename
        pseudonym = projectProperties.pseudonym

        # PROPRIEDADE DO PROJETO
        propriedadesDoProjeto = JsonTools.putMap('"title"', '"' + title + '"') + ','
        propriedadesDoProjeto = propriedadesDoProjeto + JsonTools.putMap('"abbreviated title"', '"' + abbreviatedTitle + '"') + ','
        propriedadesDoProjeto = propriedadesDoProjeto + JsonTools.putMap('"authors full name"', '"' + authorsFullName + '"') + ','
        propriedadesDoProjeto = propriedadesDoProjeto + JsonTools.putMap('"surname"', '"' + surname + '"') + ','
        propriedadesDoProjeto = propriedadesDoProjeto + JsonTools.putMap('"forename"', '"' + forename + '"') + ','
        propriedadesDoProjeto = propriedadesDoProjeto + JsonTools.putMap('"pseudonym"', '"' + pseudonym + '"')
        propriedadesDoProjeto = '"project properties" : ' + JsonTools.putObject(propriedadesDoProjeto)

        # Juntando dados do arquivo com as propriedades do projeto
        arquivo = arquivo + ', ' + propriedadesDoProjeto

        # INCLUINDO PERSONAGEM
        characters = Character()
        dadosPersonagem = characters.dictBuffer()
        dadosPersonagem = '"character" : ' + dadosPersonagem
        arquivo = arquivo + ',' + dadosPersonagem

        # Incluindo Core
        core = Core()
        dadosCore = core.dictBuffer()
        dadosCore = '"core" : ' + dadosCore
        arquivo = arquivo + ',' + dadosCore

        # Incluindo Smart Group
        smartGroup = SmartGroup()
        dadosSmartGroup = smartGroup.dictBuffer()
        dadosSmartGroup = '"smart group" : ' + dadosSmartGroup
        arquivo = arquivo + ',' + dadosSmartGroup

        # Incluindo tags
        tag = Tag()
        dadosTags = tag.dictBuffer()
        dadosTags = '"tag" : ' + dadosTags
        arquivo = arquivo + ',' + dadosTags

        arquivo = JsonTools.putObject(arquivo)

        logging.info(arquivo)

        json_acceptable_string = arquivo.replace("'", "\"")
        logging.info('json_acceptable_string =' + json_acceptable_string)
        json_object = json.loads(json_acceptable_string)

        # Write JSON file
        with open(capivaraFile, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(json_object,
                              indent=4, sort_keys=False,
                              separators=(',', ': '), ensure_ascii=False)
            outfile.write(str_)
