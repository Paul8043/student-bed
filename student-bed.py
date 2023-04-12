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
    "@rib.jut":15,
    "mattress.height":180,
    "mattress.width":900,
    "mattress.length":2100,
    "mattress.altitude":465,
    "storage.height":260,
    "storage.width":900,
    "storage.length":1310
}

# derived measures

measures["@width.1"]           = measures["@side.length"]*0.5
measures["@width.2"]           = measures["@side.length"]*2/3
measures["@width.3"]           = measures["@side.length"]

measures["stringer.thickness"] = measures["@thickness.2"]
measures["stringer.width"]     = measures["@width.3"]
measures["stringer.length"]    = measures["mattress.length"]*0.5

measures["ledger.thickness"]   = measures["@thickness.2"]
measures["ledger.width"]       = measures["@width.3"]
measures["ledger.length"]      = measures["mattress.width"]-2*measures["@width.3"]

measures["rib.thickness"]      = measures["@thickness.2"]
measures["rib.width"]          = measures["@width.2"]
measures["rib.length.1"]       = measures["ledger.length"]+2*(measures["@thickness.2"]+measures["@rib.jut"])
measures["rib.length.2"]       = measures["stringer.length"]-1.5*measures["@side.length"]+2*(measures["@thickness.2"]+measures["@rib.jut"])
measures["rib.cut.width"]      = measures["@thickness.2"]
measures["rib.cut.depth"]      = 4.5
measures["rib.cut.air"]        = 0.2

measures["batten.thickness"]   = measures["@thickness.1"]
measures["batten.width.1"]     = measures["@width.1"]
measures["batten.width.2"]     = measures["@width.2"]
measures["batten.width.3"]     = measures["@width.3"]
measures["batten.length"]      = measures["mattress.width"]
measures["batten.gap"]         = 78
measures["batten.extra"]       = (measures["stringer.length"]-measures["batten.width.3"]
-5*measures["batten.width.2"]-6*measures["batten.gap"]-measures["batten.width.1"])/2

measures["jamb.thickness"]  = measures["@thickness.2"]
measures["jamb.side"]       = measures["@side.length"]
measures["jamb.length"]     = measures["mattress.altitude"]-measures["@thickness.1"]-measures["@thickness.2"]
measures["jamb.cut.width"]  = measures["@thickness.1"]
measures["jamb.cut.depth"]  = measures["@width.2"]
measures["jamb.cut.air"]    = 0.2

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

        # stringer
        st = self.measures["stringer.thickness"]
        sw = self.measures["stringer.width"]
        sl = self.measures["stringer.length"]
        stringer = cq.Workplane("XY").box(sl,sw,st)
        #show_object(stringer,name="stringer",options={"alpha":0.2,"color":(255,170,0)})

        # ledger
        lt = self.measures["ledger.thickness"]
        lw = self.measures["ledger.width"]
        ll = self.measures["ledger.length"]
        ledger_1 = cq.Workplane("XY").box(0.5*lw,ll,lt)
        ledger_2 = cq.Workplane("XY").box(lw,ll,lt)
        #show_object(ledger_2,name="ledger",options={"alpha":0.2,"color":(255,170,0)})

        # batten
        bt   = self.measures["batten.thickness"]
        bw_1 = self.measures["batten.width.1"]
        bw_2 = self.measures["batten.width.2"]
        bw_3 = self.measures["batten.width.3"]
        bl   = self.measures["batten.length"]
        batten_1 = cq.Workplane("XY").box(bw_1,bl,bt)     # half  (only for 3D-printing)
        batten_2 = cq.Workplane("XY").box(bw_2,bl,bt)     # small (middle)
        batten_3 = cq.Workplane("XY").box(bw_3,bl,bt)     # large (outwards)
        #show_object(batten_2,name="batten",options={"alpha":0.2,"color":(255,170,0)})

        # jamb
        jt  = self.measures["jamb.thickness"]
        js  = self.measures["jamb.side"]
        jl  = self.measures["jamb.length"]
        jcw = self.measures["jamb.cut.width"]
        jcd = self.measures["jamb.cut.depth"]
        jca = self.measures["jamb.cut.air"]
        jcx  = js
        jcy  = jcw+2*jca
        jcz  = 2*(jcd+jca)
        jc          = cq.Workplane("XY").box(jcx,jcy,jcz).translate((0.5*js,0,0.5*jl))  # cutter
        jamb        = cq.Workplane("XY").box(js,js,jl).faces("<Z or >Z").shell(-jt)     # shell
        jamb_corner = jamb.cut(jc.rotate((0,0,0),(0,0,1),0))                            # cut x+
        jamb_corner = jamb_corner.cut(jc.rotate((0,0,0),(0,0,1),90))                    # cut y+
        jamb_middle = jamb_corner.cut(jc.rotate((0,0,0),(0,0,1),180))                   # cut x-
        #show_object(jc,name="cutter",options={"alpha":0.2,"color":(255,170,0)})    
        #show_object(jamb_middle,name="jamb",options={"alpha":0.2,"color":(255,170,0)})

        # rib
        rt   = self.measures["rib.thickness"]
        rw   = self.measures["rib.width"]
        rl_1 = self.measures["rib.length.1"]
        rl_2 = self.measures["rib.length.2"]
        rj   = self.measures["@rib.jut"]
        rcw  = self.measures["rib.cut.width"]
        rcd  = self.measures["rib.cut.depth"]
        rca  = self.measures["rib.cut.air"]
        rcx  = rcw+2*rca
        rcy  = rcw+2*rca
        rcz  = 2*rw
        rlxo = 0.5*(rl_1-rcw)-rj
        rsxo = 0.5*(rl_2-rcw)-rj
        ryo  = 0.5*(rcy+rt)
        rd   = rcd+rca
        rc           = cq.Workplane("XY").box(rcx,rcy,rcz)                      # cutter
        rib_ledger   = cq.Workplane("XY").box(rl_1,rt,rw).translate((0,0,0))    # rib for ledger
        rib_ledger   = rib_ledger.cut(rc.translate((+rlxo,+ryo-rd,0)))          # ledger cutter x+ y+
        rib_ledger   = rib_ledger.cut(rc.translate((+rlxo,-ryo+rd,0)))          # ledger cutter x+ y-
        rib_ledger   = rib_ledger.cut(rc.translate((-rlxo,+ryo-rd,0)))          # ledger cutter x- y+
        rib_ledger   = rib_ledger.cut(rc.translate((-rlxo,-ryo+rd,0)))          # ledger cutter x- y-
        rib_ledger   = rib_ledger.rotate((0,0,0),(0,0,1),90)
        rib_stringer = cq.Workplane("XY").box(rl_2,rt,rw).translate((0,0,0))    # rib for stringer
        rib_stringer = rib_stringer.cut(rc.translate((+rsxo,+ryo-rd,0)))        # stringer cutter x+ y+
        rib_stringer = rib_stringer.cut(rc.translate((+rsxo,-ryo+rd,0)))        # stringer cutter x+ y-
        rib_stringer = rib_stringer.cut(rc.translate((-rsxo,+ryo-rd,0)))        # stringer cutter x- y+
        rib_stringer = rib_stringer.cut(rc.translate((-rsxo,-ryo+rd,0)))        # stringer cutter x- y-
        #show_object(rscxpym,name="cutter",options={"alpha":0.2,"color":(255,170,0)}) 
        #show_object(rib_ledger,name="rib",options={"alpha":0.2,"color":(255,170,0)})   
        #show_object(rib_stringer,name="rib",options={"alpha":0.2,"color":(255,170,0)})
 
        # frame
        fsl  = self.measures["stringer.length"]
        fll  = self.measures["ledger.length"]
        fjt  = self.measures["jamb.thickness"]
        fjs  = self.measures["jamb.side"]
        fjl  = self.measures["jamb.length"]
        frj  = self.measures["@rib.jut"]
        frw  = self.measures["rib.width"]
        frl  = self.measures["rib.length.2"]
        fxo  = fsl-0.5*fjs
        fyo  = 0.5*(fll+fjs)
        fzo  = 0.5*(fjl-frw)
        frxo = 0.5*(frl+fjs)-fjt-frj
        frame = jamb_middle.rotate((0,0,0),(0,0,1),180).translate((0,+fyo,0))                   # jamb front middle
        frame = frame.union(jamb_corner.rotate((0,0,0),(0,0,1),180).translate((+fxo,+fyo,0)))   # jamb front left
        frame = frame.union(jamb_corner.rotate((0,0,0),(0,0,1),-90).translate((-fxo,+fyo,0)))   # jamb front right
        frame = frame.union(jamb_middle.rotate((0,0,0),(0,0,1),0).translate((0,-fyo,0)))        # jamb back  middle
        frame = frame.union(jamb_corner.rotate((0,0,0),(0,0,1),+90).translate((+fxo,-fyo,0)))   # jamb back  left
        frame = frame.union(jamb_corner.rotate((0,0,0),(0,0,1),0).translate((-fxo,-fyo,0)))     # jamb back  right
        frame = frame.union(rib_ledger.translate((0,0,+fzo)))                                   # rib ledger middle
        frame = frame.union(rib_ledger.translate((+fxo,0,+fzo)))                                # rib ledger left
        frame = frame.union(rib_ledger.translate((-fxo,0,+fzo)))                                # rib ledger right
        frame = frame.union(rib_stringer.translate((+frxo,+fyo,+fzo)))                          # rib stringer front left
        frame = frame.union(rib_stringer.translate((-frxo,+fyo,+fzo)))                          # rib stringer front right
        frame = frame.union(rib_stringer.translate((+frxo,-fyo,+fzo)))                          # rib stringer back  left
        frame = frame.union(rib_stringer.translate((-frxo,-fyo,+fzo)))                          # rib stringer back  right
        #show_object(frame,name="frame",options={"alpha":0.2,"color":(255,170,0)})

        # duckboard
        dst  = self.measures["stringer.thickness"]
        dsl  = self.measures["stringer.length"]
        dlt  = self.measures["ledger.thickness"]
        dlw  = self.measures["ledger.width"]
        dll  = self.measures["ledger.length"]
        dbt  = self.measures["batten.thickness"]
        dbw1 = self.measures["batten.width.1"]
        dbw2 = self.measures["batten.width.2"]
        dbw3 = self.measures["batten.width.3"]
        dbg  = self.measures["batten.gap"]
        dbe  = self.measures["batten.extra"]
        djs  = self.measures["jamb.side"]
        dxo  = 0.5*(dsl-djs)
        dyo  = 0.5*(dll+djs)
        dzo  = 0.5*(dst+dbt)
        duckboard = stringer.translate((0,dyo,0))                                # stringer front
        duckboard = duckboard.union(stringer.translate((0,-dyo,0)))              # stringer back
        duckboard = duckboard.union(ledger_2.translate((+dxo,0,0)))              # ledger   right
        duckboard = duckboard.union(ledger_1.translate((-dxo-0.25*dlw,0,0)))     # ledger   left
        duckboard = duckboard.union(batten_3.translate((+dxo,0,dzo)))            # batten   right
        duckboard = duckboard.union(batten_1.translate((-dxo-0.25*dlw,0,dzo)))   # batten   left
        xo = -0.5*dsl+dbw1+dbe+dbg+0.5*dbw2
        for i in range(5):
            duckboard = duckboard.union(batten_2.translate((xo,0,dzo)))          # batten   middle
            xo = xo+dbw2+dbg
        #show_object(duckboard,name="duckboard",options={"alpha":0.2,"color":(255,170,0)})

        # bed
        bjl  = self.measures["jamb.length"]
        bst  = self.measures["stringer.thickness"]
        bsl  = self.measures["stringer.length"]
        bxo  = 0.5*bsl
        bzo1  = 0.5*bjl
        bzo2  = bjl+0.5*bst
        bed = frame.translate((0,0,bzo1))                                                # frame
        bed = bed.union(duckboard.translate((bxo,0,bzo2)))                               # half right
        bed = bed.union(duckboard.rotate((0,0,0),(0,0,1),180).translate((-bxo,0,bzo2)))  # half left
        #show_object(bed,name="bed",options={"alpha":0.2,"color":(255,170,0)})

        # parts
        jamb_moved     = jamb_corner.translate((0,0,0))
        rib_moved      = rib_stringer.translate((600,0,180))
        stringer_moved = stringer.translate((600,0,270))
        ledger_moved   = ledger_2.translate((0,500,270))
        batten_moved   = batten_3.translate((200,500,350))
        parts = jamb_moved.union(rib_moved).union(stringer_moved).union(ledger_moved).union(batten_moved)
        show_object(parts,name="parts",options={"alpha":0.2,"color":(255,170,0)})

        self.model = bed
        return

    pass

def main() -> None:
    simple_bed = SimpleBed(measures)
    return

if __name__ == "__main__" or __name__ == "temp":
    main()