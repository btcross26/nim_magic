# nim_magic

***Note: This README has been borrowed as-is from the forked repository and modified accordingly to reflect a few small changes to the jupyter cell magic - namely the changing of the `nim` cell magic to `nimpy`, and the addition of an `inim` cell magic for quick interactive compilation of nim code within a jupyter notebook.***

Nim cell magic for JupyterLab or Juypter Python Notebooks.

Write Nim modules and use the compiled code directly in the Notebook as extension modules for the Python kernel (similar to e.g. %%cython, but for your favorite language :P ). It builds on @yglukhov 's awesome [nimpy](https://github.com/yglukhov/nimpy) library. 

## Requirements
* A [Nim](https://nim-lang.org) compiler in your path
* [nimpy](https://github.com/yglukhov/nimpy) package (`nimble install nimpy`)

## Installation
Just put the file `nim_magic.py` somewhere in Python's import path, e.g. in one of the dirs that is printed by: `python3 -c "import sys; print(sys.path)"`.

## Example
In a JupyterLab or Jupyter Notebook running a Python3 kernel:

```Python
# In [1]:
%load_ext nim_magic

# In [2]:
%%nim -d:release
proc greet(name: string): string {.exportpy.} =
  return "Hello, " & name & "!"

# In [3]:
greet("World")
    
# Out [3]:
'Hello, World!'

# In [4]:
%%inim -d:release --opt:speed
proc add_x_y(x, y: int): int =
  result = x + y

echo add_x_y(5, 6)

11

# In [5]:
%nim_clear
```

Further examples can be found [here](examples.ipynb).
