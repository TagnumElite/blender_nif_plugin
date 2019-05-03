"""Blender Plug-in for Nif import and export."""

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

import os
import sys

import bpy
import bpy.props


# Python dependencies are bundled inside the io_scene_nif/dependencies folder
_dependencies_path = os.path.join(os.path.dirname(__file__), "dependencies")
if _dependencies_path not in sys.path:
    sys.path.append(_dependencies_path)
    print(sys.path)
del _dependencies_path

from io_scene_nif import properties, operators, ui
from io_scene_nif.utility.nif_settings import NifSettings
from io_scene_nif.utility.nif_logging import NifLog

# noinspection PyBroadException
try:
    from io_scene_nif.utility import nif_debug
    nif_debug.start_debug()
except:
    print("Failed to load debug module")

# Blender addon info.
bl_info = {
    "name": "NetImmerse/Gamebryo nif format",
    "description": "Import and export files in the NetImmerse/Gamebryo nif format (.nif)",
    "author": "NifTools Team",
    "version": (3, 0, 0),  # can't read from VERSION, blender wants it hardcoded
    "blender": (2, 80, 7),
    "api": 39257,
    "location": "File > Import-Export",
    "warning": "non functional, port to blender 2.8 still in progress",
    "wiki_url": "https://blender-nif-plugin.readthedocs.io/",
    "tracker_url": "https://github.com/niftools/blender_nif_plugin/issues",
    "support": "COMMUNITY",
    "category": "Import-Export"
}


# noinspection PyUnusedLocal
def menu_func_import(self, context):
    self.layout.operator(operators.nif_import_op.NifImportOperator.bl_idname, text="NetImmerse/Gamebryo (.nif)")


# noinspection PyUnusedLocal
def menu_func_export(self, context):
    self.layout.operator(operators.nif_export_op.NifExportOperator.bl_idname, text="NetImmerse/Gamebryo (.nif)")


def register():
    bpy.utils.register_class(NifSettings)
    NifLog.register()
    properties.register()
    ui.register()
    operators.register()

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

    properties.unregister()
    ui.unregister()
    operators.unregister()
    bpy.utils.unregister_class(NifSettings)
    NifLog.unregister()


if __name__ == "__main__":
    register()
