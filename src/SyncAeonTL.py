# -*- coding: utf-8 -*-

import json
import zipfile
from zipfile import ZipFile
from DataAccess import Character
from datetime import datetime


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
    mydata = None
    data = None
    with ZipFile(AeonProjectFile, "r") as z:
        for filename in z.namelist():
            print(filename)
            with z.open(filename) as f:
                data = f.read()
                mydata = json.loads(data.decode("utf-8"))

    print(mydata["entities"])

    guidCharacter = findGuidTemplateCharacter(mydata)

    character = Character()

    lstEntities = mydata["entities"]
    characters = character.list()

    if len(lstEntities) != 0:
        for i in lstEntities:
            if i["entityType"] == guidCharacter:
                print(i["guid"])
                print(i["name"].encode("utf-8"))
                print(i["notes"])
                # pesquisar guid na base de dados se não existir incluir
                # se existir atualizar o aeon com os dados da base de dados.
                query = character.getGuid(i["guid"])
                guidPerson = i["guid"]
                if query.count()==0:
                    c = Character()
                    c.uuid = i["guid"]
                    c.name = i["name"]
                    c.background  = i["notes"]
                    c.created = datetime.now().strftime('%Y-%m-%d %H:%M:%m')
                    c.modified = datetime.now().strftime('%Y-%m-%d %H:%M:%m')
                    c.height = 0.00
                    c.weight = 0.00
                    c.age = 0
                    c.sex = "--"
                    c.local = ""
                    c.date_of_birth = ""
                    c.background = ""
                    c.ethnicity = ""
                    c.hair_color = ""
                    c.eye_color = ""
                    c.body_type = ""
                    c.archtype = ""
                    c.insertCharacter(c)
                else:
                    for c in query:
                        for j in range(len(mydata["entities"])):
                            if mydata["entities"][j]["guid"] == guidPerson:
                                c.getGuid(mydata["entities"][j]["guid"])
                                mydata["entities"][j]["name"] = c.name
                                mydata["entities"][j]["notes"] = c.background
                                break

    elif len(characters) != 0:
        # Se houver personagens na base gravar no json
        strEntities = []

        for c in characters:
            dictPerson = {
                "createRangePosition": {
                    "precision": "day",
                    "rangePropertyGuid": "B327CAD3-1CE1-475E-8F7A-C709D294EF2E",
                    "timestamp": 61921152000
                },
                "entityType": "6C857017-8B69-43D5-BD6A-B4A9B0A4A2EF",
                "guid": "",
                "icon": "person",
                "name": "",
                "notes": "",
                "sortOrder": 1,
                "swatchColor": "red"
            }
            dictPerson["guid"] = c.uuid
            dictPerson["name"] = c.name
            dictPerson["notes"] = c.background
            strEntities.append(dictPerson)

        mydata["entities"] = strEntities

    # Gravar os dados
    zf = zipfile.ZipFile(AeonProjectFile, mode="w", compression=zipfile.ZIP_DEFLATED)
    zf.writestr("timeline.json", json.dumps(mydata))
    zf.close()