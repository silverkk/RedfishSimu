import ipaddress
import socket, struct
import types
import threading, queue
from datetime import datetime
from simulator.apps import MachineType, RedfishMachineConfig, MachineComponent
import sys
import time

class model:
    def __init__(self):
        rfConfig = RedfishMachineConfig()
        self.buildPerfConfig(rfConfig.getPerfConfig())
        self.buildMachine(rfConfig.getMachines(), rfConfig.getPerfConfig())        

    def buildMachine(self, machineConfigList, perfConfig):
        self.machines = {}
        for configItem in machineConfigList:
            self.buildOneMachine(configItem, perfConfig)
    def buildOneMachine(self, machineConfig, perfConfig):
        startIp = int(ipaddress.IPv4Address(machineConfig['startIp']))
        endIp = int(ipaddress.IPv4Address(machineConfig['endIp'])) + 1        
        for ip in range(startIp, endIp):
            machine = types.SimpleNamespace()
            mac = ':'.join(['{}{}'.format(a, b)
                     for a, b
                     in zip(*[iter('{:012x}'.format(ip))]*2)])
            macDash = '-'.join(['{}{}'.format(a, b)
                     for a, b
                     in zip(*[iter('{:012x}'.format(ip))]*2)])
            machine.ip = ip
            machine.ipStr = socket.inet_ntoa(struct.pack('!L', ip))
            machine.mac = mac
            machine.macDash = macDash
            #machine.vendor = machineConfig['vendor']
            machine.vendor = MachineType[machineConfig['vendor']]
            machine.fwVersion = machineConfig['fwVersion']
            machine.model = machineConfig['model'] if 'model' in machineConfig else None
            machine.flatMode = machineConfig['flatMode'] if 'flatMode' in machineConfig else False
            machine.genIpmiFruSetting = machineConfig['genIpmiFruSetting'] if 'genIpmiFruSetting' in machineConfig else False
            machine.invalidRespLength = machineConfig['invalidRespLength'] if 'invalidRespLength' in machineConfig else False
            self.appendHealthInfo(machine, machineConfig)
            self.appendFirmwareVersionInfo(machine, machineConfig)            
            self.appendDefualtSelLogItem(machine, machineConfig)
            self.appendPowerInfo(machine, machineConfig)
            self.buildCacheInfra(machine, perfConfig)
            self.appendFirmwareUpgradeInfo(machine, machineConfig)
            self.machines[ip] = machine

    def transHealthInfo(self, machine, healthNamespace, healthDict, appendDefault, genSelLog=False):
        if 'system' in healthDict:
            if genSelLog:
                self.appendSelLogItemFromHealthInfo(machine, 'system', healthNamespace.system, healthDict['system'] )
            healthNamespace.system = healthDict['system']
        elif appendDefault:
            healthNamespace.system = 'OK'

        if 'storage' in healthDict:
            if genSelLog:
               self.appendSelLogItemFromHealthInfo(machine, 'storage', healthNamespace.storage, healthDict['storage'] )
            healthNamespace.storage = healthDict['storage']
        elif appendDefault:
            healthNamespace.storage = 'OK'

        if 'memory' in healthDict:
            if genSelLog:
               self.appendSelLogItemFromHealthInfo(machine, 'memory', healthNamespace.memory, healthDict['memory'] )
            healthNamespace.memory = healthDict['memory']
        elif appendDefault:
            healthNamespace.memory = 'OK'

        if 'NIC' in healthDict:
            if genSelLog:
               self.appendSelLogItemFromHealthInfo(machine, 'NIC', healthNamespace.NIC, healthDict['NIC'] )
            healthNamespace.NIC = healthDict['NIC']
        elif appendDefault:
            healthNamespace.NIC = 'OK'
            
        if 'Power' in healthDict:
            if genSelLog:
               self.appendSelLogItemFromHealthInfo(machine, 'Power', healthNamespace.Power, healthDict['Power'] )
            healthNamespace.Power = healthDict['Power']
        elif appendDefault:
            healthNamespace.Power = 'OK'

        if 'Processor' in healthDict:
            if genSelLog:
               self.appendSelLogItemFromHealthInfo(machine, 'Processor', healthNamespace.Processor, healthDict['Processor'] )
            healthNamespace.Processor = healthDict['Processor']
        elif appendDefault:
            healthNamespace.Processor = 'OK'

        if 'raid' in healthDict:
            if genSelLog:
               self.appendSelLogItemFromHealthInfo(machine, 'raid', healthNamespace.raid, healthDict['raid'] )
            healthNamespace.raid = healthDict['raid']
        elif appendDefault:
            healthNamespace.raid = 'OK'

        if 'Voltage' in healthDict:
            if genSelLog:
               self.appendSelLogItemFromHealthInfo(machine, 'Voltage', healthNamespace.Voltage, healthDict['Voltage'] )
            healthNamespace.Voltage = healthDict['Voltage']
        elif appendDefault:
            healthNamespace.Voltage = 'OK'
        
        if 'Battery' in healthDict:
            if genSelLog:
               self.appendSelLogItemFromHealthInfo(machine, 'Battery', healthNamespace.Battery, healthDict['Battery'] )
            healthNamespace.Battery = healthDict['Battery']
        elif appendDefault:
            healthNamespace.Battery = 'OK'

        if 'Fan' in healthDict:
            if genSelLog:
               self.appendSelLogItemFromHealthInfo(machine, 'Fan', healthNamespace.Fan, healthDict['Fan'] )
            healthNamespace.Fan = healthDict['Fan']
        elif appendDefault:
            healthNamespace.Fan = 'OK'
        
        if 'Temperature' in healthDict:
            if genSelLog:
               self.appendSelLogItemFromHealthInfo(machine, 'Temperature', healthNamespace.Temperature, healthDict['Temperature'] )
            healthNamespace.Temperature = healthDict['Temperature']
        elif appendDefault:
            healthNamespace.Temperature = 'OK'

        if 'Volume' in healthDict:
            if genSelLog:
               self.appendSelLogItemFromHealthInfo(machine, 'Volume', healthNamespace.Volume, healthDict['Volume'] )
            healthNamespace.Volume = healthDict['Volume']
        elif appendDefault:
            healthNamespace.Volume = 'OK'

        if 'Firmware' in healthDict:
            if genSelLog:
               self.appendSelLogItemFromHealthInfo(machine, 'Firmware', healthNamespace.Firmware, healthDict['Firmware'] )
            healthNamespace.Firmware = healthDict['Firmware']
        elif appendDefault:
            healthNamespace.Firmware = 'OK'

        if 'EventService' in healthDict:
            if genSelLog:
               self.appendSelLogItemFromHealthInfo(machine, 'EventService', healthNamespace.EventService, healthDict['EventService'] )
            healthNamespace.EventService = healthDict['EventService']
        elif appendDefault:
            healthNamespace.EventService = 'OK'

        if 'MgtPort' in healthDict:
            if genSelLog:
               self.appendSelLogItemFromHealthInfo(machine, 'MgtPort', healthNamespace.MgtPort, healthDict['MgtPort'] )
            healthNamespace.MgtPort = healthDict['MgtPort']
        elif appendDefault:
            healthNamespace.MgtPort = 'OK'

        if 'Manager' in healthDict:
            if genSelLog:
               self.appendSelLogItemFromHealthInfo(machine, 'Manager', healthNamespace.Manager, healthDict['Manager'] )
            healthNamespace.Manager = healthDict['Manager']
        elif appendDefault:
            healthNamespace.Manager = 'OK'

        if 'PcieDevice' in healthDict:
            if genSelLog:
               self.appendSelLogItemFromHealthInfo(machine, 'PcieDevice', healthNamespace.PcieDevice, healthDict['PcieDevice'] )
            healthNamespace.PcieDevice = healthDict['PcieDevice']
        elif appendDefault:
            healthNamespace.PcieDevice = 'OK'

    def appendHealthInfo(self, machine, machineConfig):
        healthInfo = types.SimpleNamespace()
        healthConfig = machineConfig['health']
        self.transHealthInfo(machine, healthInfo, healthConfig, True)
        machine.healthInfo = healthInfo

    def updateHealthInfo(self, ipStr, jsonInfo):
        machineInfo = self.getMachineInfo(ipStr)
        self.transHealthInfo(machineInfo, machineInfo.healthInfo, jsonInfo, False, genSelLog=True)

    def appendFirmwareVersionInfo(self, machine, machineConfig):
        firmwareVersionInfo = types.SimpleNamespace()
        if 'FirmwareVersion' in machineConfig:
            firmwareVersionInfoConfig = machineConfig['FirmwareVersion']
        else:
            firmwareVersionInfoConfig = {}
        self.transFirmwareVersionInfo(machine, firmwareVersionInfo, firmwareVersionInfoConfig)
        machine.FirmwareVersion = firmwareVersionInfo
    def transFirmwareVersionInfo(self, machine, firmwareVersionNamespace, firmwareVersionDict):
        if 'bios' in firmwareVersionDict:
            firmwareVersionNamespace.bios = firmwareVersionDict['bios']
        else:
            firmwareVersionNamespace.bios = 'bios Version'
        if 'Backplane' in firmwareVersionDict:
            firmwareVersionNamespace.Backplane = firmwareVersionDict['Backplane']
        else:
            firmwareVersionNamespace.Backplane = 'Backplane Version'        
        if 'Battery' in firmwareVersionDict:
            firmwareVersionNamespace.Battery = firmwareVersionDict['Battery']
        else:
            firmwareVersionNamespace.Battery = 'Battery Version'
        if 'Disk' in firmwareVersionDict:
            firmwareVersionNamespace.Disk = firmwareVersionDict['Disk']
        else:
            firmwareVersionNamespace.Disk = 'Disk Version'
        if 'Manager' in firmwareVersionDict:
            firmwareVersionNamespace.Manager = firmwareVersionDict['Manager']
        else:
            firmwareVersionNamespace.Manager = 'Manager Version'
        if 'NIC' in firmwareVersionDict:
            firmwareVersionNamespace.NIC = firmwareVersionDict['NIC']
        else:
            firmwareVersionNamespace.NIC = 'NIC Version'
        if 'PcieDevice' in firmwareVersionDict:
            firmwareVersionNamespace.PcieDevice = firmwareVersionDict['PcieDevice']
        else:
            firmwareVersionNamespace.PcieDevice = 'PcieDevice Version'
        if 'Power' in firmwareVersionDict:
            firmwareVersionNamespace.Power = firmwareVersionDict['Power']
        else:
            firmwareVersionNamespace.Power = 'Power Version'
        if 'Storage' in firmwareVersionDict:
            firmwareVersionNamespace.Storage = firmwareVersionDict['Storage']
        else:
            firmwareVersionNamespace.Storage = 'Storage Version'
        if 'Switch' in firmwareVersionDict:
            firmwareVersionNamespace.Switch = firmwareVersionDict['Switch']
        else:
            firmwareVersionNamespace.Switch = 'Switch Version'

    def appendSelLogItemFromHealthInfo(self, machine, componentName, beforeStatus, afterStatus):
        item = types.SimpleNamespace()
        item.datetime = datetime.now().strftime(machine.sel.datetimeFormat)
        item.message = componentName + " health changed from " + beforeStatus + " to " + afterStatus
        item.id = machine.sel.nextLogId

        while len(machine.sel.logList) >= machine.sel.maxLogItemCount:
            machine.sel.logList.pop(0)

        machine.sel.logList.append(item)
        machine.sel.logItemCount = len(machine.sel.logList)

        machine.sel.nextLogId += 1

    def appendDefualtSelLogItem(self, machine, machineConfig):
        sel = None
        if 'sel' in machineConfig:
            sel = types.SimpleNamespace()
            selConfig = machineConfig['sel']
            if 'paging' in selConfig:
                sel.paging = selConfig['paging']
            else:
                sel.paging = True

            if 'maxLogItemCount' in selConfig:
                sel.maxLogItemCount = selConfig['maxLogItemCount']
            else:
                sel.maxLogItemCount = 100

            if 'logItemPerPage' in selConfig:
                sel.logItemPerPage = selConfig['logItemPerPage']
            else:
                sel.logItemPerPage = 50

            if 'skiptoken' in selConfig:
                sel.skiptoken = selConfig['skiptoken']
            else:
                sel.skiptoken = None

            if 'skipType' in selConfig:
                sel.skipType = selConfig['skipType']
            else:
                sel.skipType = "Items"            

            if 'datetimeFormat' in selConfig:
                sel.datetimeFormat = selConfig['datetimeFormat']
            else:
                sel.datetimeFormat = "%Y-%m-%dT%H:%M:%S+08:00"
            
            #sel.logQueue = queue.Queue(maxsize=sel.maxLogItemCount)
            sel.logList = []
            for i in range(0, sel.maxLogItemCount):
                item = types.SimpleNamespace()
                item.datetime = datetime.now().strftime(sel.datetimeFormat)
                item.message = "Auto generated SEL log item when gilledfish start"
                item.id = i
                sel.logList.append(item)
            sel.nextLogId = sel.maxLogItemCount
            sel.logItemCount = len(sel.logList)
            
        machine.sel = sel    

    def appendPowerInfo(self, machine, machineConfig):
        power = None
        if 'power' in machineConfig:
            power = types.SimpleNamespace()
            powerConfig = machineConfig['power']
            if 'PowerState' in powerConfig:
                power.PowerState = powerConfig['PowerState']
            else:
                power.PowerState = 'On'

            action = types.SimpleNamespace()
            actionConfig = machineConfig['power']['action']
            action.url = actionConfig['url']
            action.PowerOn = actionConfig['PowerOn']
            action.SoftPowerOff = actionConfig['SoftPowerOff']
            action.HardPowerOff = actionConfig['HardPowerOff']

            power.action = action

        machine.power = power

    def appendFirmwareUpgradeInfo(self, machine, machineConfig):
        firmwareUpgrade = None
        if 'firmwareUpgrade' in machineConfig:
            firmwareUpgrade = types.SimpleNamespace()

            action = types.SimpleNamespace()
            actionConfig = machineConfig['firmwareUpgrade']['action']
            action.submit_upgrade_url = actionConfig['submit_upgrade_url']
            action.submit_upgrade_response = actionConfig['submit_upgrade_response']
            action.task_status_url = actionConfig['task_status_url']
            action.task_running_response = actionConfig['task_running_response']
            action.task_done_response = actionConfig['task_done_response']
            action.taskState = actionConfig['taskState']
            action.secondsUpgradeTakes = actionConfig['secondsUpgradeTakes']

            firmwareUpgrade.action = action

            firmwareUpgrade.summary = types.SimpleNamespace()

        machine.firmwareUpgrade = firmwareUpgrade

    def getMachineInfo(self, ipStr):
        ip = int(ipaddress.IPv4Address(ipStr))
        return self.machines[ip]

    def buildPerfConfig(self, perfConfig):
        #trace the performance
        self.perfStatisticEnabled = perfConfig['enablePerfStatistic'] if 'enablePerfStatistic' in perfConfig else False
        self.perfGranularity = perfConfig['granularity']
        self.performanceSummary = types.SimpleNamespace()
        self.performanceSummary.totalResTime = 0
        self.performanceSummary.totalRequestCount = 0
        self.performanceSummary.averageResTime = 0
        self.performanceSummary.maxResTime = 0
        self.performanceSummary.trend = []
        self.requestCount4Iterator = 0
        self.requestSeconds4Iterator = 0
        self.startTime4Iterator = time.time()

    def buildCacheInfra(self, machine, perfConfig):
        machine.cacheEnabled = perfConfig['enableCache'] if 'enableCache' in perfConfig else False
        if machine.cacheEnabled:
            # cache for the template
            machine.templateCache = dict()
            # cache for the rendered page
            machine.pageCache = dict()


    def appendRequestPerformance(self, startTime, endTime):
        if self.perfStatisticEnabled:
            respTime = endTime - startTime
            self.requestSeconds4Iterator = self.requestSeconds4Iterator + respTime
            self.requestCount4Iterator = self.requestCount4Iterator+1

            self.performanceSummary.totalResTime = self.performanceSummary.totalResTime + respTime
            self.performanceSummary.totalRequestCount = self.performanceSummary.totalRequestCount + 1
            if self.performanceSummary.maxResTime < respTime:
                self.performanceSummary.maxResTime = respTime
                
            if self.requestCount4Iterator >= self.perfGranularity:
                performaceItem = types.SimpleNamespace()
                performaceItem.startTime = self.startTime4Iterator
                performaceItem.endTime = time.time()
                performaceItem.averageResTime = self.requestSeconds4Iterator/self.requestCount4Iterator
                self.performanceSummary.averageResTime = self.performanceSummary.totalResTime/self.performanceSummary.totalRequestCount
                if len(self.performanceSummary.trend) > 100:
                    self.performanceSummary.trend.pop(0)
                    
                self.performanceSummary.trend.append(performaceItem)
                self.requestSeconds4Iterator = 0
                self.requestCount4Iterator = 0
                self.startTime4Iterator = performaceItem.endTime


    def getPerformanceSummary(self):
        return self.performanceSummary

# global variable
global_model = model()

   
        

