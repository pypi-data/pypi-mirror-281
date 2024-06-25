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
descList: list  # value = [('PMI1', <function <lambda> at 0xffff8f306680>), ('PMI2', <function <lambda> at 0xffff82a0e9e0>), ('PMI3', <function <lambda> at 0xffff82a0ea70>), ('NPR1', <function <lambda> at 0xffff82a0eb00>), ('NPR2', <function <lambda> at 0xffff82a0eb90>), ('RadiusOfGyration', <function <lambda> at 0xffff82a0ec20>), ('InertialShapeFactor', <function <lambda> at 0xffff82a0ecb0>), ('Eccentricity', <function <lambda> at 0xffff82a0ed40>), ('Asphericity', <function <lambda> at 0xffff82a0edd0>), ('SpherocityIndex', <function <lambda> at 0xffff82a0ee60>), ('PBF', <function <lambda> at 0xffff82a0eef0>)]
