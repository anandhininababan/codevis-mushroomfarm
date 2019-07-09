import time
import pyglet
from pyglet import graphics, clock
from pyglet.gl import *
from pyglet.window import *
from pyrr import Vector3, Vector4, matrix44, Matrix44
from Mushrooms import *
from MushroomSquare import *
from MushroomGarden import *
from CouplingPath import *
from Rock import *
import shaders
from shaders import *
from DBConnector import *
import numpy
from GUI import ShroomGUI
import threading


class MyWindow(pyglet.window.Window):
    GROUND_COLOR = [0.0,0.5,0.2,1.0]
    DATABASE_NAME = DBConnector.DATABASE_NAME
    DEFAULT_CAMPOS = [0.0, 25.0, -30.0]
    DEFAULT_CAMLOOKAT = [0.0, 0.0, 0.0]
    DEFAULT_SPEED = 3
    OVERVIEW_SPEED = 6
    # OVERVIEW_CAMPOS = [0.0, 75.0, -20.0]
    # OVERVIEW_CAMLOOKAT = [0.0, 45.0, 0.0]
    DEF_TO_OVERVIEW = (Vector3([0.0, 50.0, 10.0]), Vector3([0.0, 45.0, 0.0]))
    camPos = Vector3([0.0, 25.0, -30.0])
    camLookAt = Vector3([0.0, 0.0, 0.0])
    camSpeed = 3
    SHROOM_READ_DIST = 35
    SQR_READ_DIST = 70
    GARD_READ_DIST = 150
    #interface_width = part to the left of the screen to use
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        self.interface_width = self.width//5

        #self.set_minimum_size(400, 300)
        glClearColor(0.0, 0.6, 0.8, 0.0)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_LINE_SMOOTH_HINT, GL_DONT_CARE)
        #setup 2d drawing
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, 0, self.height)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        self.interface = ShroomGUI(self.width, self.height, self.interface_width, self)
        ShapeShader.init(self.camPos, self.width/self.height)
        ObjectShader.init(self.camPos, self.width/self.height)

        self.mushrooms = []
        self.init_textures(MyWindow.DATABASE_NAME)
        
        self.rocks = []
        self.rocks.append(Rock('textures/rocktexture.jpg'))
        self.fences = []
        self.fences.append(Fence('textures/woodtexture.jpg'))
        
        self.gardens, new_pos = self.create_from_database(MyWindow.DATABASE_NAME)

        clock.schedule_interval(self.update, 1.0/30)

        self.selected_object = None
        self.overview_mode = False
        self.frame_counter = 0

        if self.gardens:
            # new_pos = (self.gardens[0].position + self.gardens[-1].position + [self.gardens[-1].width, 0, 0])/2 + [0, 25, 0]
            self.camPos = new_pos
            self.camLookAt = self.camPos + [0, -25, 30]
            self.on_key_press(key.T, None)

    def rotateCam(self, axis, dtheta):
        rotation_mat = matrix44.create_from_axis_rotation(axis, dtheta)
        self.camLookAt -= self.camPos
        newvec = Vector4.from_vector3(self.camLookAt, 1.0)
        newvec = rotation_mat.dot(newvec)
        self.camLookAt = Vector3.from_vector4(newvec)[0]
        self.camLookAt += self.camPos

    def update(self,dt, changed=False):
        self.frame_counter = (self.frame_counter + 1)%10

        if self.keys[key.W]:    #forward
            self.camPos[2] += self.camSpeed
            self.camLookAt[2] += self.camSpeed
            changed = True
        elif self.keys[key.S]:  #backward
            self.camPos[2] -= self.camSpeed
            self.camLookAt[2] -= self.camSpeed
            changed = True
        elif self.keys[key.D]:  #left
            self.camPos[0] -= self.camSpeed
            self.camLookAt[0] -= self.camSpeed
            changed = True
        elif self.keys[key.A]:  #right
            self.camPos[0] += self.camSpeed
            self.camLookAt[0] += self.camSpeed
            changed = True
        elif self.keys[key.Q] and not self.overview_mode: # going down
            if self.camPos[1] > 3: # don't go too low
                self.camPos[1] -= self.camSpeed
                self.camLookAt[1] -= self.camSpeed
                changed = True
        elif self.keys[key.E] and not self.overview_mode: # going up
            self.camPos[1] += self.camSpeed
            self.camLookAt[1] += self.camSpeed
            changed = True
        # else:  # uncomment this section to enable looking up and looking down
        #     direction = self.camLookAt - self.camPos
            # turning_limit = direction[2] < 1
            # if self.keys[key.Z] and not (turning_limit and direction[1]>0):
            #     self.rotateCam([1.0,0.0,0.0],0.1)
            #     changed = True
            # elif self.keys[key.C] and not (turning_limit and direction[1]<0):
            #     self.rotateCam([1.0,0.0,0.0],-0.1)
            #     changed = True

        if changed:    #update camera
            set_shader_camera(self.camPos, self.camLookAt[:3])
            readable_shroom = [sh for sh in Mushroom.get_all_shroom_position() if distance_3d(sh, self.camPos) < self.SHROOM_READ_DIST]
            Mushroom.set_readable(readable_shroom)
            MushroomSquare.set_readable_to_campos(self.camPos, self.SQR_READ_DIST)
            Garden.set_readable_to_campos(self.camPos, self.GARD_READ_DIST)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.T: #toggle overview mode (camera looking down from a high place)
            self.camPos += self.DEF_TO_OVERVIEW[0] if not self.overview_mode else -self.DEF_TO_OVERVIEW[0]
            self.camLookAt += self.DEF_TO_OVERVIEW[1] if not self.overview_mode else -self.DEF_TO_OVERVIEW[1]
            self.camSpeed = self.OVERVIEW_SPEED if not self.overview_mode else self.DEFAULT_SPEED
            self.overview_mode = self.overview_mode == False
        elif symbol == key.R:   #reset camera to starting position
            self.camPos = Vector3(self.DEFAULT_CAMPOS)
            self.camLookAt = Vector3(self.DEFAULT_CAMLOOKAT)
            self.camSpeed = self.DEFAULT_SPEED
            self.overview_mode = False
        elif symbol == key.ESCAPE:
            self.close()
        self.update(1.0/30, True)

    def on_draw(self):
        self.clear()
        #3d mode
        # shapes
        glEnable(GL_DEPTH_TEST)

        glUseProgram(ShapeShader.shader)
        ShapeShader.use_color(self.GROUND_COLOR)
        graphics.vertex_list(4, ('v3f',(
            self.camPos[0] + 500.0, -0.1, self.camPos[2] + 500.0,
            self.camPos[0] + 500.0, -0.1, self.camPos[2] - 500.0,
            self.camPos[0] - 500.0, -0.1, self.camPos[2] - 500.0,
            self.camPos[0] - 500.0, -0.1, self.camPos[2] + 500.0
        )) 
        ).draw(GL_QUADS) #draw the ground

        if self.frame_counter < 5:
            undraw_detected = False
        elif self.frame_counter < 10:
            undraw_detected = True
        
        for gard in self.gardens:
            gard.draw_garden(undraw_detected=undraw_detected)
        
        ## objects
        glUseProgram(ObjectShader.shader)
        Mushroom.draw_all_shroom(undraw_detected=undraw_detected)
        Rock.draw_all_rock()

        #2d
        glDisable(GL_DEPTH_TEST)
        glUseProgram(0)
        # MushroomSquare.draw_all_warning_sign()
        MushroomSquare.draw_all_readable_names()
        MushroomSquare.draw_all_family_numbers()
        # Garden.draw_all_warning_sign()
        Garden.draw_all_readable_names()
        self.interface.draw()
        
    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if x < self.interface_width:
            self.interface.GUI_scroll(x, y, scroll_x, scroll_y)

    def on_mouse_press(self, x, y, button, modifiers):
        # render selection codes
        glUseProgram(ShapeShader.shader)
        if x >= self.interface_width:   # a click on 3d world
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            MushroomSquare.draw_all_selectable()

            # read pixel at x,y
            rgb = (GLubyte * 4)(0)
            glReadPixels(x, y, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE, rgb)
            
            # the code from read pixels is the object selectable ID (currently only squareID as only squares are selectable)
            # set selected_object to it if code exist in square instances, else set to None
            rgbcode = rgb[0] * 256 + rgb[1]
            if self.selected_object is not None:
                self.selected_object.set_unselect()
                self.selected_object = None
            if rgbcode in MushroomSquare.instances:
                self.selected_object = MushroomSquare.instances[rgbcode]
                self.selected_object.set_selected()
        else:   # let GUI handle clicks on GUI
            self.interface.GUI_click(x,y)

    def init_textures(self, database):
        db = DBConnector(database)
        textures = db.execute('SELECT * FROM visualpropertypath WHERE type = "shroom texture"')
        db_name_map = { 
            'RedField': 'rf', 
            'RedMethod': 'rm', 
            'YellowField': 'yf', 
            'YellowMethod': 'ym', 
            'BlueField': 'bf', 
            'BlueMethod': 'bm', 
            'GreenField': 'gf', 
            'GreenMethod': 'gm'}
        threads = []
        for text in textures:
            if text[1] not in db_name_map:
                continue
            else:
                # def parallel_create_Mushroom(outputlist, name, code):
                #     outputlist.append(Mushroom(name, code))
                # threads.append(GeneralThread(parallel_create_Mushroom, self.mushrooms, text[3], db_name_map[text[1]]))
                # threads[-1].start()
                code = db_name_map[text[1]]
                loop = 3 if code[1] == 'm' else 1
                for i in range(loop):
                    self.mushrooms.append(Mushroom(text[3], code, i))
        # for t in threads:
        #     t.join()
        # print(self.mushrooms)
    
    

    def create_from_database(self, database):
        gardens = []
        squares = {}
        db = DBConnector(database)
        project = db.execute("SELECT * from project")
        self.interface.set_title(project[0][2])
        del project
        methods = db.execute('SELECT * from method')
        fields = db.execute('SELECT * from field')
        refs = db.execute('SELECT * from reference')
        packs = db.execute('SELECT * FROM package')
        inherit = db.execute('SELECT * from inheritancerelationship')
        coupling = db.execute('SELECT * from couplingrelationship')
        packinpack = db.execute('SELECT * from packageinpackage')
        map_db_names = {'concrete class':'br', 'abstract class':'b', 'interface':'g', 'private':'r', 'default':'y', 'protected':'b', 'public':'g'}
        # create packages (garden)
        supermostgardens = []
        
        packTree = packageTree(packs, packinpack) #create package dependency tree
        packs = packTree.topological_sort() #sort tree to a list
        
        for pack in packs: 
            packparent = packTree.get_parent_id(pack[0])
            if packparent is None:
                move = 0 if supermostgardens == [] else supermostgardens[-1].position[0] + supermostgardens[-1].width + 10
                newgard = Garden(pack[0], pack[1], [move, 0.0, 0.0])
                gardens.append(newgard)
                supermostgardens.append(newgard)
            else:
                newgard = Garden.instances[packparent].create_subgarden(pack[0], pack[1])
                gardens.append(newgard)

            #create squares
            for ref in refs:
                if ref[1] == pack[0]: #asumsi ref[1] dan packs[i][0] is Package_id 
                    sq = gardens[-1].create_square(ref[0], ref[2], map_db_names[ref[3]])
                    squares[ref[0]] = sq
                    #fill square with shrooms
                    for method in methods:
                        if method[1] == ref[0]: # inReference == ref.elementid      
                            size = '0' if method[4] <= 10 else ('1' if method[4]<=30 else '2')
                            stype = map_db_names[method[3]] + 'm' + size
                            sq.add_shroom(method[0], method[2], stype, False)
                    for field in fields:
                        if field[1] == ref[0]:
                            stype = map_db_names[field[3]] + 'f0'
                            sq.add_shroom(field[0], field[2], stype, True)
                    sq.reset_shape()
            gardens[-1].reset_shape()
        # set square child and coupling
        for rel in inherit:
            child = rel[0]
            parent = rel[1]
            if parent in squares:
                squares[parent].add_child(squares[child])
        for rel in coupling:
            if rel[0] in squares:
                squares[rel[0]].add_coupling(squares[rel[1]])
        #clean db results
        del methods, fields, refs, packs, inherit, coupling, packinpack

        # add GUI elements
        project = db.execute('SELECT * FROM project')
        detectors = db.execute('SELECT * FROM detectionstrategy')
        detected_method = db.execute('SELECT * FROM detectedmethod')
        detected_reference = db.execute('SELECT * FROM detectedreference')
        detected_package = db.execute('SELECT * FROM detectedpackage')
        # log = db.execute('SELECT * from history')
        #set score
        self.interface.set_score(project[0][3])
        #set strategies
        self.interface.create_detection_strategies(detectors, detected_method, detected_reference, detected_package)
        
        starting_campos = (supermostgardens[-1].position + supermostgardens[0].position + [supermostgardens[-1].width, 50, 0])/2
        return gardens, starting_campos


class packageTree:
    def __init__(self, packages, pack_in_pack):
        self.nodes = {}
        # self.superpackages = {}
        
        self.create_nodes(packages)
        self.make_tree(pack_in_pack)


    def create_nodes(self, packages):
        for pack in packages:
            self.nodes[pack[0]] = packageNode(pack[0], pack)

    def make_tree(self, pack_in_pack):
        for pip in pack_in_pack:
            # self.superpackages[pip[0]] = pip[1]
            if pip[0] in self.nodes:
                container = pip[1]
                contained = pip[0]
                self.nodes[container].child.append(self.nodes[contained])
                self.nodes[contained].parent = self.nodes[container]
                
    def get_parent_id(self, pack_id):
        if pack_id in self.nodes:
            if self.nodes[pack_id].parent is not None:
                return self.nodes[pack_id].parent.id
        return None

    def topological_sort(self):
        sortedlist = []
        for node in self.nodes:
            if self.nodes[node].level() == 0:
                self.nodes[node].top_sort(sortedlist)
        return sortedlist
        # temp = sorted([self.nodes[k] for k in self.nodes], key=lambda x:x.level())
        # return [node.value for node in temp]
    

class packageNode:
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.parent = None
        self.child = []

    def level(self):
        if self.parent is None:
            return 0
        else:
            return self.parent.level()+1
    
    def top_sort(self, outputlist):
        outputlist.append(self.value)
        for child in self.child:
            child.top_sort(outputlist)




if __name__ == "__main__":
    screen = pyglet.canvas.get_display().get_default_screen()
    width = screen.width
    height = screen.height
    ShaderAttributes.set_screen_size(width, height)
    window = MyWindow(screen=screen, fullscreen=True)
    pyglet.app.run()