import platform, subprocess, psutil # type: ignore

# l'aquise des informations SE
def get_os_info():
    try:
        os_info = platform.system()  
        os_version = platform.version()  
        return os_info, os_version
    except Exception as e:
        print(f"Error getting OS info: {e}")
        return "Unknown", "Unknown"

# l'aquise des peripheriques connecte selon l'os
def get_peripherals(dict, os_info):
    try:
        if os_info == "Windows":
            import wmi   # type: ignore

            c = wmi.WMI()

            printers = [printer.Name for printer in c.Win32_Printer()]
            monitors = [monitor.Name for monitor in c.Win32_DesktopMonitor()]
            keyboards = [kbd.Name for kbd in c.Win32_Keyboard()]
            mice = [mouse.Name for mouse in c.Win32_PointingDevice()]

            dict['Printers'] = ', '.join(printers) if printers else 'None'
            dict['Monitors'] = ', '.join(monitors) if monitors else 'None'
            dict['Keyboards'] = ', '.join(keyboards) if keyboards else 'None'
            dict['Mice'] = ', '.join(mice) if mice else 'None'

        elif os_info == "Linux":
            
            try:
                usb_devices = subprocess.check_output("lsusb", universal_newlines=True).strip().split('\n')
                input_devices = subprocess.check_output("xinput list", universal_newlines=True, shell=True).strip().split('\n')
                
                usb_devices_list = ''
                for device in usb_devices:
                    usb_devices_list += ' -' + device + '\n'
                dict['USB Devices'] = usb_devices_list
                
                input_devices_list = ''
                for device in input_devices:
                    input_devices_list += ' -' + device + '\n'

                dict['Input Devices (Keyboards and Mice)'] = input_devices_list

            except subprocess.CalledProcessError as e:
                print(f"Error running subprocess command: {e}")
            except Exception as e:
                print(f"Unexpected error while getting Linux peripherals: {e}")

        elif os_info == "Darwin":
            
            try:
                printers = subprocess.check_output("lpstat -p", universal_newlines=True).strip().split('\n')
                monitors = subprocess.check_output("system_profiler SPDisplaysDataType", universal_newlines=True).strip()
                input_devices = subprocess.check_output("system_profiler SPUSBDataType", universal_newlines=True).strip()

                dict['Printers'] = ', '.join(printers) if printers else 'None'
                dict['Monitors'] = monitors if monitors else "None"
                dict["\nUSB Devices (including input devices)"] = input_devices if input_devices else "None"
            
            except subprocess.CalledProcessError as e:
                print(f"Error retrieving peripherals for macOS: {e}")
            except Exception as e:
                print(f"Unexpected error while getting macOS peripherals: {e}")

    except Exception as e:
        print(f"Error while fetching peripherals for {os_info}: {e}")

#l'aquise du pourcentage batterie
def get_battery_percentage():
    try:
        battery = psutil.sensors_battery()
        if battery:
            return battery.percent
        else:
            return "Battery information not available."
    except Exception as e:
        print(f"Error getting battery information: {e}")
        return "Error retrieving battery info."

# l'aquise des informations systeme
def get_system_info(dict):
    try:
        
        brand = platform.uname().node  

        
        os_info, os_version = get_os_info()

        
        cpu_brand = platform.processor()  
        cpu_cores = psutil.cpu_count(logical=True)  
        cpu_capacity = f"{psutil.cpu_freq().max:.2f} MHz"  

        
        memory = psutil.virtual_memory()
        memory_size = f"{memory.total / (1024 ** 3):.2f} GB"  

        
        partitions = []
        for partition in psutil.disk_partitions():
            partitions.append(partition.device)
        
        dict['Operating System'] = os_info
        dict['Operating System Version'] = os_version
        dict['Hostname'] = brand
        dict['CPU Brand'] = cpu_brand
        dict['CPU Cores'] = str(cpu_cores)
        dict['Max CPU Capacity'] = cpu_capacity
        dict['Memory Size'] = memory_size
        dict['Disc Partitions'] = f"Disc partitions: {', '.join(partitions) if partitions else 'None'}"
        
        get_peripherals(dict, os_info)

        dict['Battery'] = get_battery_percentage()

        return dict

    except Exception as e:
        print(f"Error retrieving system information: {e}")
        return {}