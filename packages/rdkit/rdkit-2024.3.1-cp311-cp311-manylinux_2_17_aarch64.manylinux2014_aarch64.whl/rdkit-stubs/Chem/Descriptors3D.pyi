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
descList: list  # value = [('PMI1', <function <lambda> at 0xffff9f1b3240>), ('PMI2', <function <lambda> at 0xffff928b5760>), ('PMI3', <function <lambda> at 0xffff928b58a0>), ('NPR1', <function <lambda> at 0xffff928b5940>), ('NPR2', <function <lambda> at 0xffff928b59e0>), ('RadiusOfGyration', <function <lambda> at 0xffff928b5a80>), ('InertialShapeFactor', <function <lambda> at 0xffff928b5b20>), ('Eccentricity', <function <lambda> at 0xffff928b5bc0>), ('Asphericity', <function <lambda> at 0xffff928b5c60>), ('SpherocityIndex', <function <lambda> at 0xffff928b5d00>), ('PBF', <function <lambda> at 0xffff928b5da0>)]
