import logging

import coloredlogs

from particle_playground.gl.window import GLWindow
from particle_playground.log import LogLevel

log = logging.getLogger(__name__)


class Program:
    def __init__(self, log_level: LogLevel = LogLevel.INFO):
        # setup logging
        coloredlogs.install(level=int(log_level.value))
        # start the OpenGL Window...
        self.gl_win = GLWindow(title='Particle Playground')

    def __del__(self):
        log.info("exiting the program...")