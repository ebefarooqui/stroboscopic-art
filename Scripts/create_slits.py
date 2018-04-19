import csv
import rhinoscriptsyntax as rs

output_directory = '/Users/ebefarooqui/Desktop/'

def readCSV(filename):
    placements = []
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile)
        for row in readCSV:
            placements.append((int(row[0]), int(row[1]), int(row[2])))
    return placements

def placeSlits(data, width, height):
    for i in range(0, len(data)):
        rect = rs.AddRectangle(rs.WorldXYPlane(), height, width)
        rs.MoveObject(rect, [data[i][0], data[i][2], 0])
    
    #export_string = '!_Export ' + '"' + str(output_directory + 'placements') + '"'
    #rs.Command(export_string)


def main():
    locs = readCSV(output_directory + 'placement.csv')
    placeSlits(locs, 0.25, 3.0)

if __name__ == "__main__":
    main()