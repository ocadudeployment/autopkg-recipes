#!/usr/bin/python
#
# Copyright 2019 Cameron Stott
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Borrowed Code from AutoPkg FlatPkgPacker.py in Autopkg core, by Jesse Peterson 

"""See docstring for DistPkgConverter class"""

import subprocess

from autopkglib import Processor, ProcessorError

__all__ = ["DistPkgConverter"]


class DistPkgConverter(Processor):
    '''Convert a pkg to a distribution using productbuild.
    Requires version 0.2.4.
    '''

    description = __doc__

    input_variables = {
        'source_pkg_path': {
            'description': 'Path to a component package',
            'required': True,
        },
        'destination_pkg': {
            'description': 'Name of destination pkg to be built',
            'required': True,
        },
    }

    output_variables = {}

    def convert(self, source_pkg, dest_pkg):
        """Converts pkg to a distribution"""
        #pylint: disable=no-self-use
        try:
            subprocess.check_call(['/usr/bin/productbuild',
                                   '--package', source_pkg, dest_pkg])
        except subprocess.CalledProcessError, err:
            raise ProcessorError("%s converting %s" % (err, source_pkg))

    def main(self):
        source_pkg = self.env.get('source_pkg_path')
        dest_pkg = self.env.get('destination_pkg')

        self.convert(source_pkg, dest_pkg)

        self.output("Converted %s to %s"
                    % (source_pkg, dest_pkg))

if __name__ == '__main__':
    PROCESSOR = DistPkgConverter()
    PROCESSOR.execute_shell()