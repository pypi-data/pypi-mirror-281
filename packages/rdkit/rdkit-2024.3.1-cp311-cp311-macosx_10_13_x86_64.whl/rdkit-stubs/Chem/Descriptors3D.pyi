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
descList: list  # value = [('PMI1', <function <lambda> at 0x1054f9b20>), ('PMI2', <function <lambda> at 0x10b3800e0>), ('PMI3', <function <lambda> at 0x10b380220>), ('NPR1', <function <lambda> at 0x10b3802c0>), ('NPR2', <function <lambda> at 0x10b380360>), ('RadiusOfGyration', <function <lambda> at 0x10b380400>), ('InertialShapeFactor', <function <lambda> at 0x10b3804a0>), ('Eccentricity', <function <lambda> at 0x10b380540>), ('Asphericity', <function <lambda> at 0x10b3805e0>), ('SpherocityIndex', <function <lambda> at 0x10b380680>), ('PBF', <function <lambda> at 0x10b380720>)]
