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
from bpy.types import AddonPreferences

# Python dependencies are bundled inside the io_scene_nif/dependencies folder
_dependencies_path = os.path.join(os.path.dirname(__file__), "dependencies")
if _dependencies_path not in sys.path:
    sys.path.append(_dependencies_path)
    print(sys.path)
del _dependencies_path

from io_scene_nif import properties, operators, ui
from io_scene_nif.utility.nif_logging import NifLog

# noinspection PyBroadException
try:
    from io_scene_nif.utility import nif_debug

    nif_debug.start_debug()
except:
    print("Failed to load debug module")

use_icons = False
try:
    # noinspection PyUnresolvedReferences
    import bpy.utils.previews

    use_icons = True
except ImportError:
    pass

global preview_collections
preview_collections = {}

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

logging_level_enum = (
    ("NOTSET", "Not Set", "Log Everything", "CHECKBOX_DEHLT", 0),
    ("DEBUG", "Debug", "Log debug, info, warnings and errors", "QUESTION", 10),
    ("INFO", "Info", "Log info, warnings and errors", "HELP", 20),
    ("WARNING", "Warning", "Log Warnings and errors", "", 30),
    ("ERROR", "Error", "Log all errors", "ERROR", 40),
    ("CRITICAL", "Critical", "Only log critical errors", "CANCEL", 50),
)


class NifSettings(AddonPreferences):
    bl_idname = __package__

    default_filepath: bpy.props.StringProperty(
        name="Default File Path",
        description="Default output file path",
        subtype='DIR_PATH',
    )

    pyffi_logging_level: bpy.props.EnumProperty(
        name="PyFFI Logging Level",
        description="",
        # update=update_pyffi_logger,
        items=logging_level_enum,
        default="WARNING",
    )

    niftools_logging_level: bpy.props.EnumProperty(
        name="NifTools Logging Level",
        description="",
        # update=update_pyffi_logger,
        items=logging_level_enum,
        default="WARNING",
    )

    default_author: bpy.props.StringProperty(
        name="Default Author",
        description="Default Author for projects, currently not in use.",
    )

    boolean: bpy.props.BoolProperty(
        name="Example Boolean",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is a preferences view for our add-on")
        layout.prop(self, "default_filepath", icon="FILE_SCRIPT")
        layout.prop(self, "pyffi_logging_level")
        layout.prop(self, "niftools_logging_level")
        layout.prop(self, "default_author", icon="USER")


# noinspection PyUnusedLocal
def menu_func_import(self, context):
    pmain = preview_collections["main"]
    if not pmain or 'niftools_logo' not in pmain:
        self.layout.operator(operators.nif_import_op.NifImportOperator.bl_idname, text="NetImmerse/Gamebryo (.nif)")
    else:
        self.layout.operator(operators.nif_import_op.NifImportOperator.bl_idname, text="NetImmerse/Gamebryo (.nif)",
                             icon_value=pmain['niftools_logo'].icon_id)


# noinspection PyUnusedLocal
def menu_func_export(self, context):
    pmain = preview_collections["main"]
    if not pmain or 'niftools_logo' not in pmain:
        self.layout.operator(operators.nif_export_op.NifExportOperator.bl_idname, text="NetImmerse/Gamebryo (.nif)")
    else:
        self.layout.operator(operators.nif_export_op.NifExportOperator.bl_idname, text="NetImmerse/Gamebryo (.nif)",
                             icon_value=pmain['niftools_logo'].icon_id)


# noinspection PyBroadException
def register():
    bpy.utils.register_class(NifSettings)
    NifLog.register()
    properties.register()
    ui.register()
    operators.register()

    try:
        custom_icons = bpy.utils.previews.new()
        material_icons = bpy.utils.previews.new()
        preview_collections["main"] = custom_icons
        preview_collections["materials"] = material_icons
    except Exception as e:
        NifLog.warn("Failed to load custom icons.", e)
        preview_collections["main"] = ""
        preview_collections["materials"] = ""

    if use_icons:
        script_path = bpy.path.abspath(os.path.dirname(__file__))
        icons_dir = os.path.join(script_path, 'icons')
        logo_path = os.path.join(icons_dir, "niftools-logo.png")
        if os.path.isfile(logo_path):
            custom_icons.load('niftools_logo', logo_path, 'IMAGE')

    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    # remove icons
    if use_icons and preview_collections["main"] != "":
        for pcoll in preview_collections.values():
            bpy.utils.previews.remove(pcoll)
        preview_collections.clear()

    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

    properties.unregister()
    ui.unregister()
    operators.unregister()
    bpy.utils.unregister_class(NifSettings)
    NifLog.unregister()


if __name__ == "__main__":
    register()
