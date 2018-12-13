import ROOT
import math
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *

class SelectionCreator(Module):
    def __init__(self, VariableNames = ["MetNoMuon"], VariableSelections = ["obj>200"]):
        self.VariableNames = []
        self.VariableSelections = []
        if not (len(VariableNames)==len(VariableSelections)):
            print "Error: Different list sizes between objects definition and selections (one of them is missing)!"
        else:
            for name, sel in zip(VariableNames, VariableSelections) :
                self.VariableNames.append(name)
                self.VariableSelections.append(sel)
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
    
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        
        if not (len(self.VariableNames)==len(self.VariableSelections)):
            print "Error: Different list sizes between objects definition and selections (one of them is missing)!"
        else:
            for name, sel in zip(self.VariableNames, self.VariableSelections) :
                obj = getattr(event, name)
                if not(eval(sel)):
                    return False
            
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed
SelectionCreatorConstructorTest = lambda : SelectionCreator( VariableNames = ["MetNoLooseMuon_pt","MetNoLooseMuon_CleanJet_mindPhi"],
                                                        VariableSelections = ["obj>250", "obj>0.5"])
SelectionCreatorConstructor = lambda : SelectionCreator( VariableNames = ["nCleanJet", "MetNoLooseMuon_pt", "MetNoLooseMuon_CleanJet_mindPhi", "diCleanJet_M", "diCleanJet_dEta"],
                                                            VariableSelections = ["obj>=2", "obj>150", "obj>0.5" , "obj>500", "obj>2" ])


