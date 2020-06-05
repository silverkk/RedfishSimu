import sys
import xml.etree.ElementTree as ET 
import json

def load_gf_config(gf_simu_config_path):
    with open(gf_simu_config_path) as json_file:
        data = json.load(json_file)
        return data
def create_ipmi_range(machineInfo):
    if 'ipmiNodeType' in machineInfo:
        Range = ET.Element("Range")
        NodeType = ET.Element("NodeType")
        NodeType.text = machineInfo['ipmiNodeType']
        Range.append(NodeType)

        StartIP = ET.Element("StartIP")
        StartIP.text = machineInfo['startIp']
        Range.append(StartIP)

        EndIP = ET.Element("EndIP")
        EndIP.text = machineInfo['endIp']
        Range.append(EndIP)

        fwVersion = machineInfo['fwVersion'].split('.')
        FwMajorVersion = ET.Element("FwMajorVersion")
        FwMajorVersion.text = fwVersion[0]
        Range.append(FwMajorVersion)

        FwMinorVersion = ET.Element("FwMinorVersion")
        FwMinorVersion.text = fwVersion[1]
        Range.append(FwMinorVersion)

        Setting = ET.Element("Setting")
        Setting.text = machineInfo['ipmiSetting']
        Range.append(Setting)

        genIpmiFruSetting = machineInfo['genIpmiFruSetting'] if 'genIpmiFruSetting' in machineInfo else False
        if genIpmiFruSetting:
            manufacturer = ET.Element("FruManufacturer")
            manufacturer.text = machineInfo['vendor']
            Range.append(manufacturer)
            
            productName = ET.Element("FruProductName")
            productName.text = machineInfo['model']
            Range.append(productName)

        return Range
    else:
        return None
    
    

def gen_ipmi_config(gf_simu_config_path, ipmi_simu_config_path, dest_ipmi_simu_config):
    gf_config = load_gf_config(gf_simu_config_path)
    tree = ET.parse(ipmi_simu_config_path) 
  
    # get root element 
    root = tree.getroot() 
  
    serverMode = root.findall('General/ServerMode')
    serverMode[0].text = "MultiMode"

    ipNumber = root.findall('MultiMode/IpNumber')
    ipNumber[0].text = str(gf_config['ipNumber'])

    startIP = root.findall('MultiMode/StartIP')
    startIP[0].text = str(gf_config['startIP'])

    multiMode = root.find('MultiMode')
    for range in multiMode.findall('Range'):
        multiMode.remove(range)

    for machineInfo in gf_config['machines']:
        range = create_ipmi_range(machineInfo)
        if range is not None:
            multiMode.append(range)
            #pass
            
    
    tree.write(dest_ipmi_simu_config)

arguments = len(sys.argv) - 1
if arguments < 3:
    print ("invalid arguments")
else :
    gf_simu_config_path = sys.argv[1]
    ipmi_simu_config_template = sys.argv[2]
    dest_ipmi_simu_config = sys.argv[3]
    gen_ipmi_config(gf_simu_config_path, ipmi_simu_config_template, dest_ipmi_simu_config)
