import pyg4ometry

def add_sens_to_file(inFile, outFile):

    r1 = pyg4ometry.gdml.Reader(inFile)
    reg1 = r1.getRegistry()

    print("Looping over volumes")
    for volname, volume in reg1.logicalVolumeDict.items():
        aux_tag = pyg4ometry.gdml.Auxiliary("SensDet", volname)
        volume .addAuxiliaryInfo(aux_tag)

    # gdml output
    w = pyg4ometry.gdml.Writer()
    w.addDetector(reg1)
    w.write(outFile)
        
def merge_files(inFileArC, inFileMin, outFile):
    
    r1 = pyg4ometry.gdml.Reader(inFileArC)
    reg1 = r1.getRegistry()
    
    r2 = pyg4ometry.gdml.Reader(inFileMin)
    reg2 = r2.getRegistry()
    
    ## Want to loop over the logical volumes, and add an auxiliary field to them
    print("Looping over ArC volumes")
    for volname, volume in reg1.logicalVolumeDict.items():
        if "AssemblyVolume" in str(type(volume)): continue
        if volname == 'volTPCActive':
            aux_tag = pyg4ometry.gdml.Auxiliary("SensDet", volname)
            volume .addAuxiliaryInfo(aux_tag)

    print("Looping over MINERvA volumes")
    for volname, volume in reg2.logicalVolumeDict.items():
        if "AssemblyVolume" in str(type(volume)): continue
        if "Fiber" in volname: continue
        aux_tag = pyg4ometry.gdml.Auxiliary("SensDet", volname)
        volume .addAuxiliaryInfo(aux_tag)

    print("Merging volumes")
    lv = reg2.logicalVolumeDict["World0x3eeb610"]
    
    # create physical volume with placement
    pv = pyg4ometry.geant4.PhysicalVolume([0,0,0],[0,0,-(6805.696+106.934)], lv, "MINERvA", reg1.logicalVolumeDict["volSurroundings2x2"], reg1)
    
    reg1.addVolumeRecursive(pv)
    
    # gdml output
    w = pyg4ometry.gdml.Writer()
    w.addDetector(reg1)
    w.write(outFile)

if __name__ == "__main__":

    inFileArC = "test.gdml"
    inFileMin = "minerva_v2_hacked.gdml"
    # outFile   = "Merged2x2MINERvA_test.gdml"    
    outFile   = "test.gdml"  
    merge_files(inFileArC, inFileMin, outFile)
