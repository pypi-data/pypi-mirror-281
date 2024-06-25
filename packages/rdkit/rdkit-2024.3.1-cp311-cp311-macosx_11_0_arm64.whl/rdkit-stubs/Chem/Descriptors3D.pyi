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
descList: list  # value = [('PMI1', <function <lambda> at 0x1034f7ce0>), ('PMI2', <function <lambda> at 0x105db3ba0>), ('PMI3', <function <lambda> at 0x105db3ce0>), ('NPR1', <function <lambda> at 0x105db3d80>), ('NPR2', <function <lambda> at 0x105db3e20>), ('RadiusOfGyration', <function <lambda> at 0x105db3ec0>), ('InertialShapeFactor', <function <lambda> at 0x105db3f60>), ('Eccentricity', <function <lambda> at 0x110b14040>), ('Asphericity', <function <lambda> at 0x110b140e0>), ('SpherocityIndex', <function <lambda> at 0x110b14180>), ('PBF', <function <lambda> at 0x110b14220>)]
