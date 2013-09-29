# -*- coding: utf-8 -*-
'''
Created on 31 mai 2012

@author: jpmena
'''
class Image(object):
    '''
    classdocs
    '''


    def __init__(self,lang="fr_FR",width=None,height=None,date=None,nomFic=None):
        '''
        Constructor
        '''
        self.width=width
        self.height=height
        self.date=date
        self.nomFic=nomFic
        self.titre=None
        self.comment=None