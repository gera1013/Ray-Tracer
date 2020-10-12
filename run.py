from gl import RayTracer, color
from sphere import * 
from obj import Envmap, Texture
import random

# creación de materiales
brick = Material(diffuse = color(0.8, 0.25, 0.25), spec = 16)
stone = Material(diffuse = color(0.4, 0.4, 0.4), spec = 4)
mirror = Material(spec = 64, t = REFLECTIVE)
glass = Material(spec = 64, ior = 1.5, t= TRANSPARENT) 

mcraft_cobblestone = Material(texture = Texture('./textures/cobblestone.bmp'))
mcraft_diamond = Material(texture = Texture('./textures/diamond.bmp'))
mcraft_dirt = Material(texture = Texture('./textures/dirt.bmp'))
mcraft_emerald = Material(texture = Texture('./textures/emerald.bmp'))
mcraft_stone = Material(texture = Texture('./textures/stone.bmp'))

# creamos espacio para renderizar
width = 512
height = 512
r = RayTracer(width, height)

# luces de distintos tipos
r.point_lights.append(PointLight(position = [2, 3, -5], intensity = 0.5, _color_= color(0.5, 0.5, 0.5)))
r.ambient_light = AmbientLight(strength = 0.5)

# environment map
#r.env_map = Envmap('./PR2/envmaps/park.bmp');

# objetos en la escena
r.scene.append(Cube([-4, 0, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([-3, 0, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([-2, 0, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([-1, 0, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([0, 0, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([1, 0, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([2, 0, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([3, 0, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([4, 0, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([-4, -1, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([-3, -1, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([-2, -1, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([-1, -1, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([0, -1, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([1, -1, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([2, -1, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([3, -1, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([4, -1, -9], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([-4, -1, -8], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([-3, -2, -8], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([-2, -2, -8], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([-1, -1, -8], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([0, -2, -8], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([1, -2, -8], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([2, -2, -8], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([3, -1, -8], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([4, -1, -8], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([-4, -2, -7], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([-3, -2, -7], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([-2, -2, -7], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([-1, -2, -7], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([0, -2, -7], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([1, -2, -7], [1, 1, 1], mcraft_stone))
r.scene.append(Cube([2, -2, -7], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([3, -2, -7], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([4, -2, -7], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([-3, -2, -6], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([-2, -2, -6], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([-1, -2, -6], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([0, -2, -6], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([1, -2, -6], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([2, -2, -6], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([3, -2, -6], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([-2, -2, -5], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([-1, -2, -5], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([0, -2, -5], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([1, -2, -5], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([2, -2, -5], [1, 1, 1], mcraft_dirt))
r.scene.append(Cube([3, -2, -5], [1, 1, 1], mcraft_dirt))

# render
r.glRayTracingRender()

# generamos el output
r.glFinish('output.bmp')
