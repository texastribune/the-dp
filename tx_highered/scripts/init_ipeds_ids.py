"""
Attempt to assign as many IPED IDs to Institutions as this script can find

Requires downloading a list of institutions from http://nces.ed.gov/ipeds

"""
import sys

from nltk.metrics import edit_distance as distance

from tx_highered.models import Institution
from . import utils

filename = sys.argv[1]

reader = utils.DictReader(open(filename, 'r'))

qs = Institution.objects.filter(ipeds_id__isnull=True)
total = qs.count()
count = 0

# pass one, exact matches
maybes = []
for row in reader:
    try:
        inst = qs.get(name=row['Name'])
        inst.ipeds_id = row['UnitID']
        inst.save()
        print inst
        count += 1
        continue
    except Institution.DoesNotExist:
        pass
        # print "MISSING:", row['Name']
    maybes.append(row)
    # print row

print "Expected %s Found %s" % (total, count)


def closest(name):
    for m in maybes:
        m['distance'] = distance(Institution.get_unique_name(name), Institution.get_unique_name(m['Name']))
    ordered = sorted(maybes, key=lambda x: x['distance'])
    return ordered[0], ordered[1]['distance'] - ordered[0]['distance']

# pass two, fun stuff
qs = Institution.objects.filter(ipeds_id__isnull=True)
haves = Institution.objects.filter(ipeds_id__isnull=False).values_list('ipeds_id', flat=True)
maybes = [x for x in maybes if int(x['UnitID']) not in haves]
for inst in qs:
    guess, confidence = closest(inst.name)
    if confidence > 0:
        if guess['distance'] == 0:
            inst.ipeds_id = guess['UnitID']
            inst.save()
    print "%d +%d\t" % (guess['distance'], confidence), inst.name, "==", guess['Name']
