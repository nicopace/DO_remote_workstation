import os
import sys
import logging

import skiff

try:
    s = skiff.rig(os.environ['DO_KEY'])
except KeyError:
    print('Environment variable DO_KEY not defined.'
          ' You can get your DigitalOcean key go to'
          ' https://cloud.digitalocean.com/settings/applications '
          'and to Pesonal Access Tokens.')
    sys.exit(1)

snapshotname = 'workstation'
droplet_name = 'workstation'

snapshots = filter(lambda i: not i.public, s.Image.all())

my_droplet = s.Droplet.get(droplet_name)

if my_droplet:
    thesnapshot = None
    try:
        thesnapshot = next((s for s in snapshots if s.name == snapshotname))
    except:
        logging.debug('There is no image to destroy')

    if thesnapshot:
        thesnapshot.delete()

    try:
        my_droplet.shutdown()
        my_droplet.wait_till_done()
    except:
        logging.debug('already powered off.')

    my_droplet.snapshot(snapshotname)
    my_droplet.wait_till_done()
else:
    logging.error('there is no image to work with')
