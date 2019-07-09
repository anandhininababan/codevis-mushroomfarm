from Mushrooms import *
from pyglet import text
from shaders import *
from Rock import *
import math 

class MushroomSquare:
    BROWN_SQUARE_COLOR = [0.38, 0.2, 0.07,1.0]
    BROWN_SQUARE_SELECTED = [0.58, 0.4, 0.2,1.0]
    GREEN_SQUARE_COLOR = [0.0, 0.7, 0.3, 1.0]
    GREEN_SQUARE_SELECTED = [0.0, 0.9, 0.4,1.0]
    INTERSHROOM_DISTANCE = 11.0
    ROW_SHROOM_NUM = 5
    MAX_SQR_WIDTH = INTERSHROOM_DISTANCE * (ROW_SHROOM_NUM + 1)
    MAX_SQR_HEIGHT = MAX_SQR_WIDTH
    # states of a mushroomsquare: 0:unselected, 1:selected, 2:related to selected object
    #squareid = 0
    instances = {}
    detected_instances = []
    readable_instances = []
    tcolor = {'b':BROWN_SQUARE_COLOR, 'b1':BROWN_SQUARE_SELECTED, 'g':GREEN_SQUARE_COLOR, 'g1':GREEN_SQUARE_SELECTED} # map types to square color, xxx1 : color when selected
    # sqtypes = tanah hijau/coklat, dikelilingi batu/tidak
    def __init__(self, sq_id, sq_name, sq_type, position, width=6, height=6):
        #MushroomSquare.squareid += 1
        self.id = sq_id      
        MushroomSquare.instances[self.id] = self        
        self.type = sq_type[0]
        self.has_rock_fence = 'r' in sq_type
        self.name = sq_name
        self.width = width
        self.height = height
        self.position = Vector3(position) #top left corner of the square
        pad = MushroomSquare.INTERSHROOM_DISTANCE
        self.next_coordinate = [position[0]+pad, position[1], position[2]+pad]
        self.next_col = 0
        #self.shrooms = [] #field shroom
         # list of mushrooms coordinates
        self.parent = [] #list of mushroomsquare ids
        self.child = [] #list of mushroomsquare ids
        self.coupling = [] #list of mushroomsquare ids
        
        self.state = 0
        maxnum = MushroomSquare.ROW_SHROOM_NUM
        dist = MushroomSquare.INTERSHROOM_DISTANCE
        self.next_shroom_vec = Vector3([dist, 0.0, 0.0])
        self.m_shroom_rows = [ObjectRow(Vector3(self.next_coordinate), maxnum, self.next_shroom_vec)]
        self.f_shroom_rows = [ObjectRow(Vector3(self.next_coordinate) + Vector3([0.0, 0.0, 0.0]), maxnum, self.next_shroom_vec)]
        # self.f_shroom_rows = [ObjectRow(Vector3(self.next_coordinate) + Vector3([0.0, 0.0, dist]), maxnum, self.next_shroom_vec)]
        self.set_drawn_square(position, MushroomSquare.MAX_SQR_WIDTH, height)
        # self.__update_next_coordinate()
        # self.detected = False
        #self.interdim = Interdimensionals()
        # self.reset_shape()
        

    def add_child(self, square):
        self.child.append(square)
        square.parent.append(self)
    
    def del_child(self, square):
        if square in self.child:
            square.parent.remove(self)
            self.child.remove(square)
    
    def add_coupling(self, square):
        self.coupling.append(square)
        square.coupling.append(self)

    def is_unselected(self):
        return self.state == 0

    def is_selected(self):
        return self.state == 1

    def is_related(self):
        return self.state == 2

    def set_selected(self):
        if self.type[-1] != '1':
            self.type += '1'
        self.state = 1
        #self.set_draw_family_label()
        for id in self.parent:
            if type(id) == int:
                MushroomSquare.instances[id].set_related()
            else:
                id.set_related()
        for id in self.child:
            if type(id) == int:
               MushroomSquare.instances[id].set_related()
            else:
                id.set_related()

    def set_unselect(self):
        #self.set_undraw_family_label()
        if self.type[-1] == '1':
            self.type = self.type[:-1]
        if self.state != 0:
            self.state = 0
            for id in self.parent:
                if type(id) == int:
                    MushroomSquare.instances[id].set_unselect()
                else:
                    id.set_unselect()
            for id in self.child:
                if type(id) == int:
                    MushroomSquare.instances[id].set_unselect()
                else:
                    id.set_unselect()              

    def set_related(self):
        self.state = 2
        #self.set_draw_family_label()
        for parent in self.parent:
            if parent.is_unselected():
                parent.set_related()
        for child in self.child:
            if child.is_unselected():
                child.set_related()

    def set_drawn_square(self, position=None, width=None, height=None):
        if width is None:
            width = self.width
        else:
            self.width = width
        if height is None:
            height = self.height
        else:
            self.height = height
        if position is None:
            position = self.position
        else:
            move_vector = Vector3(position) - self.position
            self.position += move_vector
            self.shift_shroom_positions(move_vector)
        
        self.vertices = graphics.vertex_list(4, ('v3f',(
            position[0], position[1], position[2],
            position[0]+width, position[1], position[2],
            position[0]+width, position[1], position[2]+height,
            position[0], position[1], position[2]+height
        )))
        if self.has_rock_fence:
            self.__set_rock_fence()
    
    def reset_shape(self):
        newheight = 0
        newheight += len(self.f_shroom_rows) if len(self.f_shroom_rows[-1].obj_positions)>0 else len(self.f_shroom_rows)-1
        newheight += len(self.m_shroom_rows) if len(self.m_shroom_rows[-1].obj_positions)>0 else len(self.m_shroom_rows)-1
        newheight *= MushroomSquare.INTERSHROOM_DISTANCE
        newheight += MushroomSquare.INTERSHROOM_DISTANCE
        self.set_drawn_square(height=newheight)

    def __update_next_coordinate(self):
        self.next_coordinate[2] += MushroomSquare.INTERSHROOM_DISTANCE
        #self.set_drawn_square(height=self.height+MushroomSquare.INTERSHROOM_DISTANCE)

    def add_shroom(self, shroom_id, shroom_name, shroom_type, is_field=False, auto_reset=False, size=0):
        newshroom = Vector3([0.0,0.0,0.0])
        dist = MushroomSquare.INTERSHROOM_DISTANCE
        maxnum = MushroomSquare.ROW_SHROOM_NUM
        in_front = is_field
        if not in_front: #the "not" here is a rough patch to switch fornt row and back row
            if self.f_shroom_rows[-1].is_full():
                self.__update_next_coordinate()
                new_coor = Vector3(self.next_coordinate)
                self.f_shroom_rows.append(ObjectRow(new_coor, maxnum, self.next_shroom_vec))
            newshroom = self.f_shroom_rows[-1].add_object(newshroom, shroom_id)
        else:
            if len(self.m_shroom_rows) == 1 and self.m_shroom_rows[0].is_empty():
                shift_vec = Vector3([0.0, 0.0, dist])
                for row in self.f_shroom_rows:
                    row.shift_row(shift_vec, not in_front)
            elif self.m_shroom_rows[-1].is_full():
                self.__update_next_coordinate()
                next_coor = Vector3([0.0,0.0,0.0]) + self.f_shroom_rows[0].position
                shift_vec = Vector3([0.0, 0.0, dist])
                for row in self.f_shroom_rows:
                    row.shift_row(shift_vec, not in_front)
                self.m_shroom_rows.append(ObjectRow(next_coor, maxnum, self.next_shroom_vec))
            newshroom = self.m_shroom_rows[-1].add_object(newshroom, shroom_id)
        #self.shrooms.append(newshroom)
        Mushroom.add_instance_detail(shroom_id, shroom_name, shroom_type, newshroom, is_field)
        
        
        if auto_reset:
            self.reset_shape()
        return newshroom
    
    def shift_shroom_positions(self, move_vector):
        for row in self.f_shroom_rows:
            row.shift_row(move_vector, True)
        for row in self.m_shroom_rows:
            row.shift_row(move_vector, False)

    def draw(self, colorcode = None, undraw_detected=False):
        #self.update_labels()
        if colorcode is not None:
            code1 = (colorcode // 256) / 255.0
            code2 = (colorcode % 256) / 255.0 
            ShapeShader.use_color([code1, code2, 0.0, 0.0])
        else:
            ShapeShader.use_color(MushroomSquare.tcolor[self.type])
        
        if self.id not in MushroomSquare.detected_instances or not undraw_detected:
            self.vertices.draw(GL_QUADS)
            if self.has_rock_fence:
                self.__draw_rock_fence()
        # if self.state != 0:
        #     self.__draw_family_label()

        # if self.detected:
        #     self.__draw_warning_sign()
        
    
    def get_family_number(self):
        if len(self.parent) == 0:
            return 1
        else:
            return self.parent[0].get_family_number()+1


    def __draw_family_label(self):
        fam_num = self.get_family_number()
        # get screen position of square corner
        screenpos = convert_3dcoor_to_screen(self.position)

        #draw 2D
        set_2d_mode()
        graphics.vertex_list(4, ('v2f', (
            screenpos[0],screenpos[1],
            screenpos[0], screenpos[1]+25,
            screenpos[0]+25,screenpos[1]+25,
            screenpos[0]+25, screenpos[1]
        )), ('c3B', (50,50,250, 50,50,250, 50,50,250,  50,50,250))).draw(GL_QUADS)
        text.Label(' '+str(fam_num), font_size=18, color=[0,0,0,255], x = screenpos[0], y=screenpos[1], anchor_x='left', anchor_y='bottom').draw()
        unset_2d_mode(ShapeShader.shader)

    
    def __draw_name_label(self):
        screenpos = convert_3dcoor_to_screen(self.position+ [self.width//2,0,0])
        #draw in 2d
        set_2d_mode()
        name_length = len(self.name)
        name_text = text.Label(self.name, font_size=18, color=[0,0,0,255], x = screenpos[0], y=screenpos[1], anchor_x='center', anchor_y='bottom')
        graphics.vertex_list(4, ('v2f', (
            screenpos[0]-name_text.content_width//2-2,screenpos[1],
            screenpos[0]-name_text.content_width//2-2, screenpos[1]+25,
            screenpos[0]+name_text.content_width//2+2,screenpos[1]+25,
            screenpos[0]+name_text.content_width//2+2, screenpos[1]
        )), ('c3B', (200,200,200, 200,200,200,  200,200,200,  200,200,200))).draw(GL_QUADS)
        graphics.vertex_list(4, ('v2f', (
            screenpos[0]-name_text.content_width//2-2,screenpos[1],
            screenpos[0]-name_text.content_width//2-2, screenpos[1]+25,
            screenpos[0]+name_text.content_width//2+2,screenpos[1]+25,
            screenpos[0]+name_text.content_width//2+2, screenpos[1]
        )), ('c3B', (0,0,0, 0,0,0,  0,0,0,  0,0,0))).draw(GL_LINE_LOOP)
        name_text.draw()
        unset_2d_mode(ShapeShader.shader)

    def __draw_warning_sign(self):
        screenpos = convert_3dcoor_to_screen(self.position + [self.width,0,0])
        # draw in 2d
        set_2d_mode()
        graphics.vertex_list(3, ('v2f', (
            screenpos[0], screenpos[1],
            screenpos[0]+36, screenpos[1],
            screenpos[0]+18, screenpos[1]+36
        )), ('c3B', (
            255,255,0, 255,255,0, 255,255,0
        ))).draw(GL_TRIANGLES)
        text.Label('!', font_size=18, color=[0,0,0,255], x=screenpos[0]+14, y=screenpos[1], anchor_x='left', anchor_y='bottom').draw()
        unset_2d_mode(ShapeShader.shader) 
    
    #### """

    def __set_rock_fence(self):
        hori_rocks_num = round(self.width//Rock.ROCK_WIDTH)
        verti_rocks_num = round(self.height//Rock.ROCK_WIDTH)+1
        hori_space = self.width/hori_rocks_num
        verti_space = self.height/verti_rocks_num
        self.rock_coors = []
        for i in range(hori_rocks_num):
            pos1 = self.position + Vector3([(1+i)*hori_space, 0.0, 0.0])
            pos2 = self.position + Vector3([i*hori_space, 0.0, self.height])
            self.rock_coors.append(pos1)
            self.rock_coors.append(pos2)
        for i in range(verti_rocks_num):
            pos1 = self.position + Vector3([0.0, 0.0, i*verti_space])
            pos2 = self.position + Vector3([self.width, 0.0, (1+i)*verti_space])
            self.rock_coors.append(pos1)
            self.rock_coors.append(pos2)

    def __draw_rock_fence(self):
        glUseProgram(ObjectShader.shader)
        Rock.instances[0].batch_render(self.rock_coors)
        glUseProgram(ShapeShader.shader)

    @staticmethod
    def draw_all_selectable():
        for key in MushroomSquare.instances:
            MushroomSquare.instances[key].draw(colorcode = key)

    @staticmethod
    def set_detected(square_ids):
        MushroomSquare.detected_instances = square_ids
        # for square in square_ids:
        #     if square in MushroomSquare.instances and square not in MushroomSquare.detected_instances:
        #         MushroomSquare.detected_instances.append(square)
    
    # @staticmethod
    # def unset_detected(square_ids):
    #     for square in square_ids:
    #         if square in MushroomSquare.instances and square in MushroomSquare.detected_instances:
    #             MushroomSquare.detected_instances.remove(square)
    
    @staticmethod
    def draw_all_warning_sign():
        set_2d_mode()
        for square in reversed(list(MushroomSquare.detected_instances)):
            MushroomSquare.instances[square].__draw_warning_sign()
        unset_2d_mode(ShapeShader.shader)

    @staticmethod
    def set_readable_to_campos(cam_pos, read_dist):
        MushroomSquare.readable_instances = []
        for square in MushroomSquare.instances:
            sqr_dist = distance_3d(cam_pos, MushroomSquare.instances[square].position)
            if sqr_dist < read_dist:
                MushroomSquare.readable_instances.append(square)

    @staticmethod
    def draw_all_readable_names():
        set_2d_mode()
        for square in reversed(list(MushroomSquare.readable_instances)):
            MushroomSquare.instances[square].__draw_name_label()
        unset_2d_mode(ShapeShader.shader)

    @staticmethod
    def draw_all_family_numbers():
        set_2d_mode()
        for square in reversed(list(MushroomSquare.instances)):
            if MushroomSquare.instances[square].state != 0:
                MushroomSquare.instances[square].__draw_family_label()
        unset_2d_mode(ShapeShader.shader)

class ObjectRow:
    def __init__(self, position, max_object, obj_displacement):
        self.position = position
        self.obj_positions = []
        self.indexed_obj = {}
        self.max = max_object
        self.obj_disp = obj_displacement # a Vector3 displacement 

    def get_next_position(self):
        if len(self.obj_positions) > 0:
            prev_pos = self.obj_positions[-1]
            return Vector3([0.0,0.0,0.0]) + prev_pos + self.obj_disp
        else:
            return self.position

    def add_object(self, obj_position, obj_id=None):
        if self.is_full():
            return False
        next_pos = self.get_next_position()
        obj_position[0] = next_pos[0]
        obj_position[1] = next_pos[1]
        obj_position[2] = next_pos[2]
        self.obj_positions.append(obj_position)

        if obj_id:
            self.indexed_obj[obj_id]= next_pos
            # print(list(self.indexed_obj))
        return next_pos

    def shift_row(self, vector, is_field):
        # self.position += vector
        for id in self.indexed_obj:
            Mushroom.move_shroom(id, is_field, vector)
        # for obj_pos in self.obj_positions:
        #     obj_pos += vector

    def is_full(self):
        return self.max == len(self.obj_positions)

    def is_empty(self):
        return 0 == len(self.obj_positions)