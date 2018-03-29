import Rhino
import scriptcontext
import System.Guid

def AddCircle():
    center = Rhino.Geometry.Point3d(0, 0, 0)
    radius = 10.0
    center1 = Rhino.Geometry.Point3d(1, 1, 20)
    c = Rhino.Geometry.Circle(center, radius)
    d = Rhino.Geometry.Circle(center1, radius)
    if scriptcontext.doc.Objects.AddCircle(c)!=System.Guid.Empty:
        scriptcontext.doc.Views.Redraw()
        return Rhino.Commands.Result.Success
    return Rhino.Commands.Result.Failure

if __name__=="__main__":
    AddCircle()