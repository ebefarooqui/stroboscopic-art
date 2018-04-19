import rhinoscriptsyntax as rs

def RunCommand():
  crvids = rs.GetObjects(message="select curves to loft", filter=rs.filter.curve, minimum_count=2)
  if not crvids: return

<<<<<<< HEAD
  rs.AddLoftSrf(object_ids=crvids, loft_type = 2, simplify_method = 1, value = 200) #0 = normal
=======
  rs.AddLoftSrf(object_ids=crvids, loft_type = 2, simplify_method = 1, value = 250) #0 = normal
>>>>>>> ae5693dd478301cead4f2941ffdf9fb05b19fee4

if __name__ == "__main__":
  RunCommand()
