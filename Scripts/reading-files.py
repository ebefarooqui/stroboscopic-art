import rhinoscriptsyntax as rs
import math
from os import listdir
from os.path import isfile, join


#input_directory = '/Users/ebefarooqui/Desktop/Stroboscopic-Project/Inputs/Walking Isabel/walking-isabel-AI/'
input_directory = '/Users/cortensinger/cs294-119/Stroboscopic-Project/Inputs/Leaping Wuliang/leaping-wuliang-AI/'
only_files = [f for f in listdir(input_directory) if isfile(join(input_directory, f))]
group_count = 0
groups = []


# Imports object from filename and groups it in Rhino
# so that all potential objects from the file
# can be modified together. 
# 
# Args:
#   filename: file to import
# Returns:
#   Name of group created (An integer number to represent the group) 
def import_group (filename):
    
    global group_count
    global groups

    # Import object from file 
    join_string = str(input_directory + filename)
    combined_string = '!_Import ' + '"' + join_string + '"'
    rs.Command(combined_string)

    # Get all objects imported 
    objs = rs.LastCreatedObjects(select=False)
    name = rs.AddGroup(str(group_count))
    if (name == None):
        raise ValueError("Creation of group failed")
    else:
        rs.AddObjectsToGroup(objs, name)
        group_count += 1
        groups.append(name)
        return name


# Moves grouped objects to point specified
# If group doesn't exist, ValueError raised
# 
# Args:
#   name: group name
#   translation: list of coordinates of a point to move to
# Returns:
#   boolean: true if entire move is successful, false otherwise
def move_group (name, translation):
    
    global groups

    if name not in groups:
        raise NameError("Group " + name + " doesn't exist")
    else:
        guids = rs.ObjectsByGroup(name)
        for obj in guids:
            moved = rs.MoveObject(obj, translation)
            if moved == None:
                return False
        return True

# Input function that defines the LATERAL movement of each frame
#
# Args:
#   x: Number representing the forward displacement of any time step
#      that should be matched to the corresponding y-value in this function
#   total_frames: Number of frames in this zoetrope
# Returns:
#   Int: Absolute lateral value to move the current frame
def F(x, total_frames):
   # Straight Line
   return x

   # Sin Wave
   #return 8 * math.sin(math.pi * 2 * x / total_frames)

def main():
    num_frames = len(only_files)
    num_loops = 4
    step_forward = 3
    #step_side = 3

    scale_factor = 3
    try:
	   for i in range(0, num_loops):
		  for x in range(0, num_frames):
			 #curr_move_side = step_side * (num_frames * i + (x + 1))
			 curr_move_forward = step_forward * ((num_frames - 1) * i + x)
			 curr_move_side = F(curr_move_forward, num_frames) 
			 m = move_group(import_group(only_files[x]), [curr_move_side, 0, curr_move_forward])
			 if m == False:
				print("Move Failed")
    except ValueError as err:
        print(err.args)

if __name__ == "__main__":
    main()


# for f in only_files:
#     join_string = str(input_directory + f)
#     combined_string = '!_Import ' + '"' + join_string + '"'
#     rs.Command(combined_string)

# join_string = str(input_directory + only_files[0])
# combined_string = '!_Import ' + '"' + join_string + '"'
# rs.Command(combined_string)
# objs = rs.AllObjects()
# name = rs.AddGroup("FirstObject")
# rs.AddObjectsToGroup(objs, 'FirstObject')
# guids = rs.ObjectsByGroup('FirstObject')
# for obj in guids:
#     rs.MoveObject(obj, [0,0,15])
