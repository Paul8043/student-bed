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
    "@thickness.1":18,
    "@thickness.2":27,
    "@side.length":120,
    "mattress.height":180,
    "mattress.width":900,
    "mattress.length":2100,
    "mattress.altitude":465,
    "storage.height":260,
    "storage.width":900,
    "storage.length":1310
}

# derived measures

measures["@width.1"]         = measures["@side.length"]*0.5
measures["@width.2"]         = measures["@side.length"]*2/3
measures["@width.3"]         = measures["@side.length"]

measures["stringer.height"]  = measures["@thickness.2"]
measures["stringer.width"]   = measures["@width.3"]
measures["stringer.length"]  = measures["mattress.length"]*0.5

measures["ledger.height"]    = measures["@thickness.2"]
measures["ledger.width"]     = measures["@width.3"]
measures["ledger.length"]    = measures["mattress.width"]-2*measures["@width.3"]

measures["batten.height"]    = measures["@thickness.1"]
measures["batten.width.1"]   = measures["@width.1"]
measures["batten.width.2"]   = measures["@width.2"]
measures["batten.width.3"]   = measures["@width.3"]
measures["batten.length"]    = measures["mattress.width"]
measures["batten.gap"]       = (measures["stringer.length"]-measures["batten.width.3"]-5*measures["batten.width.2"]-measures["batten.width.1"])/6

measures["cutoff.clearance"] = 0.2
measures["cutoff.thickness"] = measures["@thickness.1"]+measures["cutoff.clearance"]
measures["cutoff.width"]     = measures["@width.2"]
measures["cutoff.length"]    = (measures["@width.2"]+measures["cutoff.clearance"])*2

measures["jamb.thickness"]   = measures["@thickness.2"]
measures["jamb.side"]        = measures["@side.length"]
measures["jamb.length"]      = measures["mattress.altitude"]-measures["@thickness.1"]-measures["@thickness.2"]

measures["rib.thickness"]    = measures["@thickness.2"]
measures["rib.width"]        = measures["@width.2"]
measures["rib.length.1"]     = measures["ledger.length"]+2*(measures["@thickness.2"]+15)
measures["rib.length.2"]     = measures["stringer.length"]-1.5*measures["@side.length"]+2*(measures["@thickness.2"]+15)

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

        lh = self.measures["ledger.height"]
        lw = self.measures["ledger.width"]
        ll = self.measures["ledger.length"]
        ledger = cq.Workplane("XY").box(lw,ll,lh)
        #show_object(ledger,name="ledger",options={"alpha":0.2,"color":(255,170,0)})

        bh   = self.measures["batten.height"]
        bw_1 = self.measures["batten.width.1"]
        bw_2 = self.measures["batten.width.2"]
        bw_3 = self.measures["batten.width.3"]
        bl   = self.measures["batten.length"]
        batten_1 = cq.Workplane("XY").box(bw_1,bl,bh)     # half  (only for 3D-printing)
        batten_2 = cq.Workplane("XY").box(bw_2,bl,bh)     # small (middle)
        batten_3 = cq.Workplane("XY").box(bw_3,bl,bh)     # large (outwards)
        #show_object(batten_3,name="batten",options={"alpha":0.2,"color":(255,170,0)})

        jt = self.measures["jamb.thickness"]
        js = self.measures["jamb.side"]
        jl = self.measures["jamb.length"]
        ct = self.measures["cutoff.thickness"]
        cw = self.measures["cutoff.width"]
        cl = self.measures["cutoff.length"]
        cxp = cq.Workplane("XY").box(cw,ct,cl).translate((+0.5*js,0,0.5*jl))      # cutout x+
        cxm = cq.Workplane("XY").box(cw,ct,cl).translate((-0.5*js,0,0.5*jl))      # cutout x-
        cyp = cq.Workplane("XY").box(ct,cw,cl).translate((0,+0.5*js,0.5*jl))      # cutout y+
        jamb   = cq.Workplane("XY").box(js,js,jl).faces("<Z or >Z").shell(-jt)    # shell
        jamb_corner = jamb.cut(cxp).cut(cyp)
        jamb_middle = jamb_corner.cut(cxm)
        #show_object(cx,name="cutoff",options={"alpha":0.2,"color":(255,170,0)})
        #show_object(jamb_corner,name="jamb",options={"alpha":0.2,"color":(255,170,0)})

        rt   = self.measures["rib.thickness"]
        rw   = self.measures["rib.width"]
        rl_1 = self.measures["rib.length.1"]
        rl_2 = self.measures["rib.length.2"]
        rib_ledger   = cq.Workplane("XY").box(rt,rl_1,rw)          # rib for ledger
        rib_stringer = cq.Workplane("XY").box(rl_2,rt,rw)          # rib for stringer
        show_object(rib_ledger,name="rib",options={"alpha":0.2,"color":(255,170,0)})    

        stringer_moved = stringer.translate((600,0,250))
        ledger_moved   = ledger.translate((0,500,250))
        batten_moved   = batten_3.translate((0,500,350))
        parts = jamb.union(stringer_moved).union(ledger_moved).union(batten_moved)
        #show_object(parts,name="parts",options={"alpha":0.2,"color":(255,170,0)})

        zo = 0.5*(self.measures["stringer.height"]+self.measures["batten.height"])
        yo = 0.5*(self.measures["mattress.width"]-self.measures["stringer.width"])
        xo = 0.5*(self.measures["stringer.length"]-self.measures["batten.width.2"])
        skew = self.measures["batten.width.2"]+self.measures["batten.gap"]
        lift = 0.5*self.measures["stringer.height"]+self.measures["jamb.length"]
        stringer_front = stringer.translate((0,+yo,0))
        stringer_back  = stringer.translate((0,-yo,0))
        ledger_left    = ledger.translate((-xo,0,0))
        ledger_right   = ledger.translate((+xo,0,0))
        duckboard = stringer_front.union(stringer_back)
        duckboard = duckboard.union(ledger_left)
        duckboard = duckboard.union(ledger_right)
        duckboard = duckboard.union(batten_3.translate((0,0,zo)))        # middle
        duckboard = duckboard.union(batten_3.translate((-xo,0,zo)))      # left most
        duckboard = duckboard.union(batten_3.translate((+xo,0,zo)))      # right most
        duckboard = duckboard.union(batten_3.translate((-1*skew,0,zo)))  # 1 skew left
        duckboard = duckboard.union(batten_3.translate((+1*skew,0,zo)))  # 1 skew right
        duckboard = duckboard.union(batten_3.translate((-2*skew,0,zo)))  # 2 skew left
        duckboard = duckboard.union(batten_3.translate((+2*skew,0,zo)))  # 2 Skew right
        duckboard = duckboard.union(batten_3.translate((-3*skew,0,zo)))  # 3 skew left
        duckboard = duckboard.union(batten_3.translate((+3*skew,0,zo)))  # 3 skew right
        duckboard = duckboard.translate((0,0,lift))
        #show_object(duckboard,name="duckbboard",options={"alpha":0.2,"color":(255,170,0)})

        uplift = 0.5*self.measures["jamb.length"]
        half = duckboard
        half = half.union(jamb.translate((-xo,-yo,uplift)))  # back  left
        half = half.union(jamb.translate((+xo,-yo,uplift)))  # back  right
        half = half.union(jamb.translate((-xo,+yo,uplift)))  # front left
        half = half.union(jamb.translate((+xo,+yo,uplift)))  # front right
        #show_object(half,name="half",options={"alpha":0.2,"color":(255,170,0)})

        half_stl = half
        #half_stl = half_stl.rotate((0,0,0),(0,1,0),180).scale(0.1)
        #show_object(half_stl,name="half_stl",options={"alpha":0.2,"color":(255,170,0)})

        align = 0.5*self.measures["stringer.length"]
        bed  = half.translate((-align,0,0))
        bed  = bed.union(half.translate((+align,0,0)))
        #show_object(bed,name="bed",options={"alpha":0.2,"color":(255,170, 0)})

        self.model = bed
        return

    pass

def main() -> None:
    simple_bed = SimpleBed(measures)
    return

if __name__ == "__main__" or __name__ == "temp":
    main()