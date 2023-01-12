import math

### TPC Geometry [mm] - x: drift, y: vertical, z: beam ###

n_mod = [2,1,2]
n_tpc = [2,1,1]

ModuleDimension = [670.,2022.414,670.]

TPCActiveDimension = [302.723,1241.1,620.3]

TPCActiveCenter = {
        '00':[-487.949,-218.236,-335.],
        '01':[-182.051,-218.236,-335.],
        '10':[182.051,-218.236,-335.],
        '11':[487.949,-218.236,-335.],
        '20':[-487.949,-218.236,335.],
        '21':[-182.051,-218.236,335.],
        '30':[182.051,-218.236,335.],
        '31':[487.949,-218.236,335.],
        }

TPCActiveID = {
        '00':0,
        '01':1,
        '10':2,
        '11':3,
        '20':4,
        '21':5,
        '30':6,
        '31':7
        }

PixelPlaneCenter = {
        '00':[-639.311,-218.236,-335.],
        '01':[-30.690,-218.236,-335.],
        '10':[30.690,-218.236,-335.],
        '11':[639.311,-218.236,-335.],
        '20':[-639.311,-218.236,335.],
        '21':[-30.690,-218.236,335.],
        '30':[30.690,-218.236,335.],
        '31':[639.311,-218.236,335.],
        }

# (key/value)-swapped version of TPCActiveID
TPCActiveCopyNo = {value:key for key, value in list(TPCActiveID.items())}

def GetTPCActiveCenter(module_copynumber,halfDetector_copynumber):
    return TPCActiveCenter[str(module_copynumber)+str(halfDetector_copynumber)]

def GetTPCActiveID(module_copynumber,halfDetector_copynumber):
    return TPCActiveID[str(module_copynumber)+str(halfDetector_copynumber)]

def GetModuleCopy(pos):
    mod_x = (math.floor(pos[0]/(ModuleDimension[0]))+n_mod[0]/2)
    mod_z = (math.floor(pos[2]/(ModuleDimension[2]))+n_mod[2]/2)

    return int(mod_x+mod_z*n_mod[0])

def GetHalfDetCopy(pos):
    tpc_x = math.floor(pos[0]/(ModuleDimension[0]/2.))+n_mod[0]/2*n_tpc[0]

    return int(tpc_x)%2

