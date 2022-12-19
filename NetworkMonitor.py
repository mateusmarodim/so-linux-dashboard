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
        for interface_name, interface_addresses in if_addrs.items():
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    addressX.append(f"IP Adress: {address.address}")
                    netmask.append(f"Netmask: {address.netmask}")
                    Broadcast.append(f"Broadcast IP: {address.broadcast}")
                    interface.append(f"Interface: {interface_name} ")
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    addressX.append (f"MAC Adress: {address.address}")
                    netmask.append(f"Netmask: {address.netmask}")
                    Broadcast.append(f"Broadcast MAC: {address.broadcast}")
                    interface.append(f"Interface: {interface_name} ")
        return {
            "interface": interface,
            "adress": addressX,
            "netmask": netmask,
            "broadcast": Broadcast
        }
                   