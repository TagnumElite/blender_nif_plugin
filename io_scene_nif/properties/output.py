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
    BoolProperty,
    EnumProperty,
    StringProperty,
)
from bpy.types import PropertyGroup


def update_version(self, context):
    print("Test Update Version")


def get_games(self, context):
    print("Getting Games")
    return (
        ('SKYRIM', "Skyrim", "Skyrim game version"),
        ('OBLIVION', "Oblivion", "Oblivion game version"),
    )


class Output(PropertyGroup):
    manual: BoolProperty(
        name="Manual",
        description="Automatic version selection",
        default=True,
        update=update_version,
    )

    game: EnumProperty(
        name="Game",
        description="",
        items=get_games,
        update=update_version,
    )

    nif_version: IntProperty(
        name="Nif Version",
        description="Nif version",
        default=0,
    )

    user_version: IntProperty(
        name="User Version",
        description="user version",
        default=0,
    )

    user_version_2: IntProperty(
        name="User Version 2",
        description="second user version",
        default=0,
    )

    author: StringProperty(
        name="Author",
        description="second user version",
    )

    export_script: StringProperty(
        name="Export Script",
        description="second user version",
    )

    process_script: StringProperty(
        name="Process Script",
        description="second user version",
    )

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
