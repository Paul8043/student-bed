"""
@author: Paul8043
"""

import cadquery as cq

# some stubs to make the script ready for VS-Code and cq-editor

if 'log' not in globals():
    def log(message) -> None:
        return

if 'show_object' not in globals():
    def show_object(self, name, options={}, **kwargs) -> None:
        return
    
if 'debug' not in globals():    
    def debug() -> None:
        return
    
# how to output

def echo(message) -> None:
    log(message)
    print(message)
    return

# all measures are in mm

measures ={
    "@.plate.thickness":18,
    "@.side.length":68,
    "@.lying.height":465,
    "mattress.height":180,
    "mattress.width":900,
    "mattress.length":2100,
    "storage.height":260,
    "storage.width":900,
    "storage.length":1310
}

# derived measures

measures["stringer.side"]   = measures["@.side.length"]
measures["stringer.length"] = measures["mattress.width"]*0.5

# model class

class SimpleBed:

    def __init__(self,measures) -> None:
        self.mattress  = None
        self.storage   = None
        self.stringer  = None
        self.model     = None
        self.measures  = measures
        self.dump()
        self.build()
        return
    
    def dump(self) -> None:
        echo("")
        m = self.measures
        for key in sorted(m):
            echo(f"{key}:{m[key]}")
        echo("")
        return
    
    def make_mattress(self) -> None:
        mh = measures["mattress.height"]
        mw = measures["mattress.width"]
        ml = measures["mattress.length"]
        mattress = cq.Workplane("XY")
        mattress = mattress.box(ml,mw,mh)
        self.mattress = mattress
        #show_object(mattress,name="mattress",options={"alpha":0.2,"color":(255,170,0)})
        return
    
    def make_storage(self) -> None:
        sh = measures["storage.height"]
        sw = measures["storage.width"]
        sl = measures["storage.length"]
        storage = cq.Workplane("XY")
        storage = storage.box(sl,sw,sh)
        self.storage = storage
        #show_object(storage,name="storage",options={"alpha":0.2,"color":"cyan"})
        return
    
    def make_stringer(self) -> None:
        ss = measures["stringer.side"]
        sl = measures["stringer.length"]
        stringer = cq.Workplane("XY")
        stringer = stringer.box(sl,ss,ss)
        self.stringer = stringer
        show_object(stringer,name="stringer",options={"alpha":0.1,"color":"khaki"})
        return
    
    def build(self) -> None:
        self.make_mattress()
        self.make_storage()
        self.make_stringer()
        return

    pass

def main() -> None:
    simple_bed = SimpleBed(measures)
    return

if __name__ == "__main__" or __name__ == "temp":
    main()