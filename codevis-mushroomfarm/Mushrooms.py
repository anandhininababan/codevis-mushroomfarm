from pyglet.gl import *
from pyglet import graphics
from pyglet import gl
from pyglet import clock
from pyglet.window import key
import ShaderLoader
from ObjLoader import ObjLoader
from pyrr import Vector3, Vector4, matrix44, Matrix44
from shaders import *
import time
import numpy
import random
from DBConnector import *
import threading



class Mushroom:
    instances = {}
    instance_locations = {}
    instance_info = {}
    readable_instances = []
    detected = []
    db = DBConnector()
    shroom_paths = db.execute("SELECT path FROM visualpropertypath WHERE path LIKE '%Mushroom.obj'")
    shroom_paths = sorted([x[0] for x in shroom_paths], reverse=True) #now, list will be sorted small-medium-large
    del db
    texture_offsets = []
    data_list = []
    for i in range(3):
        mesh = ObjLoader()
        mesh.load_model(shroom_paths[i])
        num_verts = len(mesh.vertex_index)
        texture_offset = len(mesh.vertex_index) * 12
        data = numpy.array(mesh.model, dtype=GLfloat)
        texture_offsets.append(texture_offset)
        data_list.append(data)

    def __init__(self, tekstur, code, size=0):
        code += str(size)
        if code in Mushroom.instances:
            return None        
        Mushroom.instances[code] = self
        Mushroom.instance_locations[code] = []
        
        self.vao_mushroom = GLuint()
        # generate a vertex array object for the mushroom - the vao
        glGenVertexArrays(1, self.vao_mushroom)
        # bind the mushroom's vao
        glBindVertexArray(self.vao_mushroom)
        # setup the mushroom's vertex buffer object - the vbo
        vbo_sphere = pyglet.graphics.vertexbuffer.create_buffer(Mushroom.data_list[size].nbytes, GL_ARRAY_BUFFER, GL_STATIC_DRAW)
        vbo_sphere.bind()
        vbo_sphere.set_data(Mushroom.data_list[size].ctypes.data)
        
        # vertex attribute pointer settings for the mushroom vbo
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, 0)
        glEnableVertexAttribArray(0)
        
        # textures
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, Mushroom.texture_offsets[size])
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

        # self.loadingthread = GeneralThread(load_texture_image, self, tekstur)
        # self.loadingthread.run()

        image = pyglet.image.load(tekstur)

        image_data = image.get_data('RGB', image.pitch)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

        # endregion

    

    def render(self, translasi):
        # if self.loadingthread.isAlive():
        #     return
        # to draw the mushroom, we need to rebind the mushroom's vao
        
        model_loc = ObjectShader.model_loc 
        mushroom_model = matrix44.create_from_translation(translasi).flatten().astype("float32") #this is the model transformation matrix
        c_mushroom_model = numpy.ctypeslib.as_ctypes(mushroom_model)

        glBindVertexArray(self.vao_mushroom)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, c_mushroom_model)
        glDrawArrays(GL_TRIANGLES, 0, Mushroom.num_verts)
        glBindVertexArray(0)

    def batch_render(self, list_translasi, undraw_detected=False): # me-render banyak mushroom dengan tekstur sama    
        # if self.loadingthread.isAlive():
        #     return
        glBindVertexArray(self.vao_mushroom)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        model_loc = ObjectShader.model_loc
        detected_translasi = [Mushroom.instance_info[x][2] for x in Mushroom.detected]

        for translasi in list_translasi:
            if translasi not in detected_translasi or not undraw_detected:
                mushroom_model = matrix44.create_from_translation(Vector3(translasi)).flatten().astype("float32") #this is the model transformation matrix
                c_mushroom_model = numpy.ctypeslib.as_ctypes(mushroom_model)
                glUniformMatrix4fv(model_loc, 1, GL_FALSE, c_mushroom_model)
                glDrawArrays(GL_TRIANGLES, 0, Mushroom.num_verts)
        glBindVertexArray(0)

    @staticmethod
    def _draw_name_label(name, position):
        screenpos = convert_3dcoor_to_screen(position)
        # set_2d_mode()
        name_text = text.Label(name, font_size=18, color=[0,0,0,255], x = screenpos[0], y=screenpos[1], anchor_x='center', anchor_y='bottom')
        
        name_length = (name_text.content_width+5)/2
        graphics.vertex_list(4, ('v2f', (
            screenpos[0]-name_length,screenpos[1],
            screenpos[0]-name_length, screenpos[1]+25,
            screenpos[0]+name_length,screenpos[1]+25,
            screenpos[0]+name_length, screenpos[1]
        )), ('c3B', (200,200,200, 200,200,200,  200,200,200,  200,200,200))).draw(GL_QUADS)
        graphics.vertex_list(4, ('v2f', (
            screenpos[0]-name_length,screenpos[1],
            screenpos[0]-name_length, screenpos[1]+25,
            screenpos[0]+name_length,screenpos[1]+25,
            screenpos[0]+name_length, screenpos[1]
        )), ('c3B', (0,0,0, 0,0,0,  0,0,0,  0,0,0))).draw(GL_LINE_LOOP)
        name_text.draw()
        # unset_2d_mode(ShapeShader.shader)

    @staticmethod
    def draw_warning_sign(position):
        screenpos = convert_3dcoor_to_screen(position)
        screenpos[0] -= 18
        screenpos[1] += 36
        # draw in 2d
        # set_2d_mode()
        graphics.vertex_list(3, ('v2f', (
            screenpos[0], screenpos[1],
            screenpos[0]+36, screenpos[1],
            screenpos[0]+18, screenpos[1]+36
        )), ('c3B', (
            255,255,0, 255,255,0, 255,255,0
        ))).draw(GL_TRIANGLES)
        text.Label('!', font_size=18, color=[0,0,0,255], x=screenpos[0]+14, y=screenpos[1], anchor_x='left', anchor_y='bottom').draw()
        # unset_2d_mode(ShapeShader.shader) 

    @staticmethod
    def get_all_shroom_position():
        shroom_list = []
        for key in Mushroom.instance_locations:
            shroom_list += Mushroom.instance_locations[key]
        return shroom_list

    @staticmethod
    def add_instance_location(shroomtype, location):
        Mushroom.instance_locations[shroomtype].append(location)

    @staticmethod
    def add_instance_detail(shroom_id, name, shroomtype, location, is_field):
        if is_field:
            used_id = 'f'+str(shroom_id)
            Mushroom.instance_info[used_id] = [name, shroomtype, location]
        else:
            used_id = 'm'+str(shroom_id)
            Mushroom.instance_info[used_id] = [name, shroomtype, location]
        Mushroom.add_instance_location(shroomtype, location)

    @staticmethod
    def move_shroom(shroom_id, is_field, shift_vector):
        used_id = ('f' if is_field else 'm') + str(shroom_id)
        Mushroom.instance_info[used_id][2] += shift_vector 

    @staticmethod
    def set_readable(shroom_pos_list):
        Mushroom.readable_instances = shroom_pos_list

    @staticmethod
    def add_detected(shroom_ids):
        Mushroom.detected += [shroom for shroom in shroom_ids if shroom not in Mushroom.detected]

    @staticmethod
    def remove_detected(shroom_ids):
        Mushroom.detected = [shroom for shroom in Mushroom.detected if shroom not in shroom_ids]

    @staticmethod
    def set_detected(shroom_ids):
        Mushroom.detected = shroom_ids

    @staticmethod
    def draw_all_shroom(undraw_detected=False):
        for key in Mushroom.instances:
            Mushroom.instances[key].batch_render(Mushroom.instance_locations[key], undraw_detected=undraw_detected)
        set_2d_mode()
        for shroom_pos in Mushroom.readable_instances:
            all_info = Mushroom.instance_info.items()
            for info in all_info:
                if info[1][2] == shroom_pos:
                    Mushroom._draw_name_label(info[1][0], info[1][2])
        # for warned_id in Mushroom.detected:
        #     Mushroom.draw_warning_sign(Mushroom.instance_info[warned_id][2])
        unset_2d_mode(ObjectShader.shader)
        