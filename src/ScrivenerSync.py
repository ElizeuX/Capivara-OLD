# -*- coding: utf-8 -*-

from DataAccess import Character
from Utils import generate_uuid, capitalizeFirstCharacter
import xml.etree.ElementTree as ET
from xml.dom import minidom

import os


def fileRtfName(id):
    return str(id)+ ".rtf"

def createRtfFile(rtfFileName, character):
    dirDocs = "C:/Users/Elizeu/OneDrive - PRODESP/Documents/My Capivaras/scrivener_teste/teste4.scriv/Files/Docs" + "\n"
    rtfFile = "{\\rtf1\\ansi\\ansicpg1252\\uc1\deff0" + "\n"
    rtfFile += "{\\fonttbl{\\f0\\fnil\\fcharset0\\fprq2 CourierNewPSMT;}{\\f1\\fnil\\fcharset0\\fprq2 Arial-ItalicMT;}{\\f2\\fnil\\fcharset0\\fprq2 ArialMT;}{\\f3\\fnil\\fcharset0\\fprq2 Arial-BoldMT;}}" + "\n"
    rtfFile +=  "{\\colortbl;\\red0\\green0\\blue0;\\red255\\green255\\blue255;\\red255\\green0\\blue0;\\red30\\green79\\blue159;}" + "\n"
    rtfFile +=  "\\paperw12240\\paperh15840\\margl1800\\margr1800\\margt1440\\margb1440\\fet2\\ftnbj\\aenddoc" + "\n"
    rtfFile +=  "\\pgnrestart\\pgnstarts0" + "\n"
    rtfFile +=  "\\pard\\plain \\tx0\\tqr\\tx2700\\tx3110\\tx3740\\sb160\\sl288\\slmult1\\qc\\ltrch\\loch {\\f1\\fs20\\b0\\i1\\cf3 [READ ONLY - MANAGER BY CAPIVARA]}"+ "\n"
    rtfFile += "\\par\\plain {\\f2\\fs40\\b0\\i0\\cf4 " + capitalizeFirstCharacter(character.name) + "}" + "\n"
    rtfFile += "\\par\\pard\\plain \\fi360\\sl360\\slmult1\\qj\\ltrch\\loch \\f2\\fs40\\b0\\i0\\cf4" + "\n"
    rtfFile += "\\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Arqu\\loch\\af3\\hich\\af3\\dbch\\af3\\uc1\\u233\\'E9tipo: }" + "\n"
    rtfFile +=  "\\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Data de nasc.:}" + "\n"
    rtfFile +=  "\\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Idade: " + character.age + "}\n"
    rtfFile +=  "\\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Sexo: "  + character.sex + "}\n"
    rtfFile +=  "\\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Altura: " + '{0:.2f}'.format(character.height) + "m}\n"
    rtfFile +=  "\\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Peso: " + '{0:.2f}'.format(character.weight) + "kg}" + "\n"
    rtfFile +=  "\\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Tipo de corpo: " + capitalizeFirstCharacter(character.body_type) + "}{\\f2\\fs26\\b0\\i0 \\tab }" + "\n"
    rtfFile +=  "\\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Cor dos olhos: " + capitalizeFirstCharacter(character.eye_color) + "}" + "\n"
    rtfFile +=  "\\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Cor dos cabelos: " + capitalizeFirstCharacter(character.hair_color) + "}" + "\n"
    rtfFile +=  "\\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Etnicidade: " + capitalizeFirstCharacter(character.ethnicity) + "}" + "\n"
    rtfFile +=  "\\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Sa\\loch\\af3\\hich\\af3\\dbch\\af3\\uc1\\u250\\'FAde:}" + "\n"
    rtfFile +=  "\\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Local: " + character.local + "}" + "\n"
    rtfFile +=  "\\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Background:}" + "\n"
    rtfFile +=  "\\par\\plain {\\f3\\fs26\\b1\\i0 Biografia}" + "\n"
    rtfFile +=  "\\par\\plain {\\f3\\fs26\\b1\\i0 Ano                             Evento}" + "\n"
    rtfFile +=  "\\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch \\f3\\fs26\\b1\\i0" + "\n"
    rtfFile +=  "\\par\\pard\\plain \\fi360\\sl360\\slmult1\\qj\\ltrch\\loch \\f2\\fs40\\b0\\i0\\cf4" + "\n"
    rtfFile +=  "\\par\\plain \\f2\\fs40\\b0\\i0\\cf4" + "\n"
    rtfFile +=  "\\par\\plain \\f2\\fs40\\b0\\i0\\cf4" + "\n"
    rtfFile +=  "\\par\\plain \\f2\\fs40\\b0\\i0\\cf4}" + "\n"


    with open(rtfFileName, "w") as arquivo:
        arquivo.write(rtfFile)


def putCharacter(id, character, binderItem):
    binderItem.attrib["ID"] = str(id)
    binderItem.attrib["UUID"] = str(generate_uuid())
    binderItem.attrib["Created"] = character.created + " -0300"
    binderItem.attrib["Modified"] = character.modified + " -0300"
    binderItem.attrib["Type"] = "Text"
    title = ET.SubElement(binderItem, 'Title')
    title.text = capitalizeFirstCharacter(character.name)
    metadata = ET.SubElement(binderItem, 'Metadata')
    labelID = ET.SubElement(metadata, 'LabelID')
    labelID.text = "6"
    includeInCompile = ET.SubElement(metadata, 'IncludeInCompile')
    includeInCompile.text = "Yes"
    fileExtension = ET.SubElement(metadata, 'FileExtension')
    fileExtension.text = "rtf"
    iconFileName = ET.SubElement(metadata, 'IconFileName')
    iconFileName.text = "Characters (Photo).png"
    showSynopsisImage = ET.SubElement(metadata, 'ShowSynopsisImage')
    showSynopsisImage.text = "Yes"
    indexCardImageFileExtension = ET.SubElement(metadata, 'IndexCardImageFileExtension')
    indexCardImageFileExtension.text = "png"

    textSettings = ET.SubElement(binderItem, 'TextSettings')
    target = ET.SubElement(textSettings, 'Target')
    target.attrib["Type"] = "Words"
    target.text = "0"

def SyncScrivener(scrivenerProjectFile):

    # Listar todos os personagens
    c = Character()
    characters = c.list()
    tree = ET.parse(scrivenerProjectFile)
    root = tree.getroot()

    docDir = os.path.dirname(os.path.abspath(scrivenerProjectFile)) +"/Files/Docs/"


    __ID = 54
    __Type = "Text"
    __LabelID = "6"
    __IncludeInCompile = "Yes"
    __FileExtension = "rtf"
    __IconFileName = "Characters (Character Sheet).tiff"
    __ShowSynopsisImage = "Yes"
    __IndexCardImageFileExtension = "png"


    for binderItem in root.iter('BinderItem'):
        idCharacters = binderItem.get('ID')

        # pego os personagens dentro de Character
        if idCharacters == '17':

            for children in binderItem.iter('Children'):
                binderItem.remove(children)

            children = ET.SubElement(binderItem, 'Children')
            binderItem = []
            for character in characters:
                __ID = __ID + 1
                elementCharacter = ET.SubElement(children, 'BinderItem')
                putCharacter(__ID, character, elementCharacter)
                elementCharacter = ""
                createRtfFile(docDir + fileRtfName(__ID), character)

    tree.write(scrivenerProjectFile)


def loadCharacterScrivener():
    pass