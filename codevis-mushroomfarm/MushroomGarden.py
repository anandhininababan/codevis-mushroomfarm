from Mushrooms import *
from MushroomSquare import *
from CouplingPath import *
from Fence import *

class Garden:
    #PATH_WIDTH = 4.0 # width of path connecting mushroomsquares
    INTRSQR_DIST = 13.0 #distance between mushroomsquares
    SQR_DISP = MushroomSquare.MAX_SQR_WIDTH + INTRSQR_DIST
    ROW_SQR_NUM = 2 # amount of mushroomsquares to be located in a row before making a new row
    instances = {}
    readable_instances = []
    def __init__(self, id, name, position, supergarden = None):
        Garden.instances[id] = self
        self.name = name
        self.position = Vector3(position)
        self.squares = []
        self.supergarden = supergarden
        self.subgardens = []
        self.next_sqr_coor = [position[0]+Garden.INTRSQR_DIST*1.5, position[1], position[2]+Garden.INTRSQR_DIST*1.5]
        self.rows = [GardenRow(self.next_sqr_coor, Garden.ROW_SQR_NUM, Vector3([Garden.SQR_DISP, 0.0, 0.0]))]
        self.reset_shape()
        #self.row_count = 0
        self.paths = CouplingPath()
        self.detected = False

    def reset_shape(self):
        squares = self.squares
        subgardens = self.subgardens
        row_widths = [row.get_row_width() for row in self.rows]
        subgard_widths = [sg.width for sg in self.subgardens]
        normalwidth = max(row_widths+subgard_widths) + 2.5 * Garden.INTRSQR_DIST
        
        self.width = float(normalwidth)
        
        self.height = ((2+len(squares)//Garden.ROW_SQR_NUM + len(subgardens))*Garden.INTRSQR_DIST + 
            sum([row.get_row_height() for row in self.rows]) + 
            sum([sg.height for sg in subgardens]))
        self.__set_fences()
        if self.supergarden is not None:
            self.supergarden.reset_shape()
    
    def set_garden_position(self, position):
        move_vector = position - self.position
        self.position += move_vector
        self.paths.shift_paths(move_vector)
        for gard in self.subgardens:
            gard.set_garden_position(gard.position + move_vector)
        for row in self.rows:
            row.shift_row(move_vector)

    def __update_next_coor(self):
        # fills next_sqr_coor a NEW vector3 containing next position
        if not self.rows[-1].is_full():
            self.next_sqr_coor = list(self.rows[-1].get_next_position())
        else:
            self.next_sqr_coor = list(self.rows[-1].position + [0,0,self.rows[-1].get_row_height() + Garden.INTRSQR_DIST])
            self.rows.append(GardenRow(self.next_sqr_coor, Garden.ROW_SQR_NUM, Vector3([Garden.SQR_DISP, 0.0, 0.0])))

    def create_square(self, ref_id, ref_name, ref_type, autoreset=False):
        #self.row_count += 1
        self.__update_next_coor()
        new_sqr = MushroomSquare(ref_id, ref_name, ref_type, self.next_sqr_coor)
        self.squares.append(new_sqr) 
        self.rows[-1].add_square(new_sqr)
        
        ### path making
        # add path node containing the square 
        datanode = self.paths.add_node(new_sqr.position+Vector3([0.0,0.0,0.0]), new_sqr)
        self.paths.add_edge(datanode, new_sqr.position+Vector3([0.0, 0.0, -5.0]))
        # add path node connecting to previous paths
        if len(self.rows[-1].row_objects) == 1: #if first node in row
            if len(self.rows) != 1: # not first row in garden
                #vertical_shift = MushroomSquare.MAX_SQR_HEIGHT + Garden.INTRSQR_DIST
                self.paths.add_edge(new_sqr.position+Vector3([-10.0, 0.0, -5.0]), self.rows[-2].position+Vector3([-10.0, 0.0, -5.0]))
            self.paths.add_edge(new_sqr.position+Vector3([0.0, 0.0, -5.0]), new_sqr.position+Vector3([-10.0, 0.0, -5.0]))
        else:
            prev_coor = self.rows[-1].row_objects[-2].position
            self.paths.add_edge(new_sqr.position+Vector3([0.0, 0.0, -5.0]), Vector3(prev_coor)+Vector3([0.0,0.0,-5.0]))
        ### end path making

        
        if autoreset:
            self.reset_shape() #adjust garden shape to fit new square
        return new_sqr

    def count_sub_level(self):
        if self.subgardens == []:
            return 0
        else:
            return max([gard.count_sub_level() for gard in self.subgardens]) + 1

    def create_subgarden(self, id, name):
        if self.subgardens == []:
            self.next_sqr_coor = list(self.rows[-1].position + [0,0,self.rows[-1].get_row_height() + Garden.INTRSQR_DIST])
        else:
            self.next_sqr_coor = list(self.subgardens[-1].position + [0,0,self.subgardens[-1].height + Garden.INTRSQR_DIST])
        # self.rows.append(GardenRow(self.next_sqr_coor, 1, Vector3([Garden.SQR_DISP, 0.0, 0.0])))
        
        subgarden = Garden(id, name, self.next_sqr_coor, supergarden=self)
        self.subgardens.append(subgarden)
        # self.rows[-1].row_objects.append(subgarden)
        return subgarden



    def draw_garden(self, debug=False, undraw_detected=False):
        if debug:
            self.paths.draw(None,None,debug)
        sel = next((x for x in self.squares if x.state == 1), None)
        if sel is not None:
            couplings = [(sel, couple) for couple in sel.coupling]
            self.paths.draw_all_paths(couplings)
            # for couple in sel.coupling:
            #     self.paths.draw(sel, couple)

        for square in self.squares:
            square.draw(undraw_detected=undraw_detected)
        if not self.detected or not undraw_detected:
            self.draw_fences()
        if sel is not None:
            self.__draw_name_label()
            sel._MushroomSquare__draw_name_label()

    def calculate_fences(self):
        coor1 = self.position + Vector3([0,0,0])
        coor2 = self.position + Vector3([self.width, 0, 0])
        coor3 = self.position + Vector3([self.width, 0, self.height])
        coor4 = self.position + Vector3([0, 0, self.height])
        return [coor1,coor2,coor3,coor4] # calculate the 4 points to draw the fences
        
    def __set_fences(self):
        hori_fence_num = round(self.width//Fence.FENCE_WIDTH)
        verti_fence_num = round(self.height//Fence.FENCE_WIDTH)+1
        hori_space = self.width/hori_fence_num
        verti_space = self.height/verti_fence_num
        self.v_fence_coors = []
        self.h_fence_coors = []
        for i in range(hori_fence_num):
            pos1 = self.position + Vector3([(i)*hori_space, 0.0, 0.0])
            pos2 = self.position + Vector3([i*hori_space, 0.0, self.height])
            self.h_fence_coors.append(pos1)
            self.h_fence_coors.append(pos2)
        for i in range(verti_fence_num):
            pos1 = self.position + Vector3([0.0, 0.0, i*verti_space])
            pos2 = self.position + Vector3([self.width, 0.0, (i)*verti_space])
            self.v_fence_coors.append(pos1)
            self.v_fence_coors.append(pos2)

    def draw_fences(self):
        glUseProgram(ObjectShader.shader)
        Fence.instances[0].batch_render(self.v_fence_coors, True)
        Fence.instances[0].batch_render(self.h_fence_coors, False)
        glUseProgram(ShapeShader.shader)

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

    def __draw_name_label(self):
        screenpos = convert_3dcoor_to_screen(self.position+Vector3([self.width//2, 0, 0]))
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

    @staticmethod
    def set_detected(garden_ids):
        for garden in Garden.instances:
            if garden in garden_ids:
                Garden.instances[garden].detected = True 
            else:
                Garden.instances[garden].detected = False
    
    # @staticmethod
    # def unset_detected(garden_ids):
    #     for garden in garden_ids:
    #         if garden in Garden.instances:
    #             Garden.instances[garden].detected = False 

    @staticmethod
    def draw_all_warning_sign():
        for garden in Garden.instances:
            if Garden.instances[garden].detected:
                Garden.instances[garden].__draw_warning_sign()

    @staticmethod
    def set_readable_to_campos(cam_pos, read_dist):
        Garden.readable_instances = []
        for garden in Garden.instances:
            grd_dist = distance_3d(cam_pos, Garden.instances[garden].position)
            if grd_dist < read_dist:
                Garden.readable_instances.append(garden)

    @staticmethod
    def draw_all_readable_names():
        set_2d_mode()
        for garden in Garden.readable_instances:
            Garden.instances[garden].__draw_name_label()
        unset_2d_mode(ShapeShader.shader)

class GardenRow:
    def __init__(self, position, max_object, obj_displacement):
        self.position = Vector3(position)
        self.row_objects = []
        self.max = max_object
        self.obj_disp = obj_displacement # a Vector3 displacement between objects

    def get_row_height(self):
        if self.row_objects == []:
            return 0
        ans = max(self.row_objects, key=lambda x: x.height).height
        return ans

    def get_row_width(self):
        if self.row_objects == []:
            return 0
        elif len(self.row_objects) == 1:
            return self.row_objects[0].width
        position = self.row_objects[-1].position - self.row_objects[0].position
        width = abs(position[0]) + self.row_objects[-1].width
        return width

    def get_next_position(self):
        if len(self.row_objects) > 0:
            prev_pos = self.row_objects[-1].position
            return prev_pos + self.obj_disp
        else:
            return self.position

    def add_square(self, new_square):
        if self.is_full():
            return False
        next_pos = self.get_next_position()
        if (next_pos != new_square.position):
            new_square.set_drawn_square(position=next_pos)
        self.row_objects.append(new_square)
        return next_pos
    
    def shift_row(self, vector):
        self.position += vector
        for obj in self.row_objects:
            obj.set_drawn_square(position= obj.position + vector)

    def is_full(self):
        return self.max == len(self.row_objects)