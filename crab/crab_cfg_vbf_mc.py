from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = 'Full_MC_correction_281118'
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_vbf_mc.sh'
config.JobType.inputFiles = ['crab_script_vbf_mc.py','../../../PhysicsTools/NanoAODTools/scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
#config.Data.inputDataset = '/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1
#config.Data.totalUnits = 1

config.Data.outLFNDirBase = '/store/user/vmilosev/HIG_EXOv2_28112018'
config.Data.publication = False
#config.Data.outputDatasetTag = 'NanoTestPost'
config.section_("Site")
config.Site.storageSite = "T2_UK_London_IC"
config.Site.blacklist = ["T3_IT_Trieste", "T2_US_MIT"]
#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'


if 1 == 1:

    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException

    # We want to put all the CRAB project directories from the tasks we submit here into one common directory.
    # That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).

    def submit(inconfig):
        try:
            crabCommand('submit', config = inconfig)
#            crabCommand('status')
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)

    #############################################################################################
    ## From now on that's what users should modify: this is the a-la-CRAB2 configuration part. ##
    #############################################################################################

    tasks=list()
      
    #Diboson

    tasks.append(('WW_TuneCP5','/WW_TuneCP5_13TeV-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('WW_TuneCUETP8M1v2','/WW_TuneCUETP8M1_13TeV-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM'))
    tasks.append(('WZ_TuneCP5','/WZ_TuneCP5_13TeV-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('WZ_TuneCUETP8M1v2','/WZ_TuneCUETP8M1_13TeV-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM'))
    tasks.append(('ZZ_TuneCP5','/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('ZZ_TuneCUETP8M1v2','/ZZ_TuneCUETP8M1_13TeV-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM'))
    
    
    #DY
    
    tasks.append(('DYJetsToLL_M-50_HT-100to200-ext','/DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/NANOAODSIM'))
    tasks.append(('DYJetsToLL_M-50_HT-100to200','/DYJetsToLL_M-50_HT-100to200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/NANOAODSIM'))
    tasks.append(('DYJetsToLL_M-50_HT-1200to2500','/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('DYJetsToLL_M-50_HT-200to400-ext','/DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/NANOAODSIM'))
    tasks.append(('DYJetsToLL_M-50_HT-200to400','/DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/NANOAODSIM'))
    tasks.append(('DYJetsToLL_M-50_HT-2500toInf','/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/NANOAODSIM'))
    tasks.append(('DYJetsToLL_M-50_HT-400to600-ext','/DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/NANOAODSIM'))
    tasks.append(('DYJetsToLL_M-50_HT-400to600','/DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/NANOAODSIM'))
    tasks.append(('DYJetsToLL_M-50_HT-600to800','/DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/NANOAODSIM'))
    tasks.append(('DYJetsToLL_M-50_HT-70to100','/DYJetsToLL_M-50_HT-70to100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('DYJetsToLL_M-50_HT-800to1200','/DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/NANOAODSIM'))
    tasks.append(('DYJetsToLL_M-50-amcatnloFXFX-ext','/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/NANOAODSIM'))
    tasks.append(('DYJetsToLL_M-50-amcatnloFXFX','/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('DYJetsToLL_M-50-amcatnloFXFX-RECOPF','/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAOD-PU2017RECOPF_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('DYJetsToLL_M-50-amcatnloFXFX-RECOSIMstep-ext','/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/NANOAODSIM'))
    tasks.append(('DYJetsToLL_M-50-amcatnloFXFX-RECOSIMstep','/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('DYJetsToLL_M-50_Zpt-150toInf','/DYJetsToLL_M-50_Zpt-150toInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))

    #EWK 2j

    tasks.append(('WKWMinus2Jets_WToLNu_M-50','/EWKWMinus2Jets_WToLNu_M-50_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('EWKWPlus2Jets_WToLNu_M-50','/EWKWPlus2Jets_WToLNu_M-50_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('EWKZ2Jets_ZToLL_M-50','/EWKZ2Jets_ZToLL_M-50_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('EWKZ2Jets_ZToNuNu','/EWKZ2Jets_ZToNuNu_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))


	
	#QCD

	#tasks.append(('QCD_HT1000to1500','/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('QCD_HT1000to1500-new-pmx','/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('QCD_HT100to200','/QCD_HT100to200_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/NANOAODSIM'))
    tasks.append(('QCD_HT100to200-ext','/QCD_HT100to200_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/NANOAODSIM'))
    tasks.append(('QCD_HT1500to2000','/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/NANOAODSIM'))
    #tasks.append(('QCD_HT1500to2000v1','/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_old_pmx_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    #tasks.append(('QCD_HT2000toInf-BGenFilter','/QCD_HT2000toInf_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/NANOAODSIM'))
    tasks.append(('QCD_HT2000toInf','/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/NANOAODSIM'))
    #tasks.append(('QCD_HT2000toInf-old-pmx','/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_old_pmx_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('QCD_HT2000toInf-ext','/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2_ext1-v1/NANOAODSIM'))
    #tasks.append(('QCD_HT200to300v1','/QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('QCD_HT200to300','/QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/NANOAODSIM'))
    #tasks.append(('QCD_HT300to500_BGenFilter','/QCD_HT300to500_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('QCD_HT300to500','/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    #tasks.append(('QCD_HT500to700_BGenFilter','/QCD_HT500to700_BGenFilter_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('QCD_HT500to700','/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/NANOAODSIM'))
    #tasks.append(('QCD_HT500to700-old-pmx','/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_old_pmx_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('QCD_HT700to1000','/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))	
	

	#Single Top

    #tasks.append(('ST_t-channel_antitop_4f_inclusiveDecaysv1','/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('ST_t-channel_antitop_4f_inclusiveDecays','/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/NANOAODSIM'))
    #tasks.append(('ST_t-channel_top_4f_inclusiveDecaysv1','/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('ST_t-channel_top_4f_inclusiveDecays','/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/NANOAODSIM'))

    #tasks.append(('ST_tW_antitop_5f_inclusiveDecaysv1','/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('ST_tW_antitop_5f_inclusiveDecays','/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/NANOAODSIM'))
    #tasks.append(('ST_tW_top_5f_inclusiveDecaysv1','/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('ST_tW_top_5f_inclusiveDecays','/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/NANOAODSIM'))

	#TTJets

    tasks.append(('TTJets_TuneCP5-new-pmx','/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('TTJets_TuneCP5v1','/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))


	
	

	#WJetsToLnNu
			
    tasks.append(('WJetsToLNu_HT-100To200_TuneCP5','/WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-100To200_TuneCUETP8M1','/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-100To200_TuneCUETP8M1-ext','/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2_ext1-v1/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-100To200_TuneCUETP8M1-ext2','/WJetsToLNu_HT-100To200_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2_ext2-v1/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-1200To2500_TuneCP5','/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-200To400_TuneCP5','/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-200To400_TuneCUETP8M1-ext','/WJetsToLNu_HT-200To400_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2_ext1-v1/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-2500ToInf_TuneCP5','/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-400To600_TuneCP5','/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-400To600_TuneCUETP8M1','/WJetsToLNu_HT-400To600_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-600To800_TuneCP5','/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-70To100_TuneCUETP8M1','/WJetsToLNu_HT-70To100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PUMoriond17_94X_mcRun2_asymptotic_v2-v1/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-800To1200_TuneCP5','/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    
    #ZJetsToNuNu
	
    tasks.append(('ZJetsToNuNu_HT-100To200','/ZJetsToNuNu_HT-100To200_13TeV-madgraph/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('ZJetsToNuNu_HT-1200To2500','/ZJetsToNuNu_HT-1200To2500_13TeV-madgraph/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('ZJetsToNuNu_HT-200To400','/ZJetsToNuNu_HT-200To400_13TeV-madgraph/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('ZJetsToNuNu_HT-2500ToInf','/ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    #tasks.append(('ZJetsToNuNu_HT-400To600v1','/ZJetsToNuNu_HT-400To600_13TeV-madgraph/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('ZJetsToNuNu_HT-400To600-new-pmx','/ZJetsToNuNu_HT-400To600_13TeV-madgraph/RunIIFall17NanoAOD-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    #tasks.append(('ZJetsToNuNu_HT-600To800v1','/ZJetsToNuNu_HT-600To800_13TeV-madgraph/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('ZJetsToNuNu_HT-600To800-new-pmx','/ZJetsToNuNu_HT-600To800_13TeV-madgraph/RunIIFall17NanoAOD-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('ZJetsToNuNu_HT-800To1200','/ZJetsToNuNu_HT-800To1200_13TeV-madgraph/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
	
	
    for task in tasks:
        print task[0]
        config.General.requestName = task[0]+'_281118'
        config.Data.inputDataset = task[1]
        config.Data.outputDatasetTag = 'Nano_281118_'+task[0]
        submit(config)
