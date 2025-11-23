from enum import Enum

class Role(Enum):
    C = "C" #client
    PC = "PC" #premium client
    FA = "FA" #financial advisor
    FP = "FP" #financial planner
    T = "T" #teller


class Request(Enum):
    VAB = 0   # view account balance
    VIP = 1   # view investment portfolio
    MIP = 2   # modify investment portfolio
    VFA = 3   # view contact detail of FA
    VFP = 4   # view contact detail of FP
    VMI = 5   # view money market instrument
    VPI = 6   # view private consumer instrument
    AS  = 7   # access system
