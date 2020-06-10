import os
from datetime import datetime
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

import simulator.utils as utils

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
    

    