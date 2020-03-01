""" Nif User Interface, custom nif properties for objects"""

# ***** BEGIN LICENSE BLOCK *****
#
# Copyright © 2016, NIF File Format Library and Tools contributors.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#
#    * Neither the name of the NIF File Format Library and Tools
#      project nor the names of its contributors may be used to endorse
#      or promote products derived from this software without specific
#      prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# ***** END LICENSE BLOCK *****


import bpy
from bpy.props import PointerProperty, IntProperty, EnumProperty
from bpy.types import PropertyGroup
from pyffi.formats.nif import NifFormat


def _game_to_enum(name):
    symbols = ":,'\" +-*!?;./="
    table = str.maketrans(symbols, "_" * len(symbols))
    enum = name.upper().translate(table).replace("__", "_")
    return enum


_game_dict = dict()

for game in reversed(sorted(NifFormat.games.keys())):
    if game == '?':
        continue
    _game_dict[_game_to_enum(game)] = game


def _update_game(scene, context):
    scene.nif_version = NifFormat.games[_game_dict[scene.nif_game]][0]


class Scene(PropertyGroup):

    @classmethod
    def register(cls):
        bpy.types.Scene.niftools_scene = PointerProperty(
            name='Niftools Scene Property',
            description='Additional scene properties used by the Nif File Format',
            type=cls
        )

        cls.nif_game = EnumProperty(
            items=[  # TODO: Fetch games main version instead in new PyFFI version
                (_id, game, "Export for " + game)
                # implementation note: reversed makes it show alphabetically
                # (at least with the current blender)
                for _id, game in _game_dict.items()
            ],
            name="Game",
            description="For which name to export.",
            default='OBLIVION',
            update=_update_game,
        )

        cls.nif_version = IntProperty(
            name='Nif Version',
            default=50528269,
            min=-1,
            description=""
        )  # TODO: Change this to StringProperty

        cls.user_version = IntProperty(
            name='User Version',
            default=0,
            min=0,
            description="",
        )

        cls.bethesda_version = IntProperty(
            name='Bethesda Version',
            default=0,
            min=0,
            description="",
        )

    @classmethod
    def unregister(cls):
        del bpy.types.Scene.niftools_scene
