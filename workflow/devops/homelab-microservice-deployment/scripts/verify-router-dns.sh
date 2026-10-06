#!/usr/bin/env bash
# verify-router-dns.sh — confirm which IPv6 DNS a router actually hands out on a LAN.
#
# Run ON a LAN host that receives the router's RA/DHCPv6 (the homelab server works):
#   sudo bash verify-router-dns.sh <iface> <expected-dns-ipv6> [duration_s]
#   e.g. sudo bash verify-router-dns.sh enp2s0 2405:9800:b500:9736:692:26ff:fe01:ecaf 100
#
# Steps:
#   1. Captures DHCPv6 (546/547), router advertisements (icmp6 type 134) and DNS (udp 53).
#   2. Decodes DHCPv6 DNS options — tcpdump prints option 23 as "(DNS-server <addr> ...)".
#   3. Greps the raw packets for the expected address (tcpdump hexdump form).
#   4. Lists LAN devices sending DNS over IPv6 (learned from the router if not static).
#
# PASS -> the router advertises the expected IPv6 DNS.
# NOTE -> DHCPv6/RA are periodic; "not found in window" is NOT proof of failure.
#         Re-run longer, or judge by the device-source list (step 4).
# Requires: sudo, tcpdump, python3. On some ISPs / routers, RAs are rare or
# suppressed — rely on the DHCPv6 exchange, not on catching an RA.
set -u
IFACE="${1:?usage: verify-router-dns.sh <iface> <expected-dns-ipv6> [duration_s]}"
EXPECT="${2:?usage: verify-router-dns.sh <iface> <expected-dns-ipv6> [duration_s]}"
DUR="${3:-100}"
PCAP="/tmp/router-dns-verify.$$.pcap"
FILTER="(udp port 546 or udp port 547) or (icmp6 and ip6[40] == 134) or (ip6 and udp port 53)"

# tcpdump hexdump form of the address: hextets zero-padded, space-separated
PAT="$(python3 -c 'import ipaddress,sys; h=ipaddress.IPv6Address(sys.argv[1]).exploded.replace(":",""); print(" ".join(h[i:i+4] for i in range(0,32,4)))' "$EXPECT")"

echo "== capturing ${DUR}s on ${IFACE} (DHCPv6 / RA / DNS) =="
sudo rm -f "$PCAP"
sudo tcpdump -i "$IFACE" -w "$PCAP" "$FILTER" 2>/dev/null &
TPID=$!
sleep "$DUR"
sudo kill "$TPID" 2>/dev/null
wait "$TPID" 2>/dev/null || true

if [ ! -s "$PCAP" ]; then
  echo "!! no packets captured — check the interface name and that traffic exists in the window."
  exit 1
fi

echo
echo "== DHCPv6 DNS options seen =="
sudo tcpdump -r "$PCAP" -vvv -n 2>/dev/null | grep -i "DNS-server" || echo "(none in window — DHCPv6 is periodic; try a longer run)"

echo
echo "== raw-packet match for ${EXPECT} =="
if sudo tcpdump -r "$PCAP" -X 2>/dev/null | grep -i "$PAT" >/dev/null; then
  echo "FOUND (hex: $PAT)"
  FOUND=1
else
  echo "not found in window (hex pattern: $PAT)"
  FOUND=0
fi

echo
echo "== IPv6 DNS query sources (deduped) =="
sudo tcpdump -r "$PCAP" -n -q "ip6 and udp port 53" 2>/dev/null \
  | awk '{print $3}' | sed 's/\.[0-9]*$//' | sort -u
echo "(map to devices: ip -6 neigh show dev ${IFACE})"

echo
if [ "$FOUND" = 1 ] || sudo tcpdump -r "$PCAP" -vvv -n 2>/dev/null | grep -i "DNS-server" | grep -qF "$EXPECT"; then
  echo "PASS: the router currently hands out ${EXPECT} as IPv6 DNS."
  echo "NOTE: a fallback/spare DNS may also be listed — read the full DNS-server line above."
  rm -f "$PCAP"
  exit 0
else
  echo "NO DIRECT PROOF this window. DHCPv6/RA are periodic — re-run with a longer duration."
  echo "Alternative verdict: a device in the source list above with no static v6 DNS can only"
  echo "have learned the homelab DNS from the router."
  rm -f "$PCAP"
  exit 1
fi
