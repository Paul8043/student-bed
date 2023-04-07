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
    "@plate.thickness":18,
    "@side.length":68,
    "mattress.height":180,
    "mattress.width":900,
    "mattress.length":2100,
    "mattress.altitude":465,
    "storage.height":260,
    "storage.width":900,
    "storage.length":1310
}

# derived measures

measures["stringer.side"]   = measures["@side.length"]
measures["stringer.length"] = measures["mattress.length"]*0.5
measures["ledger.side"]     = measures["@side.length"]
measures["ledger.length"]   = measures["mattress.width"]-2*measures["@side.length"]
measures["batten.height"]   = measures["@plate.thickness"]
measures["batten.width"]    = measures["@side.length"]
measures["batten.length"]   = measures["mattress.width"]
measures["jamb.side"]       = measures["@side.length"]
measures["jamb.length"]     = measures["mattress.altitude"]-measures["@side.length"]-2*measures["@plate.thickness"]


# model class

class SimpleBed:

    def __init__(self,measures) -> None:
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
    
    def build(self) -> None:
        ss = measures["stringer.side"]
        sl = measures["stringer.length"]
        stringer = cq.Workplane("XY").box(sl,ss,ss)
        #show_object(stringer,name="stringer",options={"alpha":0.2,"color":(255,170,0)})

        ls = measures["ledger.side"]
        ll = measures["ledger.length"]
        ledger = cq.Workplane("XY").box(ls,ll,ls)
        #show_object(ledger,name="ledger",options={"alpha":0.2,"color":(255,170,0)})

        bh = measures["batten.height"]
        bw = measures["batten.width"]
        bl = measures["batten.length"]
        batten = cq.Workplane("XY").box(bw,bl,bh)
        #show_object(batten,name="batten",options={"alpha":0.2,"color":(255,170,0)})

        js = measures["jamb.side"]
        jl = measures["jamb.length"]
        jamb = cq.Workplane("XY").box(js,js,jl)
        #show_object(jamb,name="jamb",options={"alpha":0.2,"color":(255,170,0)})

        stringer_moved = stringer.translate((600,0,250))
        ledger_moved   = ledger.translate((0,500,250))
        batten_moved   = batten.translate((0,500,350))
        parts = jamb.union(stringer_moved).union(ledger_moved).union(batten_moved)
        show_object(parts,name="parts",options={"alpha":0.2,"color":(255,170,0)})

        self.model = parts
        return

    pass

def main() -> None:
    simple_bed = SimpleBed(measures)
    return

if __name__ == "__main__" or __name__ == "temp":
    main()