from .interface import GroupInterface
from .comfort import Groups, GroupSequencer, calculate_mjd, calculate_ymd, calculate_ct_hm
from .generator import GroupGenerator, Group
from .decoder import GroupDecoder
__version__: float = 1.98
__lib__: str = "librds"