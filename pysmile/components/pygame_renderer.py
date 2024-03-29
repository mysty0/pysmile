import pygame
from .renderer import RendererComponent
from OpenGL.GL import *
from pysmile.gl.gl_texture import GLTexture


class PyGameRendererComponent(RendererComponent):
    def __init__(self, renderer, size, static=False, shader=None):
        """
        Render pygame surface to OpenGL display
        :param renderer: renderer that will be used to render entity
        :param size: entity's size that will be displayed
        """
        super().__init__(renderer, size)
        self.shader = shader
        self.displaylist = None
        self.texture = None
        self.static = static

    def render(self, rect, entity):
        if self.renderer.need_redraw:
            if self.texture is not None:
                glDeleteTextures([self.texture])

            img = self.renderer.render(entity, rect)
            w, h = img.get_size()
            self.texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            data = pygame.image.tostring(img, "RGBA", 1)
            glTexImage2D(GL_TEXTURE_2D, 0, 4, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

            self.displaylist = GLTexture.create_tex_dl(self.texture, w, h)

            if self.static:
                self.renderer.need_redraw = False

        glPushMatrix()
        glColor4fv((1, 1, 1, 1))
        glTranslate(rect.x, rect.y, 0)
        glCallList(self.displaylist)
        glPopMatrix()
