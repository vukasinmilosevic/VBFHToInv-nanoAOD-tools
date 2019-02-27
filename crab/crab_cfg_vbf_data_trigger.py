from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()

myDate = '260219'
version = 'v3'
config.section_("General")
config.General.requestName = 'Full_MET2017_dataset_'+myDate+'_filebased'
config.General.transferLogs=True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_vbf_data_trigger.sh'
config.JobType.inputFiles = ['crab_script_vbf_data_trigger.py','../../../PhysicsTools/NanoAODTools/scripts/haddnano.py','../data/pileup/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder	 = True
config.section_("Data")
#config.Data.inputDataset = '/DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17NanoAOD-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1 
#config.Data.unitsPerJob = 2
#config.Data.totalUnits = 1

config.Data.outLFNDirBase = '/store/user/vmilosev/Trigger_skim_'+myDate
config.Data.publication = False
#config.Data.outputDatasetTag = 'NanoTestPost'
config.section_("Site")
config.Site.storageSite = "T2_UK_London_IC"

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
    #Runs
    
    tasks.append(('SingleMuon-2017B-trigger','/SingleMuon/Run2017B-31Mar2018-v1/NANOAOD'))
    tasks.append(('SingleMuon-2017C-trigger','/SingleMuon/Run2017C-31Mar2018-v1/NANOAOD'))
    tasks.append(('SingleMuon-2017D-trigger','/SingleMuon/Run2017D-31Mar2018-v1/NANOAOD'))
    tasks.append(('SingleMuon-2017E-trigger','/SingleMuon/Run2017E-31Mar2018-v1/NANOAOD'))
    tasks.append(('SingleMuon-2017F-trigger','/SingleMuon/Run2017F-31Mar2018-v1/NANOAOD'))
   
    tasks.append(('SingleElectron-2017B-trigger','/SingleElectron/Run2017B-31Mar2018-v1/NANOAOD'))
    tasks.append(('SingleElectron-2017C-trigger','/SingleElectron/Run2017C-31Mar2018-v1/NANOAOD'))
    tasks.append(('SingleElectron-2017D-trigger','/SingleElectron/Run2017D-31Mar2018-v1/NANOAOD'))
    tasks.append(('SingleElectron-2017E-trigger','/SingleElectron/Run2017E-31Mar2018-v1/NANOAOD'))
    tasks.append(('SingleElectron-2017F-trigger','/SingleElectron/Run2017F-31Mar2018-v1/NANOAOD')) 
 
    for task in tasks:
        print task[0]
        config.General.requestName = task[0]+version
        config.Data.inputDataset = task[1]
        config.Data.outputDatasetTag = 'Data'+task[0]+version
        submit(config)
