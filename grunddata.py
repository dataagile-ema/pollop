


BLOCK_INDEX_REGERING = 0
BLOCK_INDEX_OP = 1
class Grunddata:
    blocknamn = ["",""]
    blocknamn[BLOCK_INDEX_REGERING] = "Regering + stöd"
    blocknamn[BLOCK_INDEX_OP] = "Opposition"

    partier = ["V", "S", "MP", "C", "L", "M", "KD", "SD"]

    block_för_parti = [
        blocknamn[BLOCK_INDEX_OP],
        blocknamn[BLOCK_INDEX_OP],
        blocknamn[BLOCK_INDEX_OP],
        blocknamn[BLOCK_INDEX_OP],
        blocknamn[BLOCK_INDEX_REGERING],
        blocknamn[BLOCK_INDEX_REGERING],
        blocknamn[BLOCK_INDEX_REGERING],
        blocknamn[BLOCK_INDEX_REGERING]]
        
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

    valdag = "2026-09-13"

    antal_undersökningsdagar_n_rullande = 2

    antal_undersökningsdagar_n_stacked = 14








