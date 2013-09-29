# -*- coding: utf-8 -*-
'''
Created on 31 mai 2012

@author: jpmena
'''

class Galerie(object):
    '''
    classdocs
    '''


    def __init__(self,lang="fr_FR",titre=None):
        '''
        Constructor
        '''
        self.titre=titre
        self.lang=lang
        self.images=[]
        