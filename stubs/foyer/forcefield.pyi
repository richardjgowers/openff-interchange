from typing import Dict, List, Union

class Forcefield(object):
    def __init__(self, name: int): ...
    def get_parameters(
        self,
        group: str,
        key: Union[str, List[str]],
        keys_are_atom_classes: bool = False,
    ) -> Dict[str, float]: ...
    @staticmethod
    def get_generator(ff: Forcefield, gen_type: Any) -> Any: ...
