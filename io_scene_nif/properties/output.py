# ***** BEGIN LICENSE BLOCK *****
#
# Copyright © 2005-2015, NIF File Format Library and Tools contributors.
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
from bpy.props import (
    PointerProperty,
    IntProperty,
    EnumProperty,
    StringProperty,
)
from bpy.types import PropertyGroup
from pyffi.formats.nif import NifFormat


def update_version(self, context):
    print("Test Update Version")


def translate_name(name):
    symbols = ":,'\" +-*!?;./="
    table = str.maketrans(symbols, "_" * len(symbols))
    t_name = name.upper().translate(table).replace("__", "_")
    return t_name


def get_games(self, context):
    games = set()
    for name in reversed(sorted(NifFormat.games.keys())):
        if name == '?':
            continue
        games.add((translate_name(name), name, "Export for " + name))
    return games


version = {
    translate_name(game): versions[-1] for game, versions in NifFormat.games.items() if game != '?'
}


def update_game(self, context):
    sc = context.scene.niftools_output_props
    sc.nif_version = version[sc.game]


class Output(PropertyGroup):
    game: EnumProperty(
        name="Game",
        description="The game for export and version",
        items=get_games,
        update=update_game,
    )

    nif_version: IntProperty(
        name="Nif Version",
        description="Nif version",
        default=0,
        update=update_version,
    )

    user_version: IntProperty(
        name="User Version",
        description="user version",
        default=0,
        update=update_version,
    )

    user_version_2: IntProperty(
        name="User Version 2",
        description="second user version",
        default=0,
        update=update_version,
    )

    author: StringProperty(
        name="Author",
        description="Author of the mesh",
    )

    export_script: StringProperty(
        name="Export Script",
        default="Blender Nif Plugin (Export)",
    )

    process_script: StringProperty(
        name="Process Script",
        default="PyFFI (Export)",
    )

    versions = version

    @classmethod
    def register(cls):
        bpy.types.Scene.niftools_output_props = PointerProperty(
            name='Niftools Output Property',
            description='Output properties used by the Nif File Format',
            type=cls
        )

    @classmethod
    def unregister(cls):
        del bpy.types.Scene.niftools_output_props
