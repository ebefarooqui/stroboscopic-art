import rhinoscriptsyntax as rs
from os import listdir
from os.path import isfile, join

input_directory = '/Users/ebefarooqui/Desktop/Stroboscopic-Project/Inputs/Walking Isabel/walking-isabel-AI/'
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

def main():
    try:
       result_name = import_group(only_files[0])
       result_name1 = import_group(only_files[1])
    except ValueError as err:
        print(err.args)
    try:
        mvd = move_group(result_name, [0,0,15])
        mvd2 = move_group(result_name1, [0,0,5])
        if mvd == False or mvd2 == False:
            print("Move failed")
    except NameError as err:
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