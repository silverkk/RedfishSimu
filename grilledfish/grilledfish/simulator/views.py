import os
from datetime import datetime
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.template import loader, TemplateDoesNotExist

import simulator.utils as utils
import simulator.PowerActionUtil as PowerActionUtil

@csrf_exempt
def index(request):
    template = loader.get_template('simulator/index.html')
    context = {
        'name': 'grilledfish',
    }
    return HttpResponse(template.render(context, request), content_type='application/json')

@csrf_exempt
def redfish_v1(request):
    machineInfo = utils.get_machine_info(request)
    if request.method == 'GET':
        return handle_redfish_get(machineInfo, request)
    elif request.method == 'POST':        
        return handle_redfish_post(machineInfo, request)

def handle_redfish_get(machineInfo, request):
    template = utils.get_template(request)
    now = datetime.now()
    context = {
        'machineInfo': machineInfo,
        'currentTime': now.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
        'sel': utils.calc_sel_list(machineInfo, request)
    }
    responseContent = template.render(context, request)
    paddingContent = "This is the the padding text that simulator added to the reponse, simulate some supermicro server's strange behavior"
    if(machineInfo.invalidRespLength):
        responseContent = responseContent + paddingContent
    response = HttpResponse(responseContent, content_type='application/json')
    if(machineInfo.invalidRespLength):
        response['Content-Length'] = len(response.content)-len(paddingContent)
    return response

def handle_redfish_post(machineInfo, request):
    # for sel, we prepared a template even for post request, 
    # so we first try to load the template first, if not hit
    # then we switch to the normal post handler, mainly for power action
    try:
        return handle_redfish_get(machineInfo, request)
    except TemplateDoesNotExist:
        responseContent = PowerActionUtil.handle_power_action_post(machineInfo, request)
        if responseContent:
            response = HttpResponse(responseContent, content_type='application/json')
        else:
            response = HttpResponse(status=204)

        if(machineInfo.invalidRespLength):
            response['Content-Length'] = len(response.content)+50
        return response


@csrf_exempt
def web_request(request):
    machineInfo = utils.get_machine_info(request)
    template = utils.get_template(request)
    now = datetime.now()
    context = {
        'machineInfo': machineInfo,
        'currentTime': now.strftime('%Y-%m-%dT%H:%M:%S+08:00'),
        'sel': utils.calc_sel_list(machineInfo, request)
    }
    responseContent = template.render(context, request)
    paddingContent = "This is the the padding text that simulator added to the reponse, simulate some supermicro server's strange behavior"
    if(machineInfo.invalidRespLength):
        responseContent = responseContent + paddingContent

    response = HttpResponse(responseContent, content_type='application/json')
    if(machineInfo.invalidRespLength):
        response['Content-Length'] = len(response.content)-len(paddingContent)
    return response

# the request is like:
# {
#    "system":"OK",
#    "raid": "OK"
# }
@csrf_exempt
def redfish_health_control(request):
    if request.method == 'GET':
        return HttpResponse('{only POST allowed}', content_type='application/json')
    elif request.method == 'POST':
        utils.update_machine_health(request)
        return HttpResponse('{OK}', content_type='application/json')
    

    