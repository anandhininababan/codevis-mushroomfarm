from pyglet.gl import *
from pyglet import graphics
from pyglet import gl
from pyglet import clock
from pyglet.window import key
import ShaderLoader
from ObjLoader import ObjLoader
from pyrr import Vector3, Vector4, matrix44, Matrix44
from shaders import ObjectShader, ShapeShader, set_shader_camera
import time
import numpy
import random
from DBConnector import *

class Rock:
    ROCK_WIDTH = 3
    instances = []
    instance_locations = []
    db = DBConnector()
    rock_path = db.execute("SELECT path FROM visualpropertypath WHERE name = 'rock'")[0][0]
    del db
    mesh = ObjLoader()
    mesh.load_model(rock_path)
    num_verts = len(mesh.vertex_index)
    texture_offset = len(mesh.vertex_index) * 12
    data = numpy.array(mesh.model, dtype=GLfloat)
    del mesh

    def __init__(self, tekstur):
        Rock.instances.append(self)
        Rock.instance_locations.append([])

        self.vao_rock = GLuint()
        # generate a vertex array object for the rock - the vao
        glGenVertexArrays(1, self.vao_rock)
        # bind the rock's vao
        glBindVertexArray(self.vao_rock)
        # setup the rock's vertex buffer object - the vbo
        vbo_sphere = pyglet.graphics.vertexbuffer.create_buffer(Rock.data.nbytes, GL_ARRAY_BUFFER, GL_STATIC_DRAW)
        vbo_sphere.bind()
        vbo_sphere.set_data(Rock.data.ctypes.data)

        # vertex attribute pointer settings for the rock vbo
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)
        glEnableVertexAttribArray(0)
        # textures
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, Rock.texture_offset)
        glEnableVertexAttribArray(1)

        glBindBuffer(GL_ARRAY_BUFFER, 0)  # unbind the vbo
        glBindVertexArray(0)  # unbind the vao

        # region texture settings
        self.texture = GLuint(0)
        glGenTextures(1, self.texture)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        # set the texture wrapping
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # set the texture filtering
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        image = pyglet.image.load(tekstur)
        image_data = image.get_data('RGB', image.pitch)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
        # endregion

    def render(self, translasi):
        # to draw the rock, we need to rebind the rock's vao
        model_loc = ObjectShader.model_loc 
        rock_model = matrix44.create_from_translation(translasi).flatten().astype("float32") #this is the model transformation matrix
        c_rock_model = numpy.ctypeslib.as_ctypes(rock_model)

        glBindVertexArray(self.vao_rock)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, c_rock_model)
        glDrawArrays(GL_POLYGON, 0, Rock.num_verts)
        glDrawArrays(GL_TRIANGLES, 0, Rock.num_verts)
        glBindVertexArray(0)

    def batch_render(self, list_translasi): # me-render banyak rock dengan tekstur sama
        glBindVertexArray(self.vao_rock)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        model_loc = ObjectShader.model_loc

        for translasi in list_translasi:
            rock_model = matrix44.create_from_translation(Vector3(translasi)).flatten().astype("float32") #this is the model transformation matrix
            c_rock_model = numpy.ctypeslib.as_ctypes(rock_model)
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, c_rock_model)
            glDrawArrays(GL_TRIANGLES, 0, Rock.num_verts)
        glBindVertexArray(0)

    @staticmethod
    def add_instance_location(rocktype, location):
        Rock.instance_locations[rocktype].append(location)

    @staticmethod
    def draw_all_rock():
        for i in range(len(Rock.instances)):
            Rock.instances[i].batch_render(Rock.instance_locations[i])