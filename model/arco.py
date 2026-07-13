from dataclasses import dataclass

from model.cliente import Cliente


@dataclass
class Arco:
    cliente1: Cliente
    cliente2: Cliente