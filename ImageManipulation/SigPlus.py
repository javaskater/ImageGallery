# -*- coding: utf-8 -*-
import stat,os,shutil
import codecs
from ImageXMLParser import ImageParser
from xml.etree.ElementTree import XMLParser
import time
'''
Created on 31 mai 2012

@author: jpmena
'''
class SigPlus(object):
    def __init__(self):
        '''on ne fait rien'''
        self.fichierScrollBox=u'galerie.xml'
        self.fichierDescrSigPlus=u'labels.txt'
    def fromScrollBoxToSigPlus(self,repertoireScroll,repertoireSigPlus):
        galerieEnCours=None
        fichierScrollBox=os.path.join(repertoireScroll,self.fichierScrollBox)
        if os.path.exists(repertoireScroll) and os.path.exists(fichierScrollBox):
            if not os.path.exists(repertoireSigPlus):
                #on crée un répertoire avec les mêmes droits que le répertoire source
                os.mkdir(repertoireSigPlus,os.stat(repertoireScroll).st_mode)
            #on va parser le fichier en question
            handler = ImageParser()
            parser = XMLParser(target=handler)
            ficToParse = codecs.open(fichierScrollBox, "r", "utf-8")
            donneesXML = u'%s' %(ficToParse.read())
            parser.feed(donneesXML)
            galerieEnCours=parser.close()
            ficSigPlus=open(os.path.join(repertoireSigPlus,self.fichierDescrSigPlus),'w')
            for image in galerieEnCours.images:
                ficSigPlus.write(u'%s|%s|%s\n' %(image.nomFic,image.titre,image.comment))
                shutil.copy(os.path.join(repertoireScroll,image.nomFic), repertoireSigPlus)
                msImage=time.mktime(image.date.timetuple())
                os.utime(os.path.join(repertoireSigPlus,image.nomFic), (msImage, msImage))
            ficSigPlus.close()
        else:
            print u'le fichier %s n\'a pu être trouvé, abandon\n' %(fichierScrollBox)


if __name__ == '__main__':
    sP = SigPlus()
    sP.fromScrollBoxToSigPlus('/home/jpmena/RSM/VoieLibre2013', '/home/jpmena/RSM/VoieLibre2013SP/')