import os
import json
import urllib.parse
from django.template import loader
from simulator.simumodel.model import model, global_model
from django.template import loader, TemplateDoesNotExist
import simulator.utils as utils
from datetime import datetime

def handle_upgrade_action(machineInfo, request):
    full_path = request.get_full_path()
    if machineInfo.firmwareUpgrade:
        if full_path == machineInfo.firmwareUpgrade.action.submit_upgrade_url:
            machineInfo.firmwareUpgrade.lastTaskStartTime = datetime.now()
            if hasattr(machineInfo.firmwareUpgrade, 'currentTaskId'):
                machineInfo.firmwareUpgrade.currentTaskId = machineInfo.firmwareUpgrade.currentTaskId + 1
            else:
                machineInfo.firmwareUpgrade.currentTaskId = 1
            return load_upgrade_response(machineInfo, request)
        elif full_path.startswith(machineInfo.firmwareUpgrade.action.task_status_url):
            return load_task_status_response(machineInfo, request)
    return None

def load_upgrade_response(machineInfo, request):
    ip = utils.get_request_ip(request)
    full_path = machineInfo.firmwareUpgrade.action.submit_upgrade_response
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
    
def load_task_status_response(machineInfo, request):
    ip = utils.get_request_ip(request)
    now = datetime.now()
    timeSpan = now - machineInfo.firmwareUpgrade.lastTaskStartTime
    if timeSpan.total_seconds() > machineInfo.firmwareUpgrade.action.secondsUpgradeTakes:
        full_path = machineInfo.firmwareUpgrade.action.task_done_response
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
    