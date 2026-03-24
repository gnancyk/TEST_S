from ping3 import ping, verbose_ping
import socket
from ..utils.powershell_scripting import execution_powershell_hote_distant
from ..utils.extraction_texte import extracteur
from ..utils.time import convert_wmi_time
import wmi
import pythoncom

def server_disponible(hostname):
    reponse = ping(hostname)
    # print(hostname, reponse)
    # if reponse is not None:
    if reponse != False:
        return 'En ligne'
        # return True
    else:
      return 'Non disponible'
        # return False
        
        
    
def verification_port_ouvert(host, port=5986):
    try:
        # Tentative de connexion au port
        with socket.create_connection((host, port), timeout=5):
            # # The code you provided does not contain any reference to a variable or function named
            # `pr`. If you could provide more context or clarify where `pr` is used in your code, I
            # would be happy to help explain its purpose or functionality.
            print(f"Le port {port} est ouvert sur {host}.")
            return True
    except (socket.timeout, socket.error):
        # print(f"Le port {port} est fermé sur {host}.")
        return False
    
    
def verification_antivirus(hostname,username,password):
    
    query = """
                Get-Service | Where-Object { $_.DisplayName -like "*McAfee*" -or $_.DisplayName -like "*Windows Defender*" -or $_.DisplayName -like "*Kaspersky Endpoint*" }   | Select-Object Status,DisplayName,PSComputerName | ConvertTo-Json
            """
                # Get-WmiObject -Namespace "root\SecurityCenter2" -Query "SELECT * FROM AntivirusProduct" 
    return execution_powershell_hote_distant(hostname,username,password,query)

# def performances_serveur(hostname,username,password):
#     pythoncom.CoInitialize()
    
#     try:
#         conn = wmi.WMI(
#             computer=hostname,
#             user=username,
#             password=password
#         )

#         # Disques
#         drives = [{
#             'DeviceID': d.DeviceID,
#             'Size(GB)': round(int(d.Size) / (1024 ** 3), 2) if d.Size else None,
#             'FreeSpace(GB)': round(int(d.FreeSpace) / (1024 ** 3), 2) if d.FreeSpace else None
#         } for d in conn.Win32_LogicalDisk(DriveType=3)]

#         # RAM
#         os = conn.Win32_OperatingSystem()[0]
#         print(os)
#         os_info = {
#             'Caption': os.Caption,
#             'LastBootUpTime': convert_wmi_time(os.LastBootUpTime),
#             'version':os.Version,
#             'OSArchitecture':os.OSArchitecture,
#             'MUILanguages':os.MUILanguages
#         }
#         ram = {
#             'TotalRAM(GB)': round(int(os.TotalVisibleMemorySize) / (1024 ** 2), 2),
#             'FreeRAM(GB)': round(int(os.FreePhysicalMemory) / (1024 ** 2), 2)
#         }

#         # CPU Info
#         cpu_info = [{
#             'Name': c.Name,
#             'Cores': c.NumberOfCores,
#             'LogicalProcessors': c.NumberOfLogicalProcessors,
#             'MaxClockSpeed': c.MaxClockSpeed
#         } for c in conn.Win32_Processor()]

#         return {
#             'Server': hostname,
#             'os_info':os_info,
#             'Drives': drives,
#             'RAM': ram,
#             'CPU': cpu_info
#         }
#     finally:
#         pythoncom.CoUninitialize() 



def performances_serveur(hostname, username, password):
    pythoncom.CoInitialize()

    try:
        conn = wmi.WMI(
            computer=hostname,
            user=username,
            password=password
        )

        # Disques
        drives = [{
            'DeviceID': d.DeviceID,
            'Size(GB)': round(int(d.Size) / (1024 ** 3), 2) if d.Size else None,
            'FreeSpace(GB)': round(int(d.FreeSpace) / (1024 ** 3), 2) if d.FreeSpace else None
        } for d in conn.Win32_LogicalDisk(DriveType=3)]

        # RAM
        os = conn.Win32_OperatingSystem()[0]
        ram = {
            'TotalRAM(GB)': round(int(os.TotalVisibleMemorySize) / (1024 ** 2), 2),
            'FreeRAM(GB)': round(int(os.FreePhysicalMemory) / (1024 ** 2), 2)
        }

        # CPU Info
        processors = conn.Win32_Processor()
        cpu_info = [{
            'Name': c.Name,
            'Cores': c.NumberOfCores,
            'LogicalProcessors': c.NumberOfLogicalProcessors,
            'MaxClockSpeed(MHz)': c.MaxClockSpeed
        } for c in processors]

        # CPU Load
        cpu_load = processors[0].LoadPercentage if processors else None

        # OS Info
        os_info = {
            'Caption': os.Caption,
            'Version': os.Version,
            'BuildNumber': os.BuildNumber,
            'Architecture': os.OSArchitecture,
            'MUILanguages':os.MUILanguages,
            'LastBootUpTime': convert_wmi_time(os.LastBootUpTime)  # Format simplifié
        }

        # Network Info
        network = [{
            'Name': n.Description,
            'MACAddress': n.MACAddress,
            'IP': n.IPAddress[0] if n.IPAddress else None
        } for n in conn.Win32_NetworkAdapterConfiguration(IPEnabled=True)]

        # Swap Info
        swap_info = [{
            'Name': v.Name,
            'AllocatedBaseSize(MB)': v.AllocatedBaseSize,
            'CurrentUsage(MB)': v.CurrentUsage
        } for v in conn.Win32_PageFileUsage()]

        # BIOS Info
        bios = conn.Win32_BIOS()[0]
        bios_info = {
            'Manufacturer': bios.Manufacturer,
            'Version': bios.SMBIOSBIOSVersion,
            'ReleaseDate': convert_wmi_time(bios.ReleaseDate)
        }

        # System Info
        system = conn.Win32_ComputerSystem()[0]
        system_info = {
            'Manufacturer': system.Manufacturer,
            'Model': system.Model,
            'Domain': system.Domain,
            'UserName': system.UserName
        }

        return {
            'Server': hostname,
            'Drives': drives,
            'RAM': ram,
            'CPU': cpu_info,
            'CPULoad(%)': cpu_load,
            'OS': os_info,
            'Network': network,
            'Swap': swap_info,
            'BIOS': bios_info,
            'System': system_info
        }

    finally:
        pythoncom.CoUninitialize()

def recuperation_os_information(server, username, password,query="systeminfo"):
    reponse_service_distance = execution_powershell_hote_distant(server, username, password,query)
    
    ## Autre methode
    #reponse_service_distance2 = execution_powershell_hote_distant(server, username, password," systeminfo | findstr /C:\"System Boot Time\" /C:\"OS Name\" /C:\"OS Version\" /C:\"System Manufacturer\" /C:\"Processor(s) Installed\" | ConvertTo-Json")
    

    if reponse_service_distance != '':
        # os_name  = reponse_service_distance[reponse_service_distance.find("OS Name:") + len("OS Name: "):reponse_service_distance.find("OS Version:")] 
        # os_version  = reponse_service_distance[reponse_service_distance.find("OS Version:") + len("OS Version:"):reponse_service_distance.find("OS Manufacturer:")]  
        os_name  = extracteur(reponse_service_distance,"OS Name:","OS Version:")
        os_version  = extracteur(reponse_service_distance,"OS Version:","OS Manufacturer:")
        dernier_redemarrage  = extracteur(reponse_service_distance,"System Boot Time:","System Manufacturer:")
        nombre_processeurs  = extracteur(reponse_service_distance,"Processor(s):","Processor(s) Installed")
        return os_name, os_version, dernier_redemarrage, nombre_processeurs
    else:
        return 'N/A', 'N/A', 'N/A', 'N/A'
        


    