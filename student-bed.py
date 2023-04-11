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

measures["batten.height"]      = measures["@thickness.1"]
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
        st = self.measures["stringer.thickness"]
        sw = self.measures["stringer.width"]
        sl = self.measures["stringer.length"]
        stringer = cq.Workplane("XY").box(sl,sw,st)
        #show_object(stringer,name="stringer",options={"alpha":0.2,"color":(255,170,0)})

        lt = self.measures["ledger.thickness"]
        lw = self.measures["ledger.width"]
        ll = self.measures["ledger.length"]
        ledger = cq.Workplane("XY").box(lw,ll,lt)
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

        jt  = self.measures["jamb.thickness"]
        js  = self.measures["jamb.side"]
        jl  = self.measures["jamb.length"]
        jcw = self.measures["jamb.cut.width"]
        jcd = self.measures["jamb.cut.depth"]
        jca = self.measures["jamb.cut.air"]
        jcx  = js
        jcy  = 2*(jcw+jca)
        jcz  = 2*(jcd+jca)
        jc          = cq.Workplane("XY").box(jcx,jcy,jcz).translate((0.5*js,0,0.5*jl))  # cutter
        jamb        = cq.Workplane("XY").box(js,js,jl).faces("<Z or >Z").shell(-jt)     # shell
        jamb_corner = jamb.cut(jc.rotate((0,0,0),(0,0,1),0))                            # cut x+
        jamb_corner = jamb_corner.cut(jc.rotate((0,0,0),(0,0,1),90))                    # cut y+
        jamb_middle = jamb_corner.cut(jc.rotate((0,0,0),(0,0,1),180))                   # cut x-
        #show_object(jc,name="cutter",options={"alpha":0.2,"color":(255,170,0)})    
        #show_object(jamb_middle,name="jamb",options={"alpha":0.2,"color":(255,170,0)})

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
        rlcxpyp      = cq.Workplane("XY").box(rcx,rcy,rcz).translate((+rlxo,+ryo-rd,0))   # ledger cutter x+ y+
        rlcxpym      = cq.Workplane("XY").box(rcx,rcy,rcz).translate((+rlxo,-ryo+rd,0))   # ledger cutter x+ y-
        rlcxmyp      = cq.Workplane("XY").box(rcx,rcy,rcz).translate((-rlxo,+ryo-rd,0))   # ledger cutter x- y+
        rlcxmym      = cq.Workplane("XY").box(rcx,rcy,rcz).translate((-rlxo,-ryo+rd,0))   # ledger cutter x- y-
        rib_ledger   = cq.Workplane("XY").box(rl_1,rt,rw).translate((0,0,0))              # rib for ledger
        rib_ledger   = rib_ledger.cut(rlcxpyp)
        rib_ledger   = rib_ledger.cut(rlcxpym)
        rib_ledger   = rib_ledger.cut(rlcxmyp)
        rib_ledger   = rib_ledger.cut(rlcxmym)
        rscxpyp      = cq.Workplane("XY").box(rcx,rcy,rcz).translate((+rsxo,+ryo-rd,0))   # stringer cutter x+ y+
        rscxpym      = cq.Workplane("XY").box(rcx,rcy,rcz).translate((+rsxo,-ryo+rd,0))   # stringer cutter x+ y-
        rscxmyp      = cq.Workplane("XY").box(rcx,rcy,rcz).translate((-rsxo,+ryo-rd,0))   # stringer cutter x- y+
        rscxmym      = cq.Workplane("XY").box(rcx,rcy,rcz).translate((-rsxo,-ryo+rd,0))   # stringer cutter x- y-
        rib_stringer = cq.Workplane("XY").box(rl_2,rt,rw).translate((0,0,0))              # rib for stringer
        rib_stringer = rib_stringer.cut(rscxpyp)
        rib_stringer = rib_stringer.cut(rscxpym)
        rib_stringer = rib_stringer.cut(rscxmyp)
        rib_stringer = rib_stringer.cut(rscxmym)
        #show_object(rscxpym,name="cutter",options={"alpha":0.2,"color":(255,170,0)}) 
        #show_object(rib_ledger,name="rib",options={"alpha":0.2,"color":(255,170,0)})   
        show_object(rib_stringer,name="rib",options={"alpha":0.2,"color":(255,170,0)})

        fsrt = self.measures["rib.thickness"]
        fsrl = self.measures["rib.length.2"]
        fsrj = self.measures["@rib.jut"]
        fsl  = self.measures["stringer.length"]
        fll  = self.measures["ledger.length"]
        fjs  = self.measures["jamb.side"]
        fjl  = self.measures["jamb.length"]
        frw  = self.measures["rib.width"]
        fxo  = fsl-0.5*fjs
        fyo  = 0.5*(fll+fjs)
        fzo  = 0.5*(fjl-frw)
        frxo = 0.5*fsl-fsrt
        #frame = jamb_middle.translate((0,-fyo,0))                                                 # jamb front middle
        #frame = frame.union(jamb_middle.rotateAboutCenter((0,0,1),180).translate((0,+fyo,0)))     # jamb back  middle
        #frame = frame.union(jamb_corner.rotateAboutCenter((0,0,1),180).translate((+fxo,+fyo,0)))  # jamb front left
        #frame = frame.union(jamb_corner.rotateAboutCenter((0,0,1),-90).translate((-fxo,+fyo,0)))  # jamb front right
        #frame = frame.union(jamb_corner.rotateAboutCenter((0,0,1),+90).translate((+fxo,-fyo,0)))  # jamb back  left
        #frame = frame.union(jamb_corner.rotateAboutCenter((0,0,1),0).translate((-fxo,-fyo,0)))    # jamb back  right
        #frame = frame.union(ledger_rib.translate((0,0,+fzo)))                                     # ledger rib middle
        #frame = frame.union(ledger_rib.translate((+fxo,0,+fzo)))                                  # ledger rib left
        #frame = frame.union(ledger_rib.translate((-fxo,0,+fzo)))                                  # ledger rib right
        #frame = frame.union(stringer_rib.translate((frxo,+fyo,+fzo)))                                      # stringer rib front left

        #show_object(frame,name="frame",options={"alpha":0.2,"color":(255,170,0)})

        #ToDo: add new parts
        stringer_moved = stringer.translate((600,0,250))
        ledger_moved   = ledger.translate((0,500,250))
        batten_moved   = batten_3.translate((0,500,350))
        parts = jamb.union(stringer_moved).union(ledger_moved).union(batten_moved)
        #show_object(parts,name="parts",options={"alpha":0.2,"color":(255,170,0)})

        return

    pass

def main() -> None:
    simple_bed = SimpleBed(measures)
    return

if __name__ == "__main__" or __name__ == "temp":
    main()