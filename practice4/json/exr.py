import json

with open('sample-data.json') as f:
    data = json.load(f)

output = []
output.append("Interface Status")
output.append("=" * 80)
output.append(f"{'DN':<50} {'Description':<20}  {'Speed':>7}  {'MTU':>6}") #doing format like example output
output.append(f"{'-'*50} {'-'*20}  {'-'*7}  {'-'*6}")

for item in data['imdata']:
    attrs = item['l1PhysIf']['attributes'] #attributes ишинен деректерді алу
    dn    = attrs.get('dn', '') #dn іздеу
    descr = attrs.get('descr', '') #description іздеу
    speed = attrs.get('speed', '') #speed іздеу
    mtu   = attrs.get('mtu', '') #mtu іздеу
    output.append(f"{dn:<50} {descr:<20}  {speed:>7}  {mtu:>6} ") #шыққан нәрселерді форматқа келитіру


result = '\n'.join(output)
print(result)
