import contextlib
import logging
import sys

from OpenGL import GL as gl

log = logging.getLogger(__name__)


@contextlib.contextmanager
def load_shaders():
    shaders = {
        gl.GL_VERTEX_SHADER: '''\
        #version 330 core
        layout(location = 0) in vec3 vertexPosition_modelspace;
        uniform mat4 MVP;
        void main() {
            gl_Position = MVP * vec4(vertexPosition_modelspace, 1);
        }
    ''',
        gl.GL_FRAGMENT_SHADER: '''\
        #version 330 core
        out vec3 color;
        void main() {
          color = vec3(1,0,0);
        }
    '''}
    log.debug('creating the shader program')
    program_id = gl.glCreateProgram()
    shader_ids = []
    try:
        for shader_type, shader_src in shaders.items():
            shader_id = gl.glCreateShader(shader_type)
            gl.glShaderSource(shader_id, shader_src)

            log.debug(f'compiling the {shader_type} shader')
            gl.glCompileShader(shader_id)

            # check if compilation was successful
            result = gl.glGetShaderiv(shader_id, gl.GL_COMPILE_STATUS)
            nlog = gl.glGetShaderiv(shader_id, gl.GL_INFO_LOG_LENGTH)
            if nlog:
                log_msg = gl.glGetShaderInfoLog(shader_id)
                log.error(log_msg)
                sys.exit(10)

            gl.glAttachShader(program_id, shader_id)
            shader_ids.append(shader_id)

        log.debug('linking shader program')
        gl.glLinkProgram(program_id)

        # check if linking was successful
        result = gl.glGetProgramiv(program_id, gl.GL_LINK_STATUS)
        nlog = gl.glGetProgramiv(program_id, gl.GL_INFO_LOG_LENGTH)
        if nlog:
            log_msg = gl.glGetProgramInfoLog(program_id)
            log.error(log_msg)
            sys.exit(11)

        log.debug('installing shader program into rendering state')
        gl.glUseProgram(program_id)
        yield program_id
    finally:
        log.debug('cleaning up shader program')
        for shader_id in shader_ids:
            gl.glDetachShader(program_id, shader_id)
            gl.glDeleteShader(shader_id)
        gl.glUseProgram(0)
        gl.glDeleteProgram(program_id)
