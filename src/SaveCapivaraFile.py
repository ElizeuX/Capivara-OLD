from sqlalchemy import create_engine, Column, Unicode, Integer, Float, ForeignKey, MetaData, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from logger import Logs
import os, json
from datetime import datetime

from Utils import JsonTools
from DataAccess import DataUtils, FileInformation, ProjectProperties, Character, Core, SmartGroup, Tag, Biography, \
    CoreCharacterLink, TagCharacterLink

def saveCapivaraFile(capivaraFile = None):
    logs = Logs(filename="capivara.log")
    logs.record("Salvando arquivo:  %s" % capivaraFile, type="info")

    try:
        arquivo = __InsertFileInformationOnFile()

        propriedadesDoProjeto = __InsertProjectPropertiesOnFile()

        # Juntando dados do arquivo com as propriedades do projeto
        arquivo = arquivo + ', ' + propriedadesDoProjeto

        dadosPersonagem = __InsertCharaterOnFile()
        arquivo = arquivo + ',' + dadosPersonagem

        dadosCore = __InsertCoreOnFile()
        arquivo = arquivo + ',' + dadosCore

        dadosSmartGroup = __InsertSmartGroupOnFile()
        arquivo = arquivo + ',' + dadosSmartGroup

        dadosTags = __InsertTagOnFile()
        arquivo = arquivo + ',' + dadosTags

        arquivo = JsonTools.putObject(arquivo)

        json_acceptable_string = arquivo.replace("'", "\"")
        json_object = json.loads(json_acceptable_string)
    except:
        logs.record("Aconteceu um erro inesperado ao salvar o arquivo %s " + capivaraFile)
        raise UnexpectedError(30, "Não foi possível salvar o arquivo")

    # Write JSON file
    try:
        with open(capivaraFile, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(json_object,
                              indent=4, sort_keys=False,
                              separators=(',', ': '), ensure_ascii=False)
            outfile.write(str_)
    except:
        logs.record("Não foi possível salvar o arquivo %s " + capivaraFile)
        raise WritingFileError(20, "Não foi possível salvar o arquivo")

    finally:
        pass


# TODO: Atribuir código de erro
class WritingFileError(Exception):
    def __init__(self, error_code, *args, **kwargs):
        super(WritingFileError, self).__init__(*args, **kwargs)
        self.error_code = error_code

# TODO: Atribuir código de erro
class UnexpectedError(Exception):
    def __init__(self, error_code, *args, **kwargs):
        super(UnexpectedError, self).__init__(*args, **kwargs)
        self.error_code = error_code

def __InsertTagOnFile():
    # Incluindo tags
    tag = Tag()
    dadosTags = tag.dictBuffer()
    dadosTags = '"tag" : ' + dadosTags
    return dadosTags


def __InsertSmartGroupOnFile():
    # Incluindo Smart Group
    smartGroup = SmartGroup()
    dadosSmartGroup = smartGroup.toDict()
    dadosSmartGroup = '"smart group" : ' + dadosSmartGroup
    return dadosSmartGroup


def __InsertCoreOnFile():
    # Incluindo Core
    core = Core()
    dadosCore = core.toDict()
    dadosCore = '"core" : ' + dadosCore
    return dadosCore


def __InsertCharaterOnFile():
    # INCLUINDO PERSONAGEM
    characters = Character()
    dadosPersonagem = characters.toDict()
    dadosPersonagem = '"character" : ' + dadosPersonagem
    return dadosPersonagem


def __InsertProjectPropertiesOnFile():
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
    propriedadesDoProjeto = propriedadesDoProjeto + JsonTools.putMap('"abbreviated title"',
                                                                     '"' + abbreviatedTitle + '"') + ','
    propriedadesDoProjeto = propriedadesDoProjeto + JsonTools.putMap('"authors full name"',
                                                                     '"' + authorsFullName + '"') + ','
    propriedadesDoProjeto = propriedadesDoProjeto + JsonTools.putMap('"surname"', '"' + surname + '"') + ','
    propriedadesDoProjeto = propriedadesDoProjeto + JsonTools.putMap('"forename"', '"' + forename + '"') + ','
    propriedadesDoProjeto = propriedadesDoProjeto + JsonTools.putMap('"pseudonym"', '"' + pseudonym + '"')
    propriedadesDoProjeto = '"project properties" : ' + JsonTools.putObject(propriedadesDoProjeto)
    return propriedadesDoProjeto


def __InsertFileInformationOnFile():
    now = datetime.now()
    versionModel = "0.1.0"
    creator = "Capivara 0.1.0"
    device = os.environ['COMPUTERNAME']
    modified = str(now.today())
    # DADOS GERAIS DO ARQUIVO
    arquivo = JsonTools.putMap('"version model"', '"' + versionModel + '"') + ','
    arquivo = arquivo + JsonTools.putMap('"creator"', '"' + creator + '"') + ','
    arquivo = arquivo + JsonTools.putMap('"device"', '"' + device + '"') + ','
    arquivo = arquivo + JsonTools.putMap('"modified"', '"' + modified + '"')
    return arquivo