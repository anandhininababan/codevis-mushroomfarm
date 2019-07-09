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

class Fence:
    FENCE_WIDTH = 3
    instances = []
    h_instance_locations = []
    v_instance_locations = []
    db = DBConnector()
    fence_path = db.execute("SELECT path FROM visualpropertypath WHERE name = 'fence'")[0][0]
    del db
    mesh = ObjLoader()
    mesh.load_model(fence_path)
    num_verts = len(mesh.vertex_index)
    texture_offset = len(mesh.vertex_index) * 12
    data = numpy.array(mesh.model, dtype=GLfloat)
    del mesh

    def __init__(self, tekstur):
        Fence.instances.append(self)
        Fence.h_instance_locations.append([])
        Fence.v_instance_locations.append([])

        self.vao_fence = GLuint()
        # generate a vertex array object for the fence - the vao
        glGenVertexArrays(1, self.vao_fence)
        # bind the fence's vao
        glBindVertexArray(self.vao_fence)
        # setup the fence's vertex buffer object - the vbo
        vbo_sphere = pyglet.graphics.vertexbuffer.create_buffer(Fence.data.nbytes, GL_ARRAY_BUFFER, GL_STATIC_DRAW)
        vbo_sphere.bind()
        vbo_sphere.set_data(Fence.data.ctypes.data)

        # vertex attribute pointer settings for the fence vbo
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)
        glEnableVertexAttribArray(0)
        # textures
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, Fence.texture_offset)
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
        # to draw the fence, we need to rebind the fence's vao
        model_loc = ObjectShader.model_loc 
        fence_model = matrix44.create_from_translation(translasi).flatten().astype("float32") #this is the model transformation matrix
        c_fence_model = numpy.ctypeslib.as_ctypes(fence_model)

        glBindVertexArray(self.vao_fence)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, c_fence_model)
        glDrawArrays(GL_POLYGON, 0, Fence.num_verts)
        glDrawArrays(GL_TRIANGLES, 0, Fence.num_verts)
        glBindVertexArray(0)

    def batch_render(self, list_translasi, vertical=True): # me-render banyak fence dengan tekstur sama
        glBindVertexArray(self.vao_fence)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        model_loc = ObjectShader.model_loc
        if not vertical:
            rotate = matrix44.create_from_y_rotation(numpy.pi/2) # 90 degree rotation
            
        for translasi in list_translasi:
            fence_model = matrix44.create_from_translation(Vector3(translasi)) #this is the model transformation matrix
            if not vertical:
                fence_model = matrix44.multiply(rotate, fence_model)
            c_fence_model = numpy.ctypeslib.as_ctypes(fence_model.flatten().astype('float32'))
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, c_fence_model)
            glDrawArrays(GL_TRIANGLES, 0, Fence.num_verts)
        glBindVertexArray(0)

    @staticmethod
    def add_instance_location(fencetype, location, vertical=True):
        if vertical:
            Fence.v_instance_locations[fencetype].append(location)
        else:
            Fence.h_instance_locations[fencetype].append(location)

    @staticmethod
    def draw_all_fence():
        for i in range(len(Fence.instances)):
            Fence.instances[i].batch_render(Fence.h_instance_locations[i], False)
            Fence.instances[i].batch_render(Fence.v_instance_locations[i])