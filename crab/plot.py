import ROOT
import sys

def drawProgressBar(percent, barLen = 20):
    sys.stdout.write("\r")
    progress = ""
    for i in range(barLen):
        if i < int(barLen * percent):
            progress += "="
        else:
            progress += " "
    sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
    sys.stdout.flush()


def calcInvMass(file_location, prefix, hist_name):
    myHistogram = ROOT.TH1F(hist_name, hist_name,50,50,150)
    print prefix+file_location
    myFile = ROOT.TFile.Open(prefix+file_location)
    myTree = myFile.Events
    length = myTree.GetEntries()
    i=0
    print "Processing file:"
    print file_location
    for event in myTree:
        if event.nMuon>=2:
            eventSum = ROOT.TLorentzVector()
            muon1 = ROOT.TLorentzVector()
            muon2 = ROOT.TLorentzVector()
            muon1.SetPtEtaPhiM(event.Muon_pt[0],event.Muon_eta[0],event.Muon_phi[0],event.Muon_mass[0])
            muon2.SetPtEtaPhiM(event.Muon_pt[1],event.Muon_eta[1],event.Muon_phi[1],event.Muon_mass[1])
            myHistogram.Fill((muon1+muon2).M())
        i+=1
        drawProgressBar(1.0*i/length, 50)
        
    print "" 
    return myHistogram
 
prefix = "root://gfe02.grid.hep.ph.ic.ac.uk:1097/"
dataset_file = open("data_MET_tree1.txt", "r") 
dataset_list = dataset_file.readlines() 

for dataset in dataset_list:
    d = dataset[30:][:-1]
    if dataset_list.index(dataset)==0:
        Hist = calcInvMass(d, prefix, "MET_"+format(dataset_list.index(dataset)))
    else:
        Hist.Add(calcInvMass(d, prefix,  "MET_"+format(dataset_list.index(dataset))))

c1=ROOT.TCanvas()
Hist.Draw()
c1.SaveAs("test.pdf")
