import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import math
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

def CrossCleaning(obj_eta, obj_phi, cleanerObject_eta, cleanerObject_phi, label = "muon"):
    dphi = deltaPhi(obj_phi, cleanerObject_phi)
    deta = obj_eta-cleanerObject_eta
    dR = math.sqrt(dphi**2+deta**2)
    if dR<0.4:
      # print "PROBLEMATIC object "+label+":"
      # print "Jet eta = ", obj_eta, " phi = ", obj_phi
      # print "Jet eta = ", cleanerObject_eta, " phi = ", cleanerObject_phi
      # print "dR = ", dR
       return False
   # print "GOOD OBJECT, dR = ", dR
    return True




class ObjectCleaning(Module):
    def __init__(self, collectionName, outCollectionName, selection, SFnamePrefix, SFname, SFval, SFerr=[], xcleaningCollectionNames = []):
        self.collectionName = collectionName
        self.outCollectionName = outCollectionName
        self.selection = selection
        self.xcleaningCollectionNames = xcleaningCollectionNames
        self.SFnamePrefix = SFnamePrefix
        self.SFname = SFname
        self.doW = ( (SFnamePrefix is not None) or (SFname is not None) or (SFval is not None) )
        self.SFval = SFval
        self.SFerr = []

        print ' -- INFO -- ObjectCleaning for %s: selection applied is: %s'%(outCollectionName,selection)
        if len(xcleaningCollectionNames)>0:
            print ' -- INFO -- CrossCleaning is done against following collections:'
            for name in xcleaningCollectionNames:
                print name
        if (SFerr is not None): 
            print 'SF %s: considering %d systematics: %s'%(SFname,len(SFerr),SFerr)
            for i in range(len(SFerr)):
                self.SFerr.append(SFerr[i])

        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch(self.outCollectionName+"_idx", "F", lenVar ="n"+self.outCollectionName);
        self.out.branch(self.outCollectionName+"_pt", "F", lenVar ="n"+self.outCollectionName);
        self.out.branch(self.outCollectionName+"_eta", "F", lenVar ="n"+self.outCollectionName);
        self.out.branch(self.outCollectionName+"_phi", "F", lenVar ="n"+self.outCollectionName);
        self.out.branch(self.outCollectionName+"_mass", "F", lenVar ="n"+self.outCollectionName);
        if (self.doW):
            self.out.branch(self.outCollectionName+"_eventSelW", "F");
            self.out.branch(self.outCollectionName+"_eventVetoW", "F");
            for i in range(len(self.SFerr)):
                self.out.branch(self.outCollectionName+"_eventSelW"+self.SFerr[i]+"_up", "F");
                self.out.branch(self.outCollectionName+"_eventSelW"+self.SFerr[i]+"_down", "F");
                self.out.branch(self.outCollectionName+"_eventVetoW"+self.SFerr[i]+"_up", "F");
                self.out.branch(self.outCollectionName+"_eventVetoW"+self.SFerr[i]+"_down", "F");

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        objs = Collection(event, self.collectionName)

        #print 'Length of objs %s: %s'%(self.collectionName,len(objs))

        eventSelW = 1.0
        eventVetoW = 1.0
        eventSelW_err = [1.0]*2*len(self.SFerr)
        eventVetoW_err = [1.0]*2*len(self.SFerr)

        cleanObjs_idx = []
        cleanObjs_pt = []
        cleanObjs_eta = []
        cleanObjs_phi = []
        cleanObjs_mass = []

        objIdx = 0
        #brojac = -1
        for obj in objs:
           # brojac=brojac+1
            if not ( eval(self.selection) ):
                #print ' ---- Loop: obj idx %d failed'%objIdx
                objIdx += 1
                #print " Jet ", str(brojac)," fails the Obj selection -- no crossCleaning"
                continue
            #print ' ---- Loop: obj idx %d passed'%objIdx

           #crossCleaning
            xCleaned = True 
	    if len(self.xcleaningCollectionNames)>0:
                #print "Cleaning of Jet ", str(brojac)
	        for xCleaningName in self.xcleaningCollectionNames:
		    if not xCleaned:
                        break
                    xCleaningCollection = Collection(event, xCleaningName)
                    #print "Cleaning of "+self.collectionName+" against "+xCleaningName, "size = ", len(xCleaningCollection)
                    for xCleaningObj in xCleaningCollection:   
            	    	 xCleaned =CrossCleaning(obj.eta, obj.phi, xCleaningObj.eta, xCleaningObj.phi, xCleaningName)
                         if not xCleaned:
                             #print "Object should fail"
                             break
            if not xCleaned:
                continue
                
	    #print "Object is clean" 
            cleanObjs_idx.append(objIdx)
            cleanObjs_pt.append(obj.pt)
            cleanObjs_eta.append(obj.eta)
            cleanObjs_phi.append(obj.phi)
            cleanObjs_mass.append(obj.mass) 
            
#get scale factors
            if (self.doW):
                #for w in SFweights:
                    #print ' ------ loop weight value: %3.3f'%w.effSF_Loose
                werr = [1.0]*2*len(self.SFerr)
                if (self.SFnamePrefix is not None):
                    ret = Object(event,self.collectionName,index=objIdx)
                    #wobj = obj[objIdx].effSF_Loose
                    wobj = ret.__getattr__(self.SFname)
                    for i in range(len(self.SFerr)):
                        if ("syst" not in self.SFerr[i]):
                            werr[2*i] = ret.__getattr__(self.SFname+"_up")-wobj
                            werr[2*i+1] = ret.__getattr__(self.SFname+"_down")-wobj
                        else : 
                            werr[2*i] = ret.__getattr__(self.SFname+self.SFerr[i])
                            werr[2*i+1] = -1.*ret.__getattr__(self.SFname+self.SFerr[i])
                else:
                    #werr = [1.0]*2
                    wobj = self.SFval[0]
                    if (len(self.SFerr)>0):
                        werr[0] = self.SFval[1]
                        werr[1] = -1.*self.SFval[1]

                #print ' ------ loop weight value: %3.3f'%wobj
                eventSelW *= wobj
                eventVetoW *= (1-wobj)

                for i in range(len(eventSelW_err)):
                    eventSelW_err[i] *= (wobj+werr[i])
                    eventVetoW_err[i] *= (1-(wobj+werr[i]))



            objIdx += 1


        self.out.fillBranch(self.outCollectionName+"_idx", cleanObjs_idx)
        self.out.fillBranch(self.outCollectionName+"_pt", cleanObjs_pt)
        self.out.fillBranch(self.outCollectionName+"_eta", cleanObjs_eta)
        self.out.fillBranch(self.outCollectionName+"_phi", cleanObjs_phi)
        self.out.fillBranch(self.outCollectionName+"_mass", cleanObjs_mass)
        if (self.doW):
            self.out.fillBranch(self.outCollectionName+"_eventSelW",eventSelW)
            self.out.fillBranch(self.outCollectionName+"_eventVetoW",eventVetoW)
            for i in range(len(self.SFerr)):
                self.out.fillBranch(self.outCollectionName+"_eventSelW"+self.SFerr[i]+"_up",eventSelW_err[2*i]);
                self.out.fillBranch(self.outCollectionName+"_eventVetoW"+self.SFerr[i]+"_up",eventVetoW_err[2*i]);
                self.out.fillBranch(self.outCollectionName+"_eventSelW"+self.SFerr[i]+"_down",eventSelW_err[2*i+1]);
                self.out.fillBranch(self.outCollectionName+"_eventVetoW"+self.SFerr[i]+"_down",eventVetoW_err[2*i+1]);

        return True

# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

#####################
##### Jets
#####################

jetSelection = 'abs(obj.eta) < 5.0 and ((obj.puId & 0x4) > 0) and ((abs(obj.eta)<=2.7 and ((obj.jetId & 0x4) > 0 )) or (abs(obj.eta) > 2.7 and ((obj.jetId & 0x2) > 0 )))'
JetCleaningConstructor = lambda : ObjectCleaning(collectionName= "Jet", outCollectionName = "CleanJet", selection = jetSelection, SFnamePrefix = None, SFname = None, SFval = None, SFerr = None)

JetCleaningConstructorXCl = lambda : ObjectCleaning(collectionName= "Jet", outCollectionName = "CleanJet", selection = jetSelection, SFnamePrefix = None, SFname = None, SFval = None, SFerr = None, xcleaningCollectionNames = ["LooseMuon", "VetoElectron"])

bjetSel = 'obj.pt > 20 and abs(obj.eta) < 2.5 and obj.btagDeepB > 0.4941'

MediumBJetConstructor = lambda : ObjectCleaning(collectionName= "Jet", outCollectionName = "MediumBJet", selection = bjetSel,SFnamePrefix = 'Jet', SFname = 'btagSF',SFval = None, SFerr = [''])
MediumBJetConstructorData = lambda : ObjectCleaning(collectionName= "Jet", outCollectionName = "MediumBJet", selection = bjetSel,SFnamePrefix = None, SFname = None,SFval = None, SFerr = None)

#####################
##### Muons
#####################

looseMuSel = 'abs(obj.eta) < 2.4 and obj.pt > 10 and obj.pfRelIso04_all < 0.25'
tightMuSel = 'obj.tightId == 1 and obj.pfRelIso04_all < 0.15'
LooseMuonConstructor = lambda : ObjectCleaning(collectionName= "Muon", outCollectionName = "LooseMuon", selection = looseMuSel, SFnamePrefix = 'Muon', SFname = 'effSF_Loose',SFval = None, SFerr = ['_systID','_systISO'] )
CRLooseMuonConstructor = lambda : ObjectCleaning(collectionName= "Muon", outCollectionName = "CRLooseMuon", selection = looseMuSel+' and not('+tightMuSel+')',SFnamePrefix = 'Muon', SFname = 'effSF_Loose',SFval = None, SFerr = ['_systID','_systISO'] )
CRTightMuonConstructor = lambda : ObjectCleaning(collectionName= "Muon", outCollectionName = "CRTightMuon", selection = looseMuSel+' and '+tightMuSel, SFnamePrefix = 'Muon', SFname = 'effSF_Tight',SFval = None, SFerr = ['_systID','_systISO'] )

LooseMuonConstructorData = lambda : ObjectCleaning(collectionName= "Muon", outCollectionName = "LooseMuon", selection = looseMuSel, SFnamePrefix = None, SFname = None ,SFval = None, SFerr = None )
CRLooseMuonConstructorData = lambda : ObjectCleaning(collectionName= "Muon", outCollectionName = "CRLooseMuon", selection = looseMuSel+' and not('+tightMuSel+')', SFnamePrefix = None, SFname = None ,SFval = None, SFerr = None )
CRTightMuonConstructorData = lambda : ObjectCleaning(collectionName= "Muon", outCollectionName = "CRTightMuon", selection = looseMuSel+' and '+tightMuSel, SFnamePrefix = None, SFname = None ,SFval = None, SFerr = None )

#####################
##### Electrons
#####################

looseEleSel = 'abs(obj.eta) < 2.5 and obj.pt > 10 and obj.cutBased > 0'
tightEleSel = 'obj.cutBased == 4'

LooseElectronConstructor = lambda : ObjectCleaning(collectionName= "Electron", outCollectionName = "VetoElectron", selection = looseEleSel, SFnamePrefix = 'Electron', SFname = 'effSF_Veto',SFval = None, SFerr = ['_systRECO','_systRECOlowEt','_systIDISO'])
CRLooseElectronConstructor = lambda : ObjectCleaning(collectionName= "Electron", outCollectionName = "CRVetoElectron", selection = looseEleSel+' and not ('+tightEleSel+')',SFnamePrefix = 'Electron', SFname = 'effSF_Veto',SFval = None, SFerr = ['_systRECO','_systRECOlowEt','_systIDISO'])
CRTightElectronConstructor = lambda : ObjectCleaning(collectionName= "Electron", outCollectionName = "CRTightElectron", selection = looseEleSel+' and '+tightEleSel,SFnamePrefix = 'Electron', SFname = 'effSF_Tight',SFval = None, SFerr = ['_systRECO','_systRECOlowEt','_systIDISO'])

LooseElectronConstructorData = lambda : ObjectCleaning(collectionName= "Electron", outCollectionName = "VetoElectron", selection = looseEleSel, SFnamePrefix = None, SFname = None,SFval = None, SFerr = None )
CRLooseElectronConstructorData = lambda : ObjectCleaning(collectionName= "Electron", outCollectionName = "CRVetoElectron", selection = looseEleSel+' and not ('+tightEleSel+')', SFnamePrefix = None, SFname = None,SFval = None, SFerr = None )
CRTightElectronConstructorData = lambda : ObjectCleaning(collectionName= "Electron", outCollectionName = "CRTightElectron", selection = looseEleSel+' and '+tightEleSel, SFnamePrefix = None, SFname = None,SFval = None, SFerr = None )

######################
##### Taus
######################

tauSel = 'obj.pt > 18 and abs(obj.eta) < 2.3 and ((obj.idMVAoldDMdR032017v2 & 0x2) > 0) and (obj.idDecayMode > 0.5) and ((obj.idAntiEle & 0x2) > 0) and ((obj.idAntiMu & 0x1) > 0) and (abs(obj.dz)<0.2)'

VLooseTauConstructor = lambda : ObjectCleaning(collectionName= "Tau", outCollectionName = "VLooseTau", selection = tauSel,SFnamePrefix = None, SFname = None, SFval = [0.88,0.03], SFerr = ['']) 
VLooseTauConstructorData = lambda : ObjectCleaning(collectionName= "Tau", outCollectionName = "VLooseTau", selection = tauSel,SFnamePrefix = None, SFname = None, SFval = None, SFerr = None) 

######################
##### Photons
######################

photonSel = 'obj.pt > 15 and abs(obj.eta) < 2.5 and ((obj.cutBasedBitmap & 0x1)>0) and (obj.electronVeto > 0.5)'
LoosePhotonConstructor = lambda : ObjectCleaning(collectionName= "Photon", outCollectionName = "LoosePhoton", selection = photonSel,SFnamePrefix = None, SFname = None,SFval = None, SFerr = None)
