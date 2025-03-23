# Python script that processes IP addresses, performs RDAP lookups,
# and generates MikroTik-ready address-list files.

import csv
import os
from ipwhois import IPWhois
from ipwhois.exceptions import IPDefinedError
from datetime import datetime
import ipaddress
import sys

input_file = 'input_ips.txt'
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
output_csv = f'result_{timestamp}.csv'
output_rsc_networks = f'address_networks_cidr_{timestamp}.rsc'
output_rsc_asn = f'address_asn_cidr_{timestamp}.rsc'

# Check if the input file exists
if not os.path.isfile(input_file):
    print(f"❌ Error: The file '{input_file}' does not exist.")
    sys.exit(1)

csv_header = ['IP', 'ASN', 'ASN_CIDR', 'ASN_COUNTRY_CODE', 'ASN_DESCRIPTION',
              'NETWORK_NAME', 'NETWORK_CIDR', 'NETWORK_COUNTRY', 'EMAILS']

with open(input_file, 'r') as file:
    raw_ips = [line.strip() for line in file if line.strip()]

unique_ips = sorted(set(raw_ips), key=lambda ip: ipaddress.IPv4Address(ip))

print(f"Found {len(unique_ips)} unique IP addresses.")

unique_networks = set()
unique_asn_cidrs = set()

with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile, \
     open(output_rsc_networks, 'w', encoding='utf-8') as rsc_net, \
     open(output_rsc_asn, 'w', encoding='utf-8') as rsc_asn:

    writer = csv.DictWriter(csvfile, fieldnames=csv_header)
    writer.writeheader()

    rsc_net.write("/ip firewall address-list\n")
    rsc_asn.write("/ip firewall address-list\n")

    for ip in unique_ips:
        print(f"Processing IP: {ip}")
        try:
            obj = IPWhois(ip)
            res = obj.lookup_rdap()

            network_cidr = res['network'].get('cidr') if res.get('network') else None
            asn_cidr = res.get('asn_cidr')

            row = {
                'IP': ip,
                'ASN': res.get('asn'),
                'ASN_CIDR': asn_cidr,
                'ASN_COUNTRY_CODE': res.get('asn_country_code'),
                'ASN_DESCRIPTION': res.get('asn_description'),
                'NETWORK_NAME': res['network'].get('name') if res.get('network') else '',
                'NETWORK_CIDR': network_cidr,
                'NETWORK_COUNTRY': res['network'].get('country') if res.get('network') else '',
                'EMAILS': ', '.join(res['network'].get('emails', [])) if res.get('network') else ''
            }

            writer.writerow(row)

            # Handle multiple network CIDRs if present
            if network_cidr:
                for net in network_cidr.split(','):
                    net = net.strip()
                    if net and net not in unique_networks:
                        rsc_net.write(f'add address={net} list=WHOIS_NET_LIST\n')
                        unique_networks.add(net)

            # Add ASN CIDR
            if asn_cidr and asn_cidr not in unique_asn_cidrs:
                rsc_asn.write(f'add address={asn_cidr} list=WHOIS_ASN_LIST\n')
                unique_asn_cidrs.add(asn_cidr)

        except IPDefinedError:
            print(f"Private or reserved IP: {ip} — skipped")
        except Exception as e:
            print(f"Error processing {ip}: {e}")

print(f"\n✅ CSV saved to: {output_csv}")
print(f"✅ NETWORK CIDR saved to: {output_rsc_networks}")
print(f"✅ ASN CIDR saved to: {output_rsc_asn}")