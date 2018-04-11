import rhinoscriptsyntax as rs

def RunCommand():
  crvids = rs.GetObjects(message="select curves to loft", filter=rs.filter.curve, minimum_count=2)
  if not crvids: return

  rs.AddLoftSrf(object_ids=crvids, loft_type = 2, simplify_method = 1, value = 250) #0 = normal

if __name__ == "__main__":
  RunCommand()
