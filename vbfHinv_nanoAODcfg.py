#!/usr/bin/env python

import os,sys
import optparse
import commands
import math
import random

usage = 'usage: %prog [options]'
parser = optparse.OptionParser(usage)

parser.add_option('-o', '--out'         ,    dest='out'                , help='output directory for logs'             , default=os.getcwd() )
parser.add_option('-e', '--eos'         ,    dest='eos'                , help='eos path to save output file to EOS',         default='')
parser.add_option('-i', '--inputfile'    ,    dest='inputfile'           , help='full path to nanoAOD input file', default='/eos/user/a/amagnan/EWKZ2Jets_ZToLL_12Apr2018_94X_nanoAOD_test.root')
parser.add_option('-p', '--prod'    ,    dest='prod'           , help='prod date', default='181018')
parser.add_option('-S', '--no-submit'   ,    action="store_true",  dest='nosubmit'           , help='Do not submit batch job.')
(opt, args) = parser.parse_args()


logDir='%s/%s'%(opt.out,opt.prod)
os.system('mkdir -p %s'%logDir)
if len(opt.eos)>0:
    outDir='%s/%s'%(opt.eos,opt.prod)
else:
    outDir='%s'%logDir


nanoScript='../../PhysicsTools/NanoAODTools/scripts/nano_postproc.py'

lepSFtight = lambda : lepSFProducer( "LooseWP_2016", "GPMVA90_2016")
lepSFveto = lambda : lepSFProducer( "LooseWP_2016", "GPMVA90_2016")


dataModules='JetMetMinDPhiConstructor'
mcModules='JetMetMinDPhiConstructor,puAutoWeight,btagSF2017,lepSFtight,lepSFveto,jetmetUncertainties2017'

#cutString=''
#event.nJet>=2 && event.MET_pt>100'
#Flag_goodVertices>0 && Flag_globalSuperTightHalo2016Filter>0 && Flag_HBHENoiseFilter>0 && Flag_HBHENoiseIsoFilter>0 && Flag_EcalDeadCellTriggerPrimitiveFilter>0 && Flag_BadPFMuonFilter>0 && Flag_BadChargedCandidateFilter>0 && Flag_ecalBadCalibFilter>0


os.system('python %s %s %s -I VBFHToInv.NanoAODTools.postprocessing.VBFHToInvModules %s'%(nanoScript,outDir,opt.inputfile,mcModules))

