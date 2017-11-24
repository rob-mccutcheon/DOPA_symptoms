from configparser import ConfigParser
import nibabel as nib
import numpy as np
import sys

# Load file details
parser = ConfigParser()
parser.read(unicode("/home/k1201869/DOPA_symptoms/src/project_details.txt"))
beta_directory = parser.get('project_details', 'beta_directory')
main_directory = parser.get('project_details', 'main_directory')
roi_directory = parser.get('project_details', 'roi_directory')
voxel_maps_dir = ('%sresults/voxel_assigned_maps' % main_directory)
indiv_striatum_maps_np_dir = ('%sresults/indiv_striatum_maps/numpy' % main_directory)
indiv_striatum_maps_nii_dir = ('%sresults/indiv_striatum_maps/nifti' % main_directory)
striatum_file = parser.get('project_details', 'striatum_file')

# Load striatal mask
striatal_mask_nii = (roi_directory+striatum_file)
striatal_mask_temp = nib.load(striatal_mask_nii, mmap=False).get_data()  # disables 'memmap' special arrays
striatal_mask = 1 <= striatal_mask_temp

# Load affine from a beta file
beta_sample = (nib.load('%sBETA_Subject001_Condition001_Source001.nii' % beta_directory))
beta_aff = beta_sample.affine

# subject_id - get from queue script
subject_id = sys.argv[1]

# Mask whole brain  maps with striatal mask
whole_brain = np.load('%(1)s/voxel_assignment_%(2)s.npy' % {"1": voxel_maps_dir, "2": subject_id})
striatum_only = striatal_mask*whole_brain

# save as numpy
np.save('%(1)s/striatum_only_%(2)s.npy' % {"1": indiv_striatum_maps_np_dir, "2": subject_id}, striatum_only)

# Save as nifti
striatum_only_nii = nib.Nifti1Image(striatum_only, beta_aff)
nib.save(striatum_only_nii, '%(1)s/striatum_only_%(2)s.nii' % {"1": indiv_striatum_maps_nii_dir, "2": subject_id})
