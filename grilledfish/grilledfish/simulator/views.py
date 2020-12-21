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
import simulator.FirmwareUpgradeUtil as FirmwareUpgradeUtil
import time
import json

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
    #print("request for IP:" + machineInfo.ipStr)
    if request.method == 'GET':
        return handle_redfish_get(machineInfo, request)
    elif request.method == 'POST':        
        return handle_redfish_post(machineInfo, request)

def handle_redfish_get(machineInfo, request):
    try:
        response = handle_redfish_get_normal(machineInfo, request)
        return response
    except TemplateDoesNotExist:
        startTime = time.time()
        responseContent = FirmwareUpgradeUtil.handle_upgrade_action(machineInfo, request)
        if responseContent:
            response = HttpResponse(responseContent, content_type='application/json')
        else:
            response = HttpResponse(status=204)            
        if(machineInfo.invalidRespLength):
            response['Content-Length'] = len(response.content)+50
        
        endTime = time.time()
        utils.appendRequestPerformance(startTime, endTime)
        return response

def handle_redfish_get_normal(machineInfo, request):
    startTime = time.time()
    full_path = request.get_full_path()
    responseContent = None
    if machineInfo.cacheEnabled:
        responseContent = machineInfo.pageCache.get(full_path)
    
    if responseContent is None:
        template = None
        if machineInfo.cacheEnabled:
            template = machineInfo.templateCache.get(full_path)
        if template is None:
            template = utils.get_template(request)
            if machineInfo.cacheEnabled:
                machineInfo.templateCache[full_path] = template

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
        
        if machineInfo.cacheEnabled:
            machineInfo.pageCache[full_path] = responseContent

    response = HttpResponse(responseContent, content_type='application/json')
    if(machineInfo.invalidRespLength):
        response['Content-Length'] = len(response.content)-len(paddingContent)
    
    endTime = time.time()
    utils.appendRequestPerformance(startTime, endTime)
    return response

def handle_redfish_post(machineInfo, request):
    startTime = time.time()
    # for sel, we prepared a template even for post request, 
    # so we first try to load the template first, if not hit
    # then we switch to the normal post handler, mainly for power action
    try:
        response = handle_redfish_get(machineInfo, request)
        endTime = time.time()
        utils.appendRequestPerformance(startTime, endTime)
        return response
    except TemplateDoesNotExist:
        responseContent = PowerActionUtil.handle_power_action_post(machineInfo, request)
        if not responseContent:
            responseContent = FirmwareUpgradeUtil.handle_upgrade_action(machineInfo, request)

        if responseContent:
            response = HttpResponse(responseContent, content_type='application/json')
        else:
            response = HttpResponse(status=204)
            
        if(machineInfo.invalidRespLength):
            response['Content-Length'] = len(response.content)+50
        
        endTime = time.time()
        utils.appendRequestPerformance(startTime, endTime)
        return response


@csrf_exempt
def web_request(request):
    startTime = time.time()
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
    
    endTime = time.time()
    utils.appendRequestPerformance(startTime, endTime)
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
    
@csrf_exempt
def redfish_perf_summary(request):
    performanceSummary = utils.getPerformanceSummary()
    responseContent = "totalResTime: {0}, totalRequestCount: {1}, averageResTime:{2}, maxResTime:{3} \ntrend:{4}"
    trend = json.dumps([ob.__dict__ for ob in performanceSummary.trend])
    responseContent = responseContent.format(performanceSummary.totalResTime, performanceSummary.totalRequestCount, performanceSummary.averageResTime, performanceSummary.maxResTime, trend)    
    #responseContent = json.dumps(performanceSummary)
    response = HttpResponse(responseContent, content_type='application/json')
    return response