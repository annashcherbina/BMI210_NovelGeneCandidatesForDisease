import reactome_tools as rt
import numpy as np
import pandas as pd

c = rt.get_cursor()

hcmGenes = np.loadtxt('../data/hcm_definitive.txt', str)
locations = []
for gene in hcmGenes:
    c.execute('select location from GO_cellular_component where genes like \'%s\';'%(gene))
    locations.extend([row[0] for row in c.fetchall()])
locations = pd.Series(locations)
print locations.value_counts()
