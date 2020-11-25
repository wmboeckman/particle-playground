import contextlib
import ctypes
import logging

from OpenGL import GL as gl

log = logging.getLogger(__name__)


@contextlib.contextmanager
def create_vertex_array_object():
    log.debug('creating and binding the vertex array (VAO)')
    vertex_array_id = gl.glGenVertexArrays(1)
    try:
        gl.glBindVertexArray(vertex_array_id)
        yield
    finally:
        log.debug('cleaning up vertex array')
        gl.glDeleteVertexArrays(1, [vertex_array_id])


@contextlib.contextmanager
def create_vertex_buffer():
    with create_vertex_array_object():
        # A triangle
        vertex_data = [-1, -1, 0,
                       1, -1, 0,
                       0, 1, 0]
        attr_id = 0  # No particular reason for 0,
        # but must match layout location in the shader.

        log.debug('creating and binding the vertex buffer (VBO)')
        vertex_buffer = gl.glGenBuffers(1)
        try:
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer)

            array_type = (gl.GLfloat * len(vertex_data))
            sizeof_float = ctypes.sizeof(ctypes.c_float)
            gl.glBufferData(gl.GL_ARRAY_BUFFER,
                            len(vertex_data) * sizeof_float,
                            array_type(*vertex_data),
                            gl.GL_STATIC_DRAW)

            log.debug('setting the vertex attributes')
            gl.glVertexAttribPointer(
                attr_id,  # attribute 0.
                3,  # components per vertex attribute
                gl.GL_FLOAT,  # type
                False,  # to be normalized?
                0,  # stride
                None  # array buffer offset
            )

            # use currently bound VAO
            gl.glEnableVertexAttribArray(attr_id)

            yield
        finally:
            log.debug('cleaning up buffer')
            gl.glDisableVertexAttribArray(attr_id)
            gl.glDeleteBuffers(1, [vertex_buffer])
