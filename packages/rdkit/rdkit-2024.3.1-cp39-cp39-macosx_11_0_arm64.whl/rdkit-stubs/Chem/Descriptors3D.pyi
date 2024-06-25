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
descList: list  # value = [('PMI1', <function <lambda> at 0x105229dc0>), ('PMI2', <function <lambda> at 0x11205ae50>), ('PMI3', <function <lambda> at 0x11205aee0>), ('NPR1', <function <lambda> at 0x11205af70>), ('NPR2', <function <lambda> at 0x1120bd040>), ('RadiusOfGyration', <function <lambda> at 0x1120bd0d0>), ('InertialShapeFactor', <function <lambda> at 0x1120bd160>), ('Eccentricity', <function <lambda> at 0x1120bd1f0>), ('Asphericity', <function <lambda> at 0x1120bd280>), ('SpherocityIndex', <function <lambda> at 0x1120bd310>), ('PBF', <function <lambda> at 0x1120bd3a0>)]
