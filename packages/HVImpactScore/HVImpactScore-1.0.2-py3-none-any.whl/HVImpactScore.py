# Import dependencies
import copy
import cv2
import math
from multiprocessing import Pool
import numpy as np
import random
from scipy.optimize import minimize

# Class to store a list of SPH data nodes. Typically the full set of imported SPH data
# from a single simulation
class SPHData:
    
    # Class constructor
    def __init__(self):

        self.sph_nodes = []
        self.node_dict = {}

    # Private function to import SPH data from a single axis text file
    def _read_node_data(self,
                        filepath,
                        header_lines_trim):

        try:
            file = open(filepath, "r")
            raw_data = file.read()
            data = raw_data.splitlines()[header_lines_trim:]
            file.close()
            return data
        
        except:
            print("Error in SPHData._read_node_data: Unable to read " + filepath)

    # Function to import SPH data from text files
    def load_data(self,
                  x_fpath,
                  y_fpath,
                  z_fpath,
                  header_lines_trim,
                  node_diameter,
                  node_density):
         
        # Read in data from the files provided.
        xpos_data = self._read_node_data(x_fpath, header_lines_trim)
        ypos_data = self._read_node_data(y_fpath, header_lines_trim)
        zpos_data = self._read_node_data(z_fpath, header_lines_trim)

        # Iterate through list and create new node objects for each item and append to list
        for i in range(0, len(xpos_data)):

            xpos_line = xpos_data[i].split()
            ypos_line = ypos_data[i].split()
            zpos_line = zpos_data[i].split()

            node_number = int(xpos_line[0])
            node_x_loc = float(xpos_line[1])
            node_y_loc = float(ypos_line[1])
            node_z_loc = float(zpos_line[1])

            new_sph_node = SPHNode(node_number,
                               node_x_loc,
                               node_y_loc,
                               node_z_loc,
                               node_diameter,
                               node_density)
            
            self.sph_nodes.append(new_sph_node)

    # Transform the imported node data via rotation about the z-axis
    def transform_data_zrot(self, z_rot_rads):
            
        for i in range(0, len(self.sph_nodes)):
             
            node = self.sph_nodes[i]

            # Transform position w/ rotation about z axis
            rot_x_pos = node.pos[0]*math.cos(z_rot_rads) - node.pos[1]*math.sin(z_rot_rads)
            rot_y_pos = node.pos[0]*math.sin(z_rot_rads) + node.pos[1]*math.cos(z_rot_rads)
            rot_z_pos = node.pos[2]

            node.pos = np.array([rot_x_pos, rot_y_pos, rot_z_pos])

    # Function to radially duplicate and distribute nodes about the z-axis
    def dist_data_zrot(self,
                       rot_qty,
                       angle_min_rads,
                       angle_max_rads):

        rotation_list = []
        for i in range(0, rot_qty):
            rotation_list.append(random.uniform(angle_min_rads, angle_max_rads))
        
        SPHData.transform_data_zrot(self, rotation_list[0])
        SPHData._add_data_zrot(self, rotation_list[1:])
        
    # Private function used for SPH node radial distribution
    def _add_data_zrot(self,
                       z_rotation_list):

        new_node_list = []
        for rotations in z_rotation_list:
            for i in range(0, len(self.sph_nodes)):
                
                node = self.sph_nodes[i]
                new_sph_node = SPHNode(node.node_number,
                                       node.pos[0],
                                       node.pos[1],
                                       node.pos[2],
                                       node.diameter,
                                       node.density)
                
                # Perform rotation of new node
                rot_x_pos = node.pos[0]*math.cos(rotations) - node.pos[1]*math.sin(rotations)
                rot_y_pos = node.pos[0]*math.sin(rotations) + node.pos[1]*math.cos(rotations)
                rot_z_pos = node.pos[2]

                new_sph_node.pos = np.array([rot_x_pos, rot_y_pos, rot_z_pos])
                new_node_list.append(new_sph_node)

        self.sph_nodes = np.append(self.sph_nodes, new_node_list)

    # Function that rotates the data about the x axis
    def transform_data_xrot(self, x_rot_rads):

        for node in self.sph_nodes:

            # Transform position w/ rotation about x axis
            rot_x_pos = node.pos[0]
            rot_y_pos = node.pos[1]*math.cos(x_rot_rads) - node.pos[2]*math.sin(x_rot_rads)
            rot_z_pos = node.pos[1]*math.sin(x_rot_rads) + node.pos[2]*math.cos(x_rot_rads)
            
            node.pos = np.array([rot_x_pos, rot_y_pos, rot_z_pos])
    
    # Function that flips the data about the z plane (or x & y axes)
    def flip_data_zplane(self):
          
        # Iterate through the SPH data and flip about the z axis
        for node in self.sph_nodes:
              
            # Flip position about z plane
            node.pos = np.array([node.pos[0], node.pos[1], -1.0 * node.pos[2]])
           
    # Function that expands axisymmetric simulation data about the x plane
    def expand_sym_about_x_plane(self):
        
        # Create duplicate node list
        new_node_list = copy.deepcopy(self.sph_nodes)

        # Perform x plane expansion by flipping over the x plane for new nodes
        for node in new_node_list:
            node.pos[0] = -1.0 * node.pos[0]
            
        self.sph_nodes = np.append(self.sph_nodes, new_node_list)
            
    # Function that expands axisymmetric simulation data about the y plane
    def expand_sym_about_y_plane(self):
    
        # Create duplicate node list
        new_node_list = copy.deepcopy(self.sph_nodes)

        # Perform x plane expansion by flipping over the x plane for new nodes
        for node in new_node_list:
            node.pos[1] = -1.0 * node.pos[1]
            
        self.sph_nodes = np.append(self.sph_nodes, new_node_list)

# Class to store the information from a single SPH node    
class SPHNode:

    # Class constructor
    def __init__(self,
                 node_number,
                 x,
                 y,
                 z,
                 diameter,
                 density):
        
        # Initialize state
        self.node_number = node_number
        self.pos = np.array([x, y, z])
        self.diameter = diameter
        self.density = density
        self.mass = self.density*(4/3)*math.pi*math.pow(self.diameter / 2.0, 3)
        self.group_hash = None

    # Function to assign the hash key for node during image generation
    def set_group_hash(self, hash_value):

        self.group_hash = hash_value

class ExpImageProcessing:

    @staticmethod
    def load_exp_image(filepath):

        image = cv2.imread(filepath)
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_array = np.array(image_gray)
        return image_array.astype(np.float64)

    @staticmethod
    def normalize_image(image):

        normalized_image = np.zeros(np.shape(image))

        darkest_val = image.min()
        lightest_val = image.max()

        for row in range(0, np.shape(image)[0]):
            for col in range(0, np.shape(image)[1]):
                normalized_image[row, col] = 255.0 * (image[row, col] - darkest_val) / (lightest_val - darkest_val)

        return normalized_image

    @staticmethod
    def threshold_image(image, threshold_value):

        thresh_image = np.zeros(np.shape(image))

        for row in range(0, np.shape(image)[0]):
            for col in range(0, np.shape(image)[1]):

                if image[row, col] > threshold_value:
                    thresh_image[row, col] = threshold_value
                else:
                    thresh_image[row, col] = image[row, col]

                thresh_image[row, col] = 255.0 * thresh_image[row, col] / threshold_value

        return thresh_image

    @staticmethod
    def threshold_image_idw(image, 
                            threshold_margin, 
                            sample_area_array):
           
        def _inverse_distance_weighting(distances, values, power):
            
            for i in range(0, len(distances)):
                if distances[i] <= 0.0:
                    distances[i] = 0.00001

            numerator = np.sum(values / (distances ** power))
            weights = np.sum(1 / (distances ** power))
            interpolated_value = numerator / weights
            
            return interpolated_value
        
        # Create new, blank image
        thresh_image = np.zeros(np.shape(image))

        # Average each sample area to get background intensity
        bg_int_list = []
        bg_loc_list = []
        
        # Create location and intensity list for inverse distance weighted interpolation
        for i in range(0, len(sample_area_array)):
            sample_area = sample_area_array[i]
            loc_y_center = (sample_area[0][0] + sample_area[1][0]) / 2.0
            loc_x_center = (sample_area[0][1] + sample_area[1][1]) / 2.0
            bg_loc_list.append([loc_y_center, loc_x_center])
            
            area_intensity = np.average(image[sample_area[0][0]:sample_area[1][0],
                                              sample_area[0][1]:sample_area[1][1]])
            bg_int_list.append(area_intensity)

        # Subtract interpolated intensity from each pixel
        img_height = np.shape(image)[0]
        img_width = np.shape(image)[1]
        
        for row in range(0, img_height):
            for col in range(0, img_width):
                
                distances = []
                for point in range(0, len(bg_loc_list)):
                    distances.append(math.sqrt(math.pow((bg_loc_list[point][0] - row), 2) + math.pow((bg_loc_list[point][1] - col), 2)))

                sub_mag = (255.0 - _inverse_distance_weighting(np.array(distances), np.array(bg_int_list), 1)) + threshold_margin

                if image[row, col] + sub_mag > 255.0:
                    thresh_image[row, col] = 255.0
                else:
                    thresh_image[row, col] = image[row, col] + sub_mag

        return ExpImageProcessing.normalize_image(thresh_image)

    @staticmethod
    def threshold_image_multi_idw(image,
                                  partition_loc,
                                  threshold_margin,
                                  sample_area_array1,
                                  sample_area_array2):
        
        # Break up image into two parts
        image_left_section = image[:, 0:partition_loc]
        image_right_section = image[:, partition_loc:]

        # Transform the second set of sample array coordinates to local, partitioned space
        for coords in sample_area_array2:      
            coords[0][1] = coords[0][1] - partition_loc
            coords[1][1] = coords[1][1] - partition_loc

        # Perform thresholding
        thresh_left_image = ExpImageProcessing.threshold_image_idw(image_left_section,
                                                                   threshold_margin,
                                                                   sample_area_array1)
        
        thresh_right_image = ExpImageProcessing.threshold_image_idw(image_right_section,
                                                                    threshold_margin,
                                                                    sample_area_array2)

        # Restore the second set of sample array coordinates to global space
        for coords in sample_area_array2:      
            coords[0][1] = coords[0][1] + partition_loc
            coords[1][1] = coords[1][1] + partition_loc

        # Combine and return final image.
        return np.hstack((thresh_left_image, thresh_right_image))

    @staticmethod
    def apply_unit_light_absorbtion(image, abs_coef):

        laser_image = np.zeros(np.shape(image))

        for row in range(0, np.shape(image)[0]):
            for col in range(0, np.shape(image)[1]):
                laser_image[row, col] = math.exp(-1.0 * abs_coef * image[row, col])

        return laser_image
    
    @staticmethod 
    def find_abs_coefficient(density_image,
                             exp_image,
                             range_max,
                             range_min):
        
        if range_min == 0.0:
            range_min = 1.0e-10
        
        def opt_wrapper(exposure, density_img, exp_img, scoring_method):
            image = ExpImageProcessing.apply_unit_light_absorbtion(density_img, exposure)
            image_norm = ExpImageProcessing.normalize_image(image)
            return -scoring_method(image_norm, exp_img)
        
        def image_mass_diff(analysis_image, experimental_image):
        
            img_height = np.shape(analysis_image)[0]
            img_width = np.shape(analysis_image)[1]

            total_error = 0
            for row in range(0, img_height):
                for col in range(0, img_width):
                    total_error = total_error + (analysis_image[row, col] - experimental_image[row, col])

            return -1.0*abs(total_error)
        
        init_val = (range_max + range_min) / 2.0
        opt_abs = minimize(opt_wrapper, 
                           init_val,
                           args=(density_image, exp_image, image_mass_diff),
                           bounds=[(range_min, range_max)],
                           tol=1e-7).x
        
        return opt_abs
    
class SPHDataProcessing:

    @staticmethod
    def bspline_kernel(pix_1, pix_2, node_1, node_2, h_dist):

        euc_dist = math.sqrt((pix_1 - node_1)**2 + (pix_2 - node_2)**2)
        veta = euc_dist / h_dist

        if (veta <= 1.0):
            return (1 / (math.pi * h_dist**3)) * (1 - (3 / 2) * veta**2 + (3 / 4) * veta**3)
        elif (veta > 1.0 and veta <= 2.0):
            return (1 / (math.pi * h_dist**3)) * (1 / 4) * (2 - veta)**3
        else:
            return 0

    @staticmethod
    def sph_data_to_dens_map_single(sph_data,
                                     kernel,
                                     kernel_radius,
                                     px_size,
                                     img_min_x,
                                     img_max_x,
                                     img_min_y,
                                     img_max_y,
                                     verbose=False):
        
        # Partition the nodes into pixels for faster rendering
        SPHDataProcessing._partition_nodes(sph_data, px_size)      
        
        # Determine the number of adjacent pixels to look in for rastering
        adj_px = math.ceil(2.0 * kernel_radius / px_size)
        
        # Initialize the mass_map
        dens_map = np.zeros((img_max_y - img_min_y, img_max_x - img_min_x))

        # Iterate over all the pixels
        for row in range(img_min_y, img_max_y):
            if verbose is True:
                print("Processing row " + str(row))
            for col in range(img_min_x, img_max_x):

                # Calculate the hash value of the current pixel
                c_pixel_hash_num = (row, col)

                # Calculate the 2D physical position of the pixel
                c_pixel_coord_1 = row * px_size # row direction
                c_pixel_coord_2 = col * px_size # column direction
                
                # Survey around pixel to determine value using kernel
                for s_row in range(c_pixel_hash_num[0] - adj_px, c_pixel_hash_num[0] + adj_px + 1):
                    for s_col in range(c_pixel_hash_num[1] - adj_px, c_pixel_hash_num[1] + adj_px + 1):
                        
                        s_hash = str((s_row, s_col))
                        
                        if s_hash in sph_data.node_dict:
                            for node in sph_data.node_dict[s_hash]:
                                dens_map[row - img_min_y, col - img_min_x] += node.mass*kernel(c_pixel_coord_1,
                                                                                                c_pixel_coord_2,
                                                                                                node.pos[1],
                                                                                                node.pos[2],
                                                                                                kernel_radius)

        return dens_map

    @staticmethod
    def sph_data_to_dens_map_multi_rot(sph_data,
                                       kernel,
                                       kernel_radius,
                                       px_size,
                                       img_min_x,
                                       img_max_x,
                                       img_min_y,
                                       img_max_y,
                                       adl_rotation_qty,
                                       rotation_min,
                                       rotation_max,
                                       x_angle,
                                       verbose=False):

        # Create rotated versions of analysis data and append as datapacks
        dens_map_datapack = []
        for i in range(0, adl_rotation_qty + 1):
            angle = random.uniform(rotation_min, rotation_max)
            data_pack = {"data": sph_data,
                         "kernel": kernel,
                         "kernel_radius": kernel_radius,
                         "px_size": px_size,
                         "img_min_x": img_min_x,
                         "img_max_x": img_max_x,
                         "img_min_y": img_min_y,
                         "img_max_y": img_max_y,
                         "z_angle": angle,
                         "x_angle": x_angle,
                         "verbose": verbose,
                         "is_copy": True}
            dens_map_datapack.append(data_pack)

        # Process data
        with Pool() as pool:
            result = pool.map(SPHDataProcessing._dens_map_parallel, dens_map_datapack)

        # Sum the density from all rotations and divide by the number of rotations to normalize
        img_height = np.shape(result[0])[0]
        img_width = np.shape(result[0])[1]
        sum_density_map = np.zeros([img_height, img_width])
        for row in range(0, img_height):
            for col in range(0, img_width):
                for sample in range(0, len(result)):
                    sum_density_map[row, col] = sum_density_map[row, col] + result[sample][row, col]

        norm_density_map = sum_density_map / (adl_rotation_qty + 1)

        return norm_density_map
        
    @staticmethod
    def _get_node_hash(px_size, pos_1, pos_2):

        return str(SPHDataProcessing._get_node_hash_numbers(px_size, pos_1, pos_2))
    
    @staticmethod
    def _get_node_hash_numbers(px_size, pos_1, pos_2):

        hash_coord_1 = round(pos_1/px_size)
        hash_coord_2 = round(pos_2/px_size)
        return (hash_coord_1, hash_coord_2)
    
    @staticmethod
    def _partition_nodes(sph_data, px_size):
        
        for node in sph_data.sph_nodes:
            hash_coord_1 = 0
            hash_coord_2 = 0
            hash_key = None

            (hash_coord_1, hash_coord_2) = SPHDataProcessing._get_node_hash_numbers(px_size, 
                                                                                    node.pos[1], 
                                                                                    node.pos[2])
            hash_key = SPHDataProcessing._get_node_hash(px_size, 
                                                        node.pos[1], 
                                                        node.pos[2])

            node.set_group_hash((hash_coord_1, hash_coord_2))

            if hash_key in sph_data.node_dict:
                sph_data.node_dict[hash_key].append(node)
            else:
                sph_data.node_dict[hash_key] = []
                sph_data.node_dict[hash_key].append(node)

    # Define wrapper for parallel processing
    @staticmethod
    def _dens_map_parallel(sph_data_pack):
        sph_data_copy = copy.deepcopy(sph_data_pack["data"])
        sph_data_copy.transform_data_zrot(sph_data_pack["z_angle"])
        sph_data_copy.transform_data_xrot(sph_data_pack["x_angle"])
        density_map = SPHDataProcessing.sph_data_to_dens_map_single(sph_data_copy,
                                                                    sph_data_pack["kernel"],
                                                                    sph_data_pack["kernel_radius"],
                                                                    sph_data_pack["px_size"],
                                                                    sph_data_pack["img_min_x"],
                                                                    sph_data_pack["img_max_x"],
                                                                    sph_data_pack["img_min_y"],
                                                                    sph_data_pack["img_max_y"],
                                                                    sph_data_pack["verbose"])
        return density_map
    
class scoring:

    @staticmethod
    def score_images(analysis_image,
                     experimental_image,
                     threshold):

        img_height = np.shape(analysis_image)[0]
        img_width = np.shape(analysis_image)[1]

        mse_error = 0
        limit = 255.0 - threshold
        exp_thresh_int_total = 0

        for y in range(0, img_height):
            for x in range(0, img_width):
                if analysis_image[y, x] < limit or experimental_image[y, x] < limit:
                    mse_error = mse_error + math.pow(analysis_image[y, x] - experimental_image[y, x], 2)
                    
                if experimental_image[y, x] < limit:
                    exp_thresh_int_total = exp_thresh_int_total + math.pow(255.0 - experimental_image[y, x], 2)
        
        return 1.0 - mse_error / exp_thresh_int_total