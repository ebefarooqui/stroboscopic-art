import rhinoscriptsyntax as rs
import math
import csv
from os import listdir
from os.path import isfile, join

input_directory = '/Users/ebefarooqui/Desktop/Stroboscopic-Project/Inputs/Walking Isabel/walking-isabel-AI/'
output_directory = '/Users/ebefarooqui/Desktop/Stroboscopic-Project/Output/'
only_files = [f for f in listdir(input_directory) if isfile(join(input_directory, f))]
box_width = 0
box_height = 1.5
pipe_diameter = 0.4
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
def F (x, total_frames):
   # Straight Line
   return x

   # Sin Wave
   #return 8 * math.sin(math.pi * 2 * x / total_frames)

def calculateWidth (files):
    
    global box_width
    
    for filename in files:
        join_string = str(input_directory + filename)
        combined_string = '!_Import ' + '"' + join_string + '"'
        rs.Command(combined_string)

        objs = rs.LastCreatedObjects(select=False)[0]
    
        bounding_pts = rs.BoundingBox([objs], view_or_plane=rs.WorldXYPlane())

        maxX = 0
        minX = 0
        minY = 0
        minZ = 0
        for pt in bounding_pts:
            if pt[0] < minX:
                minX = pt[0]
            if pt[0] > maxX:
                maxX = pt[0]
            if pt[1] < minY:
                minY = pt[1]
            if pt[2] < minZ:
                minZ = pt[2]

        if abs(maxX - minX) > box_width:
            box_width = abs(maxX - minX)

        rs.DeleteObject(objs)

# Imports frame from filename, prepares it for 3D printing,
# and then exports it as an .stl file.
# 
# Args:
#   filename: string representing filename
#   diameter: d of circle used to pipe figure
def output_frame (filename):

    global box_height
    global box_width
    global pipe_diameter

    # Import object from file 
    join_string = str(input_directory + filename)
    combined_string = '!_Import ' + '"' + join_string + '"'
    rs.Command(combined_string)

    # Get all objects imported 
    objs = rs.LastCreatedObjects(select=False)[0]
    
    # Close curve
    closed_curve = rs.CloseCurve(objs, 0.5)
    rs.DeleteObject(objs)
    
    # Rebuild curve to create smoother shape
    rs.RebuildCurve(closed_curve, 3, 100)

    # Pipe figure with radius of 0.25
    piped = rs.AddPipe(closed_curve,0,pipe_diameter)[0]

    rs.MoveObject(piped, [0,0,0])

    bounding_pts = rs.BoundingBox([piped], view_or_plane=rs.WorldXYPlane())

    maxX = 0
    minX = 0
    minY = 0
    minZ = 0
    for pt in bounding_pts:
        if pt[0] < minX:
            minX = pt[0]
        if pt[0] > maxX:
            maxX = pt[0]
        if pt[1] < minY:
            minY = pt[1]
        if pt[2] < minZ:
            minZ = pt[2]
    
    epsilon = 0.5
    center = 0
    one = [center - (box_width / 2) - box_height,minY-epsilon,-1 * pipe_diameter]
    two = [center - (box_width / 2) - box_height,minY-epsilon,pipe_diameter]
    three = [center + (box_width / 2) + box_height,minY-epsilon,pipe_diameter]
    four = [center + (box_width / 2) + box_height,minY-epsilon,-1 * pipe_diameter]
    five = [center - (box_width / 2) - box_height,minY+epsilon,-1 * pipe_diameter]
    six = [center - (box_width / 2) - box_height,minY+epsilon,pipe_diameter]
    seven = [center + (box_width / 2) + box_height,minY+epsilon,pipe_diameter]
    eight = [center + (box_width / 2) + box_height,minY+epsilon,-1 * pipe_diameter]
    
    bowx = rs.AddBox([two, three, four, one, six, seven, eight, five])


    # rect = rs.AddRectangle(rs.WorldXYPlane(), box_width, box_height)
    #rect = rs.AddRectangle(rs.WorldXYPlane(), box_width, box_height)
    # Potentially use solid but smaller in height rect
    # rs.MoveObject(rect, [minX, minY - 3.0, minZ + pipe_diameter])
    # piped_rect = rs.AddPipe(rect,0,pipe_diameter)
    rs.DeleteObject(closed_curve)
    # rs.DeleteObject(rect)
    rs.SelectObjects([piped, bowx])
    
    rs.Command("_-Export "+output_directory+filename+'.stl'+" _Enter _Tolerance=.001  _Enter")

def read_placements(filename):
    data = []
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile)
        for row in readCSV:
            data.append((int(row[0]), int(row[1]), int(row[2])))
    return data

def create_slits (data, width, height):
    for i in range(0, len(data)):
        rect = rs.AddRectangle(rs.WorldXYPlane(), width, height)
        rs.MoveObject(rect, [data[i][0], data[i][2], 0])
    
    export_string = '!_Export ' + '"' + str(output_directory + 'placements') + '"'
    rs.Command(export_string)

def place_slits ():
    
    global box_height
    global box_width
    global output_directory
    
    locs = read_placements(output_directory + 'placement.csv')
    print(box_width)
    # create_slits(locs, box_width * 1.875, box_height * 1.875)
    create_slits(locs, 38.6, 1.26)

def write_CSV(filename, data):
    global output_directory
    myFile = open(output_directory + filename, 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(data)

def create_frames():
    num_frames = len(only_files)
    num_loops = 4
    step_forward = 10
    placement_data = []

    try:
        for i in range(0, num_loops):
            for x in range(0, num_frames):
                curr_move_forward = step_forward * ((num_frames - 1) * i + x)
                curr_move_side = F(curr_move_forward, num_frames)
                m = move_group(import_group(only_files[x]), [curr_move_side, 0, curr_move_forward])
                output_frame(only_files[x])
                placement_data.append((curr_move_side, 0, curr_move_forward))
                if m == False:
                    print("Move failed")
    except ValueError as err:
        print(err.args)
    write_CSV('placement.csv',placement_data)
    rs.DeleteObjects(rs.AllObjects(select=True))

def main():
    calculateWidth(only_files)
    create_frames()
    place_slits()

if __name__ == "__main__":
    main()