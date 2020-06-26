import adsk.core, adsk.fusion, traceback
import math

#RoHal 2020

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Create a document.
        doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)

        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)

        # Get the root component of the active design.
        rootComp = design.rootComponent

# #  ######################################################################################################################
        sk1 = rootComp.sketches.add(rootComp.xYConstructionPlane)

# #  ######################################################################################################################
        
        n = 50                          #number of teeth

    # Film dimensions (expressed in cm); standard 8mm here
        fp = 0.381                      #frame pitch
        w1 = 0.8                        #film width
        w2 = 0.3                        #running width
        w3 = 0.7                        #flange width
        w4 = 0.091                      #distance perforation from edge
        w5 = 0.181                      #width of perforation


        sf = 0.005                      #shrinkage

        r1 = n * fp / (2 * math.pi)     #sprocket radius; film runs on this
        r2 = 0.25 - sf                  #radius of sprocket axle/shaft
        r3 = r1 + 0.0                   #flange radius; 0.0 = no flange
        w6 = 0.5                        # small flange extra width
        d1 = 0.1                        #depth of channel
        f1 = 0.5 + sf                   #recess thickness
        b1 = 0.5                        #boss protrudes this amount
        x = 0
        
        #dimensions of sprocket tooth
        spr_length = 0.100
        spr_width = 0.150
        spr_height = 0.100

        spr_ch = 0.050                  # chamfer length from corner

  
#       # Draw a line to use as the axis of revolution.
        lines = sk1.sketchCurves.sketchLines
        axis  = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(0, 1, 0))
   
        # Draw section shape of hub
        points = adsk.core.ObjectCollection.create() 
        lines = sk1.sketchCurves.sketchLines;
        line1 = lines.addByTwoPoints(adsk.core.Point3D.create(x, w1+w3+w6, r3), adsk.core.Point3D.create(x, w1+w3+w6, r1-d1-f1))
        #recess in hub#########################################################################
        line13 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(x, f1, r1-d1-f1))
        line14 = lines.addByTwoPoints(line13.endSketchPoint, adsk.core.Point3D.create(x, f1, r2+f1))
        line15 = lines.addByTwoPoints(line14.endSketchPoint, adsk.core.Point3D.create(x, w1+w3+w6+b1, r2+f1))
        line16 = lines.addByTwoPoints(line15.endSketchPoint, adsk.core.Point3D.create(x, w1+w3+w6+b1, r2))
        line2 = lines.addByTwoPoints(line16.endSketchPoint, adsk.core.Point3D.create(x, 0, r2))
        ######################################################################################
        line3 = lines.addByTwoPoints(line2.endSketchPoint, adsk.core.Point3D.create(x, 0, r1))
        line4 = lines.addByTwoPoints(line3.endSketchPoint, adsk.core.Point3D.create(x, w2+w6, r1))
        line5 = lines.addByTwoPoints(line4.endSketchPoint, adsk.core.Point3D.create(x, w2+w6, r1-d1))
        line6 = lines.addByTwoPoints(line5.endSketchPoint, adsk.core.Point3D.create(x, w1-w2+w6, r1-d1))
        line7 = lines.addByTwoPoints(line6.endSketchPoint, adsk.core.Point3D.create(x, w1-w2+w6, r1))
        line8 = lines.addByTwoPoints(line7.endSketchPoint, adsk.core.Point3D.create(x, w1+w6, r1))
        line9 = lines.addByTwoPoints(line8.endSketchPoint, adsk.core.Point3D.create(x, w1+w6, r3))
        line10 = lines.addByTwoPoints(line9.endSketchPoint, adsk.core.Point3D.create(x, w1+w3+w6, r3))
        
#########################################################################################################################
         # Get the profile defining the sprocket hub.
        prof = sk1.profiles.item(0)

        # Create an revolution input to be able to define the input needed for a revolution
        # while specifying the profile and that a new component is to be created
        revolves = rootComp.features.revolveFeatures
        revInput = revolves.createInput(prof, axis, adsk.fusion.FeatureOperations.NewComponentFeatureOperation)

        # Define that the extent is an angle of 2pi to get a torus.
        angle = adsk.core.ValueInput.createByReal(2*(math.pi))
        revInput.setAngleExtent(False, angle)

        # Create the extrusion.
        ext = revolves.add(revInput)

        
#########################################################################################################################


        #draw tooth profile        
        sketches = rootComp.sketches
        sk2 = sketches.add(rootComp.yZConstructionPlane)
        points2 = adsk.core.ObjectCollection.create() 
        lines2 = sk2.sketchCurves.sketchLines;
        line21 = lines2.addByTwoPoints(adsk.core.Point3D.create(-spr_length/2, (w1-w4+w6), r1), adsk.core.Point3D.create(-spr_length/2, (w1-w4+w6), spr_height-spr_ch+r1))
        line22 = lines2.addByTwoPoints(line21.endSketchPoint, adsk.core.Point3D.create(-spr_length/2+spr_ch, (w1-w4+w6), spr_height+r1))
        line23 = lines2.addByTwoPoints(line22.endSketchPoint, adsk.core.Point3D.create(spr_length/2-spr_ch, (w1-w4+w6), spr_height+r1))
        line24 = lines2.addByTwoPoints(line23.endSketchPoint, adsk.core.Point3D.create(spr_length/2, (w1-w4+w6), spr_height-spr_ch+r1))
        line25 = lines2.addByTwoPoints(line24.endSketchPoint, adsk.core.Point3D.create(spr_length/2, (w1-w4+w6), r1))
        line26 = lines2.addByTwoPoints(line25.endSketchPoint, adsk.core.Point3D.create(-spr_length/2, (w1-w4+w6), r1))
        

        # Get the profile defined by the tooth.
        prof = sk2.profiles.item(0)

        # Create an extrusion input
        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        
        # Define that the extent is a distance extent of 'distance'.
        distance = adsk.core.ValueInput.createByReal(-spr_width)
        extInput.setDistanceExtent(False, distance)

        # Create the extrusion.
        ext = extrudes.add(extInput)

        # Get the body created by extrusion
        body = rootComp.bRepBodies.item(0)
        
        # Create input entities for circular pattern
        inputEntites = adsk.core.ObjectCollection.create()
        inputEntites.add(body)
        
        # Get Y axis for circular pattern
        yAxis = rootComp.yConstructionAxis
        
        # Create the input for circular pattern
        circularFeats = rootComp.features.circularPatternFeatures
        circularFeatInput = circularFeats.createInput(inputEntites, yAxis)
        
        # Set the quantity of the elements
        circularFeatInput.quantity = adsk.core.ValueInput.createByReal(n)
        
        # Set the angle of the circular pattern
        circularFeatInput.totalAngle = adsk.core.ValueInput.createByString('360 deg')
        
        # Set symmetry of the circular pattern
        circularFeatInput.isSymmetric = False
        
        # Create the circular pattern
        circularFeat = circularFeats.add(circularFeatInput)

        #####################################################################################################################################################


    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))