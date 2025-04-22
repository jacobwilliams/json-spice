from spiceypy import furnsh, tparse, pdpool, pcpool, dtpool, gcpool, gdpool, dvpool
try:
    # this will allow loading JSON files with comments
    import json5 as json
except:
    # if not present, fallback to regular json (won't allow comments)
    import json


def furnsh_json_kernel(kernel_path: str) -> None:
    """
    Load a JSON kernel into SPICE.

    See: `furnsh_dict` for details.

    Parameters
    ----------
    kernel_path : str
        The path to the JSON kernel file.
    """

    if not kernel_path.lower().endswith('.json'):
        # in this case, just use a normal furnsh
        furnsh(kernel_path)
    else:
        # use the custom routine:
        with open(kernel_path, 'r') as f:
            data = json.load(f)
        furnsh_dict(data)

def furnsh_dict(data: dict) -> None:
    """
    Load a JSON kernel data into SPICE.

    Note: there are two modifications to support JSON SPICE kernels:

    1. if the variable name starts with '+', then the SPICE '+=' syntax is used to add to an existing variable if it exists.
    2. if a string value starts with '@', it is treated as a UTC string and converted to a double precision number representing "UTC seconds past J2000".

    Reference: https://degenerateconic.com/json-spice.html

    Parameters
    ----------
    d : dict
        The JSON kernel data as a dictionary.
    """

    for item, value in data.items():

        if isinstance(value, (list, tuple)):  # a list of values
            n = len(value)
            if n == 0:
                raise Exception("Empty arrays are not supported in JSON SPICE kernels.")

            # first if any are strings, check for @ syntax and convert to int
            value = [tparse(x[1:])[0] if isinstance(x, str) and x.startswith('@') else x for x in value]

            # what is the type of this list?
            if all(isinstance(x, str) for x in value):
                # a list of strings
                type = str
            elif all(isinstance(x, int) or isinstance(x, float) or isinstance(x, bool) for x in value):
                # a list of integers, floats, bools
                type = float
                value = [float(x) for x in value]
            else:
                raise Exception("Unsupported array type in JSON SPICE kernel.")

        elif isinstance(value, str):
            n = 1
            if value.startswith('@'):
                # a string with @ syntax, convert to UTC seconds past J2000
                type = float
                value = [tparse(value[1:])[0]]
            else:
                # a normal string
                type = str
                value = [value]

        elif isinstance(value, (int, float, bool)):
            n = 1
            type = float
            value = [float(value)]

        elif isinstance(value, dict):
            raise Exception("Nested dictionaries are not supported in JSON SPICE kernels.")
                    
        # check for += and add to existing variable if it exists
        if item.startswith('+'):

            item = item[1:]
            try:
                n_existing, typeout = dtpool(item)
                found = n_existing > 0 and typeout != 'X'
            except:
                found = False

            if found:
                if typeout == 'C':  # character
                    if type == str:
                        values = [str(s) for s in gcpool(item, 0, n)]
                    else:
                        raise Exception("Cannot add to existing character variable with a non-string value.")
                elif typeout == 'N':  # numeric
                    if type == float:
                        values = [float(x) for x in gdpool(item, 0, n)]
                    else:
                        raise Exception("Cannot add to existing numeric variable with a non-float value.")
                if found:
                    values.extend(value)  # append new values to existing ones
                    value = values
                    dvpool(item)  # delete the existing variable from the pool
                else:
                    raise Exception(f"Variable '{item}' not found in SPICE pool for += operation.")

        # add the variable
        if type == float:
            pdpool ( item, value )
        elif type == str:
            pcpool ( item, value )



    


