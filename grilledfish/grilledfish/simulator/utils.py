import os
import json
import urllib.parse
from django.template import loader
from simulator.simumodel.model import model, global_model
from django.template import loader, TemplateDoesNotExist

def get_request_ip(request):
    host = request.get_host()
    host_ip = host.split(':')[0]
    return host_ip

def get_machine_info(request):
    host_ip = get_request_ip(request)
    machineInfo = global_model.getMachineInfo(host_ip)
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
    machineInfo = get_machine_info(request)
    full_path = request.get_full_path()
    template_path = calc_correct_template_path(machineInfo, full_path, request.method.lower())
    try:
        template = loader.get_template(template_path)
        return template
    except IsADirectoryError:
        template_path = os.path.join(template_path, 'index.json')
    except TemplateDoesNotExist:
        path_without_param = request.path
        template_path = calc_correct_template_path(machineInfo, path_without_param, request.method.lower())

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
        if(machine.sel.paging):
            skip = request.GET.get(machine.sel.skiptoken)
            if(skip):
                skip = int(skip)
                if(machine.sel.skipType == "Items"):
                    start_id = skip
                    end_id = skip+machine.sel.logItemPerPage
                    next_skip = skip+machine.sel.logItemPerPage
                else:
                    start_id = skip*machine.sel.logItemPerPage
                    end_id = (skip+1)*machine.sel.logItemPerPage
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
                    sel_nextSkip = machine.sel.logItemPerPage                
        else:
            sel_logList = machine.sel.logList
    
    return {
        'logList':sel_logList,
        'nextSkip':sel_nextSkip
    }

    

