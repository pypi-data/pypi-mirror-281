from .datatypes import Group
from .generator import GroupGenerator, GroupIdentifier
from dataclasses import dataclass

@dataclass
class DABEnsembleTable:
    """See https://www.etsi.org/deliver/etsi_en/301700_301799/301700/01.01.01_60/en_301700v010101p.pdf
    frequency = channel frequency in khz"""
    mode: int
    frequency: int
    eld: int
@dataclass
class DABServiceTable:
    """See https://www.etsi.org/deliver/etsi_en/301700_301799/301700/01.01.01_60/en_301700v010101p.pdf"""
    variant_code: int
    sld: int
    eld:int=0
    linkage:int=0

@dataclass
class GeneralRadioTextPlus:
    """Not used yet"""
    toggle: bool
    running: bool
    content_type: int
    start: int
    lenght: int
    content_type_2: int
    start_2: int
    lenght_2: int

class UnUsableGroup(Exception): pass

class ODA:
    @staticmethod
    def DABCrossrefrence_AID(basic: Group, group: GroupIdentifier) -> Group:
        """See https://www.etsi.org/deliver/etsi_en/301700_301799/301700/01.01.01_60/en_301700v010101p.pdf"""
        if group.group_version or group.group_number > 13 or group.group_number < 7:
            raise UnUsableGroup("DAB Crossrenfence can use (7-13)A")
        return GroupGenerator.oda_aid(basic, group, 0x0093, 0x0000)

    @staticmethod
    def DabCrossrefrence(basic: Group, group: GroupIdentifier, es_flag: bool, details: DABEnsembleTable | DABServiceTable) -> Group:
        """See https://www.etsi.org/deliver/etsi_en/301700_301799/301700/01.01.01_60/en_301700v010101p.pdf"""
        if group.group_version or group.group_number > 13 or group.group_number < 7:
            raise UnUsableGroup("DAB Crossrenfence can use (7-13)A")
        data = [0,0,0]
        data[0] |= (int(es_flag) << 4)
        if not es_flag:
            data[0] |= ((details.mode & 0b11) << 2) #type: ignore
            data[0] |= ((details.mode & 0b111111111111111111) >> 16) #type: ignore

            data[1] = ((details.frequency / 16) & 0b001111111111111111) #type: ignore

            data[2] = details.eld #type: ignore
        else:
            data[0] |= (details.variant_code & 0b1111) #type: ignore
            match details.variant_code: #type: ignore
                case 0:
                    data[1] = details.eld #type: ignore
                case 1:
                    data[1] = details.linkage #type: ignore
            data[2] = details.sld #type: ignore
        return GroupGenerator.custom(basic, group, data)