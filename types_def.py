
from dataclasses import dataclass, field
@dataclass
class Urval:
    färger_partier_urval: list[str] = field(default_factory=list)
    partier_urval: list[str] = field(default_factory=list)
