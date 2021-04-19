"""
The code in this file has been largely borrowed and modified from the following
GitHub location: https://github.com/apahl/nim_magic. The resulting code in this file
is relicensed under the MIT license, Copyright (c) 2021 Benjamin Cross.

The original code is borrowed and copied under the following MIT license:

Copyright (c) 2018 Axel Pahl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


# original author: Axel Pahl
# modificiations by: Benjamin Cross
# modified: 2021-04-19


import os
import shutil
import sys
import time
import subprocess as sp
from IPython.core.magic import (Magics, magics_class,
                                line_magic, cell_magic)


@magics_class
class NimMagics(Magics):
    def __init__(self, shell):
        super(NimMagics, self).__init__(shell)
        self._dir = "_nimmagic"

    def _get_name(self):
        name = time.strftime("nim%y%m%d%H%M%S")
        return name

    def _nim_compile(self, code, cmd, name, pstdout=False):
        if not os.path.isdir(self._dir):
            os.mkdir(self._dir)

        with open(f"{self._dir}/{name}.nim", "wt") as f:
            f.write(code)
        cp = sp.run(
            cmd,
            shell=True,
            check=False,
            encoding="utf8",
            stdout=sp.PIPE,
            stderr=sp.PIPE,
        )
        if cp.stderr.strip():
            print(cp.stderr.strip())
        if pstdout and cp.stdout.strip():
            print(cp.stdout.strip())
        return cp.returncode

    @line_magic
    def nim_clear(self, cmd):
        """
        %nim_clear
        will remove the temporary dirs used by nim_magic.
        """
        shutil.rmtree(self._dir, ignore_errors=True)
        print("Removed temporary files used by nim_magic.")

    @cell_magic
    def nimpy(self, options, code):
        """
        `options` can be left empty or contain further compile options, e.g. "-d:release"
        (separated by space).

        Example:

        %%nimpy -d:release
        <code to compile in release mode>
        """
        # add nimpy import to code
        code = "import nimpy\n\n" + code

        # create compile command for dynamic library
        name = self._get_name()
        platform = sys.platform
        if platform.startswith("win"):
            ext = "pyd"
        elif platform in ["darwin", "linux"]:
            ext = "so"
        else:
            raise RuntimeError("unrecognized system platform")
        dir = self._dir
        options += f" --hints:off --app:lib --out:{dir}/{name}.{ext}"
        cmd = f"nim c {options} {dir}/{name}.nim"
        returncode = self._nim_compile(code, cmd, name)
        if returncode == 0:
            glbls = self.shell.user_ns
            import_exec = f"from {self._dir}.{name} import *"
            exec(import_exec, glbls)

    @cell_magic
    def inim(self, options, code):
        """
        `options` can be left empty or contain further arguments to pass to the
        compiled binary

        Example:

        %%inim -d:release
        <code to compile and get output in interctive mode>
        """
        name = self._get_name()
        options += f" --run --hints:off --out:{self._dir}/{name}"
        cmd = f"nim c {options} {self._dir}/{name}.nim"
        _ = self._nim_compile(code, cmd, name, True)


def load_ipython_extension(ipython):
    ipython.register_magics(NimMagics)
