
from enum import Enum
class block_index(Enum):
    regering = 0
    höger_op = 1
class Grunddata:
    blocknamn = ["",""]
    blocknamn[block_index.regering.value] = "Regering + stöd"
    blocknamn[block_index.höger_op.value] = "Högeropposition"

    partier = ["V", "S", "MP", "C", "L", "M", "KD", "SD"]

    block_för_parti = [
        blocknamn[block_index.regering.value],
        blocknamn[block_index.regering.value],
        blocknamn[block_index.regering.value],
        blocknamn[block_index.regering.value],
        blocknamn[block_index.höger_op.value],
        blocknamn[block_index.höger_op.value],
        blocknamn[block_index.höger_op.value],
        blocknamn[block_index.höger_op.value]]
        
    färg_för_parti = [
        "#B00000",
        "#ed1b34",
        "#83CF39",
        "#009933",
        "#6BB7EC",
        "#1B49DD",
        "#231977",
        "#dddd00",
    ]

    gräns_småparti = 4.5
    riksdagsspärr = 4.0







