#version 330
in layout(location = 0) vec3 position;

uniform mat4 vp;
uniform mat4 model;

void main()
{
    gl_Position = vp *  vec4(position, 1.0f);
}
