from .GeneralClass import GeneralClass

from ..Operation.CreateConstantString import CreateConstantString
from ..Operation.PlaceBlockWithBlockStates import PlaceBlockWithBlockStates
from ..Operation.AddInt16ZValue0 import AddInt16ZValue0
from ..Operation.PlaceBlock import PlaceBlock
from ..Operation.AddZValue0 import AddZValue0
from ..Operation.NOP import NOP
from ..Operation.AddInt32ZValue0 import AddInt32ZValue0
from ..Operation.PlaceBlockWithBlockStatesDeprecated import PlaceBlockWithBlockStatesDeprecated
from ..Operation.AddXValue import AddXValue
from ..Operation.SubtractXValue import SubtractXValue
from ..Operation.AddYValue import AddYValue
from ..Operation.SubtractYValue import SubtractYValue
from ..Operation.AddZValue import AddZValue
from ..Operation.SubtractZValue import SubtractZValue
from ..Operation.AddInt16XValue import AddInt16XValue
from ..Operation.AddInt32XValue import AddInt32XValue
from ..Operation.AddInt16YValue import AddInt16YValue
from ..Operation.AddInt32YValue import AddInt32YValue
from ..Operation.AddInt16XValue import AddInt16XValue
from ..Operation.AddInt32XValue import AddInt32XValue
from ..Operation.AddInt16YValue import AddInt16YValue
from ..Operation.AddInt32YValue import AddInt32YValue
from ..Operation.AddInt16ZValue import AddInt16ZValue
from ..Operation.AddInt32ZValue import AddInt32ZValue
from ..Operation.SetCommandBlockData import SetCommandBlockData
from ..Operation.PlaceBlockWithCommandBlockData import PlaceBlockWithCommandBlockData
from ..Operation.AddInt8XValue import AddInt8XValue
from ..Operation.AddInt8YValue import AddInt8YValue
from ..Operation.AddInt8ZValue import AddInt8ZValue
from ..Operation.UseRuntimeIDPool import UseRuntimeIDPool
from ..Operation.PlaceRuntimeBlock import PlaceRuntimeBlock
from ..Operation.PlaceBlockWithRuntimeId import PlaceBlockWithRuntimeId
from ..Operation.PlaceRuntimeBlockWithCommandBlockData import PlaceRuntimeBlockWithCommandBlockData
from ..Operation.PlaceRuntimeBlockWithCommandBlockDataAndUint32RuntimeID import PlaceRuntimeBlockWithCommandBlockDataAndUint32RuntimeID
from ..Operation.PlaceCommandBlockWithCommandBlockData import PlaceCommandBlockWithCommandBlockData
from ..Operation.PlaceRuntimeBlockWithChestData import PlaceRuntimeBlockWithChestData
from ..Operation.PlaceRuntimeBlockWithChestDataAndUint32RuntimeID import PlaceRuntimeBlockWithChestDataAndUint32RuntimeID
from ..Operation.AssignDebugData import AssignDebugData
from ..Operation.PlaceBlockWithChestData import PlaceBlockWithChestData
from ..Operation.PlaceBlockWithNBTData import PlaceBlockWithNBTData
from ..Operation.Terminate import Terminate


def GetBDXCommandPool() -> dict[int, GeneralClass]:
    """
    Return dict[commandId(..operationId):int, PythonClass:GeneralClass]
    """
    return {
        1: CreateConstantString(),
        5: PlaceBlockWithBlockStates(),
        6: AddInt16ZValue0(),
        7: PlaceBlock(),
        8: AddZValue0(),
        9: NOP(),
        12: AddInt32ZValue0(),
        13: PlaceBlockWithBlockStatesDeprecated(),
        14: AddXValue(),
        15: SubtractXValue(),
        16: AddYValue(),
        17: SubtractYValue(),
        18: AddZValue(),
        19: SubtractZValue(),
        20: AddInt16XValue(),
        21: AddInt32XValue(),
        22: AddInt16YValue(),
        23: AddInt32YValue(),
        24: AddInt16ZValue(),
        25: AddInt32ZValue(),
        26: SetCommandBlockData(),
        27: PlaceBlockWithCommandBlockData(),
        28: AddInt8XValue(),
        29: AddInt8YValue(),
        30: AddInt8ZValue(),
        31: UseRuntimeIDPool(),
        32: PlaceRuntimeBlock(),
        33: PlaceBlockWithRuntimeId(),
        34: PlaceRuntimeBlockWithCommandBlockData(),
        35: PlaceRuntimeBlockWithCommandBlockDataAndUint32RuntimeID(),
        36: PlaceCommandBlockWithCommandBlockData(),
        37: PlaceRuntimeBlockWithChestData(),
        38: PlaceRuntimeBlockWithChestDataAndUint32RuntimeID(),
        39: AssignDebugData(),
        40: PlaceBlockWithChestData(),
        41: PlaceBlockWithNBTData(),
        88: Terminate()
    }
