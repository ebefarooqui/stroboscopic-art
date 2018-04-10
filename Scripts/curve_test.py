import rhinoscriptsyntax as rs
curve1 = rs.GetObject("Select first curve to compare", rs.filter.curve)
curve2 = rs.GetObject("Select second curve to compare", rs.filter.curve)
if rs.CurveDirectionsMatch(curve1, curve2):
    print "Curves are in the same direction"
else:
    print "Curve are not in the same direction"