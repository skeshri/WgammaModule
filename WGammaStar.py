#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor


from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class ExampleAnalysis(Module):
    def __init__(self,jetid=2):
        self.jetid=jetid
    def beginJob(self,histFile=None,histDirName=None):
	pass
    def Daughters(self,genParticles,pdgid):
        daught_par = [];
        daught_ref = [];
        index = 0
        for particle in genParticles:
            if(particle.status==1 and particle.genPartIdxMother == pdgid):
                daught_par.append(particle)
                daught_ref.append(index)
            index += 1
        return daught_par,daught_ref

    def LeptFromW(self,daughters,isMuon):
        nLeptFromW=0
        daughterLeptonsFromW=[]
        for daughter in daughters:
            if(isMuon and (abs(daughter.pdgId)==13)):
                daughterLeptonsFromW.append(daughter)
                nLeptFromW+=1
            if((not isMuon) and (abs(daughter.pdgId)==11)):
                daughterLeptonsFromW.append(daughter)
                nLeptFromW+=1
        return nLeptFromW,daughterLeptonsFromW

    def analyze(self, event):
        genParticles = Collection(event, "GenPart")
        pLeptMom = -1
        isMuon = False
 
	for particle  in genParticles :
	  pdg_Id = abs(particle.pdgId)
         # print("particle Status=%d ; pdgId : %d" % (particle.status, particle.pdgId))
          if ( pdg_Id == 11 and particle.status == 1)  : 
	    if (particle.genPartIdxMother < 0) :
               continue
            else :
                pLeptMom = particle.genPartIdxMother  #index to mother
                while (abs(genParticles[pLeptMom].pdgId) == 11) : 
	           if (genParticles[pLeptMom].genPartIdxMother < 0) :
                      break
                   else :
                      pLeptMom = genParticles[pLeptMom].genPartIdxMother
                      #print("!!!! After pLeptMom = %d" %genParticles[pLeptMom].pdgId)
            isMuon = False
          elif(pdg_Id == 13 and particle.status == 1)  : 
	    if (particle.genPartIdxMother < 0) :
               continue
            else :
                pLeptMom = particle.genPartIdxMother  #index to mother
                #print("particle Status=%d ; pdgId : %d" % (particle.status, particle.pdgId))
                while (abs(genParticles[pLeptMom].pdgId) == 13) : 
	           if (genParticles[pLeptMom].genPartIdxMother < 0) :
                      break
                   else :
                      pLeptMom = genParticles[pLeptMom].genPartIdxMother
                      #print("!!!! After pLeptMom = %d" %genParticles[pLeptMom].pdgId)
            isMuon = True
          else :
              continue
          if(genParticles[pLeptMom].pdgId==25):  # fixit 25->24
              daughters,daughters_ref = self.Daughters(genParticles,25) # fixit 25->24
              if(not (len(daughters)==2)) : # fixit 2 -> 4
                  continue
              nLeptFromW,daughterLeptonsFromW = self.LeptFromW(daughters,isMuon)
              if(not (len(daughterLeptonsFromW)==2)) : # fixit 2 -> 4
                  continue
#              print ("nLeptonFromW : %d , "%nLeptFromW)
#              print ("daughterLeptonsFromW 1  : %d , "%daughterLeptonsFromW[0].pdgId)
#              print ("daughterLeptonsFromW 2  : %d , "%daughterLeptonsFromW[1].pdgId)
              
#              if(isMuon):




#              for daughterIdx in daughterLeptonsFromW :
#                  print("daughter pdgid  from reference: %d"%daughterIdx.pdgId)

#              for daughterIdx in daughters_ref1 :
#                  print("daughter pdgid  from reference: %d"%genParticles[daughterIdx].pdgId)
              #print ("W mila , numberof Daughters = %d" %nDaughters)

          #    if(genParticles)

#      else :
#          continue
        return True


#files=["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/WGstarToLNuEE_012Jets_13TeV-madgraph/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/E4C53384-D213-E811-AA04-801844E560A4.root"]
files=["root://cms-xrd-global.cern.ch//store/mc/RunIIFall17NanoAOD/VBFToHiggs0PMToZZTo2e2nutJJ_M125_GaSM_13TeV_phantom_pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/00000/F8DD3F9A-D6CA-E811-8E6F-FA163EB8F024.root"]
p=PostProcessor(".",files,cut=None,branchsel=None,modules=[ExampleAnalysis()],noOut=True,provenance=True)
p.run()
