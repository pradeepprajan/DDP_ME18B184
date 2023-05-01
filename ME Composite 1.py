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
    numSpheres = 10
    for num in range(0,numSpheres):
        oX = random.uniform(-3,3)
        oY = random.uniform(-3,3)
        oZ = random.uniform(-3,3)
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
        body2.name = "Particulate"+str(num)
