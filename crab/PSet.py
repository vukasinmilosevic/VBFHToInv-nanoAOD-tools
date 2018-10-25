#this fake PSET is needed for local test and for crab to figure the output filename
#you do not need to edit it unless you want to do a local test using a different input file than
#the one marked below
import FWCore.ParameterSet.Config as cms
process = cms.Process('NANO')
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring(),
#	lumisToProcess=cms.untracked.VLuminosityBlockRange("254231:1-254231:24")
)
process.source.fileNames = [
	#'/eos/user/a/amagnan/datatest.root' ##you can change only this line
        '/eos/user/a/amagnan/EWKZ2Jets_ZToLL_12Apr2018_94X_nanoAOD_test.root'
]
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))
process.output = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string('tree.root'))
process.out = cms.EndPath(process.output)

