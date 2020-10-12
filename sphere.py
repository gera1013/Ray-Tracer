import numpy as np
from numpy import arccos, arctan2
from gl import color, mathVectorSubstraction, mathDotProduct, mathFrobenius, mathVectorAdd, mathVectorTimesScalar, mathLinalgNormal

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

WHITE = color(1, 1, 1)

class Material(object):
    # inicialización
    def __init__(self, diffuse = WHITE, spec = 0, ior = 1, texture = None, t = OPAQUE):
        # color del pixel
        self.diffuse = diffuse
        self.spec = spec

        # tipo del material
        self.type = t
        self.ior = ior

        # textura del material
        self.texture = texture


class Intersect(object):
    # inicialización
    def __init__(self, distance, point, normal, texture, obj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.texture = texture
        self.scene_object = obj

class AmbientLight(object):
    # inicialización
    def __init__(self, strength = 0, _color_ = WHITE):
        self.strength = strength
        self.color = _color_

class PointLight(object):
    # inicialización
    def __init__(self, position = [0, 0, 0], intensity = 1, _color_ = WHITE):
        self.position = position
        self.intensity = intensity
        self.color = _color_

class DirectionalLight(object):
    # inicialización
    def __init__(self, direction = [0, -1, 0], _color_ = WHITE, intensity = 1):
        self.direction = mathLinalgNormal(direction)
        self.intensity = intensity
        self.color = _color_

class Sphere(object):
    # inicialización
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        # Regresa falso o verdadero si hace interseccion con una esfera

        L = mathVectorSubstraction(self.center, orig)
        tca = mathDotProduct(L, dir)
        magnitude_L = mathFrobenius(L)

        d = (magnitude_L ** 2 - tca ** 2) ** 0.5
        
        if d > self.radius:
            return None

        # thc es la distancia de P1 al punto perpendicular al centro
        thc = (self.radius ** 2 - d ** 2) ** 0.5
        t0 = tca - thc
        t1 = tca + thc
        
        if t0 < 0:
            t0 = t1

        if t0 < 0: # t0 tiene el valor de t1
            return None

        hit = mathVectorAdd(orig, mathVectorTimesScalar(t0, dir))

        norm = mathVectorSubstraction(hit, self.center)
        norm = mathLinalgNormal(norm)

        u = 1 - (arctan2(norm[2], norm[0]) / (2 * np.pi) + 0.5)
        v =  arccos(-norm[1]) / np.pi

        uvs = [u, v]

        return Intersect(
            distance = t0,
            point = hit,
            normal = norm,
            texture = uvs,
            object = self
        )

class Plane(object):
    def __init__(self, position, normal, material):
        self.position = position
        self.normal = mathLinalgNormal(normal)
        self.material = material

    def ray_intersect(self, orig, dir):
        denom = mathDotProduct(dir, self.normal)

        if abs(denom) > 0.0001:
            t = mathDotProduct(self.normal, mathVectorSubstraction(self.position, orig)) / denom
            if t > 0:
                hit = mathVectorAdd(orig, mathVectorTimesScalar(t, dir))

                return Intersect(
                    distance = t,
                    point = hit,
                    normal = self.normal,
                    texture = None,
                    obj = self
                )

        return None

# Cubos
class Cube(object):
    def __init__(self, position, size, material):
        self.position = position
        self.size = size
        self.material = material
        self.planes = []

        halfSizeX = size[0] / 2
        halfSizeY = size[1] / 2
        halfSizeZ = size[2] / 2

        self.planes.append(Plane(mathVectorAdd(position, [halfSizeX, 0, 0]), [1, 0, 0], material))
        self.planes.append(Plane(mathVectorAdd(position, [-halfSizeX, 0, 0]), [-1, 0, 0], material))

        self.planes.append(Plane(mathVectorAdd(position, [0, halfSizeY, 0]), [0, 1, 0], material))
        self.planes.append(Plane(mathVectorAdd(position, [0, -halfSizeY, 0]), [0, -1, 0], material))

        self.planes.append(Plane(mathVectorAdd(position, [0, 0, halfSizeZ]), [0, 0, 1], material))
        self.planes.append(Plane(mathVectorAdd(position, [0, 0, -halfSizeZ]), [0, 0, -1], material))


    def ray_intersect(self, orig, dir):

        epsilon = 0.001

        boundsMin = [0, 0, 0]
        boundsMax = [0, 0, 0]

        for i in range(3):
            boundsMin[i] = self.position[i] - (epsilon + self.size[i] / 2)
            boundsMax[i] = self.position[i] + (epsilon + self.size[i] / 2)

        t = float('inf')
        intersect = None

        for plane in self.planes:
            planeInter = plane.ray_intersect(orig, dir)

            if planeInter is not None:
                # Si estoy dentro del bounding box
                if planeInter.point[0] >= boundsMin[0] and planeInter.point[0] <= boundsMax[0]:
                    if planeInter.point[1] >= boundsMin[1] and planeInter.point[1] <= boundsMax[1]:
                        if planeInter.point[2] >= boundsMin[2] and planeInter.point[2] <= boundsMax[2]:
                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter

                                if abs(plane.normal[0]) > 0:
                                    # mapear uvs para eje x. Uso coordenadas en Y y Z.
                                    u = (planeInter.point [1] - boundsMin[1]) / (boundsMax[1] - boundsMin[1])
                                    v = (planeInter.point [2] - boundsMin[2]) / (boundsMax[2] - boundsMin[2])

                                elif abs(plane.normal[1]) > 0:
                                    # mapear uvs para eje y. Uso coordenadas en X y Z.
                                    u = (planeInter.point [0] - boundsMin[0]) / (boundsMax[0] - boundsMin[0])
                                    v = (planeInter.point [2] - boundsMin[2]) / (boundsMax[2] - boundsMin[2])

                                elif abs(plane.normal[2]) > 0:
                                    # mapear uvs para eje Z. Uso coordenadas en X y Y.
                                    u = (planeInter.point [0] - boundsMin[0]) / (boundsMax[0] - boundsMin[0])
                                    v = (planeInter.point [1] - boundsMin[1]) / (boundsMax[1] - boundsMin[1])

                                uvs = [u, v]

        if intersect is None:
            return None

        return Intersect(
            distance = intersect.distance,
            point = intersect.point,
            normal = intersect.normal,
            texture = uvs,
            obj = self
        )