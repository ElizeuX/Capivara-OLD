import gi

gi.require_version(namespace='Gtk', version='3.0')

from DataAccess import Character
from Utils import generate_uuid
import xml.etree.ElementTree as ET


def createRtfFile():
    dirDocs = "C:/Users/Elizeu/OneDrive - PRODESP/Documents/My Capivaras/scrivener_teste/teste4.scriv/Files/Docs"
    rtfFile = '''{\\rtf1\\ansi\\ansicpg1252\\uc1\deff0
        {\\fonttbl{\\f0\\fnil\\fcharset0\\fprq2 CourierNewPSMT;}{\\f1\\fnil\\fcharset0\\fprq2 Arial-ItalicMT;}{\\f2\\fnil\\fcharset0\\fprq2 ArialMT;}{\\f3\\fnil\\fcharset0\\fprq2 Arial-BoldMT;}}
        {\\colortbl;\\red0\\green0\\blue0;\\red255\\green255\\blue255;\\red255\\green0\\blue0;\\red30\\green79\\blue159;}
        \\paperw12240\\paperh15840\\margl1800\\margr1800\\margt1440\\margb1440\\fet2\\ftnbj\\aenddoc
        \\pgnrestart\\pgnstarts0
        \pard\plain \tx0\tqr\tx2700\tx3110\tx3740\sb160\sl288\slmult1\qc\ltrch\loch {\f1\fs20\b0\i1\cf3 [READ ONLY - MANAGER BY CAPIVARA]}
        \\par\\plain {\\f2\\fs40\\b0\\i0\\cf4 Character Name}
        \\par\\pard\\plain \\fi360\\sl360\\slmult1\\qj\\ltrch\\loch \\f2\\fs40\\b0\\i0\\cf4
        \\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Arqu\\loch\\af3\\hich\\af3\\dbch\\af3\\uc1\\u233\\'E9tipo: }
        \\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Data de nasc.:}
        \\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Idade:}
        \\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Sexo:}
        \\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Altura: 1.90}
        \\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Peso: 100}
        \\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Tipo de corpo:}{\\f2\\fs26\\b0\\i0 \\tab }
        \\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Cor dos olhos: Verdes}
        \\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Cor dos cabelos:}
        \\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Etnicidade:}
        \\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Sa\\loch\\af3\\hich\\af3\\dbch\\af3\\uc1\\u250\\'FAde:}
        \\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Local:}
        \\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch {\\f3\\fs26\\b1\\i0 Background:}
        \\par\\plain {\\f3\\fs26\\b1\\i0 Biografia}
        \\par\\plain {\\f3\\fs26\\b1\\i0 Ano                             Evento}
        \\par\\pard\\plain \\tx360\\tqr\\tx3124\\tx3196\\tx4075\\li3197\\fi-2837\\sb160\\sl288\\slmult1\\ql\\ltrch\\loch \\f3\\fs26\\b1\\i0
        \\par\\pard\\plain \\fi360\\sl360\\slmult1\\qj\\ltrch\\loch \\f2\\fs40\\b0\\i0\\cf4
        \\par\\plain \\f2\\fs40\\b0\\i0\\cf4
        \\par\\plain \\f2\\fs40\\b0\\i0\\cf4
        \\par\\plain \\f2\\fs40\\b0\\i0\\cf4}'''


    with open("testefile.rtf", "w") as arquivo:
        arquivo.write(rtfFile)




def putCharacter(id, name, binderItem):
    binderItem.attrib["ID"] = str(id)
    binderItem.attrib["UUID"] = str(generate_uuid())
    binderItem.attrib["Created"] = "-0300"
    binderItem.attrib["Modified"] = "2021-09-24 04:56:09 -0300"
    binderItem.attrib["Type"] = "Text"
    title = ET.SubElement(binderItem, 'Title')
    title.text = name
    metadata = ET.SubElement(binderItem, 'Metadata')
    labelID = ET.SubElement(metadata, 'LabelID')
    labelID.text = "6"
    includeInCompile = ET.SubElement(metadata, 'IncludeInCompile')
    includeInCompile.text = "Yes"
    fileExtension = ET.SubElement(metadata, 'FileExtension')
    fileExtension.text = "rtf"
    iconFileName = ET.SubElement(metadata, 'IconFileName')
    iconFileName.text = "Characters (Character Sheet).tiff"
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


    __ID = 53
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
                putCharacter(__ID, character.name, elementCharacter)
                elementCharacter = ""

    createRtfFile()
    tree.write('output.xml')


def loadCharacterScrivener():
    pass