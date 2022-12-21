import os
import json
import urllib.parse
from django.template import loader
from simulator.simumodel.model import model, global_model
from django.template import loader, TemplateDoesNotExist

def get_request_ip(request):
    host = request.get_host()
    if host.startswith("["):
        host_ip = host[host.index('[')+1:host.index(']')]
    else:
        host_ip = host.split(':')[0]
    return host_ip

def get_machine_info(request):
    host_ip = get_request_ip(request)
    return get_machine_info_by_ip(host_ip)

def get_machine_info_by_ip(ip):
    machineInfo = global_model.getMachineInfo(ip)
    return machineInfo

def get_template_path(machineInfo, path, method, safeCharactor=''):
    if machineInfo.model:
        template_prefix = 'simulator/' + machineInfo.vendor.name + '/' +  machineInfo.model + '/' + machineInfo.fwVersion
    else:
        template_prefix = 'simulator/' + machineInfo.vendor.name + '/' + machineInfo.fwVersion
    
    if machineInfo.flatMode:
        if safeCharactor:
            template_path = os.path.join(template_prefix, urllib.parse.quote(path, safe=safeCharactor))
        else:
            template_path = os.path.join(template_prefix, urllib.parse.quote(path, safe=''))
        if method:
            template_path = template_path + '.' + method
        template_path = template_path + '.json'
    else:
        if path.startswith("/redfish/"):
            path = path[9:] # ignore the started "/redfish/"

        template_path = os.path.join(template_prefix, path)
        if template_path[-1] == '/':
            if method:
                template_path = os.path.join(template_path, method + '.index.json')
            else:
                template_path = os.path.join(template_path, 'index.json')

    return template_path

def to_lower_encoding(path):
    path = path.replace("%2F", "%2f")
    path = path.replace("%3F", "%3f")
    path = path.replace("%3D", "%3d")
    path = path.replace("%3A", "%3a")
    return path

def calc_correct_template_path(machineInfo, path, httpMethod):
    cwd = os.getcwd()
    template_path = get_template_path(machineInfo, path, None)
    if os.path.exists(os.path.join("simulator/templates", template_path)):
        return template_path

    template_path = to_lower_encoding(template_path)
    if os.path.exists(os.path.join("simulator/templates", template_path)):
        return template_path

    template_path = get_template_path(machineInfo, path, None, '%')
    if os.path.exists(os.path.join("simulator/templates", template_path)):
        return template_path
        
    template_path = to_lower_encoding(template_path)
    if os.path.exists(os.path.join("simulator/templates", template_path)):
        return template_path

    template_path = get_template_path(machineInfo, path, httpMethod)
    if os.path.exists(os.path.join("simulator/templates", template_path)):
        return template_path

    template_path = to_lower_encoding(template_path)
    if os.path.exists(os.path.join("simulator/templates", template_path)):
        return template_path

    if path[-1] == '/':
        path = path[:-1]
    else:
        path = path + '/'
    template_path = get_template_path(machineInfo, path, None)
    if os.path.exists(os.path.join("simulator/templates", template_path)):
        return template_path

    template_path = to_lower_encoding(template_path)
    if os.path.exists(os.path.join("simulator/templates", template_path)):
        return template_path

    template_path = get_template_path(machineInfo, path, httpMethod)
    if os.path.exists(os.path.join("simulator/templates", template_path)):
        return template_path

    template_path = to_lower_encoding(template_path)
    if os.path.exists(os.path.join("simulator/templates", template_path)):
        return template_path

    return template_path

def get_template(request):
    ip = get_request_ip(request)
    full_path = request.get_full_path()
    path_without_param = request.path
    method = request.method.lower()
    #machineInfo = get_machine_info(request)
    return get_template_by_ip(ip, full_path, path_without_param, method)

def get_template_by_ip(ip, full_path, path_without_param, method):
    machineInfo = global_model.getMachineInfo(ip)    
    template_path = calc_correct_template_path(machineInfo, full_path, method)
    try:
        template = loader.get_template(template_path)
        return template
    except IsADirectoryError:
        template_path = os.path.join(template_path, 'index.json')
    except TemplateDoesNotExist:
        
        template_path = calc_correct_template_path(machineInfo, path_without_param, method)

    template = loader.get_template(template_path)
    return template

def update_machine_health(request):
    body_unicode = request.body.decode()
    request_json = json.loads(body_unicode)
    host_ip = get_request_ip(request)
    global_model.updateHealthInfo(host_ip, request_json)
    #if ''

def calc_sel_list(machine, request):
    sel_logList = None
    sel_nextSkip = None
    if(machine.sel):
        if(getattr(machine.sel, "paging", None)):
            skip = request.GET.get(machine.sel.skiptoken)
            if(skip):
                skip = int(skip)
                if(machine.sel.skipType == "Items"):
                    start_id = skip
                    end_id = skip+machine.sel.logItemPerPage
                    next_skip = skip+machine.sel.logItemPerPage
                else:
                    start_id = (skip-1)*machine.sel.logItemPerPage
                    end_id = skip*machine.sel.logItemPerPage
                    next_skip = skip+1

                sel_logList = machine.sel.logList[start_id:end_id]
                if(end_id >= len(machine.sel.logList)):
                    sel_nextSkip = None
                else:
                    sel_nextSkip = next_skip
            else:
                sel_logList = machine.sel.logList[0:machine.sel.logItemPerPage]
                if(machine.sel.logItemPerPage >= len(machine.sel.logList)):
                    sel_nextSkip = None
                else:
                    if(machine.sel.skipType == "Items"):
                        sel_nextSkip = machine.sel.logItemPerPage                        
                    else:
                        sel_nextSkip = 2
        else:
            sel_logList = machine.sel.logList
    
    return {
        'logList':sel_logList,
        'nextSkip':sel_nextSkip
    }

def appendRequestPerformance(startTime, endTime):
    global_model.appendRequestPerformance(startTime, endTime)

def getPerformanceSummary():
    return global_model.getPerformanceSummary()

def getFimwareUpgradeTasksSummary(ipStr):
    machineInfo = global_model.getMachineInfo(ipStr)
    return machineInfo.firmwareUpgrade.summary