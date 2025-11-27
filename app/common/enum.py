from enum import Enum

class Role(Enum):
    C = "C" #client
    PC = "PC" #premium client
    FA = "FA" #financial advisor
    FP = "FP" #financial planner
    T = "T" #teller

ROLE_LABELS = {
    Role.C: "Client",
    Role.PC: "Premium Client",
    Role.FA: "Financial Advisor",
    Role.FP: "Financial Planner",
    Role.T: "Teller",
}


class Request(Enum):
    VAB = 0   # view account balance
    VIP = 1   # view investment portfolio
    MIP = 2   # modify investment portfolio
    VFA = 3   # view contact detail of FA
    VFP = 4   # view contact detail of FP
    VMI = 5   # view money market instrument
    VPI = 6   # view private consumer instrument
    AS  = 7   # access system

REQUEST_LABELS = {
    Request.VAB: "view account balance",
    Request.VIP: "view investment portfolio",
    Request.MIP: "modify investment portfolio",
    Request.VFA: "view contact detail of FA",
    Request.VFP: "view contact detail of FP",
    Request.VMI: "view money market instrument",
    Request.VPI: "view private consumer instrument",
    Request.AS:  "access system",
}