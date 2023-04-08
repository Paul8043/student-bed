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
    "@thickness.slim":18,
    "@thickness.plumb":27,
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

measures["stringer.height"] = measures["@thickness.plumb"]
measures["stringer.width"]  = measures["@side.length"]
measures["stringer.length"] = measures["mattress.length"]*0.5
measures["batten.height"]   = measures["@thickness.slim"]
measures["batten.width"]    = measures["@side.length"]
measures["batten.length"]   = measures["mattress.width"]
measures["batten.gap"]      = (measures["stringer.length"]-9*measures["batten.width"])/8
measures["jamb.side"]       = measures["@side.length"]
measures["jamb.length"]     = measures["mattress.altitude"]-measures["@thickness.slim"]-measures["@thickness.plumb"]

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
        sh = self.measures["stringer.height"]
        sw = self.measures["stringer.width"]
        sl = self.measures["stringer.length"]
        stringer = cq.Workplane("XY").box(sl,sw,sh)
        #show_object(stringer,name="stringer",options={"alpha":0.2,"color":(255,170,0)})

        bh = self.measures["batten.height"]
        bw = self.measures["batten.width"]
        bl = self.measures["batten.length"]
        batten = cq.Workplane("XY").box(bw,bl,bh)
        #show_object(batten,name="batten",options={"alpha":0.2,"color":(255,170,0)})

        js = self.measures["jamb.side"]
        jl = self.measures["jamb.length"]
        jamb = cq.Workplane("XY").box(js,js,jl)
        #show_object(jamb,name="jamb",options={"alpha":0.2,"color":(255,170,0)})

        stringer_moved = stringer.translate((600,0,250))
        batten_moved   = batten.translate((0,500,350))
        parts = jamb.union(stringer_moved).union(batten_moved)
        #show_object(parts,name="parts",options={"alpha":0.2,"color":(255,170,0)})

        zo = 0.5*(self.measures["stringer.height"]+self.measures["batten.height"])
        yo = 0.5*(self.measures["mattress.width"]-self.measures["stringer.width"])
        xo = 0.5*(self.measures["stringer.length"]-self.measures["batten.width"])
        skew = self.measures["batten.width"]+self.measures["batten.gap"]
        stringer_front = stringer.translate((0,+yo,0))
        stringer_back  = stringer.translate((0,-yo,0))
        duckboard = stringer_front.union(stringer_back)
        duckboard = duckboard.union(batten.translate((0,0,zo)))        # middle
        duckboard = duckboard.union(batten.translate((-xo,0,zo)))      # left most
        duckboard = duckboard.union(batten.translate((+xo,0,zo)))      # right most
        duckboard = duckboard.union(batten.translate((-1*skew,0,zo)))  # 1 skew left
        duckboard = duckboard.union(batten.translate((+1*skew,0,zo)))  # 1 skew right
        duckboard = duckboard.union(batten.translate((-2*skew,0,zo)))  # 2 skew left
        duckboard = duckboard.union(batten.translate((+2*skew,0,zo)))  # 2 Skew right
        duckboard = duckboard.union(batten.translate((-3*skew,0,zo)))  # 3 skew left
        duckboard = duckboard.union(batten.translate((+3*skew,0,zo)))  # 3 skew right
        show_object(duckboard,name="duckbboard",options={"alpha":0.2,"color":(255,170,0)})

        self.model = parts
        return

    pass

def main() -> None:
    simple_bed = SimpleBed(measures)
    return

if __name__ == "__main__" or __name__ == "temp":
    main()