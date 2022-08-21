


BLOCK_INDEX_REGERING = 0
BLOCK_INDEX_HÖGER_OP = 1
class Grunddata:
    blocknamn = ["",""]
    blocknamn[BLOCK_INDEX_REGERING] = "Regering + stöd"
    blocknamn[BLOCK_INDEX_HÖGER_OP] = "Högeropposition"

    partier = ["V", "S", "MP", "C", "L", "M", "KD", "SD"]

    block_för_parti = [
        blocknamn[BLOCK_INDEX_REGERING],
        blocknamn[BLOCK_INDEX_REGERING],
        blocknamn[BLOCK_INDEX_REGERING],
        blocknamn[BLOCK_INDEX_REGERING],
        blocknamn[BLOCK_INDEX_HÖGER_OP],
        blocknamn[BLOCK_INDEX_HÖGER_OP],
        blocknamn[BLOCK_INDEX_HÖGER_OP],
        blocknamn[BLOCK_INDEX_HÖGER_OP]]
        
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

    gräns_småparti = 6
    riksdagsspärr = 4.0

    valdag = "2022-09-11"







