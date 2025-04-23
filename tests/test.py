import jsonspice  # import this one first to monkeypatch spiceypy
import spiceypy

# v = spiceypy.gdpool('hello', 0, 10)

# spiceypy.furnsh('de-403-masses.tpc.txt')
jsonspice.furnsh_json_kernel('de-403-masses.tpc')

jsonspice.furnsh_dict({"abc": [1,2,3]})
v = spiceypy.gdpool('abc', 0, 10)
print(v)

jsonspice.furnsh_dict({"+abc": [4,5,6]})
v = spiceypy.gdpool('abc', 0, 10)
print(v)


jsonspice.furnsh_dict({"time": '@1972-JAN-1'})
v = spiceypy.gdpool('time', 0, 10)
print(v)


jsonspice.furnsh_dict({"+time": '@1972-JAN-2'})
v = spiceypy.gdpool('time', 0, 10)
print(v)


jsonspice.furnsh_json_kernel('test.json')
v = spiceypy.gdpool('time', 0, 10)
print(v)

# use the monkeypatched furnsh from spiceypy:
spiceypy.furnsh('test.json')
v = spiceypy.gdpool('time', 0, 10)
print(v)

# an example of an invalid @ string, that just returns a string:
jsonspice.furnsh_dict({"time2": '@SYNTAX-ERROR'})
v = spiceypy.gcpool('time2', 0, 10)
print(v)

