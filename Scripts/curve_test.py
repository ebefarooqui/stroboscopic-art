import rhinoscriptsyntax as rs
from os import listdir
from os.path import isfile, join

input_directory = '/Users/ebefarooqui/Desktop/Stroboscopic-Project/Inputs/Walking Isabel/walking-isabel-AI/'
only_files = [f for f in listdir(input_directory) if isfile(join(input_directory, f))]
box_width = 17.53
box_height = 1.5
pipe_diameter = 0.4

def output_frame (filename):

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
    one = [center - (box_width / 2),minY-epsilon,-1 * pipe_diameter]
    two = [center - (box_width / 2),minY-epsilon,pipe_diameter]
    three = [center + (box_width / 2),minY-epsilon,pipe_diameter]
    four = [center + (box_width / 2),minY-epsilon,-1 * pipe_diameter]
    five = [center - (box_width / 2),minY+epsilon,-1 * pipe_diameter]
    six = [center - (box_width / 2),minY+epsilon,pipe_diameter]
    seven = [center + (box_width / 2),minY+epsilon,pipe_diameter]
    eight = [center + (box_width / 2),minY+epsilon,-1 * pipe_diameter]
    
    bowx = rs.AddBox([two, three, four, one, six, seven, eight, five])

    # rs.MoveObject(bowx, [])


output_frame(only_files[0])