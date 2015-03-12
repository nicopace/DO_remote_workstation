import os
import sys

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

my_droplet = s.Droplet.get(droplet_name)

my_droplet.destroy()
my_droplet.wait_till_done()
