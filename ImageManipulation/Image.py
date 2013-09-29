# -*- coding: utf-8 -*-
from PIL import Image
from datetime import datetime
import stat,os,shutil
'''
Created on 11 nov. 2011

@author: jpmena
'''
class GALImage(object):
    def __init__(self,path_to_original):
        self.path=path_to_original
        self.newDims = {'width':None,'height':None}
        self.thumbDims = {'width':None,'height':None}
        self.img=None
        self.wficFinal=None
        self.tficFinal=None
        #lien entre les suffixe et le format au sens PIL
        self.formats={'jpg':'jpeg','png':'png'}

    def creeImagePlusPetite(self,new_dims,thumbDims,repFinal):
        stats_img_orig = os.stat(self.path)
        dirFicInitial=os.path.dirname(self.path)
        nomFicInitial=os.path.basename(self.path)
        tabFicInitial=nomFicInitial.split('.')
        base_nomFicInitial=u'.'.join(tabFicInitial[0:len(tabFicInitial)-1])
        suffixe=tabFicInitial[len(tabFicInitial)-1].lower()
        nomFicInitialCorrige=u"%s.%s" %(base_nomFicInitial,suffixe)
        shutil.copyfile(self.path,os.path.join(repFinal,nomFicInitialCorrige))
        self.img = Image.open(os.path.join(repFinal,nomFicInitialCorrige))
        (oldWidth,oldHeight) = self.img.size
        format=self.formats[suffixe]
        nomWFicFinal=u"web_%s.%s" %(base_nomFicInitial,suffixe)
        nomThFicFinal=u"thumb_%s.%s" %(base_nomFicInitial,suffixe)
        self.wficFinal=os.path.join(repFinal,nomWFicFinal)
        self.tficFinal=os.path.join(repFinal,nomThFicFinal)
        if new_dims['width'] is not None and new_dims['height'] is not None:
            self.newDims = (new_dims['width'],new_dims['height']);
        elif new_dims['width'] is not None:
            scalingFactor = new_dims['width']*1.0/oldWidth
            self.newDims['width'] = int(oldWidth * scalingFactor)
            self.newDims['height'] = int(oldHeight * scalingFactor)
        elif new_dims['height'] is not None:
            scalingFactor = new_dims['height']*1.0/oldHeight
            self.newDims['width'] = int(oldWidth * scalingFactor)
            self.newDims['height'] = int(oldHeight * scalingFactor)
        if thumbDims['width'] is not None and thumbDims['height'] is not None:
            self.thumbDims = (thumbDims['width'],thumbDims['height']);
        elif thumbDims['width'] is not None:
            scalingFactor = thumbDims['width']*1.0/oldWidth
            self.thumbDims['width'] = int(oldWidth * scalingFactor)
            self.thumbDims['height'] = int(oldHeight * scalingFactor)
        elif thumbDims['height'] is not None:
            scalingFactor = thumbDims['height']*1.0/oldHeight
            self.thumbDims['width'] = int(oldWidth * scalingFactor)
            self.thumbDims['height'] = int(oldHeight * scalingFactor)
        self.newDims['wOnh']=self.newDims['width']*1.0/self.newDims['height']
        self.thumbDims['wOnh']=self.thumbDims['width']*1.0/self.thumbDims['height']
        web_img=self.img.resize((self.newDims['width'],self.newDims['height']),Image.ANTIALIAS)
        web_img.save(self.wficFinal,format)
        #self.img.thumbnail((self.newDims['width'],self.newDims['height']),Image.ANTIALIAS)
        #self.img.save(self.wficFinal,format)
        self.img.thumbnail((self.thumbDims['width'],self.thumbDims['height']),Image.ANTIALIAS)
        self.img.save(self.tficFinal,format)
        #on garde les dates de création et de modificaion du fichier initial
        os.utime(self.wficFinal, (stats_img_orig[stat.ST_ATIME], stats_img_orig[stat.ST_MTIME]))
        os.utime(self.tficFinal, (stats_img_orig[stat.ST_ATIME], stats_img_orig[stat.ST_MTIME]))
        os.remove(os.path.join(repFinal,nomFicInitialCorrige))
        return (self.wficFinal,self.tficFinal,self.newDims,self.thumbDims)
    
    def genereXMLDesc(self,outFile=None):
        date_prise_vue=datetime.fromtimestamp(os.stat(self.path)[stat.ST_MTIME]).strftime('%d/%m/%Y-%H:%M:%S')
        nomWFic=os.path.basename(self.wficFinal)
        nomThFic=os.path.basename(self.tficFinal)
        uXml=u"<image width=\"%d\" height=\"%d\" name=\"%s\" date=\"%s\">\n" %(self.newDims['width'],
                                                                   self.newDims['height'],nomWFic,date_prise_vue)
        uXml+=u"\t<thumbnail width=\"%d\" height=\"%d\" name=\"%s\" />\n" %(self.thumbDims['width'],
                                                                   self.thumbDims['height'],nomThFic)
        uXml+=u"\t<titre lang=\"fr_FR\"><![CDATA[xxxxxxxxx]]></titre>\n"
        uXml+=u"\t<comment lang=\"fr_FR\">\n"
        uXml+=u"\t<![CDATA[yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy]]>\n"
        uXml+=u"\t</comment>\n"
        uXml+=u"</image>\n"
        return uXml

if __name__ == '__main__':
    #images=["P1000787.JPG", "P1000794.JPG", "P1000795.JPG","P1000798.JPG", "P1000806.JPG", "P1000810.JPG",
     #       "P1000812.JPG","P1000815.JPG","P1000819.JPG","P1000825.JPG","P1000827.JPG","P1000829.JPG","P1000831.JPG",
      #      "P1000835_crop.JPG","P1000848.JPG","P1000861.JPG",'P1000867_crop.JPG','P1000868_crop.JPG','P1000870_crop.JPG',
       #     'P1000871.JPG','P1000872.JPG','P1000874_crop.JPG','P1000875.JPG','P1000877.JPG','P1000880.JPG']
    images=["DSC03731.JPG","DSC03733.JPG","DSC03734.JPG","DSC03735.JPG","LA_VOIE_EST_LIBRE.JPG","DSC03736.JPG","DSC03737.JPG","DSC03738.JPG","DSC03744.JPG"]
    repSource=u"/home/jpmena/Pictures/RSM/VoieLibre2013"
    repDest=u"/home/jpmena/RSM/VoieLibre2013/"
    if not os.path.exists(repDest):
        #on crée un répertoire avec les mêmes droits que le répertoire source
        os.mkdir(repDest,os.stat(repSource).st_mode)
    descXml=open(os.path.join(repDest,'galerie.xml'),'w')
    descXml.write(u'<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<galerie>\n')
    descXml.write(u'<titre lang=\"fr_FR\"><![CDATA[xxxxxxxxxxxxxxxxxxxxxxxx]]></titre>\n')
    for iname in images:
        im=GALImage(os.path.join(repSource,iname))
        im.creeImagePlusPetite({'width':1000,'height':None}, {'width':100,'height':None},repDest)
        descXml.write(im.genereXMLDesc())
        print u"Le ratio longeur sur hauteur est %f" %(im.newDims['wOnh'])
    descXml.write(u'</galerie>')
    descXml.close()