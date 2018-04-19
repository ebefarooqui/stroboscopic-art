import rhinoscriptsyntax as rs
import math
from os import listdir
from os.path import isfile, join


input_directory = '/Users/ebefarooqui/Desktop/Stroboscopic-Project/Inputs/Walking Isabel/walking-isabel-AI/'
output_directory = '/Users/ebefarooqui/Desktop/'
#input_directory = '/Users/cortensinger/cs294-119/Stroboscopic-Project/Inputs/Walking Isabel/walking-isabel-AI/'
only_files = [f for f in listdir(input_directory) if isfile(join(input_directory, f))]

def modify_input (filename):

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
    piped = rs.AddPipe(closed_curve,0,0.4)[0]

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
    

    rect = rs.AddRectangle(rs.WorldXYPlane(), abs(maxX - minX), 3.0)
    rs.MoveObject(rect, [minX, minY - 3.0, minZ])
    rs.AddPipe(rect,0,0.4)
    rs.DeleteObject(closed_curve)
    rs.DeleteObject(rect)

    export_string = '!_Export ' + '"' + str(output_directory + filename) + '"'
    rs.Command(export_string)


def main():
    modify_input(only_files[0])

if __name__ == "__main__":
    main()