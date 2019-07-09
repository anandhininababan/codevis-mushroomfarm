import pyglet
from pyglet import graphics
from pyglet.gl import *
from pyglet.text.formats.structured import ImageElement
from Mushrooms import *
from MushroomSquare import *
from MushroomGarden import *
from shaders import *
from DBConnector import *



class ShroomGUI:
    def __init__(self, width, height, interface_width, window, smell_score = 100, position = [0, 0], title="abcdefghijklmno"):
        
        self.width = width
        self.height = height

        #iw = self.cnvCoor((interface_width,0))[0]
        iw = interface_width
        self.interface_width = iw
        ih = self.height
        self.position = position
        self.fore_batch = graphics.Batch()
        self.back_batch = graphics.Batch()
        background = pyglet.graphics.OrderedGroup(0)
        foreground = pyglet.graphics.OrderedGroup(1)
        self.objectlist = []
        self.strategy_activity = []
        self.detected_shroom = {}
        self.detected_square = {}
        self.detected_garden = {}

        self.interface_box = self.back_batch.add(4, GL_QUADS, background, ('v2f',(
            position[0], position[1],
            position[0]+iw, position[1],
            position[0]+iw, position[1]+ih,
            position[0], position[1]+ih
        )), ('c4B', (
            255,255,255,255,
            255,255,255,255,
            255,255,255,255,
            255,255,255,255
        )))
        db = DBConnector()
        gui_textures = db.execute("SELECT * FROM visualpropertypath WHERE type = 'gui texture'")
        self.texture_paths = {}
        for texture in gui_textures:
            self.texture_paths[texture[1]] = texture[3]        
        del db

        # project title
        self.title = pyglet.text.Label(title,
                                        font_size=17,
                                        x = position[0]+10, y=position[1]+ih-10, width = iw-20, 
                                        anchor_x="left", anchor_y="top", color=(0,0,0,255), 
                                        align="center", multiline=True, batch= self.fore_batch)


        #code score
        self.scoreboard = pyglet.image.load(self.texture_paths['score'])
        self.scoreboard.anchor_y = self.scoreboard.height//2
        self.scoreboard.anchor_x = self.scoreboard.width//2
        self.score_pos = (position[0]+iw//2, position[1] + ih - self.scoreboard.height//2-30-self.title.content_height)
        self.score = pyglet.text.Label("", 
                                font_size = 42,
                                x = self.score_pos[0]-5, y= self.score_pos[1]+17,
                                anchor_x='center', anchor_y='center', color=(255,255,255,255), batch = self.fore_batch)
        self.set_score(smell_score)
        
        
        # making detection strategies box
        self.strategies_box = GUIBox(8, ih//2-12-iw//2-self.title.content_height, iw-16, iw+14, self.back_batch, foreground)
        strategieslabel = pyglet.text.Label ("Code Smell", font_name='Calibri',font_size=18, x=10, y = ih//2+iw//2+8-self.title.content_height, color=(0,0,0,255), batch=self.fore_batch, group=foreground)
        self.checkbox = pyglet.image.load(self.texture_paths['checkbox empty'])
        self.checkedbox = pyglet.image.load(self.texture_paths['checkbox checked'])
       

    def create_detection_strategies(self, strategies, detected_methods, detected_references, detected_package):
        self.detector = DetectionStrategies(strategies, detected_methods, detected_references, detected_package)
        self.init_strategies()
        for strat in strategies:
            self.add_strategies(strat[0], strat[1])
        self.finalize_strategies()

    def init_strategies(self, strategylists=[]):
        self.strategy_activity = []
        for strat in strategylists:
            self.strategy_activity.append([strat, False])

    def add_strategies(self, stratId, strategyname):
        self.strategy_activity.append([strategyname, False])
    
    def finalize_strategies(self):
        iw, ih = self.interface_width, self.height
        recloc = pyglet.resource.FileLocation('./')
        strat_string = "".join(["<p> <img src='{}'>{}</p>".format(self.texture_paths['checkbox empty'], x) for x,_ in self.strategy_activity])+"<br>"
        strat_doc = pyglet.text.decode_html(strat_string, location = recloc)
        self.strategies = pyglet.text.layout.IncrementalTextLayout(strat_doc, iw-20, iw+8, multiline=True, batch=self.fore_batch)
        endchar = self.strategies.get_position_on_line(self.strategies.get_line_count()-1, 999)
        #print(self.strategies.document.get_style())
        self.strategies.document.set_style(0, endchar, {'font_name':'calibri', 'font_size':15, 'line_spacing':20})
        self.strategies.x = 10
        self.strategies.y = ih//2-8-iw//2-self.title.content_height

    def set_title(self, title):
        self.title.text = title

    def set_score(self, score):
        self.score.text = str(score)
    
    def inside_control_box(self, x, y):
        return True ## testing

    def GUI_scroll(self, x, y, scroll_x, scroll_y):
        if self.strategies_box.is_inside(x, y):
            self.strategies.view_y += 10 * scroll_y
        # elif self.history_box.is_inside(x, y):
        #     self.log.view_y += 10 *scroll_y

    def GUI_click(self, x, y):
        if self.strategies_box.is_inside(x,y):
            #testing
            self.strategies.begin_update()
            clickedline = self.strategies.get_line_from_point(x,y)
            strategyId = clickedline + 1 
            linehead = self.strategies.get_position_from_line(clickedline)
            if self.strategy_activity[clickedline][1]:
                self.strategy_activity[clickedline][1] = False
                newbox = ImageElement(self.checkbox)
            else:
                self.strategy_activity[clickedline][1] = True
                newbox = ImageElement(self.checkedbox)
                
            active_detectors = [id+1 for id in range(len(self.strategy_activity)) if self.strategy_activity[id][1]]
            shrooms, squares, gardens = self.detector.get_detected(active_detectors)
            Mushroom.set_detected(shrooms)
            MushroomSquare.set_detected(squares)
            Garden.set_detected(gardens)

            self.strategies.document.delete_text(linehead, linehead+1)
            self.strategies.document.insert_element(linehead, newbox)
            self.strategies.end_update()
   
    def draw(self):
        set_2d_mode()                                 
        self.back_batch.draw()
        self.scoreboard.blit(*self.score_pos)
        self.fore_batch.draw()
        unset_2d_mode(ShapeShader.shader)


class GUIBox:
    def __init__(self, x, y, width, height, batch, group=None, color=[0,0,0], filled = False, drawn=True):
        self.x = x 
        self.y = y 
        self.width = width
        self.height = height
        if drawn:
            if filled:        
                self.shape = batch.add(4, GL_QUADS, group, ('v2f', (
                    x,y, x+width,y, x+width,y+height, x,y+height
                )),('c3B', (
                    *color, *color, *color, *color
                )))
            else:
                self.shape = batch.add_indexed(4, GL_LINES, group,
                [0,1,1,2,2,3,3,0],
                ('v2f', (
                    x,y, x+width,y, x+width,y+height, x,y+height
                )), ('c3B', (
                    *color, *color, *color, *color
                )))

    def is_inside(self, x, y):
        return x > self.x and x < self.x+self.width and y > self.y and y < self.y+self.height

class DetectionStrategies:
    method_strategy = {}
    reference_strategy = {}
    package_strategy = {}

    # tabel strategies berisi kolom: ID, name, type
    # detected_object berisi object ID, strategy ID
    def __init__(self, strategies, detected_methods, detected_references, detected_packages):
        for strat in strategies:
            if strat[2] == "method":
                self.method_strategy[strat[0]] = set()
            elif strat[2] == "reference":
                self.reference_strategy[strat[0]] = set()
            else:
                self.package_strategy[strat[0]] = set()
        for det in detected_methods:
            self.method_strategy[det[1]].add('m'+str(det[0]))
        for det in detected_references:
            self.reference_strategy[det[1]].add(det[0])
        for det in detected_packages:
            self.package_strategy[det[1]].add(det[0])

    def get_detected(self, strategy_id_list):
        detected_methods = []
        detected_references = []
        detected_packages = []

        for strat_id in strategy_id_list:
            if strat_id in self.method_strategy:
                detected_methods.append(self.method_strategy[strat_id])
            elif strat_id in self.reference_strategy:
                detected_references.append(self.reference_strategy[strat_id])
            elif strat_id in self.package_strategy:
                detected_packages.append(self.package_strategy[strat_id])

        if detected_methods:
            detected_methods = list(detected_methods[0].intersection(*detected_methods[1:]))
        if detected_references:
            detected_references = list(detected_references[0].intersection(*detected_references[1:]))
        if detected_packages:
            detected_packages = list(detected_packages[0].intersection(*detected_packages[1:]))
            

        return detected_methods, detected_references, detected_packages
