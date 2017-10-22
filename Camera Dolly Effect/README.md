# Location
Camera Data context > Lens > Dolly Effect
(The camera will have to be set in Perspective mode)

Blender version: 2.78 and above

# Camera Dolly Effect
This script is used to set-up a driver in the Focal Length camera´s datablock towards an object working as a focal point, which size looks unchanged when moving the camera away and towards such point, and this way, creating the famous camera dolly effect tipically used in cinema.

The driver is set over the Focal Length parameter of the camera, so, when moving the camera or the focal object, the Focal Length changes automatically with the distance between the two.

The driver is initially set using the current Focal Length and distance between the two objects. You can later change the Focal Length used with the Initial Focal Length slider. You will notice that the distance taken as a reference (configured in the driver) doesn´t change when changing the Initial Focal Length or when moving the objects. So, if you need a new "base distance" to take as reference, just clean the object field of the focal point, configure your camera as you like, and reselect the focal point object. This will create another driver based on the new distance between the two objects.

# Warning
Because this script uses the Focal Length parameter of the camera to set a driver, any other pre-created driver will be deleted and overwritten. An icon will appear to notify the user about this.

You are fine if you have animation keyframes work on such parameter. These will not be deleted, but will not be used either, as drivers takes precedence over keyframed animation.

# Note
To make the driver work and update automatically, the "Auto Run Python Scripts" option of the User Preferences must be enabled (and saved for future use). The path is User Preferences > File > Auto Run Python Scripts. Then you can save your preferences as default with the below button "Save User Settings".
