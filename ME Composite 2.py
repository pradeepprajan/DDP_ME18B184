#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback, random,math

def run(context):
    app = adsk.core.Application.get()
    design = app.activeProduct

    # get the root component of the active design
    rootComp = design.rootComponent
    
    # create a new sketch on the xz plane
    sketches = rootComp.sketches
    xzPlane = rootComp.xZConstructionPlane
    sketch = sketches.add(xzPlane)

    # draw a rectangle
    rectangles = sketch.sketchCurves.sketchLines
    centerPoint = adsk.core.Point3D.create(0,0,-5)
    cornerPoint = adsk.core.Point3D.create(5,5,-5)
    rectangle = rectangles.addCenterPointRectangle(centerPoint,cornerPoint)

    # extrusion
    profile = sketch.profiles.item(0)
    extrudes = rootComp.features.extrudeFeatures
    distance = adsk.core.ValueInput.createByReal(10)
    extrude1 = extrudes.addSimple(profile,distance,adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    body1 = extrude1.bodies.item(0)
    body1.name = "host_matrix"

    # sphere
    values = [-2.692,-1.399,0.674,-0.665,0.971,1.151,1.096,-1.781,1.262,2.163,0.276,0.659,0.350,-1.064,1.336,-0.677,2.422,0.166,-1.663,-0.677,-2.682,0.267,1.689,0.000,-0.024,0.157,1.161,0.301,0.156,0.503]
    for i in range(1,11):
        oX = values[3*(i-1)]/10
        oY = values[3*(i-1)+1]/10
        oZ = values[3*(i-1)+2]/10
        radius = 0.4
        origin2 = adsk.core.Point3D.create(oX,oY,oZ)
        xyPlane = rootComp.xYConstructionPlane
        sketch2 = sketches.add(xyPlane)
        circles = sketch2.sketchCurves.sketchCircles
        circle = circles.addByCenterRadius(origin2,radius)
        lines = sketch2.sketchCurves.sketchLines
        axisLine = lines.addByTwoPoints(adsk.core.Point3D.create((oX-radius),oY,oZ),adsk.core.Point3D.create((oX+radius),oY,oZ))
        prof = sketch2.profiles.item(0)
        revolves = rootComp.features.revolveFeatures
        angle = adsk.core.ValueInput.createByReal(2*math.pi)
        revCut = revolves.createInput(prof,axisLine,adsk.fusion.FeatureOperations.CutFeatureOperation)
        revCut.setAngleExtent(False,angle)
        sphere = revolves.add(revCut)
        revInputNewBody = revolves.createInput(prof,axisLine,adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        revInputNewBody.setAngleExtent(False,angle)
        sphere2 = revolves.add(revInputNewBody)
        body2 = sphere2.bodies.item(0)
        body2.name = "Particulate"+str(i)
