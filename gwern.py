# -*- coding: utf-8 -*-

#titre          :gwern.py
#description    :pilote le formulaire gwern.ui du projet GwernQGIS.qgs
#auteur         :Jérôme Fernandez
#date           :Juin 2016
#version        :5
#==============================================================================
#***************************************************************************

#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#                    
#**************************************************************************/

DEBUGMODE = False

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import csv, codecs, os, os.path, re, datetime

listePlante = None
cBArr = None
cBAESN = None
choixListe = None
cochePourc = None
cochePourcMult = None
pourc = None

myLayer = None
myDialog = None
myFeature = None
stack = None
tabGw = None
champEnCours = None

sitFonc = None

rqTypoPlain = None
rqGenePlain = None
rqHydroPlain = None
rqBioPlain = None
rqContextePlain = None
rqBilanPlain = None
recomTechPlain = None
espAnimalPlain = None
espVegetalPlain = None

rqTypo = None
rqGene = None
rqHydro = None
rqBio = None
rqContexte = None
rqBilan = None
recomTech = None
espAnimal = None
toponyme = None

datCreatio = None
observateur = None
calendarWidget = None
annulerDate = None
effacerDate = None
lFiltreUnique = None
tFiltreUnique = None
unique = None
lstUnique = None

prodrome1 = None
corBio1 = None
hydromSol = None
hydromApp = None
hydromDisp = None
freqSubm = None
etendSubm = None
foncHydro = None
foncEpur = None
diagHydro = None
foncBio = None
etatCons = None
nivMenace = None
faisabInt = None
nivPrior = None


gFiltreMultiple = None
tFiltreMultiple = None
tFiltreMultipleEV = None


multiple = None
lstMultiple = None
lstChoix = None
annulerMultiple = None
validerMultiple = None

lstMultiple_2 = None
lstChoix_2 = None
annulerMultiple_2 = None
validerMultiple_2 = None

principal = None
secondaire = None
complementaire = None
aller = None
retour = None
aller_2 = None
retour_2 = None

permanence = None
inconnu = None
temporaire = None
saisonnier = None
permanent = None

prodrome2 = None
corBio2 = None
SAGE = None
critDelim = None
entreeEau = None
sortieEau = None
foncHydro = None
foncEpur = None
espVegetal = None
foncBio = None
actDans = None
actAutour = None
instrument = None
foncier = None
zonPLU = None
valSocEco = None
atteinte = None
menace = None
foncMaj = None
valMaj = None
preconAct = None
contexInt = None

police1 = None
police2 = None
police3 = None

image = None
plus = None
moins = None
gauche = None
droite = None
lPhoto = None
photo1 = None
photo2 = None
photo3 = None
photo4 = None

propoZHIEP = None
propoZSGE = None

class Filter(QObject):
    def eventFilter(self, widget, event):
        global champEnCours
        if widget == myDialog:
            if event.type()== QEvent.Resize:
                dialGeom()
            if event.type() == QEvent.Move:
                dialGeom()
    
        #------------------------------List choix unique---------Effacement----
        if widget == unique:
            if event.type() == QEvent.MouseButtonRelease:

                champEnCours ="3"
                tFiltreUnique.setText("")              
                #unique.setVisible(False)
                stack.setCurrentIndex(0)
            return False
        #-----------------------Fin list choix unique-------------------------
        
        if widget == datCreatio:

            if event.type() == QEvent.MouseButtonRelease:
                stack.setCurrentIndex(4)
                
                if str(datCreatio.text()) != "":
                    calendarWidget.setSelectedDate(QDate.fromString(datCreatio.text(), 'dd/MM/yyyy'))
                else:
                    auj = datetime.datetime.now()
                    
                    calendarWidget.setSelectedDate(QDate.fromString(str(auj.day) + '/' + str(auj.month) + '/' + str(auj.year), 'dd/MM/yyyy'))
            return False

        
        #------------------------Prodrome-----------------------------
        if widget == prodrome1:
            if event.type() == QEvent.MouseButtonRelease:
                lFiltreUnique.setVisible(True)
                tFiltreUnique.setVisible(True)
                cochePourc.setVisible(True)
                item2 = None
                lstUnique.clear()
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Prodrome.csv", 'r', encoding='utf-8')             
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    lstUnique.addItem(item)

                    if prodrome1.text().find('%]')>0:

                        if data.strip() == prodrome1.text().strip()[:prodrome1.text().find('[')].strip():
                            item2 = lstUnique.count()
                    else :

                        if data.rstrip() == prodrome1.text().rstrip():
                            item2 = lstUnique.count()

                if item2 != None:  
                    lstUnique.setCurrentRow(item2-1)
                stack.setCurrentIndex(1)
                champEnCours = "prodrome1"
            return False
        #---------------------------------Fin prodrome--------------------------
        #------------------------Corine principal-----------------------------
        if widget == corBio1:
            if event.type() == QEvent.MouseButtonRelease:
                lFiltreUnique.setVisible(True)
                tFiltreUnique.setVisible(True)
                cochePourc.setVisible(True)
                item2 = None
                lstUnique.clear()
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Corine_Biotope.csv", 'r', encoding='utf-8')
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    lstUnique.addItem(item)
                    
                    
                    if corBio1.text().find('%]')>0:

                        if data.rstrip() == corBio1.text().rstrip()[:corBio1.text().find('[')].rstrip():
                            item2 = lstUnique.count()
                    else :

                        if data.rstrip() == corBio1.text().rstrip():
                            item2 = lstUnique.count()                    

                if item2 != None:  
                    lstUnique.setCurrentRow(item2-1)
                stack.setCurrentIndex(1)
                champEnCours = "corBio1"
    
            return False
        #---------------------------------Fin corine principal--------------------------
        #------------------------Hydromorphie du sol------------------------------------
        if widget == hydromSol:
            if event.type() == QEvent.MouseButtonRelease:
                lFiltreUnique.setVisible(False)
                tFiltreUnique.setVisible(False)
                cochePourc.setVisible(False)
                item2 = None
                lstUnique.clear()
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Hydromorphie.csv", 'r', encoding='utf-8')
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    lstUnique.addItem(item)

                    if libelle.rstrip() == hydromSol.text():
                        item2 = lstUnique.count()
                if item2 != None:  
                    lstUnique.setCurrentRow(item2-1)
                stack.setCurrentIndex(1)
                champEnCours = "hydromSol"
            return False
        #---------------------------------Fin---------------------------------
        #------------------------HydromApp------------------------------------
        if widget == hydromApp:
            
            if event.type() == QEvent.MouseButtonRelease:
                lFiltreUnique.setVisible(False)
                tFiltreUnique.setVisible(False)
                cochePourc.setVisible(False)
                item2 = None
                lstUnique.clear()
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Profondeur.csv", 'r', encoding='utf-8')
                for line in reader:
                    lstUnique.addItem(line)
                    if line.rstrip()  == hydromApp.text():
                        item2 = lstUnique.count()
                if item2 != None:  
                    lstUnique.setCurrentRow(item2-1)
                stack.setCurrentIndex(1)
                champEnCours = "hydromApp"
            return False
        #---------------------------------Fin hydromApp------------------------
        #------------------------HydromDisp------------------------------------
        if widget == hydromDisp:
            if event.type() == QEvent.MouseButtonRelease:
                lFiltreUnique.setVisible(False)
                tFiltreUnique.setVisible(False)
                cochePourc.setVisible(False)
                item2 = None
                lstUnique.clear()
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Profondeur.csv", 'r', encoding='utf-8')
                for line in reader:
                    lstUnique.addItem(line)
                    if line.rstrip() == hydromDisp.text():
                        item2 = lstUnique.count()
                if item2 != None:  
                    lstUnique.setCurrentRow(item2-1)
                stack.setCurrentIndex(1)
                champEnCours = "hydromDisp"
            return False
        #---------------------------------Fin -------------------------------
        #------------------------freqSubm------------------------------------
        if widget == freqSubm:
            if event.type() == QEvent.MouseButtonRelease:
                lFiltreUnique.setVisible(False)
                tFiltreUnique.setVisible(False)
                cochePourc.setVisible(False)
                item2 = None
                lstUnique.clear()
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Frequence_Submersion.csv", 'r', encoding='utf-8')
                for line in reader:
                    data, libelle = line.split(';')
                    lstUnique.addItem(libelle)
                    if libelle.rstrip() == freqSubm.text():
                        item2 = lstUnique.count()
                if item2 != None:  
                    lstUnique.setCurrentRow(item2-1)
                stack.setCurrentIndex(1)
                champEnCours = "freqSubm"
            return False
        #---------------------------------Fin --------------------------------
        #------------------------etendSubm------------------------------------
        if widget == etendSubm:
            if event.type() == QEvent.MouseButtonRelease:
                lFiltreUnique.setVisible(False)
                tFiltreUnique.setVisible(False)
                cochePourc.setVisible(False)
                item2 = None
                lstUnique.clear()
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Etendue_Submersion.csv", 'r', encoding='utf-8')
                for line in reader:
                    data, libelle = line.split(';')
                    lstUnique.addItem(libelle)
                    if libelle.rstrip() == etendSubm.text():
                        item2 = lstUnique.count()
                if item2 != None:  
                    lstUnique.setCurrentRow(item2-1)
                #unique.setVisible(True)
                stack.setCurrentIndex(1)
                champEnCours = "etendSubm"
            return False
        #---------------------------------Fin --------------------------------      
        #------------------------diagHydro------------------------------------
        if widget == diagHydro:
            if event.type() == QEvent.MouseButtonRelease:
                lFiltreUnique.setVisible(False)
                tFiltreUnique.setVisible(False)
                cochePourc.setVisible(False)
                item2 = None
                lstUnique.clear()
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Diagnostic_Hydrologique.csv", 'r', encoding='utf-8')
                for line in reader:
                    data, libelle = line.split(';')
                    lstUnique.addItem(libelle) 
                    if libelle.rstrip() == diagHydro.text():
                        item2 = lstUnique.count()
                if item2 != None:  
                    lstUnique.setCurrentRow(item2-1)
                stack.setCurrentIndex(1)
                champEnCours = "diagHydro"
            return False
        #---------------------------------Fin -------------------------------       
        #------------------------etatCons------------------------------------
        if widget == etatCons:
            if event.type() == QEvent.MouseButtonRelease:
                lFiltreUnique.setVisible(False)
                tFiltreUnique.setVisible(False)
                cochePourc.setVisible(False)
                item2 = None
                lstUnique.clear()
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Diagnostic_Biologique.csv", 'r', encoding='utf-8')
                for line in reader:
                    data, libelle = line.split(';')
                    lstUnique.addItem(libelle) 
                    if libelle.rstrip() == etatCons.text():
                        item2 = lstUnique.count()
                if item2 != None:  
                    lstUnique.setCurrentRow(item2-1)
                #unique.setVisible(True)
                stack.setCurrentIndex(1)
                champEnCours = "etatCons"
            return False
        #---------------------------------Fin --------------------------------     
        #------------------------nivMenace------------------------------------
        if widget == nivMenace:
            if event.type() == QEvent.MouseButtonRelease:
                lFiltreUnique.setVisible(False)
                tFiltreUnique.setVisible(False)
                cochePourc.setVisible(False)
                item2 = None
                lstUnique.clear()
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Niveau_Menace.csv", 'r', encoding='utf-8')
                for line in reader:
                    data, libelle = line.split(';')
                    lstUnique.addItem(libelle) 
                    if libelle.rstrip() == nivMenace.text():
                        item2 = lstUnique.count()
                if item2 != None:  
                    lstUnique.setCurrentRow(item2-1)
                stack.setCurrentIndex(1)
                champEnCours = "nivMenace"
            return False
        #---------------------------------Fin --------------------------------
        #------------------------faisabInt------------------------------------
        if widget == faisabInt:
            if event.type() == QEvent.MouseButtonRelease:
                lFiltreUnique.setVisible(False)
                tFiltreUnique.setVisible(False)
                cochePourc.setVisible(False)
                item2 = None
                lstUnique.clear()
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Faisabilite.csv", 'r', encoding='utf-8')
                for line in reader:
                    data, libelle = line.split(';')
                    lstUnique.addItem(libelle) 
                    if libelle.rstrip() == faisabInt.text():
                        item2 = lstUnique.count()
                if item2 != None:  
                    lstUnique.setCurrentRow(item2-1)
                stack.setCurrentIndex(1)
                champEnCours = "faisabInt"
            return False
        #---------------------------------Fin -------------------------------
        #------------------------nivPrior------------------------------------
        if widget == nivPrior:
            if event.type() == QEvent.MouseButtonRelease:
                lFiltreUnique.setVisible(False)
                tFiltreUnique.setVisible(False)
                cochePourc.setVisible(False)
                item2 = None
                lstUnique.clear()
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Niveau_Priorite.csv", 'r', encoding='utf-8')
                for line in reader:
                    data, libelle = line.split(';')
                    lstUnique.addItem(libelle)
                    if libelle.rstrip() == nivPrior.text():
                        item2 = lstUnique.count()
                if item2 != None:  
                    lstUnique.setCurrentRow(item2-1)
                stack.setCurrentIndex(1)
                champEnCours = "nivPrior"
            return False
        #---------------------------------Fin --------------------------
        #---------------------Prodrome secondaire-------------------------
        if widget == prodrome2:
            if event.type() == QEvent.MouseButtonRelease:
                cochePourcMult.setVisible(True)
                gFiltreMultiple.setVisible(True)
                tFiltreMultiple.setText("")
                lstMultiple.clear()
                lstChoix.clear()

                reader = codecs.open(os.path.dirname(__file__) + "/tables/Prodrome.csv", 'r', encoding='utf-8')               
                for line in reader:
                
                    if line[:1] != u";":
                        data, libelle = line.split(';')
                        item = QListWidgetItem(libelle)
                        item.setData(3,data)

                        if ';' + data + ';' in  ';' + str(prodrome2.text()) + ';' or ';' + data + '[' in  ';' + str(prodrome2.text())or ';' + data + ' [' in  ';' + str(prodrome2.text()):
                            
                            if prodrome2.text().find(data + u' [')>0 or prodrome2.text().find(data + u'[')>-1:

                                listEnPlace = prodrome2.text().split(';')
                                for ite in listEnPlace:
                                    

                                    if u'[' in ite:
                                        code, poupou = ite.split('[')
                                        code = code.strip()
                                        if code==data:
                                            poupou = poupou.replace('%]','').strip()
                                            item.setText(item.text().replace('\r','').replace('\n','') + '[' + str(poupou) + '%]' + '\r\n')
                                            lstChoix.addItem(item)
                                            code = ''
                                            poupou=''
                                            break
                                    else:
                                        q=QMessageBox()
                                        q.setText(str(item.text()))
                                        lstChoix.addItem(item)
                            else:
                                lstChoix.addItem(item)    
                        else:
                            lstMultiple.addItem(item)
                champEnCours = "prodrome2"

                if myLayer.isEditable():
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(True)
                    permanence.setVisible(False)
                    retour.setVisible(True)
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)                 
                    retour.setVisible(False)
                stack.setCurrentIndex(2)
            return False  
        #-------------------------Fin prodrome secondaire------------------------
        #---------------------Corine secondaire-------------------------
        if widget == corBio2:
            if event.type() == QEvent.MouseButtonRelease:
                cochePourcMult.setVisible(True)
                gFiltreMultiple.setVisible(True)
                tFiltreMultiple.setText("")
                lstMultiple.clear()
                lstChoix.clear()

                reader = codecs.open(os.path.dirname(__file__) + "/tables/Corine_Biotope.csv", 'r', encoding='utf-8')               
                for line in reader:
                
                    if line[:1] != u";":
                        data, libelle = line.split(';')
                        item = QListWidgetItem(libelle)
                        item.setData(3,data)

                        if ';' + data + ';' in  ';' + str(corBio2.text()) + ';' or ';' + data + '[' in  ';' + str(corBio2.text())or ';' + data + ' [' in  ';' + str(corBio2.text()):
                            
                            if corBio2.text().find(data + u' [')>0 or corBio2.text().find(data + u'[')>-1:

                                listEnPlace = corBio2.text().split(';')
                                for ite in listEnPlace:
                                    

                                    if u'[' in ite:
                                        code, poupou = ite.split('[')
                                        code = code.strip()
                                        if code==data:
                                            poupou = poupou.replace('%]','').strip()
                                            item.setText(item.text().replace('\r','').replace('\n','') + '[' + str(poupou) + '%]' + '\r\n')
                                            lstChoix.addItem(item)
                                            code = ''
                                            poupou=''
                                            break
                                    else:
                                        lstChoix.addItem(item)
                            else:
                                lstChoix.addItem(item)    
                        else:
                            lstMultiple.addItem(item)                        

                champEnCours = "corBio2"

                if myLayer.isEditable():
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(True)
                    permanence.setVisible(False)
                    retour.setVisible(True)
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)                 
                    retour.setVisible(False)
                stack.setCurrentIndex(2)
            return False  
        #-------------------------Fin Corine secondaire------------------------
        
        
        #---------------------SAGE-------------------------
        if widget == SAGE:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()

                reader = codecs.open(os.path.dirname(__file__) + "/tables/SAGE.csv", 'r', encoding='utf-8')               
                for line in reader:
                
                    if line[:1] != u";":
                        data, libelle = line.split(';')
                        item = QListWidgetItem(libelle)
                        item.setData(3,data)
                        if ';' + data + ';' in  ';' + str(SAGE.text()) + ';':
                            lstChoix.addItem(item)                         
                        else:
                            lstMultiple.addItem(item)
                champEnCours = "SAGE"

                if myLayer.isEditable():
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(True)
                    permanence.setVisible(False)
                    retour.setVisible(True)
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)                 
                    retour.setVisible(False)
                stack.setCurrentIndex(2)
            return False  
        #-------------------------Fin SAGE------------------------        

        #-----------------------------Critere de delimitation------------------
        if widget == critDelim:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()            
            
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Delimitation.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if ';' + data + '(' in  ';' + str(critDelim.text()) :
                        if ';' + data + '(1)' in  ';' + str(critDelim.text()) :
                            item.setFont(police1)
                        if ';' + data + '(2)' in  ';' + str(critDelim.text()) :
                            item.setFont(police2)
                        if ';' + data + '(3)' in  ';' + str(critDelim.text()) :
                            item.setFont(police3)
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)  
                        
                if myLayer.isEditable():
                    principal.setVisible(True)
                    secondaire.setVisible(True)
                    complementaire.setVisible(True)
                    aller.setVisible(False)
                    permanence.setVisible(False)
                    retour.setVisible(True)                    
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)
                    retour.setVisible(False)
                    

                stack.setCurrentIndex(2)
                champEnCours = "critDelim"
            return False    

        #--------------Fin Critere de delimitation----------------------------
        #-----------------------------entreeEau-------------------------------
        if widget == entreeEau:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()            
            
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Entree_Eau.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if u';' + data + u'(' in  u';' + str(entreeEau.text()) :
                        if u';' + data + u'(1)' in  u';' + str(entreeEau.text()) :
                            item.setFont(police1)
                        if u';' + data + u'(2)' in  u';' + str(entreeEau.text()) :
                            item.setFont(police2)
                        if u';' + data + u'(3)' in  u';' + str(entreeEau.text()) :
                            item.setFont(police3)    
                        if re.search(r";" + data + "\([1-3]\)\[0\]",u';' + str(entreeEau.text())):  
                            item.setText(item.text()[:len(item.text())-2] + u" (Inconnu)" + item.text()[len(item.text())-2:] )
                        if re.search(r";" + data + "\([1-3]\)\[5\]",u';' + str(entreeEau.text())):  
                            item.setText(item.text()[:len(item.text())-2] + u" (Temporaire/Intermittent)" + item.text()[len(item.text())-2:] )
                        if re.search(r";" + data + "\([1-3]\)\[4\]",u';' + str(entreeEau.text())):  
                            item.setText(item.text()[:len(item.text())-2] + u" (Saisonnier)" + item.text()[len(item.text())-2:] )
                        if re.search(r";" + data + "\([1-3]\)\[3\]",u';' + str(entreeEau.text())):  
                            item.setText(item.text()[:len(item.text())-2] + u" (Permanent)" + item.text()[len(item.text())-2:] )                            
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)  
                
                
                if myLayer.isEditable():
                    principal.setVisible(True)
                    secondaire.setVisible(True)
                    complementaire.setVisible(True)
                    aller.setVisible(False)
                    permanence.setVisible(True)
                    retour.setVisible(True)                    
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)                
                    retour.setVisible(False)
                

                stack.setCurrentIndex(2)
                champEnCours = "entreeEau"
            return False    

        #--------------Fin ------------------------------------------------
        #-----------------------------sortieEau-------------------------------
        if widget == sortieEau:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()            
            
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Sortie_Eau.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if ';' + data + '(' in  ';' + str(sortieEau.text()) :
                        if ';' + data + '(1)' in  ';' + str(sortieEau.text()) :
                            item.setFont(police1)
                        if ';' + data + '(2)' in  ';' + str(sortieEau.text()) :
                            item.setFont(police2)
                        if ';' + data + '(3)' in  ';' + str(sortieEau.text()) :
                            item.setFont(police3)
                        if re.search(r";" + data + "\([1-3]\)\[0\]",u';' + str(sortieEau.text())):  
                            item.setText(item.text()[:len(item.text())-2] + u" (Inconnu)" + item.text()[len(item.text())-2:] )
                        if re.search(r";" + data + "\([1-3]\)\[5\]",u';' + str(sortieEau.text())):  
                            item.setText(item.text()[:len(item.text())-2] + u" (Temporaire/Intermittent)" + item.text()[len(item.text())-2:] )
                        if re.search(r";" + data + "\([1-3]\)\[4\]",u';' + str(sortieEau.text())):  
                            item.setText(item.text()[:len(item.text())-2] + u" (Saisonnier)" + item.text()[len(item.text())-2:] )
                        if re.search(r";" + data + "\([1-3]\)\[3\]",u';' + str(sortieEau.text())):  
                            item.setText(item.text()[:len(item.text())-2] + u" (Permanent)" + item.text()[len(item.text())-2:] )     
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)  
                
                if myLayer.isEditable():
                    principal.setVisible(True)
                    secondaire.setVisible(True)
                    complementaire.setVisible(True)
                    aller.setVisible(False)
                    permanence.setVisible(True)
                    retour.setVisible(True)                    
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)                
                    retour.setVisible(False)
                stack.setCurrentIndex(2)
                champEnCours = "sortieEau"
            return False    

        #--------------Fin ------------------------------------------------
        #-----------------------------foncHydro----------------------------
        if widget == foncHydro:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()            
            
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Fonctions_Hydrologiques.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if ';' + data + '(' in  ';' + str(foncHydro.text()) :
                        if ';' + data + '(1)' in  ';' + str(foncHydro.text()) :
                            item.setFont(police1)
                        if ';' + data + '(2)' in  ';' + str(foncHydro.text()) :
                            item.setFont(police2)
                        if ';' + data + '(3)' in  ';' + str(foncHydro.text()) :
                            item.setFont(police3)
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)  
                if myLayer.isEditable():
                    principal.setVisible(True)
                    secondaire.setVisible(True)
                    complementaire.setVisible(True)
                    aller.setVisible(False)
                    permanence.setVisible(False)
                    retour.setVisible(True)                    
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)  
                    retour.setVisible(False)
                stack.setCurrentIndex(2)
                champEnCours = "foncHydro"
            return False    

        #--------------Fin -------------------------------------------------
        #-----------------------------foncEpur----------------------------
        if widget == foncEpur:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()            
            
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Fonctions_Epuratrices.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    
                    if ';' + data + '(' in  ';' + str(foncEpur.text()) :
                        if ';' + data + '(1)' in  ';' + str(foncEpur.text()) :
                            item.setFont(police1)
                        if ';' + data + '(2)' in  ';' + str(foncEpur.text()) :
                            item.setFont(police2)
                        if ';' + data + '(3)' in  ';' + str(foncEpur.text()) :
                            item.setFont(police3)
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)  
 
                if myLayer.isEditable():
                    principal.setVisible(True)
                    secondaire.setVisible(True)
                    complementaire.setVisible(True)
                    aller.setVisible(False)
                    permanence.setVisible(False)
                    retour.setVisible(True)
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)  
                    retour.setVisible(False)
                
                stack.setCurrentIndex(2)
                champEnCours = "foncEpur"
            return False    

        #--------------Fin -------------------------------------------------
        #---------------------espVegetal------------------------------------
        if widget == espVegetalPlain:
            global listePlante
            if event.type() == QEvent.MouseButtonRelease:
                tFiltreMultipleEV.setText("")
                lstMultiple_2.clear()
                lstChoix_2.clear()

                reader = codecs.open(os.path.dirname(__file__) + u"/tables/Especes_Vegetales.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle, Arr, AESN = line.replace('\r\n', '').replace('\r', '').replace('\n', '').split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if ';' + data + ';' in  ';' + str(espVegetalPlain.toPlainText()) + ';':
                        lstChoix_2.addItem(item)                         
                    else:
                        if ("Arr" in listePlante and Arr == "1") or ("AESN" in listePlante and AESN == "1"):
                            lstMultiple_2.addItem(item)
                champEnCours = "espVegetal"
                
                #if myLayer.isEditable():
                #    principal.setVisible(False)
                 #   secondaire.setVisible(False)
                #    complementaire.setVisible(False)
                #    aller.setVisible(True)
                #    permanence.setVisible(False)
                 #   retour.setVisible(True)                    
                #else:
                #    principal.setVisible(False)
                #    secondaire.setVisible(False)
                #    complementaire.setVisible(False)
                #    aller.setVisible(False)
                #    permanence.setVisible(False)  
                #    retour.setVisible(False)
                choixListe.setVisible(True)
                stack.setCurrentIndex(3)
            return False  
        #-------------------------Fin espveg------------------------
        #-----------------------------foncBio----------------------------------
        if widget == foncBio:
            
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()            
            
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Fonctions_Biologiques.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if ';' + data + '(' in  ';' + str(foncBio.text()) :
                        if ';' + data + '(1)' in  ';' + str(foncBio.text()) :
                            item.setFont(police1)
                        if ';' + data + '(2)' in  ';' + str(foncBio.text()) :
                            item.setFont(police2)
                        if ';' + data + '(3)' in  ';' + str(foncBio.text()) :
                            item.setFont(police3)
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)  
                if myLayer.isEditable():
                    principal.setVisible(True)
                    secondaire.setVisible(True)
                    complementaire.setVisible(True)
                    aller.setVisible(False)
                    permanence.setVisible(False)
                    retour.setVisible(True)
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)                  
                    retour.setVisible(False)
                stack.setCurrentIndex(2)
                champEnCours = "foncBio"
            return False    

        #--------------Fin ----------------------------------------------------
        #-----------------------------actDans----------------------------------
        if widget == actDans:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()            
            
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Activites.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if ';' + data + '(' in  ';' + str(actDans.text()) :
                        if ';' + data + '(1)' in  ';' + str(actDans.text()) :
                            item.setFont(police1)
                        if ';' + data + '(2)' in  ';' + str(actDans.text()) :
                            item.setFont(police2)
                        if ';' + data + '(3)' in  ';' + str(actDans.text()) :
                            item.setFont(police3)
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)  
                if myLayer.isEditable():
                    principal.setVisible(True)
                    secondaire.setVisible(True)
                    complementaire.setVisible(True)
                    aller.setVisible(False)
                    permanence.setVisible(False)
                    retour.setVisible(True)
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)                 
                    retour.setVisible(False)
                stack.setCurrentIndex(2)
                champEnCours = "actDans"
            return False    

        #--------------Fin -------------------------------------------------
        #-----------------------------actAutour----------------------------------
        if widget == actAutour:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()            
            
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Activites.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if ';' + data + '(' in  ';' + str(actAutour.text()) :
                        if ';' + data + '(1)' in  ';' + str(actAutour.text()) :
                            item.setFont(police1)
                        if ';' + data + '(2)' in  ';' + str(actAutour.text()) :
                            item.setFont(police2)
                        if ';' + data + '(3)' in  ';' + str(actAutour.text()) :
                            item.setFont(police3)
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)  
                if myLayer.isEditable():
                    principal.setVisible(True)
                    secondaire.setVisible(True)
                    complementaire.setVisible(True)
                    aller.setVisible(False)
                    permanence.setVisible(False)
                    retour.setVisible(True)                    
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)
                    retour.setVisible(False)                    
                
                stack.setCurrentIndex(2)
                champEnCours = "actAutour"
            return False    

        #--------------Fin -------------------------------------------------
        #---------------------instrument------------------------------------
        if widget == instrument:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()

                reader = codecs.open(os.path.dirname(__file__) + "/tables/Instruments.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if ';' + data + ';' in  ';' + str(instrument.text()) + ';':
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)
                champEnCours = "instrument"
                if myLayer.isEditable():
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(True)
                    permanence.setVisible(False)
                    retour.setVisible(True)
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)
                    retour.setVisible(False)
                
                stack.setCurrentIndex(2)
            return False  
        #-------------------------Fin------------------------
        #---------------------foncier------------------------------------
        if widget == foncier:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()

                reader = codecs.open(os.path.dirname(__file__) + "/tables/Statuts_Fonciers.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if ';' + data + ';' in  ';' + str(foncier.text()) + ';':
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)
                champEnCours = "foncier"
                if myLayer.isEditable():
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(True)
                    permanence.setVisible(False)
                    retour.setVisible(True)
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)  
                    retour.setVisible(False)
                stack.setCurrentIndex(2)
            return False  
        #-------------------------Fin------------------------
        #---------------------zonPLU-------------------------
        if widget == zonPLU:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()

                reader = codecs.open(os.path.dirname(__file__) + "/tables/Zonage_PLU.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if ';' + data + ';' in  ';' + str(zonPLU.text()) + ';':
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)
                champEnCours = "zonPLU"
                if myLayer.isEditable():
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(True)
                    permanence.setVisible(False)
                    retour.setVisible(True)
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)  
                    retour.setVisible(False)
                stack.setCurrentIndex(2)
            return False  
        #-------------------------Fin------------------------
        #-----------------------------valSocEco----------------------------------
        if widget == valSocEco:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()            
            
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Valeurs_Socio_Eco.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if ';' + data + '(' in  ';' + str(valSocEco.text()) :
                        if ';' + data + '(1)' in  ';' + str(valSocEco.text()) :
                            item.setFont(police1)
                        if ';' + data + '(2)' in  ';' + str(valSocEco.text()) :
                            item.setFont(police2)
                        if ';' + data + '(3)' in  ';' + str(valSocEco.text()) :
                            item.setFont(police3)
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)  
                if myLayer.isEditable():
                    principal.setVisible(True)
                    secondaire.setVisible(True)
                    complementaire.setVisible(True)
                    aller.setVisible(False)
                    permanence.setVisible(False)
                    retour.setVisible(True)
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)                  
                    retour.setVisible(False)
                stack.setCurrentIndex(2)
                champEnCours = "valSocEco"
            return False    

        #--------------Fin -------------------------------------------------
        #-----------------------------atteinte----------------------------------
        if widget == atteinte:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()            
            
                reader = codecs.open(os.path.dirname(__file__) + "/tables/Atteintes.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if ';' + data + '(' in  ';' + str(atteinte.text()) :
                        if ';' + data + '(1)' in  ';' + str(atteinte.text()) :
                            item.setFont(police1)
                        if ';' + data + '(2)' in  ';' + str(atteinte.text()) :
                            item.setFont(police2)
                        if ';' + data + '(3)' in  ';' + str(atteinte.text()) :
                            item.setFont(police3)
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)  
                if myLayer.isEditable():
                    principal.setVisible(True)
                    secondaire.setVisible(True)
                    complementaire.setVisible(True)
                    aller.setVisible(False)
                    permanence.setVisible(False)
                    retour.setVisible(True)
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)                  
                    retour.setVisible(False)
                stack.setCurrentIndex(2)
                champEnCours = "atteinte"
            return False    

        #--------------Fin -------------------------------------------------
        #---------------------menace-------------------------
        if widget == menace:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()

                reader = codecs.open(os.path.dirname(__file__) + "/tables/Menaces.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if ';' + data + ';' in  ';' + str(menace.text()) + ';':
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)
                champEnCours = "menace"
                if myLayer.isEditable():
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(True)
                    permanence.setVisible(False)
                    retour.setVisible(True)
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)  
                    retour.setVisible(False)
                stack.setCurrentIndex(2)
            return False
        #-------------------------Fin------------------------
        #---------------------foncMaj-------------------------
        if widget == foncMaj:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()

                reader = codecs.open(os.path.dirname(__file__) + "/tables/Fonctions_Majeures.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if ';' + data + ';' in  ';' + str(foncMaj.text()) + ';':
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)
                champEnCours = "foncMaj"
                if myLayer.isEditable():
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(True)
                    permanence.setVisible(False)
                    retour.setVisible(True)
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)
                    retour.setVisible(False)
                
                stack.setCurrentIndex(2)
            return False
        #-------------------------Fin------------------------
        #---------------------valMaj-------------------------
        if widget == valMaj:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()

                reader = codecs.open(os.path.dirname(__file__) + "/tables/Valeurs_Majeures.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if ';' + data + ';' in  ';' + str(valMaj.text()) + ';':
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)
                champEnCours = "valMaj"
                if myLayer.isEditable():
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(True)
                    permanence.setVisible(False)
                    retour.setVisible(True)
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)
                    retour.setVisible(False)

                stack.setCurrentIndex(2)
            return False
        #-------------------------Fin------------------------
        #---------------------preconAct-------------------------
        if widget == preconAct:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()

                reader = codecs.open(os.path.dirname(__file__) + "/tables/Preconisations_Actions.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if ';' + data + ';' in  ';' + str(preconAct.text()) + ';':
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)
                champEnCours = "preconAct"
                if myLayer.isEditable():
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(True)
                    permanence.setVisible(False)
                    retour.setVisible(True)
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)
                    retour.setVisible(False)
                
                stack.setCurrentIndex(2)
            return False
        #-------------------------Fin------------------------
        #---------------------contexInt-------------------------
        if widget == contexInt:
            if event.type() == QEvent.MouseButtonRelease:
                gFiltreMultiple.setVisible(False)
                cochePourcMult.setVisible(False)
                lstMultiple.clear()
                lstChoix.clear()

                reader = codecs.open(os.path.dirname(__file__) + "/tables/Contextes_Interventions.csv", 'r', encoding='utf-8')               
                for line in reader:
                    data, libelle = line.split(';')
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if ';' + data + ';' in  ';' + str(contexInt.text()) + ';':
                        lstChoix.addItem(item)                         
                    else:
                        lstMultiple.addItem(item)
                champEnCours = "contexInt"
                if myLayer.isEditable():
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(True)
                    permanence.setVisible(False)
                    retour.setVisible(True)
                else:
                    principal.setVisible(False)
                    secondaire.setVisible(False)
                    complementaire.setVisible(False)
                    aller.setVisible(False)
                    permanence.setVisible(False)
                    retour.setVisible(False)
                stack.setCurrentIndex(2)
            return False
        return False
        
def formOpen(dialog, layer, feature):


    global myDialog
    myDialog = dialog
    
    global myLayer
    myLayer = layer
    
    global myFeature
    myFeature = feature
    
    global stack
    stack = dialog.findChild(QStackedWidget,"stack")
    stack.setCurrentIndex(0)
    global tabGw
    tabGw =  dialog.findChild(QTabWidget, "tabGw")

    global champEnCours
    champEnCours =""
    
    global listePlante
    global cBArr
    global cBAESN
    global choixListe
    global cochePourc
    global cochePourcMult
    global pourc

    cBArr = dialog.findChild(QCheckBox, "cBArr")
    cBAESN = dialog.findChild(QCheckBox, "cBAESN")
    choixListe = dialog.findChild(QGroupBox,"choixListe")
    cochePourc = dialog.findChild(QCheckBox, "cochePourc")
    cochePourcMult = dialog.findChild(QCheckBox, "cochePourcMult")
    PATH = os.path.dirname(__file__) + "/config.txt"
    if os.path.isfile(PATH):
        
        #ouverture et lecture fichier config
        reader = codecs.open(os.path.dirname(__file__) + "/config.txt", 'r', encoding='utf-8') 
    else:
        reader = ""    
    listePlante = 'Arr'
    pourc = 'non'
    for line in reader:
        if "=" in line:
            variable,valeur= line.split('=')
            if "listePlante" in variable:
                listePlante=valeur  
            if "setGeometry" in variable:
                dialog.setGeometry(eval(valeur))
            if "pourcRecouvrement" in variable:
                pourc = valeur
    if "Arr" in listePlante:
        cBArr.setChecked(True)
    else:
        cBArr.setChecked(False)
    if "AESN" in listePlante:
        cBAESN.setChecked(True)
    else:
        cBAESN.setChecked(False)
    if "oui" in pourc:
        cochePourc.setChecked(True)
        cochePourcMult.setChecked(True)
    else:
        pourc = 'non'
        cochePourc.setChecked(False)
        cochePourcMult.setChecked(False)
        
    cBArr.released.connect(lambda: listePlanteChange())
    cBAESN.released.connect(lambda: listePlanteChange())
    cochePourc.released.connect(lambda: pourcRecouvChange())
    cochePourcMult.released.connect(lambda: pourcMultRecouvChange())
    infoPolyg = dialog.findChild(QLabel,"infoPolyg")

   #d = QgsDistanceArea()
    #d.setSourceCrs(layer.crs().srsid())
    #d.setEllipsoid(layer.crs().ellipsoidAcronym())
    #d.setEllipsoidalMode(True)
    if feature.geometry() != None:
        infoPolyg.setText(str(round(feature.geometry().area()/10000,2)) + u" ha")
    
#saisielibre
    global rqTypoPlain
    global rqGenePlain
    global rqHydroPlain
    global rqBioPlain
    global rqContextePlain
    global rqBilanPlain
    global recomTechPlain
    global espAnimalPlain

    global rqTypo
    global rqGene
    global rqHydro
    global rqBio
    global rqContexte
    global rqBilan
    global recomTech
    global espAnimal
    global toponyme
    
    global sitFonc
  
    sitFonc = dialog.findChild(QLineEdit,"sitFonc")
    
    if layer.isEditable():
        completer1 = QCompleter()
        sitFonc.setCompleter(completer1)    
        
        model1 = QStringListModel()
        completer1.setModel(model1)
     
        idx1 = myLayer.fieldNameIndex("sitFonc")
        values1 = myLayer.uniqueValues( idx1 )
        for item in values1:
            if str(item) is "NULL":
                values1.remove(item)
                break
        #tadam = str(values1).replace("NULL,","").replace("[","").replace("]","").replace(" u'","").replace("'","")
        #values1= tadam.split(", ")

        model1.setStringList(values1)

    
    rqTypoPlain = dialog.findChild(QPlainTextEdit,"rqTypoPlain")
    rqTypoPlain.textChanged.connect(rqTypoTextChanged)    
    rqTypo = dialog.findChild(QLineEdit,"rqTypo")
    rqTypoPlain.setPlainText(rqTypo.text())
    
    rqGenePlain = dialog.findChild(QPlainTextEdit,"rqGenePlain")
    rqGenePlain.textChanged.connect(rqGeneTextChanged)    
    rqGene = dialog.findChild(QLineEdit,"rqGene")
    rqGenePlain.setPlainText(rqGene.text())
    
    rqHydroPlain = dialog.findChild(QPlainTextEdit,"rqHydroPlain")
    rqHydroPlain.textChanged.connect(rqHydroTextChanged)
    rqHydro = dialog.findChild(QLineEdit,"rqHydro")
    rqHydroPlain.setPlainText(rqHydro.text())

    rqBioPlain = dialog.findChild(QPlainTextEdit,"rqBioPlain")
    rqBioPlain.textChanged.connect(rqBioTextChanged)
    rqBio = dialog.findChild(QLineEdit,"rqBio")   
    rqBioPlain.setPlainText(rqBio.text())
    
    rqContextePlain = dialog.findChild(QPlainTextEdit,"rqContextePlain")
    rqContextePlain.textChanged.connect(rqContexteTextChanged) 
    rqContexte = dialog.findChild(QLineEdit,"rqContexte")
    rqContextePlain.setPlainText(rqContexte.text())
    
    rqBilanPlain = dialog.findChild(QPlainTextEdit,"rqBilanPlain")
    rqBilanPlain.textChanged.connect(rqBilanTextChanged) 
    rqBilan = dialog.findChild(QLineEdit,"rqBilan")
    rqBilanPlain.setPlainText(rqBilan.text())
    
    recomTechPlain = dialog.findChild(QPlainTextEdit,"recomTechPlain")
    recomTechPlain.textChanged.connect(recomTechTextChanged)
    recomTech = dialog.findChild(QLineEdit,"recomTech")
    recomTechPlain.setPlainText(recomTech.text())
    
    espAnimalPlain = dialog.findChild(QPlainTextEdit,"espAnimalPlain")
    espAnimalPlain.textChanged.connect(espAnimalTextChanged)
    espAnimal = dialog.findChild(QLineEdit,"espAnimal")
    espAnimalPlain.setPlainText(espAnimal.text())
    
    toponyme = dialog.findChild(QLineEdit,"toponyme")
    toponyme.textChanged.connect(toponymeTextChanged) 
    if not layer.isEditable():
    
        rqTypoPlain.setEnabled(False)    
        rqGenePlain.setEnabled(False)
        rqHydroPlain.setEnabled(False)
        rqBioPlain.setEnabled(False)
        rqContextePlain.setEnabled(False)
        rqBilanPlain.setEnabled(False)
        recomTechPlain.setEnabled(False)
        espAnimalPlain.setEnabled(False)
        toponyme.setEnabled(False)
    else:
        rqTypoPlain.setEnabled(True)
        rqTypoPlain.textChanged.connect(validate)   
    
        rqGenePlain.setEnabled(True)
        rqGenePlain.textChanged.connect(validate)
        
        rqHydroPlain.setEnabled(True)
        rqHydroPlain.textChanged.connect(validate)
        
        rqBioPlain.setEnabled(True)
        rqBioPlain.textChanged.connect(validate)
        
        rqContextePlain.setEnabled(True)
        rqContextePlain.textChanged.connect(validate)
        
        rqBilanPlain.setEnabled(True)
        rqBilanPlain.textChanged.connect(validate)
        
        recomTechPlain.setEnabled(True)
        recomTechPlain.textChanged.connect(validate)
        
        espAnimalPlain.setEnabled(True)
        espAnimalPlain.textChanged.connect(validate)
        
        toponyme.setEnabled(True)
        toponyme.textChanged.connect(validate)
        
        
#date et  valeurs uniques#############################################################
    
        

         

#choix unique#############################################################

    if layer.isEditable():

        global datCreatio
        global observateur
        global calendarWidget
        global annulerDate
        global effacerDate
        global lFiltreUnique
        global tFiltreUnique
        global unique
        global lstUnique
        global prodrome1
        global corBio1
        global hydromSol
        global hydromApp
        global hydromDisp
        global freqSubm
        global etendSubm
        global diagHydro
        global etatCons
        global faisabInt
        global nivMenace
        global nivPrior


        annulerDate = dialog.findChild(QPushButton,"annulerDate")
        annulerDate.clicked.connect(annulerSaisieDate)
        
        effacerDate = dialog.findChild(QPushButton,"effacerDate")
        effacerDate.clicked.connect(effacerSaisieDate)
        
        datCreatio = dialog.findChild(QLineEdit,"datCreatio")
        _filter = Filter(datCreatio)
        datCreatio.installEventFilter(_filter)
        
        observateur = dialog.findChild(QLineEdit,"observateu")
        
        if layer.isEditable():
            completer2 = QCompleter()
            observateur.setCompleter(completer2)
            model2 = QStringListModel()
            completer2.setModel(model2)
            
            idx2 = myLayer.fieldNameIndex("observateu")
            values2 = myLayer.uniqueValues( idx2 )

            for item in values2:
                if str(item) is "NULL":
                    values2.remove(item)
                    break

            model2.setStringList(values2)

        
        calendarWidget = dialog.findChild(QCalendarWidget,"calendarWidget")
        calendarWidget.selectionChanged.connect(dateChange)
           
        unique = dialog.findChild(QWidget,"unique")
        _filter = Filter(unique)
        unique.installEventFilter(_filter)
        
        lstUnique = dialog.findChild(QListWidget,"lstUnique")   
        lstUnique.setProperty("FingerScrollable", True) 
        #lstUnique.itemSelectionChanged.connect(selLstUniqueChange) 
        lstUnique.itemClicked.connect(selLstUniqueChange) 
        
        tFiltreUnique = dialog.findChild(QLineEdit,"tFiltreUnique")    
        tFiltreUnique.textChanged.connect(tFiltreUniqueTextChanged) 

        lFiltreUnique = dialog.findChild(QLabel,"lFiltreUnique")    
   
        
        prodrome1 = dialog.findChild(QLineEdit,"prodrome1")
        _filter = Filter(prodrome1)
        prodrome1.installEventFilter(_filter)
        
        corBio1 = dialog.findChild(QLineEdit,"corBio1")
        _filter = Filter(corBio1)
        corBio1.installEventFilter(_filter)

        hydromSol = dialog.findChild(QLineEdit,"hydromSol")
        _filter = Filter(hydromSol)
        hydromSol.installEventFilter(_filter)

        hydromApp = dialog.findChild(QLineEdit,"hydromApp")
        _filter = Filter(hydromApp)
        hydromApp.installEventFilter(_filter)
        
        hydromDisp = dialog.findChild(QLineEdit,"hydromDisp")
        _filter = Filter(hydromDisp)
        hydromDisp.installEventFilter(_filter)
        
        freqSubm = dialog.findChild(QLineEdit,"freqSubm")
        _filter = Filter(freqSubm)
        freqSubm.installEventFilter(_filter)
        
        etendSubm = dialog.findChild(QLineEdit,"etendSubm")
        _filter = Filter(etendSubm)
        etendSubm.installEventFilter(_filter)
        
        diagHydro = dialog.findChild(QLineEdit,"diagHydro")
        _filter = Filter(diagHydro)
        diagHydro.installEventFilter(_filter)
        
        faisabInt = dialog.findChild(QLineEdit,"faisabInt")
        _filter = Filter(faisabInt)
        faisabInt.installEventFilter(_filter)
        
        etatCons = dialog.findChild(QLineEdit,"etatCons")
        _filter = Filter(etatCons)
        etatCons.installEventFilter(_filter)
        
        nivMenace = dialog.findChild(QLineEdit,"nivMenace")
        _filter = Filter(nivMenace)
        nivMenace.installEventFilter(_filter)
        
        nivPrior = dialog.findChild(QLineEdit,"nivPrior")
        _filter = Filter(nivPrior)
        nivPrior.installEventFilter(_filter)
#finChoixUnique#################################################################################################################


#choix multiple################################################################################################################## 
    global gFiltreMultiple
    global tFiltreMultiple
    global tFiltreMultipleEV
    global multiple

    global inconnu
    global saisonnier
    global temporaire
    global permanent
    
    global lstMultiple
    global lstChoix
    global annulerMultiple
    global validerMultiple
    global lstMultiple_2
    global lstChoix_2
    global annulerMultiple_2
    global validerMultiple_2
    global principal
    global secondaire
    global complementaire
    global aller
    global retour
    global aller_2
    global retour_2
    global permanence
    global prodrome2
    global corBio2
    global SAGE
    global critDelim
    global entreeEau
    global sortieEau
    global foncHydro
    global foncEpur
    global espVegetal
    global espVegetalPlain
    global foncBio
    global actDans
    global actAutour
    global instrument
    global foncier
    global zonPLU
    global valSocEco
    global atteinte
    global menace
    global foncMaj
    global valMaj
    global preconAct
    global contexInt   

    global police1
    global police2
    global police3  
    
    police1 = QFont("Arial",8)
    police1.setBold(True)
    police1.setUnderline(True)     
    police2 = QFont("Arial",8) 
    police2.setBold(True)
    police2.setUnderline(False)    
    police3 = QFont("Arial",8)    
    police3.setBold(False)
    police3.setUnderline(False) 
    
    gFiltreMultiple = dialog.findChild(QGroupBox,"gFiltreMultiple")
    tFiltreMultiple = dialog.findChild(QLineEdit, "tFiltreMultiple")
    
    tFiltreMultipleEV = dialog.findChild(QLineEdit, "tFiltreMultipleEV")
    
    multiple = dialog.findChild(QWidget,"multiple")

    inconnu = dialog.findChild(QRadioButton, "inconnu")
    saisonnier = dialog.findChild(QRadioButton, "saisonnier")
    temporaire = dialog.findChild(QRadioButton, "temporaire")
    permanent = dialog.findChild(QRadioButton, "permanent")

    lstMultiple = dialog.findChild(QListWidget,"listMultiple")
    lstChoix = dialog.findChild(QListWidget,"listChoix")
    lstMultiple_2 = dialog.findChild(QListWidget,"listMultiple_2")
    lstChoix_2 = dialog.findChild(QListWidget,"listChoix_2")     
    permanence = dialog.findChild(QGroupBox,"permanence")
    retour = dialog.findChild(QPushButton,"retour")
    aller = dialog.findChild(QPushButton,"aller")
    retour_2 = dialog.findChild(QPushButton,"retour_2")
    aller_2 = dialog.findChild(QPushButton,"aller_2")
    principal = dialog.findChild(QPushButton,"principal")
    secondaire = dialog.findChild(QPushButton,"secondaire")
    complementaire = dialog.findChild(QPushButton,"complementaire")
    annulerMultiple = dialog.findChild(QPushButton, "annulerMultiple")
    validerMultiple = dialog.findChild(QPushButton, "validerMultiple")
    annulerMultiple_2 = dialog.findChild(QPushButton, "annulerMultiple_2")
    validerMultiple_2 = dialog.findChild(QPushButton, "validerMultiple_2")
    
    tFiltreMultipleEV.textChanged.connect(tFiltreMultipleTextChanged)
    tFiltreMultiple.textChanged.connect(tFiltreMultipleTextChanged)
    aller.clicked.connect(lambda: btnMult(aller))
    aller_2.clicked.connect(lambda: btnMult(aller_2))
    principal.clicked.connect(lambda: btnMult(principal))
    secondaire.clicked.connect(lambda: btnMult(secondaire))
    complementaire.clicked.connect(lambda: btnMult(complementaire))
    retour.clicked.connect(lambda: btnMult(retour))
    retour_2.clicked.connect(lambda: btnMult(retour_2))
    annulerMultiple.clicked.connect(lambda: btnMult(annulerMultiple))
    validerMultiple.clicked.connect(lambda: btnMult(validerMultiple))
    annulerMultiple_2.clicked.connect(lambda: btnMult(annulerMultiple))
    validerMultiple_2.clicked.connect(lambda: btnMult(validerMultiple_2))
    
    prodrome2 = dialog.findChild(QLineEdit,"prodrome2")
    _filter = Filter(prodrome2)
    prodrome2.installEventFilter(_filter)    
    corBio2 = dialog.findChild(QLineEdit,"corBio2")
    _filter = Filter(corBio2)
    corBio2.installEventFilter(_filter)
    
    SAGE = dialog.findChild(QLineEdit,"SAGE")
    _filter = Filter(SAGE)
    SAGE.installEventFilter(_filter)    
    
    critDelim = dialog.findChild(QLineEdit,"critDelim")
    _filter = Filter(critDelim)
    critDelim.installEventFilter(_filter)
    entreeEau = dialog.findChild(QLineEdit,"entreeEau")
    _filter = Filter(entreeEau)
    entreeEau.installEventFilter(_filter)
    sortieEau = dialog.findChild(QLineEdit,"sortieEau")
    _filter = Filter(sortieEau)
    sortieEau.installEventFilter(_filter)    
    foncHydro = dialog.findChild(QLineEdit,"foncHydro")
    _filter = Filter(foncHydro)
    foncHydro.installEventFilter(_filter)    
    foncEpur = dialog.findChild(QLineEdit,"foncEpur")
    _filter = Filter(foncEpur)
    foncEpur.installEventFilter(_filter)
    
    espVegetalPlain = dialog.findChild(QPlainTextEdit,"espVegetalPlain")
    espVegetal = dialog.findChild(QLineEdit,"espVegetal")
    espVegetalPlain.setPlainText(espVegetal.text())
    _filter = Filter(espVegetal)
    espVegetalPlain.installEventFilter(_filter)  

    if layer.isEditable():
        
        espVegetalPlain.setEnabled(True)
        espVegetalPlain.textChanged.connect(validate)
    
    foncBio = dialog.findChild(QLineEdit,"foncBio")
    _filter = Filter(foncBio)
    foncBio.installEventFilter(_filter)    
    actDans = dialog.findChild(QLineEdit,"actDans")
    _filter = Filter(actDans)
    actDans.installEventFilter(_filter)    
    actAutour = dialog.findChild(QLineEdit,"actAutour")
    _filter = Filter(actAutour)
    actAutour.installEventFilter(_filter)    
    instrument = dialog.findChild(QLineEdit,"instrument")
    _filter = Filter(instrument)
    instrument.installEventFilter(_filter)    
    foncier = dialog.findChild(QLineEdit,"foncier")
    _filter = Filter(foncier)
    foncier.installEventFilter(_filter)    
    zonPLU = dialog.findChild(QLineEdit,"zonPLU")
    _filter = Filter(zonPLU)
    zonPLU.installEventFilter(_filter)    
    valSocEco = dialog.findChild(QLineEdit,"valSocEco")
    _filter = Filter(valSocEco)
    valSocEco.installEventFilter(_filter)    
    atteinte = dialog.findChild(QLineEdit,"atteinte")
    _filter = Filter(atteinte)
    atteinte.installEventFilter(_filter)    
    menace = dialog.findChild(QLineEdit,"menace")
    _filter = Filter(menace)
    menace.installEventFilter(_filter)    
    foncMaj = dialog.findChild(QLineEdit,"foncMaj")
    _filter = Filter(foncMaj)
    foncMaj.installEventFilter(_filter)    
    valMaj = dialog.findChild(QLineEdit,"valMaj")
    _filter = Filter(valMaj)
    valMaj.installEventFilter(_filter)    
    preconAct = dialog.findChild(QLineEdit,"preconAct")
    _filter = Filter(preconAct)
    preconAct.installEventFilter(_filter)    
    contexInt = dialog.findChild(QLineEdit,"contexInt")
    _filter = Filter(contexInt)
    contexInt.installEventFilter(_filter)    

#case a cocher
    global propoZHIEP
    global propoZSGE
    
    propoZHIEP = dialog.findChild(QCheckBox,"propoZHIEP")
    propoZSGE = dialog.findChild(QCheckBox,"propoZSGE")  
    
    propoZSGE.stateChanged.connect(lambda: propoZS(feature))
    propoZHIEP.stateChanged.connect(lambda: propoZH(feature))
    
        
    if not layer.isEditable():
        propoZHIEP.setEnabled(False)
        propoZSGE.setEnabled(False)
    else:
        propoZHIEP.setEnabled(True)
        propoZSGE.setEnabled(True)
#photos
    
    global image
    global plus
    global moins
    global gauche
    global droite
    global lPhoto
    global photo1
    global photo2
    global photo3
    global photo4
    image = dialog.findChild(QLabel,"image")    
    plus = dialog.findChild(QPushButton,"plus")
    moins = dialog.findChild(QPushButton,"moins")
    gauche = dialog.findChild(QPushButton,"gauche")
    droite = dialog.findChild(QPushButton,"droite")
    lPhoto = dialog.findChild(QLabel,"lPhoto")
    photo1 = dialog.findChild(QLineEdit,"photo1")
    photo2 = dialog.findChild(QLineEdit,"photo2")   
    photo3 = dialog.findChild(QLineEdit,"photo3")   
    photo4 = dialog.findChild(QLineEdit,"photo4")  
    if layer.isEditable():
        plus.clicked.connect(lambda: btnPhoto(plus,feature))
        moins.clicked.connect(lambda: btnPhoto(moins,feature))
    else:
        plus.setVisible(False)
        moins.setVisible(False)
    gauche.clicked.connect(lambda: btnPhoto(gauche,feature))
    droite.clicked.connect(lambda: btnPhoto(droite,feature))
   
    affichePhoto(feature)

    buttonBox = dialog.findChild(QDialogButtonBox,"dialogButtonBox")

    if layer.isEditable():
        dialog.attributeChanged.connect(validate)
        #buttonBox.accepted.disconnect(myDialog.accept)

    #buttonBox.accepted.connect(validate)
    #buttonBox.rejected.connect(myDialog.reject)

      #featureForm.disconnectButtonBox()
        #buttonBox.accepted.disconnect(myDialog.accept)
        #buttonBox.accepted.connect(validate)
        #buttonBox.rejected.connect(myDialog.resetValues)
    
        _filter = Filter(myDialog)
        myDialog.installEventFilter(_filter)
def modifFichierConfig():

    config ='' 
    PATH = os.path.dirname(__file__) + "/config.txt"
    if os.path.isfile(PATH):
        
        with open(os.path.dirname(__file__) + "/config.txt",'r') as f:
            lines = f.readlines()
            for line in lines:
                # str.lower permet de ne pas s'occuper des majuscules
                if "listePlante" in line :
                    config = config + "listePlante=" + listePlante  + '\r\n'
                elif "pourcRecouvrement" in line : 
                    config = config + "pourcRecouvrement=" + pourc  + '\r\n'
                else:
                    if not line.replace(' ','').replace('\r\n', '').replace('\r', '').replace('\n', '') == '':
                        config = config + line
            if not listePlante in config:
                config = config + "listePlante=Arr" + '\r\n'
            elif not 'pourcRecouvrement' in config:
                config = config + "pourcRecouvrement=" + pourc + '\r\n'
        f.close
    else:
        config = "setGeometry=" + str(myDialog.geometry()).replace("PyQt4.QtCore.","") + '\r\n' + "listePlante=Arr" + '\r\n' + "pourRecouvrement=non" + '\r\n'
    with open(os.path.dirname(__file__) + "/config.txt",'w') as g:
        config = config.replace('\r\r','\n').replace('\r\n','\n').replace('\n\n','\n')
        g.write(config)
        g.close
def pourcRecouvChange():

    global pourc
    if cochePourc.isChecked()  :
        pourc = "oui"
        cochePourcMult.setChecked(True)
    else:
        pourc = "non"
        cochePourcMult.setChecked(False)

    modifFichierConfig()
def pourcMultRecouvChange():
    global pourc
    if cochePourcMult.isChecked()  :
        pourc = "oui"
        cochePourc.setChecked(True)
    else:
        pourc = "non"
        cochePourc.setChecked(False)
    modifFichierConfig()
def listePlanteChange():

    global listePlante
    listePlante = ""
    if cBArr.isChecked():
        listePlante = "Arr"
    if cBAESN.isChecked():
        if listePlante == "":
            listePlante = "AESN"
        else:
            listePlante = listePlante + ",AESN"

    if  not cBArr.isChecked() and not cBAESN.isChecked():
        listePlante = "Arr"
        cBArr.setChecked(True)
        cBArr.update()
    modifFichierConfig()

    
    lstMultiple_2.clear()

    concat=""
    for i in range(lstChoix_2.count()): 
        if concat == "":
            concat = lstChoix_2.item(i).data(3)
        else:
            concat = concat + ";" + lstChoix_2.item(i).data(3)   

    
    
    reader = codecs.open(os.path.dirname(__file__) + u"/tables/Especes_Vegetales.csv", 'r', encoding='utf-8')               
    for line in reader:
        data, libelle, Arr, AESN = line.replace('\r\n', '').replace('\r', '').replace('\n', '').split(';')
        item = QListWidgetItem(libelle)
        item.setData(3,data)
        if ';' + data + ';' in  ';' + concat + ';':
            lstChoix.addItem(item)                         
        else:
            if ("Arr" in listePlante and Arr == "1") or ("AESN" in listePlante and AESN == "1"):
                lstMultiple_2.addItem(item)   
def propoZH(feature):
    if not propoZHIEP.isChecked():
        propoZSGE.setChecked(False)
def propoZS(feature):
    if propoZSGE.isChecked():
        propoZHIEP.setChecked(True)
def affichePhoto(feature):
    mort = False
    lien = ""
    if photo1.text() and photo1.text() != "NULL":
        lien = u"Photo1 : " + photo1.text()
        if os.path.isfile(photo1.text()):
            image.setPixmap(QPixmap(photo1.text()).scaled(image.width(),image.height(),Qt.KeepAspectRatio,Qt.FastTransformation))
            lPhoto.setText(u"Photo1 : " + photo1.text())
        else:
            mort = True
    if photo2.text() and photo2.text() != "NULL":
        if lien == "":
            lien = u"Photo2 : " + photo2.text()
        if os.path.isfile(photo2.text()):
            if lPhoto.text() == "":
                image.setPixmap(QPixmap(photo2.text()).scaled(image.width(),image.height(),Qt.KeepAspectRatio,Qt.FastTransformation))
                lPhoto.setText(u"Photo2 : " + photo2.text())
        else:
            mort = True
    if photo3.text() and photo3.text() != "NULL":
        if lien == "":
            lien = u"Photo3 : " + photo3.text()
        if os.path.isfile(photo3.text()):
            if lPhoto.text() == "":
                image.setPixmap(QPixmap(photo3.text()).scaled(image.width(),image.height(),Qt.KeepAspectRatio,Qt.FastTransformation))
                lPhoto.setText(u"Photo3 : " + photo3.text())
        else:
            mort = True
    if photo4.text() and photo4.text() != "NULL":
        if lien == "":
            lien = u"Photo4 : " + photo4.text()
        if os.path.isfile(photo4.text()):
            if lPhoto.text() == "":
                image.setPixmap(QPixmap(photo4.text()).scaled(image.width(),image.height(),Qt.KeepAspectRatio,Qt.FastTransformation))
                lPhoto.setText(u"Photo4 : " + photo4.text())
        else:
            mort = True
    if lPhoto.text() == "":
        if lien == "":
            image.setPixmap(QPixmap("./images/ap.png"))
            lPhoto.setText(u"Photo1")
        else:
            image.setPixmap(QPixmap("./images/apD.png"))
            lPhoto.setText(lien)            
    if myLayer.isEditable():  
        if mort == True:
            lienMort(feature)
def lienMort(feature):
    reply = QMessageBox.question(myDialog,u"Fichier inexistant",u"Un ou plusieurs liens vers des photos sont invalides. Souhaitez-vous les effacer?",QMessageBox.Yes,QMessageBox.No)   
    if reply == QMessageBox.Yes:
        if photo1.text():
            if not os.path.isfile(photo1.text()):
                if lPhoto.text() == u"Photo1 : " + photo1.text():
                    lPhoto.setText(u"Photo1")
                    image.setPixmap(QPixmap("./images/ap.png"))
                photo1.setText(u"")
        if photo2.text():              
            if not os.path.isfile(photo2.text()):
                if lPhoto.text() == u"Photo2 : " + photo2.text():
                    lPhoto.setText(u"Photo2")
                    image.setPixmap(QPixmap("./images/ap.png"))
                photo2.setText(u"")
        if photo3.text:                
            if not os.path.isfile(photo3.text()):
                if lPhoto.text() == u"Photo3 : " + photo3.text():
                    lPhoto.setText(u"Photo3")
                    image.setPixmap(QPixmap("./images/ap.png"))
                photo3.setText(u"")
        if photo4.text:                
            if not os.path.isfile(photo4.text()):
                if lPhoto.text() == u"Photo4 : " + photo4.text():
                    lPhoto.setText(u"Photo4")
                    image.setPixmap(QPixmap("./images/ap.png"))
                photo4.setText(u"")
        affichePhoto(feature)
def btnPhoto(btn,feature):
    if btn == plus:
        if (photo4.text() and photo4.text() != "NULL") and (photo3.text() and photo3.text() != "NULL") and (photo2.text() and photo2.text() != "NULL") and (photo1.text() and photo1.text() != "NULL" ):
            msgBox = QMessageBox()
            msgBox.setText(u"La liste de photos est pleine. Il faut d'abord en supprimer une pour pouvoir en renseigner une nouvelle.")
            msgBox.exec_()
        else:
            fileName = QFileDialog.getOpenFileName(myDialog,u"Open Image", u"C:\\", u"(*.jpg)")
            if fileName != None:       
                if not photo1.text() or photo1.text() == "NULL":
                    photo1.setText(fileName)
                    image.setPixmap(QPixmap(photo1.text()).scaled(image.width(),image.height(),Qt.KeepAspectRatio,Qt.FastTransformation))
                    lPhoto.setText(u"Photo1 : " + photo1.text())
                    
                elif not photo2.text() or photo2.text() == "NULL":
                    photo2.setText(fileName)
                    image.setPixmap(QPixmap(photo2.text()).scaled(image.width(),image.height(),Qt.KeepAspectRatio,Qt.FastTransformation))
                    lPhoto.setText(u"Photo2 : " + photo2.text())

                elif not photo3.text() or photo3.text() == "NULL":
                    photo3.setText(fileName)
                    image.setPixmap(QPixmap(photo3.text()).scaled(image.width(),image.height(),Qt.KeepAspectRatio,Qt.FastTransformation))
                    lPhoto.setText(u"Photo3 : " + photo3.text()) 

                elif not photo4.text() or photo4.text() == "NULL":
                    photo4.setText(fileName)
                    image.setPixmap(QPixmap(photo4.text()).scaled(image.width(),image.height(),Qt.KeepAspectRatio,Qt.FastTransformation))
                    lPhoto.setText(u"Photo4 : " + photo4.text())
                    
    elif btn == moins:
        reply = QMessageBox.question(myDialog,u"Annulation",u"Etes-vous sur de vouloir effacer le lien vers cette photo?",QMessageBox.Yes,QMessageBox.No)
        if reply == QMessageBox.Yes:   
            if lPhoto.text()[5:6] == "1":
                photo1.setText(u"")
            elif lPhoto.text()[5:6] == "2":
                photo2.setText(u"")        
            elif lPhoto.text()[5:6] == "3":
                photo3.setText(u"")       
            elif lPhoto.text()[5:6] == "4":
                photo4.setText(u"")       
            lPhoto.setText(u"")
            affichePhoto(feature)
    elif btn == gauche:
        if lPhoto.text()[:6] == "Photo1":
            if photo4.text():
                lPhoto.setText(u"Photo4 : " + photo4.text())
                if os.path.isfile(photo4.text()):
                    image.setPixmap(QPixmap(photo4.text()).scaled(image.width(),image.height(),Qt.KeepAspectRatio,Qt.FastTransformation))
                else:
                    image.setPixmap(QPixmap("./images/apD.png"))
            else:
                image.setPixmap(QPixmap("./images/ap.png"))
                lPhoto.setText(u"Photo4")
        else:
            if lPhoto.text()[5:6] == "2":
                lineEdit = photo1
            elif lPhoto.text()[5:6] == "3":
                lineEdit = photo2      
            elif lPhoto.text()[5:6] == "4":
                lineEdit = photo3    

            if lineEdit.text():
                lPhoto.setText(u"Photo" + str(int(lPhoto.text()[5:6])-1) + " : " + lineEdit.text())
                if os.path.isfile(lineEdit.text()):
                    image.setPixmap(QPixmap(lineEdit.text()).scaled(image.width(),image.height(),Qt.KeepAspectRatio,Qt.FastTransformation))
                else:
                    image.setPixmap(QPixmap("./images/apD.png"))                   
            else:
                image.setPixmap(QPixmap("./images/ap.png"))
                lPhoto.setText(u"Photo" + str(int(lPhoto.text()[5:6])-1))        

        
    elif btn == droite:
        if lPhoto.text()[:6] == "Photo4":
            if photo1.text():
                lPhoto.setText(u"Photo1 : " + photo1.text())
                if os.path.isfile(photo1.text()):
                    image.setPixmap(QPixmap(photo1.text()).scaled(image.width(),image.height(),Qt.KeepAspectRatio,Qt.FastTransformation))
                else:
                    image.setPixmap(QPixmap("./images/apD.png"))
            else:
                image.setPixmap(QPixmap("./images/ap.png"))
                lPhoto.setText(u"Photo1")
        else:
            if lPhoto.text()[5:6] == "2":
                lineEdit = photo3
            elif lPhoto.text()[5:6] == "3":
                lineEdit = photo4      
            elif lPhoto.text()[5:6] == "1":
                lineEdit = photo2      
            if lineEdit.text():
                lPhoto.setText(u"Photo" + str(int(lPhoto.text()[5:6])+1) + " : " + lineEdit.text())
                if os.path.isfile(lineEdit.text()):
                    image.setPixmap(QPixmap(lineEdit.text()).scaled(image.width(),image.height(),Qt.KeepAspectRatio,Qt.FastTransformation))
                else:
                    image.setPixmap(QPixmap(u"./images/apD.png"))                   
            else:
                image.setPixmap(QPixmap(u"./images/ap.png"))
                lPhoto.setText(u"Photo" + str(int(lPhoto.text()[5:6])+1))
def dialGeom():
 
    config =''   

    PATH = os.path.dirname(__file__) + "/config.txt"

    if os.path.isfile(PATH): 

        with open(os.path.dirname(__file__) + "/config.txt",'r') as f:
            lines = f.readlines()
            for line in lines:
                if "setGeometry" in line :
                    line = "setGeometry=" + str(myDialog.geometry()).replace("PyQt4.QtCore.","") + '\r\n'
                else:
                    if not line.replace(' ','').replace('\r\n', '').replace('\r', '').replace('\n', '') == '':
                        config = config + line
            if not 'setGeometry' in config:
                config = config +  "setGeometry=" + str(myDialog.geometry()).replace("PyQt4.QtCore.","") +'\r\n'
        f.close
    else:

        config = "setGeometry=" + str(myDialog.geometry()).replace("PyQt4.QtCore.","") + '\r\n' + "listePlante=Arr" + '\r\n'
    with open(os.path.dirname(__file__) + "/config.txt",'w') as g:

        g.write(config)
        g.close
def btnMult(btn):
    global champEnCours

    if btn == aller:
        items = lstMultiple.selectedItems()
        
        if champEnCours in u"corBio2,prodrome2":

            concat=""
            for i in range(lstChoix.count()): 
                if concat == "":
                    concat = lstChoix.item(i).data(3)
                    if '%]' in lstChoix.item(i).text():
                        biotope,pore = lstChoix.item(i).text().split('[')
                        pore = pore.replace('%]','').rstrip()
                        concat = concat + "[" + pore + "%]"
                else:
                    concat = concat + ";" + lstChoix.item(i).data(3)
                    if '%]' in lstChoix.item(i).text():
                        biotope,pore = lstChoix.item(i).text().split('[')
                        pore = pore.replace('%]','').rstrip()
                        concat = concat + "[" + pore + "%]"

                                            
            for j in list(items):

                it = lstMultiple.takeItem(lstMultiple.row(j))            
                if concat == "":

                    concat = it.data(3)
                    lstChoix.addItem(it)
                    if u'oui' in pourc :

                        (value, ok) = QInputDialog.getInt (myDialog, "% recouvrement", str(it.text()) + ' :') 
                        if ok and value <101 and value > 0:
                            it.setText(it.text().replace('\r','').replace('\n','') + '[' +  str(value) + '%]' + '\r\n')
                            concat = concat + '[' + str(value) + '%]'   
                else:
                    concat = concat + ";" + it.data(3)
                    if u'oui' in pourc :
                        (value, ok) = QInputDialog.getInt (myDialog, "% recouvrement", str(it.text()) + ' :') 
                        if ok and value <101 and value>0:
                            it.setText(it.text().replace('\r','').replace('\n','') + '[' +  str(value) + '%]' + '\r\n')
                            concat = concat + '[' + str(value) + '%]'   

                    if len(concat)> 254:
                        m = QMessageBox()
                        m.setText(u"le champ est limité à 254 caractère. " + it.text() + u" ne peut être ajouté.")
                        m.exec_()
                    else:
                        lstChoix.addItem(it)
        else:        
            for k in list(items):
                it = lstMultiple.takeItem(lstMultiple.row(k))
                lstChoix.addItem(it)    
            lstChoix.sortItems()
    elif btn == aller_2:
        items = lstMultiple_2.selectedItems()
        if champEnCours == u"espVegetal":
            concat=""
            for i in range(lstChoix_2.count()): 
                if concat == "":
                    concat = lstChoix_2.item(i).data(3)
                else:
                    concat = concat + ";" + lstChoix_2.item(i).data(3)
            for j in list(items):
                it = lstMultiple_2.takeItem(lstMultiple_2.row(j))            
                if concat == "":
                    concat = it.data(3)
                    lstChoix_2.addItem(it)
                else:
                    concat = concat + ";" + it.data(3)
                    if len(concat)> 254:
                        m = QMessageBox()
                        m.setText(u"le champ est limité à 254 caractère. " + it.text() + u" ne peut être ajouté.")
                        m.exec_()
                    else:
                        lstChoix_2.addItem(it)        
        
    elif btn == principal:

        items = lstMultiple.selectedItems()
        for i in list(items):

            it = lstMultiple.takeItem(lstMultiple.row(i))
            if champEnCours in u"entreeEau,sortieEau":
                if inconnu.isChecked():
                    it.setText(it.text()[:len(it.text())-2] + u" (Inconnu)" + it.text()[len(it.text())-2:] )
                if saisonnier.isChecked():
                    it.setText(it.text()[:len(it.text())-2] + u" (Saisonnier)" + it.text()[len(it.text())-2:])
                if permanent.isChecked():
                    it.setText(it.text()[:len(it.text())-2] + u" (Permanent)" + it.text()[len(it.text())-2:])
                if temporaire.isChecked():
                    it.setText(it.text()[:len(it.text())-2] + u" (Temporaire/Intermittent)" + it.text()[len(it.text())-2:])
            it.setFont(police1)
            lstChoix.addItem(it)
        lstChoix.sortItems()

    elif btn == secondaire:

        items = lstMultiple.selectedItems()
        for i in list(items):
            it = lstMultiple.takeItem(lstMultiple.row(i))
            if champEnCours in u"entreeEau,sortieEau":
                if inconnu.isChecked():
                    it.setText(it.text()[:len(it.text())-2] + u" (Inconnu)" + it.text()[len(it.text())-2:] )
                if saisonnier.isChecked():
                    it.setText(it.text()[:len(it.text())-2] + u" (Saisonnier)" + it.text()[len(it.text())-2:])
                if permanent.isChecked():
                    it.setText(it.text()[:len(it.text())-2] + u" (Permanent)" + it.text()[len(it.text())-2:])
                if temporaire.isChecked():
                    it.setText(it.text()[:len(it.text())-2] + u" (Temporaire/Intermittent)" + it.text()[len(it.text())-2:])
            it.setFont(police2)
            lstChoix.addItem(it)
        lstChoix.sortItems() 

    elif btn == complementaire:

        items = lstMultiple.selectedItems()
        for i in list(items):
            it = lstMultiple.takeItem(lstMultiple.row(i))
            if champEnCours in u"entreeEau,sortieEau":
                if inconnu.isChecked():
                    it.setText(it.text()[:len(it.text())-2] + u" (Inconnu)" + it.text()[len(it.text())-2:] )
                if saisonnier.isChecked():
                    it.setText(it.text()[:len(it.text())-2] + u" (Saisonnier)" + it.text()[len(it.text())-2:])
                if permanent.isChecked():
                    it.setText(it.text()[:len(it.text())-2] + u" (Permanent)" + it.text()[len(it.text())-2:])
                if temporaire.isChecked():
                    it.setText(it.text()[:len(it.text())-2] + u" (Temporaire/Intermittent)" + it.text()[len(it.text())-2:])
            it.setFont(police3)
            lstChoix.addItem(it)
        lstChoix.sortItems()

    elif btn == retour:
        items = lstChoix.selectedItems()
        for i in list(items):
            it = lstChoix.takeItem(lstChoix.row(i))
            it.setFont(police3)
            if champEnCours in u"entreeEau,sortieEau":
                it.setText(it.text().replace(u" (Inconnu)",""))
                it.setText(it.text().replace(u" (Saisonnier)",""))
                it.setText(it.text().replace(u" (Permanent)",""))
                it.setText(it.text().replace(u" (Temporaire/Intermittent)",""))
            if champEnCours in u"corBio2,prodrome2":
                if "%]" in it.text():
                    garde,jete = it.text().split('[')
                    garde=garde.strip()
                    it.setText(garde)
            
            lstMultiple.addItem(it)
        lstMultiple.sortItems
    elif btn == retour_2:
        items = lstChoix_2.selectedItems()
        for i in list(items):
            it = lstChoix_2.takeItem(lstChoix_2.row(i))
            it.setFont(police3)
            lstMultiple_2.addItem(it)
        lstMultiple_2.sortItems
    elif btn == annulerMultiple:
        champEnCours =""
        

        stack.setCurrentIndex(0)
    elif btn == validerMultiple:
        #items = lstChoix.findItems("",Qt.MatchRegExp)
        concat=""
        for i in range(lstChoix.count()): 
            if concat == "":
                concat = lstChoix.item(i).data(3)
                if '%]' in lstChoix.item(i).text():
                    biotope,pore = lstChoix.item(i).text().split('[')
                    pore = pore.replace('%]','').strip()
                    concat = concat + "[" + pore + "%]"   
            else:
                concat = concat + ";" + lstChoix.item(i).data(3)
                if '%]' in lstChoix.item(i).text():
                    biotope,pore = lstChoix.item(i).text().split('[')
                    pore = pore.replace('%]','').strip()
                    concat = concat + "[" + pore + "%]"
            if champEnCours in u"critDelim,entreeEau,sortieEau,foncHydro,foncEpur,foncBio,actDans,actAutour,valSocEco,atteinte":
                
                if lstChoix.item(i).font() == police1:
                    concat = concat + u"(1)"
                elif lstChoix.item(i).font() == police2:
                    concat = concat + u"(2)"
                elif lstChoix.item(i).font() == police3:
                    concat = concat + u"(3)"
                if champEnCours in u"entreeEau,sortieEau":
                #ajout permanence
                    if u"(Inconnu)" in lstChoix.item(i).text():
                        concat = concat + u"[0]"
                    elif u"(Temporaire/Intermittent)" in lstChoix.item(i).text():
                        concat = concat + u"[5]"
                    elif u"(Saisonnier)" in lstChoix.item(i).text():
                        concat = concat + u"[4]"
                    elif u"(Permanent)" in lstChoix.item(i).text():
                        concat = concat + u"[3]"
                    
        if champEnCours == "critDelim":
            critDelim.setText(concat)
        if champEnCours == "prodrome2":
            prodrome2.setText(concat)
        if champEnCours == "corBio2":
            corBio2.setText(concat)
        if champEnCours == "SAGE":
            SAGE.setText(concat)           
        if champEnCours == "entreeEau":
            entreeEau.setText(concat)
        if champEnCours == "sortieEau":
            sortieEau.setText(concat)
        if champEnCours == "foncHydro":
            foncHydro.setText(concat)
        if champEnCours == "foncEpur":
            foncEpur.setText(concat)
        if champEnCours == "foncBio":
            foncBio.setText(concat)
        if champEnCours == "actDans":
            actDans.setText(concat)
        if champEnCours == "actAutour":
            actAutour.setText(concat)
        if champEnCours == "instrument":
            instrument.setText(concat)
        if champEnCours == "foncier":
            foncier.setText(concat)
        if champEnCours == "zonPLU":
            zonPLU.setText(concat)
        if champEnCours == "valSocEco":
            valSocEco.setText(concat)
        if champEnCours == "atteinte":
            atteinte.setText(concat)
        if champEnCours == "menace":
            menace.setText(concat)
        if champEnCours == "foncMaj":
            foncMaj.setText(concat)
        if champEnCours == "valMaj":
            valMaj.setText(concat)
        if champEnCours == "preconAct":
            preconAct.setText(concat)
        if champEnCours == "contexInt":
            contexInt.setText(concat)            
        tabGw.setFocus()
        champEnCours =""

        stack.setCurrentIndex(0)   
    elif btn == validerMultiple_2:
        concat=""
        for i in range(lstChoix_2.count()): 
            if concat == "":
                concat = lstChoix_2.item(i).data(3)
            else:
                concat = concat + ";" + lstChoix_2.item(i).data(3)
        espVegetalPlain.setPlainText(concat)         
        tabGw.setFocus()
        champEnCours =""

        stack.setCurrentIndex(0)
def tFiltreMultipleTextChanged():
    global champEnCours
    if champEnCours == "corBio2":
        
        lstMultiple.clear()
        reader = codecs.open(os.path.dirname(__file__) + "/tables/Corine_Biotope.csv", 'r', encoding='utf-8')               
        for line in reader:
            
            if line[:1] != u";":
                data, libelle = line.split(';')
                if data[:len(tFiltreMultiple.text())]==tFiltreMultiple.text() or libelle[len(data)+1:len(data)+1+len(tFiltreMultiple.text())].lower()==tFiltreMultiple.text().lower():
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if not  ';' + data + ';' in  ';' + str(corBio2.text()) + ';':
                        lstMultiple.addItem(item)
        champEnCours = "corBio2"
        stack.setCurrentIndex(2)
    if champEnCours == "prodrome2":
    
        lstMultiple.clear()
        reader = codecs.open(os.path.dirname(__file__) + "/tables/Prodrome.csv", 'r', encoding='utf-8')               
        for line in reader:
            
            if line[:1] != u";":
                data, libelle = line.split(';')
                if data[:len(tFiltreMultiple.text())]==tFiltreMultiple.text() or libelle[len(data)+1:len(data)+1+len(tFiltreMultiple.text())].lower()==tFiltreMultiple.text().lower():
                    item = QListWidgetItem(libelle)
                    item.setData(3,data)
                    if not  ';' + data + ';' in  ';' + str(prodrome2.text()) + ';':
                        lstMultiple.addItem(item)
        champEnCours = "prodrome2"
        stack.setCurrentIndex(2)
        
    if champEnCours == "espVegetal":
        global listePlante 

        lstMultiple_2.clear()
        reader = codecs.open(os.path.dirname(__file__) + u"/tables/Especes_Vegetales.csv", 'r', encoding='utf-8')               
        for line in reader:
            data, libelle, Arr, AESN = line.replace('\r\n', '').replace('\r', '').replace('\n', '').split(';')
            if data[:len(tFiltreMultipleEV.text())]==tFiltreMultipleEV.text() or libelle[:len(tFiltreMultipleEV.text())].lower()==tFiltreMultipleEV.text().lower():
                item = QListWidgetItem(libelle)
                item.setData(3,data)
                if not ';' + data + ';' in  ';' + str(espVegetalPlain.toPlainText()) + ';':
                    if ("Arr" in listePlante and Arr == "1") or ("AESN" in listePlante and AESN == "1"):
                        lstMultiple_2.addItem(item)
        champEnCours = "espVegetal"
        stack.setCurrentIndex(3)
def tFiltreUniqueTextChanged():
    global champEnCours

    if champEnCours == "corBio1":
        item2 = None
        lstUnique.clear()
        reader = codecs.open(os.path.dirname(__file__) + "/tables/Corine_Biotope.csv", 'r', encoding='utf-8')
        for line in reader:
            #if line.find(tFiltreUnique.text())!=-1:
            data, libelle = line.split(';')
            if data[:len(tFiltreUnique.text())]==tFiltreUnique.text() or libelle[len(data)+1:len(data)+1+len(tFiltreUnique.text())].lower()==tFiltreUnique.text().lower():
                item = QListWidgetItem(libelle)
                item.setData(3,data)
                lstUnique.addItem(item)
                if data.rstrip() == corBio1.text():
                    item2 = lstUnique.count()

        if item2 != None:  
            lstUnique.setCurrentRow(item2-1)
        stack.setCurrentIndex(1)
        champEnCours = "corBio1"
        
    if champEnCours == "prodrome1":
        item2 = None
        lstUnique.clear()
        reader = codecs.open(os.path.dirname(__file__) + "/tables/Prodrome.csv", 'r', encoding='utf-8')
        for line in reader:
            #if line.find(tFiltreUnique.text())!=-1:
            data, libelle = line.split(';')
            
            if data[:len(tFiltreUnique.text())]==tFiltreUnique.text() or libelle[len(data)+1:len(data)+1+len(tFiltreUnique.text())].lower()==tFiltreUnique.text().lower():
                item = QListWidgetItem(libelle)
                item.setData(3,data)
                lstUnique.addItem(item)
                if data.rstrip() == prodrome1.text():
                    item2 = lstUnique.count()

        if item2 != None:  
            lstUnique.setCurrentRow(item2-1)
        stack.setCurrentIndex(1)
        champEnCours = "prodrome1"

def selLstUniqueChange():
    global champEnCours
    item = lstUnique.currentItem() 
    if champEnCours == "corBio1":

        if u'oui' in pourc:
            (value, ok) = QInputDialog.getInt (myDialog, "Pourcentage de recouvrement", str(item.data(3)) + ' :') 
            if ok and value <101 and value>0:
                corBio1.setText(item.data(3).rstrip() + '[' + str(value) + '%]')
            else:
                corBio1.setText(item.data(3).rstrip())
        else:    
            corBio1.setText(item.data(3).rstrip())
    elif champEnCours == "prodrome1":

        if u'oui' in pourc:
            (value, ok) = QInputDialog.getInt (myDialog, "% recouvrement", str(item.text()) + ' :') 
            if ok and value <101 and value>0:
                prodrome1.setText(item.data(3).rstrip() + '[' + str(value) + '%]')
            else:
                prodrome1.setText(item.data(3).rstrip())
        else:    
            prodrome1.setText(item.data(3).rstrip())    

    elif champEnCours == "hydromSol":
        hydromSol.setText(item.text().rstrip())
    elif champEnCours == "hydromApp":
        hydromApp.setText(item.text()[:len(item.text())-2])
    elif champEnCours == "hydromDisp":
        hydromDisp.setText(item.text()[:len(item.text())-2])
    elif champEnCours == "freqSubm":
        freqSubm.setText(item.text().rstrip())
        if freqSubm.text()[:6] == u"Jamais":
            etendSubm.setText(u"Sans Objet")
    elif champEnCours == "etendSubm":
        etendSubm.setText(item.text().rstrip())
        if freqSubm.text()[:6] == u"Jamais" and etendSubm.text()[:10] != "Sans objet":
            freqSubm.setText(u"")
    elif champEnCours == "diagHydro":
        diagHydro.setText(item.text().rstrip())
    elif champEnCours == "etatCons":
        etatCons.setText(item.text().rstrip())
    elif champEnCours == "faisabInt":
        faisabInt.setText(item.text().rstrip())
    elif champEnCours == "nivMenace":
        nivMenace.setText(item.text().rstrip())
    elif champEnCours == "nivPrior":
        nivPrior.setText(item.text().rstrip())
    
    tabGw.setFocus()
    champEnCours =""
    stack.setCurrentIndex(0) 

def espAnimalTextChanged():
    if len(espAnimalPlain.toPlainText())>254:
        curseur = espAnimalPlain.textCursor() 
        pos=curseur.position()      
        espAnimalPlain.setPlainText(espAnimalPlain.toPlainText()[:254])
        curseur.setPosition(pos) 
        espAnimalPlain.setTextCursor(curseur)
def rqTypoTextChanged():
    if len(rqTypoPlain.toPlainText())>254:
        curseur = rqTypoPlain.textCursor() 
        pos=curseur.position()      
        rqTypoPlain.setPlainText(rqTypoPlain.toPlainText()[:254])
        curseur.setPosition(pos) 
        rqTypoPlain.setTextCursor(curseur) 
def rqGeneTextChanged():
    if len(rqGenePlain.toPlainText())>254:
        curseur = rqGenePlain.textCursor() 
        pos=curseur.position()      
        rqGenePlain.setPlainText(rqGenePlain.toPlainText()[:254])
        
        curseur.setPosition(pos) 
        rqGenePlain.setTextCursor(curseur) 
def rqContexteTextChanged():
    if len(rqContextePlain.toPlainText())>254:
        curseur = rqContextePlain.textCursor() 
        pos=curseur.position()      
        rqContextePlain.setPlainText(rqContextePlain.toPlainText()[:254])
        curseur.setPosition(pos) 
        rqContextePlain.setTextCursor(curseur) 
def rqHydroTextChanged():
    if len(rqHydroPlain.toPlainText())>254:
        curseur = rqHydroPlain.textCursor() 
        pos=curseur.position()      
        rqHydroPlain.setPlainText(rqHydroPlain.toPlainText()[:254])
        curseur.setPosition(pos) 
        rqHydroPlain.setTextCursor(curseur)     
def rqBioTextChanged():
    if len(rqBioPlain.toPlainText())>254:
        curseur = rqBioPlain.textCursor() 
        pos=curseur.position()      
        rqBioPlain.setPlainText(rqBioPlain.toPlainText()[:254])
        curseur.setPosition(pos) 
        rqBioPlain.setTextCursor(curseur) 
def rqBilanTextChanged():
    if len(rqBilanPlain.toPlainText())>254:
        curseur = rqBilanPlain.textCursor() 
        pos=curseur.position()      
        rqBilanPlain.setPlainText(rqBilanPlain.toPlainText()[:254])
        curseur.setPosition(pos) 
        rqBilanPlain.setTextCursor(curseur)
def recomTechTextChanged():
    if len(recomTechPlain.toPlainText())>254:
        curseur = recomTechPlain.textCursor() 
        pos=curseur.position()      
        recomTechPlain.setPlainText(recomTechPlain.toPlainText()[:254])
        curseur.setPosition(pos) 
        recomTechPlain.setTextCursor(curseur)
def toponymeTextChanged():
    if len(toponyme.text())>254:
        curseur = toponyme.textCursor() 
        pos=curseur.position()      
        toponyme.setText(toponyme.text()[:254])
        curseur.setPosition(pos) 
        toponyme.setTextCursor(curseur)  

def dateChange():
    datCreatio.setText(calendarWidget.selectedDate().toString("dd/MM/yyyy"))
    stack.setCurrentIndex(0)
    
def annulerSaisieDate():
    stack.setCurrentIndex(0)
        
def effacerSaisieDate():
    datCreatio.setText("")
    stack.setCurrentIndex(0)
    
def validate():
    
    #valide = True
    if len(hydromApp.text()) != 0 and len(hydromDisp.text()) != 0:
        if int(hydromDisp.text()) < int(hydromApp.text()):
            #valide = False
            msgBox = QMessageBox()
            msgBox.setText(u"la profondeur d'apparition des traces d'hydromorphie est supérieure à celle de disparition! Le champ concernant la profondeur de disparition a été effacé.")
            msgBox.exec_()
            hydromDisp.setText("")
    #myFeature['rqBio'] = rqBio.toPlainText()
    
    #if valide == True:
    
        # Return the form as accpeted to QGIS.
        #myDialog.accept()
        #myDialog.save()
    rqTypo.setText(rqTypoPlain.toPlainText())        
    rqGene.setText(rqGenePlain.toPlainText()) 
    rqHydro.setText(rqHydroPlain.toPlainText()) 
    rqBio.setText(rqBioPlain.toPlainText()) 
    rqContexte.setText(rqContextePlain.toPlainText()) 
    rqBilan.setText(rqBilanPlain.toPlainText()) 
    recomTech.setText(recomTechPlain.toPlainText()) 
    espVegetal.setText(espVegetalPlain.toPlainText())

        
    espAnimal.setText(espAnimalPlain.toPlainText())   
    
        
        
        
        
        
        
