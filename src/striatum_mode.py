from configparser import ConfigParser
import nibabel as nib
import numpy as np
import glob
from json import loads
from scipy import stats

parser = ConfigParser()
# If running locally the path: '/Users/robmcc/mnt/droplet/home/k1201869/DOPA_symptoms/src/project_details.txt'
# Also amend project_details.txt file depending on where you are running
# If running on the NaN: '/home/k1201869/DOPA_symptoms/src/project_details.txt'
parser.read('/Users/robmcc/mnt/droplet/home/k1201869/DOPA_symptoms/src/project_details.txt')
main_directory = parser.get('project_details', 'main_directory')
beta_directory = parser.get('project_details', 'beta_directory')
voxel_maps_dir = ('%sresults/voxel_assigned_maps' % main_directory)
img_dim = (loads(parser.get("project_details", "image_dimension")))
img_dim = [int(i)for i in img_dim]
xvoxels = range(0, img_dim[0])
yvoxels = range(0, img_dim[1])
zvoxels = range(0, img_dim[2])

# Load affine from a beta file
beta_sample = (nib.load('%sBETA_Subject001_Condition001_Source001.nii' % beta_directory))
beta_aff = beta_sample.affine

# all whole brain voxel assignments into a 4d array
filelist = sorted(glob.glob('%s/*.npy' % voxel_maps_dir))
partic = range(0, len(filelist)-1)
voxel_assignments = np.zeros((50, img_dim[0], img_dim[1], img_dim[2]))

# find modal value for each voxel (if a tie takes lowest value)
for i in partic:
    voxel_assignments[i, :, :, :] = np.array(np.load(filelist[i]))

voxel_mode = np.zeros((img_dim[0], img_dim[1], img_dim[2]))

for x in xvoxels:
    for y in yvoxels:
        for z in zvoxels:
            indiv_voxel = voxel_assignments[:, x, y, z]  # change to x,y,z
            voxel_mode[x, y, z] = stats.mode(indiv_voxel)[0]

# save as numpy
np.save('%(1)s/voxel_mode.npy' % {"1": voxel_maps_dir}, voxel_mode)

# Save as nifti
voxel_mode_nii = nib.Nifti1Image(voxel_mode, beta_aff)
nib.save(voxel_mode_nii, '%(1)s/voxel_mode_1.nii' % {"1": voxel_maps_dir})

# TESTING
from matplotlib import pyplot as plt
a=voxel_assignments[0,:,:,:]
plt.imshow(a[:,40,:])
plt.show()
