
STORE = {}

import os
from importlib import import_module

dirname = os.path.dirname(os.path.abspath(__file__)) + '/effects'

for f in os.listdir(dirname):
    if f[0] != '_' and os.path.isfile("%s/%s" % (dirname, f)) and f[-3:] == ".py":
        name = f.replace('.py','')
        effect_module = import_module("effects."+name)
        STORE[name] = {
            'metadata': effect_module._metadata,
            'class': effect_module.Effect
        }

print(STORE)