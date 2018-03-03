# Location
Camera Data context > Lens > Camera to Isometric view

Blender version: 2.79 (but a lot of older Blender versions will work as well)

# Isometric Camera
This is a very tiny script which sets an Orthogonal Isometric view for all the selected Cameras.
It's just a single button which will iterate over all selected objects and if it finds a camera,
will set the nearest mathematically accurate Isometric View for it.
The script is angle-wise, so it will try to match the nearest isometric quadrant according to
the current viewpoint and will keep your camera angle as possible. This means that if you have
say for example, 438º into the Z rotation channel, it will give you something like 405º instead
of the equivalent 45º of a new un-rotated camera. This enables you to animate the camera and use
this script without destroying your current animated rotations and avoiding to manually re-rotate
the camera to fix the f-curves.

# Usage
- For all the cameras you are interested, make them to point approximately in the direction that you
  would like to look Isometrically.
- Select the cameras you want to set as Isometric.
- Press the "Camera to Isometric view" button.

# Note
This script was only tested with XYZ Euler Rotation mode.
