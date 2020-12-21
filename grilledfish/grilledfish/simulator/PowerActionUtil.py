import os
import json
import urllib.parse
from django.template import loader
from simulator.simumodel.model import model, global_model
from django.template import loader, TemplateDoesNotExist

def handle_power_action_post(machineInfo, request):
    full_path = request.get_full_path()
    if machineInfo.power and full_path == machineInfo.power.action.url:
        trans_power_action(machineInfo, request)
        #machineInfo.pageCache[full_path] = None
        return "{\"result\":\"good\"}"

    return None
def trans_power_action(machineInfo, request):
    body_unicode = request.body.decode()
    request_json = json.loads(body_unicode)
    action = request_json["ResetType"]
    if action == machineInfo.power.action.PowerOn:
        machineInfo.power.PowerState = "On"
    elif action == machineInfo.power.action.SoftPowerOff:
        machineInfo.power.PowerState = "Off"
    elif action == machineInfo.power.action.HardPowerOff:
        machineInfo.power.PowerState = "Off"
    else:
        machineInfo.power.PowerState = action

    