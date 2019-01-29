#this fake PSET is needed for local test and for crab to figure the output filename
#you do not need to edit it unless you want to do a local test using a different input file than
#the one marked below
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes
import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
#	lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)

#for Data

#process.source.lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
#JSONfile = '../data/pileup/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'
#myLumis = LumiList.LumiList(filename = JSONfile).getCMSSWString().split(',')
#process.source.lumisToProcess.extend(myLumis)

process.source.fileNames = [
	#'/eos/user/a/amagnan/datatest.root' ##you can change only this line
       #'/eos/user/a/amagnan/EWKZ2Jets_ZToLL_12Apr2018_94X_nanoAOD_test.root'
    'root://xrootd.grid.hep.ph.ic.ac.uk///store/mc/RunIIFall17NanoAOD/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/NANOAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/310000/68FC1A44-119B-E811-82C3-1866DA890A68.root'
         #'root://cms-xrd-global.cern.ch//store/data/Run2017B/MET/NANOAOD/31Mar2018-v1/710000/D477E3DA-0A47-E811-8621-0CC47A4C8E98.root'
]
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)

