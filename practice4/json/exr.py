import json

with open('sample-data.json') as f: 
    data = json.load(f)

output = []
output.append("Interface Status")
output.append("=" * 80)
output.append(f"{'DN':<50} {'Description':<20}  {'Speed':>7}  {'MTU':>6}")
output.append(f"{'-'*50} {'-'*20}  {'-'*7}  {'-'*6}")

for item in data['imdata']:
    attrs = item['l1PhysIf']['attributes']
    dn    = attrs.get('dn', '')
    descr = attrs.get('descr', '')
    speed = attrs.get('speed', '')
    mtu   = attrs.get('mtu', '')
    output.append(f"{dn:<50} {descr:<20}  {speed:>7}  {mtu:>6} ")


result = '\n'.join(output)
print(result)


with open('interface_status.txt', 'w') as f:
    f.write(result + '\n')