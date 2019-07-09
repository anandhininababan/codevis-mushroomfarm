"""import pyglet
from pyglet.gl import *
from pyglet import *
from pyglet.window import *

import tinyblend as blend
import pyshaders as shaders
from pyglbuffers import Buffer
from pyrr import Vector3, Vector4, matrix44, Matrix44

class MyWindow(Window):
    def __init__(self, width, height, title=''):
        super(MyWindow, self).__init__(width, height, title)
        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        self.shader = shaders.from_files_names('shaders/shape_vert.glsl', 'shaders/shape_frag.glsl')
        self.shader.use()
        self.shader.enable_all_attributes()
        self.shader.owned = False
        shaders.transpose_matrices(False)
        self.upload_uniforms()
        self.cubevertices = graphics.vertex_list_indexed(8, 
                    [0,1,2,3,   0,1,5,4,    1,2,6,5,    2,3,7,6,    3,0,4,7,    4,5,6,7], # make 6 quads
                    ('v3f', (
                        50,50,50,   #0
                        50,-50,50,  #1
                        -50,-50,50, #2
                        -50,50,50,  #3
                        50,50,-50,  #4
                        50,-50,-50, #5
                        -50,-50,-50,#6
                        -50,50,-50  #7
                    )), ('c3B', (
                        255,0,0,
                        255,255,255,
                        0,0,255,
                        0,255,0,
                        255,255,0,
                        0,255,255,
                        255,0,255,
                        25,25,25
                    ))
                )

    def upload_uniforms(self):
        unif = self.shader.uniforms
        unif.vp = Matrix44.

    def on_draw(self):
        self.clear()
        self.cubevertices.draw(GL_QUADS)


WINDOW = 400
if __name__ == '__main__':
   MyWindow(WINDOW, WINDOW, 'Pyglet Colored Cube')
   pyglet.app.run()
"""

from shaders import *
from pyglet import *
from pyglet.gl import *
from pyglet.window import key
from pyrr import Vector3, Vector4, matrix44, Matrix44

class MyWindow(window.Window):
    
    def __init__(self, width, height, title=''):
        super(MyWindow, self).__init__(width, height, title)
        self.keys = key.KeyStateHandler()
        self.push_handlers(self.keys)
        gl.glClearColor(0, 0, 0, 1)
        gl.glEnable(gl.GL_DEPTH_TEST)  
        ShapeShader.init(Vector3([-5.0,-5.0,-5.0]))
        self.vl = graphics.vertex_list(4, ('v3f',(
            1000.0, 3.0, 1000.0,
            1000.0, 3.0, -1000.0,
            -1000.0, -3.0, -1000.0,
            -1000.0, -3.0, 1000.0
        )) 
        #,('c3B', (130,0,0,130,0,0,130,0,0,130,0,0))
        )

    def on_draw(self):
        self.clear()
        self.vl.draw(GL_QUADS)

WINDOW = 400
if __name__ == '__main__':
   MyWindow(WINDOW, WINDOW, 'Pyglet Colored Cube')
   pyglet.app.run()