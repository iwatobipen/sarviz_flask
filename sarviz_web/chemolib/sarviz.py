# this is core function of SAR visualizetion.

from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem.Draw import SimilarityMaps
from sklearn.svm import SVC
from matplotlib import cm
import numpy as np
import pickle
import uuid

modelf = open( "./dataprep/svcmodel.pkl", "rb" )
model = pickle.load( modelf )

def calc_fp_arr( mol ):
    fp = AllChem.GetMorganFingerprintAsBitVect( mol, 2 )
    arr = np.zeros((1,))
    DataStructs.ConvertToNumpyArray( fp, arr )
    return arr

def getProba( fp, probabilityfunc ):
    # probability function returns 2 x 1 matrix.
    return probabilityfunc( fp )[0][1]
#save fig random or unique name!!! avoid chaching
def mapperfunc( mol ):
    fig, weight = SimilarityMaps.GetSimilarityMapForModel( mol,
                                                           SimilarityMaps.GetMorganFingerprint,
                                                            lambda x:getProba( x, model.predict_proba ),
                                                            colorMap=cm.bwr )
    cls_result = model.predict( calc_fp_arr(mol) )
    fname = uuid.uuid1().hex+".png"
    fig.savefig( "static/tempfig/"+fname, bbox_inches = "tight" )
    return cls_result, fname

def molprop_calc( mol ):
    mw = round( Descriptors.MolWt( mol ), 2 )
    mollogp = round( Descriptors.MolLogP( mol ), 2 )
    tpsa = round( Descriptors.TPSA( mol ), 2  )
    return [ mw, mollogp, tpsa ]
