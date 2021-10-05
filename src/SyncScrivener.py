# -*- coding: utf-8 -*-

from DataAccess import Character
from Utils import generate_uuid, capitalizeFirstCharacter
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os
import binascii
from logger import Logs

logs = Logs(filename="capivara.log")

def base64ToRtfFile(fileRTF_content, strBase64):
    width = 16378
    height = 15822
    hex_content = binascii.a2b_base64(strBase64)
    hex_content = binascii.hexlify(hex_content)
    hex_content = (' '.join(["{0:b}".format(x) for x in hex_content]))
    fileRTF_content = fileRTF_content.replace("<#LEAKS_IMAGE>",
                                              '\pard\widctlpar\sb360\sa60\sl240\slmult1\qc{\pict{\*\picprop}\wmetafile8\picw16378\pich15822\picwgoal3795\pichgoal3660 ' + str(
                                                  hex_content))
    return fileRTF_content


def putQuot(field):
    # field.replace('"', '"\ulnone NOME"\"')
    pass


def getRtf():
    rtfFile = '''{\\rtf1\\ansi\\ansicpg1252\\deff0\\nouicompat\\deflang1046\\deflangfe1046{\\fonttbl{\\f0\\fmodern Fira Code;}{\\f1\\fswiss\\fprq2\\fcharset0 Arial Black;}{\\f2\\fswiss\\fprq2\\fcharset0 Arial;}{\\f3\\fnil\\fcharset2 Symbol;}}
{\\colortbl ;\\red255\\green0\\blue0;\\red0\\green0\\blue0;\\red122\\green122\\blue122;}
{\\*\\generator Riched20 10.0.19041}{\\*\\mmathPr\\mdispDef1\\mwrapIndent1440 }\\viewkind4\\uc1 
\\pard\\box\\brdrdash\\brdrw0 \\sb360\\sa60\\sl240\\slmult1\\qc\\cf1\\f0\\fs24 [READ ONLY - MANAGER BY CAPIVARA]\\cf2\\expndtw-20\\kerning28\\caps\\f1\\fs72\\par

<#LEAKS_IMAGE>}\par

\\pard\\widctlpar\\sb360\\sa60 @name\\par

\\pard\\widctlpar\\sa200\\sl288\\slmult1\\cf0\\expndtw0\\kerning0\\caps0\\f2\\fs22\\par

\\pard\\keep\\keepn\\widctlpar\\sb120\\sl288\\slmult1\\cf3\\caps\\f1\\fs28 F\\'cdSICO\\par

\\pard\\widctlpar\\li720\\sl240\\slmult1\\cf0\\b\\caps0\\f2\\fs22 Arqu\\'e9tipo\\b0  : <arquetipo>\\par
\\b Data de Nasc.\\b0  : <data de nasc>\\par
\\b Idade : \\b0 @age\\par
\\b Sexo : \\b0 @sex\\par
\\b Altura : \\b0 @height\\par
\\b Peso : \\b0 @weight\\par
\\b Tipo de corpo : \\b0 @body_type\\par
\\b Rosto :\\b0  <rosto>\\par
\\b Cor dos olhos :\\b0  @eye_color\\par
\\b Cor dos cabelos : \\b0 @hair_color\\par
\\b Boca :\\b0  <boca>\\par
\\b Bra\\'e7os : \\b0 <bra\\'e7os>\\par
\\b Pernas : \\b0 <pernas>\\par
\\b Imperfei\\'e7\\'f5es : \\b0 <imperfei\\'e7\\'f5es>\\par
\\b Local : \\b0 @local\\par
\\par

\\pard\\keep\\keepn\\widctlpar\\sb120\\sl288\\slmult1\\cf3\\caps\\f1\\fs28 Detalhes\\line\\caps0\\fs26 Geral\\par

\\pard\\widctlpar\\li720\\sl240\\slmult1\\cf0\\b\\f2\\fs22 Motivo :\\b0  <motivo>\\line\\b H\\'e1bitos : \\b0 <h\\'e1bitos>\\par

\\pard\\widctlpar\\sl240\\slmult1\\par
\\cf3\\f1\\fs26 Vista o personagem\\par

\\pard\\widctlpar\\li720\\sl240\\slmult1\\cf0\\b\\f2\\fs22 Traje : \\b0 <traje>\\par
\\b Sapatos : \\b0 <sapatos>\\par
\\par

\\pard\\widctlpar\\sl240\\slmult1\\cf3\\f1\\fs26 Postura\\par

\\pard\\widctlpar\\li720\\sl240\\slmult1\\cf0\\b\\f2\\fs22 M\\'e3os/Gestos : \\b0 <maos/gestos>\\line\\b P\\'e9s/Pernas : \\b0 <pes/pernas>\\line\\b Tronco/Cabe\\'e7a : \\b0 <tronco/cabeca>\\line\\par

\\pard\\widctlpar\\sl240\\slmult1\\cf3\\f1\\fs26 Bens Materiais\\par

\\pard\\widctlpar\\li720\\sl240\\slmult1\\cf0\\b\\f2\\fs22 Resid\\'eancia : \\b0 <residencia>\\line\\b C\\'f4modo favorito : \\b0 <comodo favorito>\\line\\b Vista da Janela : \\b0 <vista da janela>\\line\\b Ve\\'edculos : \\b0 <veiculos>\\par
\\par
\\par

\\pard\\widctlpar\\sl240\\slmult1\\cf3\\caps\\f1\\fs28 aprofundamentos\\par

\\pard\\widctlpar\\sl276\\slmult1\\caps0\\fs26 Lista de Rituais do Personagem\\par

\\pard{\\pntext\\f3\\'B7\\tab}{\\*\\pn\\pnlvlblt\\pnf3\\pnindent0{\\pntxtb\\'B7}}\\fi-360\\li1440\\sl240\\slmult1\\cf0\\f2\\fs22 <rito 1>\\par
{\\pntext\\f3\\'B7\\tab}<rito 2>\\par
{\\pntext\\f3\\'B7\\tab}<rito 3>\\cf3\\f1\\fs26\\par

\\pard\\li720\\sl240\\slmult1\\par

\\pard\\sl240\\slmult1 Sonho\\par

\\pard\\li720\\sl240\\slmult1\\cf0\\f2\\fs22 <sonho do personagem>\\par

\\pard\\sl240\\slmult1\\par
\\cf3\\f1\\fs26 Biografia\\par

\\pard\\li720\\sl240\\slmult1\\cf0\\f2\\fs22 <9999>- <evento 1>\\par
<9999>- <evento 2>\\par
<9999>- <evento N>\\par

\\pard\\sl240\\slmult1\\par
\\cf3\\f1\\fs26 Background\\par

\\pard\\li720\\sl240\\slmult1\\cf0\\f2\\fs22 <background>\\par
}'''

    return rtfFile


def fileRtfName(id):
    return str(id) + ".rtf"


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
    logs.record("Iniciando a sincronização com o Scrivener ", type="info", colorize=True)
    # Listar todos os personagens
    c = Character()
    characters = c.list()
    tree = ET.parse(scrivenerProjectFile)
    root = tree.getroot()

    docDir = os.path.dirname(os.path.abspath(scrivenerProjectFile)) + "/Files/Docs/"

    # TODO: Obter o max BinderItem e atribuir o novo __ID

    __ID = 54
    __Type = "Text"
    __LabelID = "6"
    __IncludeInCompile = "Yes"
    __FileExtension = "rtf"
    __IconFileName = "Characters (Character Sheet).tiff"
    __ShowSynopsisImage = "Yes"
    __IndexCardImageFileExtension = "png"

    logs.record("Obtendo BinderItem ", type="info", colorize=True)

    for binderItem in root.iter('BinderItem'):
        idCharacters = binderItem.get('ID')

        # pego os personagens dentro de Character
        if idCharacters == '17':

            for children in binderItem.iter('Children'):
                binderItem.remove(children)

            children = ET.SubElement(binderItem, 'Children')
            binderItem = []
            for character in characters:
                rtfFile = getRtf()

                __ID = __ID + 1
                elementCharacter = ET.SubElement(children, 'BinderItem')
                putCharacter(__ID, character, elementCharacter)

                rtfFile = rtfFile.replace("@name", character.name)
                rtfFile = rtfFile.replace("@age", character.age)
                rtfFile = rtfFile.replace("@sex", character.sex)
                rtfFile = rtfFile.replace("@height", '{0:.2f}'.format(character.height))
                rtfFile = rtfFile.replace("@weight", '{0:.2f}'.format(character.weight))
                rtfFile = rtfFile.replace("@eye_color", character.eye_color)
                rtfFile = rtfFile.replace("@hair_color", character.hair_color)
                rtfFile = rtfFile.replace("@body_type", character.body_type)
                rtfFile = rtfFile.replace("@local", character.local)
                rtfFile = base64ToRtfFile(rtfFile, character.picture)
                rtfFileName = docDir + fileRtfName(__ID)

                logs.record("Adicionando o %s no Binder do Scrivener " % rtfFileName, type="info", colorize=True)

                with open(rtfFileName, "w") as arquivo:
                    arquivo.write(rtfFile)

                logs.record("Sincronização com o Scrivener executada com sucesso.", type="info", colorize=True)


    tree.write(scrivenerProjectFile)
