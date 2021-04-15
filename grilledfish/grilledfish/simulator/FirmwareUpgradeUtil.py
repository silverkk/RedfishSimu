import os
import json
import urllib.parse
from django.template import loader
from simulator.simumodel.model import model, global_model
from django.template import loader, TemplateDoesNotExist
import simulator.utils as utils
from datetime import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect

def handle_upgrade_action(machineInfo, request):
    full_path = request.get_full_path()
    if machineInfo.firmwareUpgrade:
        if full_path == machineInfo.firmwareUpgrade.action.submit_upgrade_url:
            machineInfo.firmwareUpgrade.summary.lastTaskStartTime = datetime.now()
            if hasattr(machineInfo.firmwareUpgrade.summary, 'currentTaskId'):
                machineInfo.firmwareUpgrade.summary.currentTaskId = machineInfo.firmwareUpgrade.summary.currentTaskId + 1
            else:
                machineInfo.firmwareUpgrade.summary.currentTaskId = 1
            
            machineInfo.firmwareUpgrade.summary.status = 'running'
            return load_upgrade_response(machineInfo, request)
        elif full_path.startswith(machineInfo.firmwareUpgrade.action.task_status_url):
            return load_task_status_response(machineInfo, request)
    return None

def load_upgrade_response(machineInfo, request):    
    if machineInfo.firmwareUpgrade.action.submit_upgrade_response_type:
        return load_upgrade_response_on_type(machineInfo, request)
    elif machineInfo.firmwareUpgrade.action.submit_upgrade_response:
        return load_upgrade_response_from_template(machineInfo, request, None, None)

def load_upgrade_response_from_template(machineInfo, request, full_path, path_without_param):
    ip = utils.get_request_ip(request)
    if full_path is None:
        full_path = machineInfo.firmwareUpgrade.action.submit_upgrade_response
    if path_without_param is None:
        path_without_param = machineInfo.firmwareUpgrade.action.submit_upgrade_response
    method = 'get'
    template = utils.get_template_by_ip(ip, full_path, path_without_param, method)
    now = datetime.now()
    context = {
        'machineInfo': machineInfo,
        'currentTime': now.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
    }
    responseContent = template.render(context, request)
    return responseContent

def load_upgrade_response_on_type(machineInfo, request):
    response_type = machineInfo.firmwareUpgrade.action.submit_upgrade_response_type
    if response_type == 'Location':
        response_location = load_upgrade_response_from_template(machineInfo, request, machineInfo.firmwareUpgrade.action.submit_upgrade_response_location, machineInfo.firmwareUpgrade.action.submit_upgrade_response_location)
        if hasattr(machineInfo.firmwareUpgrade.action, 'submit_upgrade_response'):            
            response_body = load_upgrade_response_from_template(machineInfo, request, machineInfo.firmwareUpgrade.action.submit_upgrade_response, machineInfo.firmwareUpgrade.action.submit_upgrade_response)
        else:
            response_body = ''
        http_code = machineInfo.firmwareUpgrade.action.submit_upgrade_response_code        
        response = HttpResponse(response_body, status=http_code, content_type='application/json')
        response['Location'] = response_location+ "" # convert django.utils.safestring to python string
    else:
        response = None
    return response

def load_task_status_response(machineInfo, request):
    ip = utils.get_request_ip(request)
    now = datetime.now()
    timeSpan = now - machineInfo.firmwareUpgrade.summary.lastTaskStartTime
    if timeSpan.total_seconds() > machineInfo.firmwareUpgrade.action.secondsUpgradeTakes:
        full_path = machineInfo.firmwareUpgrade.action.task_done_response
        machineInfo.firmwareUpgrade.summary.status = 'done'
        increase_firmware_version(machineInfo.FirmwareVersion, machineInfo)
    else:
        full_path = machineInfo.firmwareUpgrade.action.task_running_response
    path_without_param = full_path
    method = 'get'
    template = utils.get_template_by_ip(ip, full_path, path_without_param, method)
    
    context = {
        'machineInfo': machineInfo,
        'currentTime': now.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
    }
    responseContent = template.render(context, request)
    return responseContent

def increase_firmware_version(versionInfo, machineInfo):
    if hasattr(versionInfo, 'bios'):
        versionInfo.bios = increate_one_version(versionInfo.bios, machineInfo)
    if hasattr(versionInfo, 'Manager'):
        versionInfo.Manager = increate_one_version(versionInfo.Manager, machineInfo)

def increate_one_version(versionItem, machineInfo):
    lastVersion = str(machineInfo.firmwareUpgrade.summary.currentTaskId-1)
    x = versionItem.rfind(".")
    if x >= 0:
        lastpart = versionItem[x+1:]
        lastpartInt = int(lastpart)
        return versionItem[0:x] + "." + str(lastpartInt+1)
    else:
        return versionItem[0:len(versionItem)-len(lastVersion)] + str(machineInfo.firmwareUpgrade.summary.currentTaskId)
    #if versionItem.endswith(lastVersion):
    #     return versionItem[0:len(versionItem)-len(lastVersion)] + str(machineInfo.firmwareUpgrade.summary.currentTaskId)
    # else:
    #    return versionItem + str(machineInfo.firmwareUpgrade.summary.currentTaskId)