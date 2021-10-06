# -*- coding: utf-8 -*-

import json
import zipfile
from zipfile import ZipFile
from DataAccess import Character, CharacterMap
from datetime import datetime
import pandas as pd

def dateToTimestamp(value):
    my_datetime = datetime(value.year, value.month, value.day)
    result = 0
    try:
        result = datetime.timestamp(my_datetime)
    except:
        print (type(my_datetime))

    return result

def findGuidTemplateCharacter(mydata):
    # Localizar o guid do Template Character
    # Versão "name" : "Aeon Timeline 1.x Template", name == Person
    # Versão  "name" : "Date-based Fiction Template", name == Character
    guidCharacter = ""
    for i in mydata["template"]["types"]:
        if i["name"] == "Character":
            guidCharacter = i["guid"]
            break
    return guidCharacter

def SyncAeonTimeLine(AeonProjectFile):
    # TODO: Colocar logs
    # TODO: Capiturar erros
    # TODO: Tratar timestamp do personagem
    # TODO: Verificar quem é o rangePropertyGuid

    mydata = None
    data = None
    with ZipFile(AeonProjectFile, "r") as z:
        for filename in z.namelist():
            print(filename)
            with z.open(filename) as f:
                data = f.read()
                mydata = json.loads(data.decode("utf-8"))

    guidCharacter = findGuidTemplateCharacter(mydata)

    character = Character()

    lstEntities = mydata["entities"]
    characters = character.list()

    # Atualizar os personagens no AeonTL
    if len(lstEntities) != 0:
        for i in lstEntities:
            if i["entityType"] == guidCharacter:
                query = character.getGuid(i["guid"])
                guidPerson = i["guid"]
                if query.count() != 0:
                    for c in query:
                        for j in range(len(mydata["entities"])):
                            if mydata["entities"][j]["guid"] == guidPerson:
                                c.getGuid(mydata["entities"][j]["guid"])
                                mydata["entities"][j]["name"] = c.name
                                mydata["entities"][j]["notes"] = c.notes
                                break
                else:
                    # TODO: Levantar a exception e gravar na log.
                    print("Erro")
                    print('Personagem "%s" existe no AeonTL mas não tem a Capivara dele' % guidPerson)

    # Incluir novos personagens no AeonTL
    if characters.count() > 0:
        strEntities = []
        for c in characters:
            guidPerson = c.uuid
            found = False
            for i in lstEntities:
                if i["entityType"] == guidCharacter:
                    if i["guid"] == guidPerson:
                        found = True
                        break

            if not found:
                 dictPerson = {
                     "createRangePosition": {
                         "precision": "day",
                         "rangePropertyGuid": "B327CAD3-1CE1-475E-8F7A-C709D294EF2E",
                         "timestamp": 0
                     },
                     "entityType": guidCharacter,
                     "guid": "",
                     "icon": "person",
                     "name": "",
                     "notes": "",
                     "sortOrder": 1,
                     "swatchColor": "red"
                 }
                 dictPerson["guid"] = c.uuid
                 dictPerson["name"] = c.name
                 dictPerson["notes"] = c.notes
                 mydata["entities"].append(dictPerson)


    # Gravar os dados
    zf = zipfile.ZipFile(AeonProjectFile, mode="w", compression=zipfile.ZIP_DEFLATED)
    zf.writestr("timeline.json", json.dumps(mydata))
    zf.close()
