import pygame
import random
from pysmile.game import Game
from pysmile.entity import Entity
from pysmile.components.renderer import RendererComponent
from pysmile.components.transform import TransformComponent
from pysmile.components.exit_on_escape import ExitOnEscape
from pysmile.components.move import MoveComponent
from pysmile.components.key_control import KeyControlComponent
from pysmile.components.collisions.tile_map_collider import TileMapCollider
from pysmile.components.collisions.box_collider import BoxCollider
from pysmile.components.name import NameComponent
from pysmile.tilemap.tilemap import TileMap
from pysmile.tilemap.tileset import TileSet
from pysmile.tilemap.tilemap_renderer import TileMapRenderer
from pysmile.renderers.tile_renderer import TileRenderer
from pysmile.math.vector2 import Vector2


class PyDungeons:
    @staticmethod
    def build_wall_rect(map, rect):
        for y in range(rect.height):
            if y == 0 or y == rect.height-1:
                for x in range(0, rect.width):
                    map[rect.y + y][rect.x + x] = ["wall_mid"]
                    map[rect.y + y-1][rect.x + x] = ["floor_1", "wall_top_mid"]
            if y == rect.height - 1:
                continue
            map[rect.y + y][rect.x] = ["floor_1", "wall_side_mid_right"]
            map[rect.y + y][rect.right-1] = ["floor_1", "wall_side_mid_left"]

        map[rect.y-1][rect.x] = ["floor_1", "wall_corner_top_left"]
        map[rect.y][rect.x] = ["wall_corner_left"]

        map[rect.y - 1][rect.right-1] = ["floor_1", "wall_corner_top_right"]
        map[rect.y][rect.right-1] = ["wall_corner_right"]

        map[rect.bottom-2][rect.x] = ["floor_1", "wall_corner_bottom_left"]
        map[rect.bottom-2][rect.right - 1] = ["floor_1", "wall_corner_bottom_right"]

    @staticmethod
    def start():
        pygame.init()
        pygame.display.set_caption('PyDungeon')
        size = (640, 480)
        game = Game()
        game.setup_default_components(size)
        scene = game.scene

        tilemap = Entity()
        scene.add_entity(tilemap)
        tilemap.add_component(NameComponent("tilemap"))

        tilemap.add_component(TransformComponent(Vector2(0, 0)))

        ts = TileSet()
        ts.load("./assets/tileset.png", "./assets/tileinfo.info")
        tm = TileMap(ts, size)
        mp = [[["floor_"+str(random.randrange(1, 8))] for _ in range(24)] for _ in range(24)]
        PyDungeons.build_wall_rect(mp, pygame.Rect(2, 2, 10, 10))
        tm.load_letters(mp)
        tilemap.add_component(tm)
        tilemap.add_component(TileMapCollider(tm, ["wall_mid", "wall_side_mid_right", "wall_side_mid_left"]))
        tilemap.add_component(RendererComponent(TileMapRenderer(), size))

        player = Entity()
        scene.add_entity(player)
        player.add_component(NameComponent("player"))

        key_bindings = [[pygame.K_a], [pygame.K_d], [pygame.K_w], [pygame.K_s]]

        player.add_component(MoveComponent(1, 2))
        player.add_component(KeyControlComponent(key_bindings))
        player.add_component(TransformComponent(Vector2(100, 100)))
        player.add_component(BoxCollider((16*2, 22*2), Vector2(0, 12)))
        player.add_component(RendererComponent(TileRenderer(ts.tiles["knight_f_idle_anim"], ts), (16*2, 28*2)))

        game.add_component(ExitOnEscape())

        game.run()
