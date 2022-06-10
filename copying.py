import shutil
import os
import pandas as pd

workDir = '/home/nielsemb/work/mounts/Bluebear_projects/background_fit'

prior_data = pd.read_csv(os.path.join(*[workDir, 'prior_data.csv']))

for i in prior_data.index:

    ID = prior_data.loc[i, 'ID']
    
    fname = os.path.join(*[workDir, 'results', ID, ID+'_samples.npz'])
    
    if os.path.exists(fname):

        for ext in ['_samples_model.png', '_prior_model.png']:
            src = os.path.join(*[workDir, 'results', ID, ID+ext])

            dst = os.path.join(*['/home/nielsemb/work/repos/Morse/images', os.path.basename(src)])
            
            if os.path.exists(dst):
                continue

            shutil.copy(src, dst)