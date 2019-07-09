from pyglet.gl import *
from pyglet import *
import ShaderLoader
from ObjLoader import ObjLoader
from pyrr import Vector3, Vector4, matrix44, Matrix44
import numpy

class ShaderAttributes:
    FOVY = 65.0 #degrees field of view
    NEAR_CLIP = 0.1
    FAR_CLIP = 400.0
    WIDTH = 1280.0
    HEIGHT = 720.0
    ASPECT_RATIO = 1280.0 / 720

    @staticmethod
    def set_screen_size(width, height):
        SA = ShaderAttributes
        SA.WIDTH = width
        SA.HEIGHT = height
        SA.ASPECT_RATIO = width / height
        projection_matrix = matrix44.create_perspective_projection_matrix(SA.FOVY, SA.ASPECT_RATIO, SA.NEAR_CLIP, SA.FAR_CLIP)
        ShapeShader.projection = projection_matrix
        ObjectShader.projection = projection_matrix

SA = ShaderAttributes

def set_shader_camera(position, lookAt):
    view = matrix44.create_look_at(position, lookAt, ObjectShader.cameraUp)
    ShapeShader.vp = matrix44.multiply(view, ObjectShader.projection)
    c_vp = numpy.ctypeslib.as_ctypes(ShapeShader.vp.flatten().astype("float32"))
    glUseProgram(ObjectShader.shader)
    glUniformMatrix4fv(ObjectShader.vp_loc, 1, GL_FALSE, c_vp)
    glUseProgram(ShapeShader.shader)
    glUniformMatrix4fv(ShapeShader.vp_loc, 1, GL_FALSE, c_vp)

def set_2d_mode():
    glUseProgram(0)
    glDisable(GL_DEPTH_TEST)

def unset_2d_mode(shader):
    glEnable(GL_DEPTH_TEST)
    glUseProgram(shader)

def distance_3d(coor1, coor2):
    return sum((coor1-coor2)**2)**0.5

def convert_3dcoor_to_screen(coor):
    screenpos = matrix44.apply_to_vector(ShapeShader.vp, Vector4.from_vector3(coor, 1.0))
    if screenpos[3] == 0:
        screenpos[3] += 0.01
    screenpos = screenpos/screenpos[3]
    #if screenpos[0] < -1 or screenpos[0] > 1 or screenpos[1] < -1 or screenpos[1] > 1:
    #    return [-10,-10]
    screenpos = [(screenpos[0]+1)*SA.WIDTH//2, (screenpos[1]+1)*SA.HEIGHT//2] 
    return screenpos

class ObjectShader:
    shader = None
    #shape_shader = None
    cameraUp = numpy.array([0.0, 1.0, 0.0], dtype='float')
    projection = None
    vp_loc = None
    model_loc = None 

    @staticmethod
    def init(position = Vector3([0.0,0.0,-5.0]), aspect_ratio = SA.ASPECT_RATIO):
        ObjectShader.projection = matrix44.create_perspective_projection_matrix(SA.FOVY, aspect_ratio, SA.NEAR_CLIP, SA.FAR_CLIP)
        if ObjectShader.shader is None:
            ObjectShader.create_shader()
            ObjectShader.vp_loc = glGetUniformLocation(ObjectShader.shader, b"vp")
            ObjectShader.model_loc = glGetUniformLocation(ObjectShader.shader, b"model")
            ObjectShader.create_perspective_projection(position)

    @staticmethod
    def create_shader():
        ObjectShader.shader = ShaderLoader.compile_shader("shaders/object_vert.glsl", "shaders/object_frag.glsl")
        #ObjectShader.shape_shader = ShaderLoader.compile_shader("shaders/shape_vert.glsl", "shaders/shape_frag.glsl")
        glUseProgram(ObjectShader.shader)

    @staticmethod
    def create_perspective_projection(position, lookAt = Vector3([0,0,0])):
        view = matrix44.create_look_at(position, lookAt, ObjectShader.cameraUp)
        vp = matrix44.multiply(view, ObjectShader.projection).flatten().astype("float32")
        c_vp = numpy.ctypeslib.as_ctypes(vp)
        glUniformMatrix4fv(ObjectShader.vp_loc, 1, GL_FALSE, c_vp)



class ShapeShader:
    shader = None
    cameraUp = numpy.array([0.0, 1.0, 0.0], dtype='float')
    projection = None
    vp_loc = None
    col_loc = None
    vp = None
    used_color = [0.0, 0.0, 0.0, 0.0]

    @staticmethod
    def init(position = Vector3([0.0,0.0,-5.0]), aspect_ratio= SA.ASPECT_RATIO):
        ShapeShader.projection = matrix44.create_perspective_projection_matrix(SA.FOVY, aspect_ratio, SA.NEAR_CLIP, SA.FAR_CLIP)
        if ShapeShader.shader is None:
            ShapeShader.create_shader()
            ShapeShader.vp_loc = glGetUniformLocation(ShapeShader.shader, b"vp")
            ShapeShader.col_loc = glGetUniformLocation(ShapeShader.shader, b"vColor")
            ShapeShader.create_perspective_projection(position)

    @staticmethod
    def create_shader():
        ShapeShader.shader = ShaderLoader.compile_shader("shaders/shape_vert.glsl", "shaders/shape_frag.glsl")
        glUseProgram(ShapeShader.shader)

    @staticmethod
    def create_perspective_projection(position, lookAt = Vector3([0,0,0])):
        view = matrix44.create_look_at(position, lookAt, ShapeShader.cameraUp)
        ShapeShader.vp = matrix44.multiply(view, ShapeShader.projection)
        c_vp = numpy.ctypeslib.as_ctypes(ShapeShader.vp.flatten().astype("float32"))
        glUniformMatrix4fv(ShapeShader.vp_loc, 1, GL_FALSE, c_vp)

    @staticmethod
    def use_color(color):
        ShapeShader.used_color = color
        col = Vector4(color).flatten().astype('float32')
        c_col = numpy.ctypeslib.as_ctypes(col)
        glUniform4fv(ShapeShader.col_loc, 1, c_col)

    @staticmethod
    def draw(gl_mode, vert_list, color):
        pass #! to be implemented

    