# -*- coding: utf-8 -*-
"""
Minimal DHCP server for isolated direct-cable lab deployment.

⚠️  WARNING: 仅用于隔离的直连实验网络（电脑 ↔ 单台设备网线直连）。
   不要在校园网、公司网、家庭 LAN 或已有 DHCP Server 的网络中运行，
   否则会影响其他设备的网络获取。

Usage:
    python dhcp_server.py --server-ip 192.168.53.100 --offer-ip 192.168.53.117 \
        --subnet 255.255.255.0 --lease 600
"""
import argparse
import socket
import struct
import time

def build_option(code, data):
    return bytes([code, len(data)]) + data

def build_offer_packet(request, msg_type, server_ip, offer_ip, subnet, lease):
    # parse client MAC (chaddr) from request
    if len(request) >= 28:
        chaddr = request[28:44]
    else:
        chaddr = b"\x00" * 16
    xid = request[4:8]
    flags = request[10:12]
    yiaddr = socket.inet_aton(offer_ip)
    siaddr = socket.inet_aton("0.0.0.0")
    giaddr = b"\x00\x00\x00\x00"
    # BOOTP header
    header = b"\x02"          # op BOOTREPLY
    header += b"\x01\x06\x00" # htype eth, hlen 6, hops 0
    header += xid
    header += b"\x00\x00"     # secs
    header += flags
    header += b"\x00\x00\x00\x00"  # ciaddr
    header += yiaddr
    header += siaddr
    header += giaddr
    header += chaddr
    header += b"\x00" * 192   # sname(64)+file(128)
    # magic cookie
    cookie = b"\x63\x82\x53\x63"
    opts = bytes([msg_type, 1, 1])                     # 53: DHCP message type (1 byte: 2=OFFER,5=ACK)
    opts += build_option(54, socket.inet_aton(server_ip))  # server id
    opts += build_option(51, struct.pack("!I", lease))     # lease time
    opts += build_option(1, socket.inet_aton(subnet))      # subnet mask
    opts += build_option(3, socket.inet_aton(server_ip))   # router = our ip
    opts += b"\xff"                                      # end
    return header + cookie + opts

def parse_options(payload):
    """Return dict of option code -> value bytes from a DHCP payload."""
    cookie_idx = payload.find(b"\x63\x82\x53\x63")
    if cookie_idx < 0:
        return {}
    i = cookie_idx + 4
    opts = {}
    while i < len(payload):
        code = payload[i]
        if code == 0:
            i += 1
            continue
        if code == 255:
            break
        if i + 2 > len(payload):
            break
        ln = payload[i + 1]
        if i + 2 + ln > len(payload):
            break
        opts[code] = payload[i + 2:i + 2 + ln]
        i += 2 + ln
    return opts

def main():
    ap = argparse.ArgumentParser(description="Isolated-lab DHCP server (do NOT use on normal LAN)")
    ap.add_argument("--server-ip", required=True, help="this machine's static IP on the isolated link")
    ap.add_argument("--offer-ip", required=True, help="IP to hand the single client")
    ap.add_argument("--subnet", default="255.255.255.0")
    ap.add_argument("--lease", type=int, default=600)
    ap.add_argument("--timeout", type=int, default=180, help="seconds to run before exit")
    a = ap.parse_args()

    print("DHCP server starting on %s -> offers %s" % (a.server_ip, a.offer_ip), flush=True)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind((a.server_ip, 67))
    s.settimeout(2)
    start = time.time()
    while time.time() - start < a.timeout:
        try:
            data, addr = s.recvfrom(4096)
        except socket.timeout:
            continue
        if len(data) < 240:
            continue
        opts = parse_options(data)
        mtype = opts.get(53, b"\x00")[0] if 53 in opts else 0
        if mtype == 1:
            print("[DISCOVER] from %s -> OFFER %s" % (addr[0], a.offer_ip), flush=True)
            s.sendto(build_offer_packet(data, 2, a.server_ip, a.offer_ip, a.subnet, a.lease),
                     ("255.255.255.255", 68))
        elif mtype == 3:
            print("[REQUEST] from %s -> ACK %s" % (addr[0], a.offer_ip), flush=True)
            s.sendto(build_offer_packet(data, 5, a.server_ip, a.offer_ip, a.subnet, a.lease),
                     ("255.255.255.255", 68))
            print("CLIENT_ASSIGNED=%s" % a.offer_ip, flush=True)
    print("DHCP server stopped after %ds." % a.timeout, flush=True)

if __name__ == "__main__":
    main()
