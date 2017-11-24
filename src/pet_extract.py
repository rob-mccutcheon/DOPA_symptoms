from configparser import ConfigParser
import nibabel as nib
import numpy as np
import sys
import os

parser = ConfigParser()
# If running locally the path: '/Users/robmcc/mnt/droplet/home/k1201869/DOPA_symptoms/src/project_details.txt'
# Also amend project_details.txt file depending on where you are running
# If running on the NaN: '/home/k1201869/DOPA_symptoms/src/project_details.txt'

# parser.read('/Users/robmcc/mnt/droplet/home/k1201869/DOPA_symptoms/src/project_details.txt')
parser.read('/home/k1201869/DOPA_symptoms/src/project_details.txt')

main_directory = parser.get('project_details', 'main_directory')
beta_directory = parser.get('project_details', 'beta_directory')
striatum_maps_dir = ('%sresults/indiv_striatum_maps' % main_directory)
pet_maps_dir = ('%sdata/ki_maps' % main_directory)
num_networks = int(parser.get('project_details', 'num_networks'))
pet_csv_path = ('%sresults/pet_network_kis/pet_network_kis.csv' % main_directory)

# Get subject id from queue script
subject_id = sys.argv[1]

# Load PET beta_map
pet_filename = os.listdir('%(1)s/%(2)s/' % {"1": pet_maps_dir, "2": subject_id})
pet_map_nii = nib.load('%(1)s/%(2)s/%(3)s' % {"1": pet_maps_dir, "2": subject_id, "3": pet_filename[0]})
pet_map = np.array(pet_map_nii.get_data())

# Load striatal voxel_assignments
striatal_map = np.load('%(1)s/numpy/striatum_only_%(2)s.npy' % {"1": striatum_maps_dir, "2": subject_id})

# Mean ki for each networks
# Array to store mean ki for each network
network_kis = np.zeros([2, num_networks])
network_kis[0, :] = range(1, num_networks+1)

for network in range(0, num_networks-1):
    # Mask pet map for each network (nb - TRUE means the value is masked)
    mask = striatal_map != network
    masked_pet_map = np.ma.masked_array(pet_map, mask)
    # Calculate mean ki of voxels within the mask
    network_kis[1, network] = masked_pet_map.mean(axis=None)

# Open csv and append row,  first column is subject ID
# Data to write
save_to_csv = np.column_stack([[int(subject_id)], [network_kis[1, :]]])

# Open the file in append mode
pet_csv = file(pet_csv_path, 'a')
np.savetxt(pet_csv, save_to_csv, delimiter=",")
pet_csv.close()
