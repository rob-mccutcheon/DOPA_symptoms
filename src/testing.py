import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import nibabel as nib
import os
matplotlib.pyplot.ion() #makes

cd '/Users/robmcc/mnt/droplet/home/k1201869/DOPA_symptoms/results/conn_analysis/conn_dopasymptoms/results/firstlevel/ANALYSIS_01'
cd '/Users/robmcc/mnt/droplet/home/k1201869/DOPA_symptoms/results/voxel_assigned_maps'
ls

a = (nib.load('BETA_Subject001_Condition001_Source001.nii'))
a_np = np.array(a.get_data())
b = np.load('voxel_assignment_001.npy')

a_np
a_np.shape


a_np[41,43,40]
a2 = a.get_data()
a2.shape
aff = a.affine


c = nib.Nifti1Image(b, aff)

nib.save(c, 'striat_map_nif.nii')

plt.imshow(a2[:, :, 40])
plt.imshow(b[:, :, 37])
plt.show()



pwd
ls
