"""
 Descriptors derived from a molecule's 3D structure

"""
from __future__ import annotations
from rdkit.Chem.Descriptors import _isCallable
from rdkit.Chem import rdMolDescriptors
__all__ = ['CalcMolDescriptors3D', 'descList', 'rdMolDescriptors']
def CalcMolDescriptors3D(mol, confId = None):
    """
    
        Compute all 3D descriptors of a molecule
        
        Arguments:
        - mol: the molecule to work with
        - confId: conformer ID to work with. If not specified the default (-1) is used
        
        Return:
        
        dict
            A dictionary with decriptor names as keys and the descriptor values as values
    
        raises a ValueError 
            If the molecule does not have conformers
        
    """
def _setupDescriptors(namespace):
    ...
descList: list  # value = [('PMI1', <function <lambda> at 0x7fe56f641440>), ('PMI2', <function <lambda> at 0x7fe56f641b20>), ('PMI3', <function <lambda> at 0x7fe56f641bc0>), ('NPR1', <function <lambda> at 0x7fe56f641c60>), ('NPR2', <function <lambda> at 0x7fe56f641d00>), ('RadiusOfGyration', <function <lambda> at 0x7fe56f641da0>), ('InertialShapeFactor', <function <lambda> at 0x7fe56f641e40>), ('Eccentricity', <function <lambda> at 0x7fe56f641ee0>), ('Asphericity', <function <lambda> at 0x7fe56f641f80>), ('SpherocityIndex', <function <lambda> at 0x7fe56f642020>), ('PBF', <function <lambda> at 0x7fe56f6420c0>)]
