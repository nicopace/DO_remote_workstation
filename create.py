import sys
import os
import logging

import skiff

snapshotname = ''

try:
    s = skiff.rig(os.environ['DO_KEY'])
except KeyError:
    print('Environment variable DO_KEY not defined.'
          ' You can get your DigitalOcean key go to'
          ' https://cloud.digitalocean.com/settings/applications '
          'and to Pesonal Access Tokens.')
    sys.exit(1)

snapshots = filter(lambda i: not i.public, s.Image.all())
keys = s.Key.all()
key = keys[0]

try:
    thesnapshot = next((s for s in snapshots if s.name == snapshotname))
except StopIteration:
    logging.warning('using default snapshot')
    thesnapshot = snapshots[0]

my_droplet = s.Droplet.create(name='workstation',
                              region='nyc3',
                              size='512mb',
                              image=thesnapshot.id,
                              ssh_keys=[key]
                              )

# wait until droplet is created
my_droplet.wait_till_done()
# refresh network information
my_droplet = my_droplet.refresh()
my_droplet = my_droplet.reload()

print 'root@'+my_droplet.v4[0].ip_address
