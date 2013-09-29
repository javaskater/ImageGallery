# -*- coding: utf-8 -*-
'''
Created on 31 mai 2012

@author: jpmena
'''
from domaine import Galerie, Image
from datetime import datetime

class ImageParser(object):
    '''
    Le but est de parser les images du fichier XML et de les mettre dans un tableau d'images pour SIGPLUS
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.galerieEnCours=None
        self.imageEnCours=None
        self.dataOf={}
        
    def start(self, tag, attrib):
        '''appelé lors d'une balise ouvrante'''
        if tag=="galerie":
            self.galerieEnCours=Galerie.Galerie()
        elif tag=="image" and self.galerieEnCours is not None:
            dImage=datetime.strptime(attrib['date'],'%d/%m/%Y-%H:%M:%S')
            self.imageEnCours=Image.Image(width=attrib['width'],height=attrib['height'],date=dImage,nomFic=attrib['name'])
            for attribut in dir(self.imageEnCours):
                self.dataOf[attribut]=False
            self.dataOf['thumbnail']=False
        elif self.galerieEnCours is not None and self.imageEnCours is not None and self.dataOf[tag] is not None and self.dataOf[tag] == False:
            self.dataOf[tag]=True
            
    def data(self, data):
        estunchardefin=len(data)==2 and data[0:1]=='\n'
        #retrouver le tag en cours
        if self.galerieEnCours is not None and self.imageEnCours is not None and not estunchardefin:
            tagsEnCours=filter(lambda k:self.dataOf[k]==True,self.dataOf.keys())
            if len(tagsEnCours) == 1:
                tag=tagsEnCours[0]
                if tag=="titre":
                    self.imageEnCours.titre=data
                elif tag=="comment":
                    self.imageEnCours.comment=data
        elif self.galerieEnCours is not None:
            self.galerieEnCours.titre=data
            
    
    def end(self, tag):
        if tag=="image":
            if self.galerieEnCours is not None and self.imageEnCours is not None:
                self.galerieEnCours.images.append(self.imageEnCours)
                self.imageEnCours = None
        elif tag != "galerie" and self.galerieEnCours is not None and self.imageEnCours is not None and self.dataOf[tag] is not None and self.dataOf[tag] == True:
            self.dataOf[tag]=False
    
    def close(self):
        return self.galerieEnCours