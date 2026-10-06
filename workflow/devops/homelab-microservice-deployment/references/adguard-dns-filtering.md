# AdGuard Home — DNS Filtering & Coverage Audits

> `adguard/adguardhome` on the Panomete homelab — the LAN-wide DNS filter (server `192.168.1.121:53`).
> Client-side DNS re-pointing/diagnostics: see the `windows-pc-ops` skill.

## Container & files

| Item | Value |
|------|-------|
| Container | `adguard` — compose at `~/dns/compose.yml` (project `dns`, its own network) |
| Web UI | `127.0.0.1:7000` → container 3000; public via `adguard.panomete.com` |
| DNS | `0.0.0.0:53` and `[::]:53` (tcp+udp) |
| Config volume | `dns_adguard-conf` → `AdGuardHome.yaml` (root-owned, mode 600 — edit via `sudo tee`/`sudo python3` on the volume path or `docker exec`; back up first; recreate the container to apply) |
| Data volume | `dns_adguard-work` → `data/querylog.json`, `data/stats.db`, `data/filters/*.txt` |

## First move: prove the server blocks

```bash
# Known-ad domains — expect 0.0.0.0 / :: (blocked)
for d in doubleclick.net ads.google.com googlesyndication.com; do
  echo -n "$d -> "; dig +short +time=3 +tries=1 "$d" @192.168.1.121 | tr '\n' ' '; echo; done
# Control — expect real IPs
dig +short example.com @192.168.1.121
```

Rule volume: `docker exec adguard sh -c "cat /opt/adguardhome/work/data/filters/*.txt | grep -cvE '^#|^$|^!'"` — millions of rules is normal.
Freshness: `docker exec adguard ls -la /opt/adguardhome/work/data/filters/` — mtimes older than the update interval (default 24h) mean downloads are failing.

## "AdGuard isn't blocking anything" — audit ladder

The complaint is almost always **coverage, not the server**. In order:

1. Prove the server blocks (above).
2. Find who actually queries it: parse a query-log sample with `scripts/adguard-qlog-stats.py`. Devices missing from the log aren't using AdGuard at all.
3. Test from the problem device itself: system resolver vs direct query —
   `nslookup doubleclick.net` (system) and `nslookup doubleclick.net 192.168.1.121`.
   System returns real IPs while the direct query is blocked → the device bypasses AdGuard.
4. Inspect the device's configured DNS (Windows: `netsh interface ipv4 show dnsservers` / `ipv6`).
5. The two usual verdicts: stale/manual DNS on the device, or the IPv6 DNS leak below.

### Query-log analysis notes

- `querylog.json` is **concatenated JSON objects** — not an array, not JSONL (split on `{"T":`). It grows to hundreds of MB; a `tail -c 3000000` sample taken inside the container covers hours.
- `stats.db` is **bbolt (Go), NOT SQLite** (`sqlite3` fails with "file is not a database"). For stats use the `/control/stats` API (auth required) or parse the query log.
- Per-client blocked rates of 74–100% are NORMAL on phones/TVs — ad SDKs retry blocked domains in loops. Sanity-check with a control domain instead of chasing the percentage.
- Client shapes: LAN devices show `192.168.1.x`; host/docker-side traffic appears as the docker bridge gateway (`172.18.x`).

## The IPv6 DNS bypass (the silent leak)

**Windows prefers RA/RDNSS-advertised IPv6 DNS over statically configured IPv4 DNS.** If the router advertises ISP IPv6 DNS, IPv6-capable devices resolve through the ISP — unfiltered — even when DHCP hands out the AdGuard IP.

- Detect on the device: `netsh interface ipv6 show dnsservers` — "DNS servers configured through DHCP" entries pointing at the ISP = the leak.
- Fix server-side first — AdGuard must listen on IPv6:
  - `AdGuardHome.yaml`: `dns.bind_hosts: ['0.0.0.0', '::']` (backup; root-owned file)
  - compose: add `"[::]:53:53/tcp"` + `"[::]:53:53/udp"` publishes → `docker compose up -d`
  - verify server-side: `dig +short doubleclick.net @<server-global-v6>` → `0.0.0.0`
- Then fix clients: static IPv6 DNS = the server's global IPv6 (see `windows-pc-ops`), or — LAN-wide, better — make the router hand out the homelab v6 itself (see *Router-side fix* below).

## Docker IPv6 publishing + UFW — why v6 :53 times out from the LAN

For `[::]:53` on an **IPv4-only container**, Docker falls back to the userland `docker-proxy` (v6→v4 cannot be DNAT'd). Userland-proxy traffic terminates on the **host INPUT chain**, so UFW's default-deny applies. IPv4 published ports work because Docker's DNAT rules bypass UFW.

Symptoms: `ss -tlnp` shows `[::]:53` listening; the server itself can query its own global v6 (loopback path); LAN clients time out (`Test-NetConnection <v6> -Port 53` fails).

Fix (firewall is user-managed — hand over the commands, don't apply unasked):

```bash
sudo ufw allow from <LAN-IPv6-prefix>::/64 to any port 53 proto udp comment 'LAN DNS v6'
sudo ufw allow from <LAN-IPv6-prefix>::/64 to any port 53 proto tcp comment 'LAN DNS v6'
```

Scope to the LAN /64 — an `[::]:53` listener without it is an open-resolver risk whenever the router firewall lets unsolicited v6 through.

## Router-side fix — make the router hand out the homelab DNS (Huawei ONT / AIS)

Per-device fixes (static v6 DNS, UFW) only cover devices you touch. The LAN-wide fix lives in the ONT's IPv6 page — **DHCPv6 Server Configuration** (IPv6 LAN section). The user applies router changes themselves: hand over exact field values, then verify server-side once they say done.

- **"DNS Source on the LAN Side"** — `WAN port` / "DNS agent" (both = relay the ISP's DNS) → **`Static configuration`**.
- **"Preferred DNS (IPv6)"** = primary → the homelab server's global v6 (on this server: `2405:9800:b500:9736:692:26ff:fe01:ecaf`).
- **"Spare DNS (IPv6)"** = secondary → blank for strictest (on failure devices fall back to the DHCPv4 AdGuard — still filtered), or `2606:4700:4700::1111` for an availability net (small unfiltered-race caveat). Current state: spare = Cloudflare.
- Leave **Enable Route Advertisement** + **Enable DHCPv6 Server** CHECKED — they deliver the DNS. Devices pick it up on reconnect / next refresh.

Vault walkthrough to reuse: `home-lab/essential_component/router-dns-setup.md`.

### Verify server-side — never trust the router UI alone

1. **Decode what the router actually hands out.** tcpdump decodes the DHCPv6 DNS option (23) in clear text:

   ```bash
   sudo tcpdump -i <iface> -vvv -n "udp port 546 or udp port 547"          # live
   sudo tcpdump -r file.pcap -vvv -n "udp port 546 or udp port 547"        # from a capture
   # expect: ... (DNS-server 2405:9800:...:ecaf 2606:4700:4700::1111)
   ```

   DHCPv6 is periodic and any LAN client's exchange counts (the server's own systemd-networkd client solicits too). **A short capture may contain no RA at all — don't require one; the DHCPv6 exchange is the dependable probe.** To grep a saved pcap's hex for an address, convert to tcpdump hexdump form (hextets zero-padded, space-separated): `2405:9800:b500:9736:692:26ff:fe01:ecaf` → `2405 9800 b500 9736 0692 26ff fe01 ecaf`.
2. **Prove devices use it.** List unique IPv6 sources querying DNS:

   ```bash
   sudo tcpdump -i <iface> -n -q "ip6 and udp port 53" | awk '{print $3}' | sed 's/\.[0-9]*$//' | sort -u
   ip -6 neigh show dev <iface>       # map addresses -> MACs -> devices
   ```

   A source with no static DNS config querying the homelab's v6 can only have learned it from the router → change propagated. (v6-originated queries surface in AdGuard's log as the docker gateway `172.18.x` — don't expect device IPs there.)
3. Ready-made: `scripts/verify-router-dns.sh <iface> <expected-v6> [seconds]` — captures DHCPv6/RA/DNS, decodes, greps, and prints the device-source list.

### Maintenance

- The homelab global v6 is EUI-64 on a **dynamic ISP prefix**: if the ISP renumbers, update (1) router Preferred DNS, (2) the UFW v6 rule, (3) any static client v6 DNS. Devices fall back to the v4 AdGuard meanwhile — still filtered.
- Devices can still bypass by design: hardcoded resolvers, Android Private DNS, browser DoH/Secure DNS.

## Config facts worth knowing

- `filtering_enabled: true` + `protection_enabled: true`; custom rules live in `user_rules` — if the user expected custom blocks and the list is empty, they were never added / are gone.
- Upstreams: two DoH entries (Quad9 + Cloudflare) — a single upstream is a LAN-wide SPOF.
- DHCP is disabled in AdGuard — the router does DHCP and hands out `192.168.1.121`.
- The **"No Google" filter list is enabled** — `www.google.com` resolves to `0.0.0.0` intentionally. Don't "fix" it; confirm intent before touching it.
