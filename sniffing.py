from scapy.all import sniff, Dot11
from collections import Counter

mac_counter = Counter()

def packet_handler(pkt):
    if pkt.haslayer(Dot11):
        mac = pkt.addr2
        if mac:
            mac_counter[mac] += 1

def start_sniffing(interface="wlan0mon"):
    sniff(iface=interface, prn=packet_handler, store=0)

def get_mac_counts():
    return dict(mac_counter)