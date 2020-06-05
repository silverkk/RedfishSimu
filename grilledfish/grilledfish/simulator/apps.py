from django.apps import AppConfig
import enum
import sys
import json

class SimulatorConfig(AppConfig):
    name = 'simulator'

class MachineType(enum.Enum): 
    idrac8 = 1
    idrac9 = 2
    ilo4 = 3
    ilo5 = 4
    lenovo = 5
    Huawei = 6
    pcsd = 7
    supermicro = 8
    Inspur = 9
    idrac7 = 10
    Intel = 11
    Kontron = 12
    H3C = 13
    sugon = 14
    nettrix = 15

class MachineComponent(enum.Enum):
    system = 'system'
    raid = 'raid'
    storage = 'storage'

class RedfishMachineConfig:
    def getMachines(self):
        with open("grilledfish.json") as json_file:
            data = json.load(json_file)
            return data['machines']