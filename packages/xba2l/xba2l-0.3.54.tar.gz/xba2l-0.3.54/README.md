
xba2l is an a2l file parsing toolkit that provides syntax analysis compatible with [ASAM MCD-2 MC 1.7.1](https://www.asam.net/standards/detail/mcd-2-mc/)

## Feature

1. Fast syntax parsing
2. Written entirely in Python language, suitable for Python 3.10 and above
3. Automatic detection of codec

## Installation

```
pip install xba2l
```

## Quick start

After the installation of XBA2L is complete, create a new file `quick_start.py`, copy the following code and save it

``` python
import dataclasses
import json
import os
import sys


from xba2l import a2l_util
from xba2l.etc import tool

a2l_filename = input("Please input a2l filename:")
if not os.path.isfile(a2l_filename):
   print("file not exists")
else:
   err, asap2, module = a2l_util.parse_a2l(a2l_filename)
   if err is not None:
      print(err)
   else:
      # dump asap2 to console
      json.dump(
            dataclasses.asdict(
                asap2,
                dict_factory=lambda pairs: {
                    pair[0]: pair[1] for pair in pairs if pair[1] is not None and pair[0] != "elements" and not pair[0].endswith("_dict")
                },
            ),
            sys.stdout,
            indent=4,
            cls=tool.JsonEncoder,
        )         

```

Run `python3 quick_start.py` on your console, enter the file name, and you will see the parsed a2l node information output to the terminal


## Performance

Run the following performance test command, replacing **{a2l filename}** with your **a2l** filename or the directory of  containing **a2l** files

``` shell
python3 -m xba2l.performance "{a2l filename}"   
```

Here's the result of my laptop running. **CPU: Intel(R) i9-13900HX**

* Include measurements

   | File Size[MB]	| Axis	| Charecteristic	| Blob	| Measurement	| Used Time[s] |
   |-----------------|--------|-----------------|--------|--------------|--------------|
   | 4.0	            | 312	   | 2920	         | 0	   | 3151	      | 0.4          | 
   | 5.7	            | 887	   | 3491	         | 0	   | 6426	      | 0.5          |           
   | 8.1	            | 16	   | 16436	         | 0	   | 8919	      | 0.8          | 
   | 17.6	         | 78	   | 26167	         | 0	   | 18165	      | 1.4          | 
   | 21.1	         | 3569	| 25909	         | 0	   | 19902	      | 1.7          | 
   | 25.0	         | 129	   | 41857	         | 0	   | 37313	      | 2.7          | 
   | 31.2	         | 129	   | 46976	         | 0	   | 41605	      | 2.5          | 
   | 34.3	         | 156	   | 50322	         | 0	   | 46661	      | 2.7          | 

* Exclude measurements

   | File Size[MB]	| Axis	| Charecteristic	| Blob	| Measurement	| Used Time[s] |
   |-----------------|--------|-----------------|--------|--------------|--------------|
   | 4.0	            | 312	   | 2920	         | 0	   | 0	         | 0.3          | 
   | 5.7	            | 887	   | 3491	         | 0	   | 0	         | 0.4          | 
   | 8.1	            | 16	   | 16436	         | 0	   | 0	         | 0.7          | 
   | 17.6	         | 78	   | 26167	         | 0	   | 0	         | 1.2          | 
   | 21.1	         | 3569	| 25909	         | 0	   | 0	         | 1.5          | 
   | 25.0	         | 129	   | 41857	         | 0   	| 0	         | 1.9          | 
   | 31.2	         | 129	   | 46976	         | 0	   | 0	         | 2.1          | 
   | 34.3	         | 156	   | 50322	         | 0	   | 0         	| 2.2          | 


## Help

- a2l_base.py

   **Options**: 辅助选项类

   ``` python   
   class Options:
      calculate_memory_size: bool   # Whether to calculate the memory size of the parsed data, default is *False*
      ignore_measurements: bool     # Whether to ignore Mesurement, default to *tru*
      read_instance: bool           # Whether to handle instance class variables Instans, with default *Tru*
   ```

- a2l_util.py

   **parse_a2l** : Run **a2l** file parsing, and the data type returned is defined by referring to the various class definitions in `a2l_lib.py`

   ``` python
   def parse_a2l(
      fn_or_content: str | bytes, 
      encoding: str | None = None, 
      options: a2l_base.Options | None = None,
   ) -> tuple[Exception | None, a2l_lib.Asap2 | None, a2l_lib.Module | None]:
   ```
   1. Input:
   
      `fn_or_content`：**a2l** filename, or the contents of the **a2l** file being read

      `encoding`: file encoding, automatically detected if not specified

      `options`: arguments for parsing, refer to **a2l_base.Options**

   2. Output:
   
      If the run is successful, the first parameter returned is **None**, followed by **Asap2** and **Module** objects. If the run fails, the first parameter returned is an **Exception** object that describes the reason for the failure

- a2l_lib.py

   This file defines a number of classes corresponding to the names of each element in the [ASAM MCD-2 MC 1.7.1](https://www.asam.net/standards/detail/mcd-2-mc/) standard to describe the parsing results; For example, ASAP2 is the root node class that A2L resolves

   ``` python   
   class Asap2:
      asap2_version: Asap2Version  # Version information
      project: Project             # Project Node
      ...

   ```