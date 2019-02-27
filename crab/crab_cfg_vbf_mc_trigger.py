from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()

myDate = '260219'

config.section_("General")
config.General.requestName = 'Full_MC_correction_'+myDate
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_vbf_mc_trigger.sh'
config.JobType.inputFiles = ['crab_script_vbf_mc_trigger.py','../../../PhysicsTools/NanoAODTools/scripts/haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
#config.Data.inputDataset = '/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1
#config.Data.totalUnits = 1

config.Data.outLFNDirBase = '/store/user/vmilosev/Trigger_skim_'+myDate
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
      
    

	#WJetsToLnNu
			
    tasks.append(('WJetsToLNu_HT-100To200_TuneCP5','/WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-1200To2500_TuneCP5','/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-200To400_TuneCP5','/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-2500ToInf_TuneCP5','/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v3/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-400To600_TuneCP5','/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-600To800_TuneCP5','/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('WJetsToLNu_HT-800To1200_TuneCP5','/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))

    tasks.append(('ttH_HToInvisible_M125_13TeV_TuneCP5','/ttH_HToInvisible_M125_13TeV_TuneCP5_powheg_pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))	
    tasks.append(('ggZH_ZToQQ_HToInvisible_M125','/ggZH_ZToQQ_HToInvisible_M125_13TeV_powheg_pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('ggZH_ZToLL_HToInvisible_M125','/ggZH_ZToLL_HToInvisible_M125_13TeV_powheg_pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('ggZH_HToInvisible_M125_TuneCP5','/ggZH_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('ZH_ZToQQ_HToInvisible_M125','/ZH_ZToQQ_HToInvisible_M125_13TeV_powheg_pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('ZH_ZToLL_HToInvisible_M125','/ZH_ZToLL_HToInvisible_M125_13TeV_TuneCP5_powheg_pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('WplusH_WToQQ_HToInvisible_M125','/WplusH_WToQQ_HToInvisible_M125_13TeV_powheg_pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('WminusH_WToQQ_HToInvisible_M125','/WminusH_WToQQ_HToInvisible_M125_13TeV_powheg_pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('VBF_HToInvisible_M125_13TeV_TuneCP5','/VBF_HToInvisible_M125_13TeV_TuneCP5_powheg_pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    tasks.append(('GluGlu_HToInvisible_M125_TuneCP5','/GluGlu_HToInvisible_M125_TuneCP5_13TeV_powheg_pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'))
    
    for task in tasks:
        print task[0]
        config.General.requestName = task[0]+'trigger'
        config.Data.inputDataset = task[1]
        config.Data.outputDatasetTag = 'MC_'+task[0]+'trigger'
        submit(config)
