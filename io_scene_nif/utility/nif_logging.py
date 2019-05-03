""" Nif Utilities, stores logging across the code base"""

# ***** BEGIN LICENSE BLOCK *****
# 
# Copyright © 2005-2016, NIF File Format Library and Tools contributors.
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

import logging
from .nif_settings import get_settings


class _MockOperator:
    def report(self, level, message):
        print(str(level) + ": " + message)


class NifLog:
    """A simple custom exception class for export errors.
    This module require initialisation of an operator reference to function."""
    
    # Injectable operator reference used to perform reporting, default to simple logging
    op = _MockOperator()

    @classmethod
    def register(cls, operator=None):
        """Register this after the NifAddonPrefs"""
        settings = get_settings()
        NifLog.op = operator
        NifLog.niftools_logger = logging.getLogger("niftools")
        try:
            NifLog.niftools_logger.setLevel(getattr(logging, settings.niftools_logging_level))
        except AttributeError:
            NifLog.niftools_logger.setLevel(logging.WARNING)
            print("Failed to fetch Niftools Logging Level")
        NifLog.pyffi_logger = logging.getLogger("pyffi")
        try:
            NifLog.pyffi_logger.setLevel(getattr(logging, settings.pyffi_logging_level))
        except AttributeError:
            NifLog.pyffi_logger.setLevel(logging.WARNING)
            print("Failed to fetch PyFFI Logging Level")
        NifLog.log_handler = logging.StreamHandler()
        NifLog.log_handler.setLevel(logging.DEBUG)
        NifLog.log_formatter = logging.Formatter("%(name)s:%(levelname)s:%(message)s")
        NifLog.log_handler.setFormatter(NifLog.log_formatter)
        NifLog.niftools_logger.addHandler(NifLog.log_handler)
        NifLog.pyffi_logger.addHandler(NifLog.log_handler)

    @classmethod
    def unregister(cls):
        NifLog.op = _MockOperator()

    @staticmethod
    def debug(message):
        """Report a debug message."""
        NifLog.op.report({'DEBUG'}, message)

    @staticmethod
    def info(message):
        """Report an informative message."""
        NifLog.op.report({'INFO'}, message)

    @staticmethod
    def warn(message):
        """Report a warning message."""
        NifLog.op.report({'WARNING'}, message)

    @staticmethod
    def error(message):
        """Report an error and return ``{'FINISHED'}``. To be called by
        the :meth:`execute` method, as::

            return error('Something went wrong.')

        Blender will raise an exception that is passed to the caller.

        .. seealso::

            The :ref:`error reporting <dev-design-error-reporting>` design.
        """
        NifLog.op.report({'ERROR'}, message)
        return {'FINISHED'}
