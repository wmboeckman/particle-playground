import contextlib
import logging
import sys

import glfw
from OpenGL import GL as gl

from particle_playground.gl.matrix import create_mvp
from particle_playground.gl.shader import load_shaders
from particle_playground.gl.vertex import create_vertex_buffer

log = logging.getLogger(__name__)


class GLWindow:
    def __init__(self, width=500, height=400, title='OpenGL Window'):
        with create_main_window(width, height, title) as window:
            self.window = window
            log.info("created main window")
            with create_vertex_buffer():
                with load_shaders() as program_id:
                    log.info("loaded shaders")
                    self.mvp_matrix_id, self.mvp = create_mvp(program_id, width, height)
                    log.info("entering main loop")
                    self.main_loop()

    def main_loop(self):
        while (
                glfw.get_key(self.window, glfw.KEY_ESCAPE) != glfw.PRESS and
                not glfw.window_should_close(self.window)
        ):
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

            # Set the view matrix
            gl.glUniformMatrix4fv(self.mvp_matrix_id, 1, False, self.mvp)

            # Draw the triangle
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

            glfw.swap_buffers(self.window)
            glfw.poll_events()

        log.info("stopping the GL window...")
        del self

    def __del__(self):
        log.info("closed the window")


@contextlib.contextmanager
def create_main_window(width, height, title: str):
    if not glfw.init():
        log.error('failed to initialize GLFW')
        sys.exit(1)
    try:
        log.debug('requiring modern OpenGL without any legacy features')
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        log.debug('opening window')
        window = glfw.create_window(width, height, title, None, None)
        if not window:
            log.error('failed to open GLFW window.')
            sys.exit(2)
        glfw.make_context_current(window)

        log.debug('set background to dark blue')
        gl.glClearColor(0, 0, 0.4, 0)

        yield window

    finally:
        log.debug('terminating window context')
        glfw.terminate()
