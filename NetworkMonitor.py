import psutil 

class NetworkMonitor:

    def __init__(self):
        pass

    
    def network_info(self):
        interface = []
        addressX = []
        netmask = []
        Broadcast = []
        if_addrs = psutil.net_if_addrs()
        i = 0
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    addressX[i] = (f"IP Adress: {address.address}")
                    netmask[i] = (f"Netmask: {address.netmask}")
                    Broadcast[i] =(f"Broadcast IP: {address.broadcast}")
                    interface[i] = (f"Interface: {interface_name} ")
                    i = i+1
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    addressX[i] = (f"MAC Adress: {address.address}")
                    netmask[i] = (f"Netmask: {address.netmask}")
                    Broadcast[i] =(f"Broadcast MAC: {address.broadcast}")
                    interface[i] = (f"Interface: {interface_name} ")
                    i = i+1
        return {
            "interface": interface,
            "adress": addressX,
            "netmask": netmask,
            "broadcast": Broadcast
        }
                   