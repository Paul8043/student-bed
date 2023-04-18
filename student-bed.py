"""
@author: Paul8043
"""

import cadquery as cq
from cadquery import exporters

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
    "@rib.jut":16,
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
measures["rib.cut.air"]        = 0

measures["batten.thickness"]   = measures["@thickness.1"]
measures["batten.width.1"]     = measures["@width.1"]
measures["batten.width.2"]     = measures["@width.2"]
measures["batten.width.3"]     = measures["@width.3"]
measures["batten.length"]      = measures["mattress.width"]
measures["batten.gap"]         = 78
measures["batten.extra"]       = (measures["stringer.length"]-measures["batten.width.3"]
-5*measures["batten.width.2"]-6*measures["batten.gap"]-measures["batten.width.1"])/2

measures["jamb.thickness"]  = measures["@thickness.2"]      # -2.5  for 3D-printing
measures["jamb.side"]       = measures["@side.length"]
measures["jamb.length"]     = measures["mattress.altitude"]-measures["@thickness.1"]-measures["@thickness.2"]
measures["jamb.cut.width"]  = measures["@thickness.1"]
measures["jamb.cut.depth"]  = measures["@width.2"]
measures["jamb.cut.air"]    = 0                             # 1.3  for 3D-printing

# model class

class SimpleBed:

    def __init__(self,measures) -> None:
        self.model     = None
        self.measures  = measures
        self.dump()
        self.bom()
        self.build()
        self.jamb_broad()
        self.jamb_small()
        self.jamb_jig()
        self.rib_short()
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
        jcx  = js+2*jca
        jcy  = jcw+2*jca
        jcz  = 2*(jcd+jca)
        #echo(f"jamb-cutter:{jcx},{jcy},{jcz}")
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
        #echo(f"rib-cutter:{rcx},{rcy},{rcz}")
        #echo(f"rd:{rd}")
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
        #show_object(rc,name="cutter",options={"alpha":0.2,"color":(255,170,0)}) 
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
        #show_object(parts,name="parts",options={"alpha":0.2,"color":(255,170,0)})

        # 3D-Printing
        batch_1 = jamb_corner.translate((0,0,0))
        batch_1 = batch_1.union(jamb_middle.translate((200,0,0)))
        batch_1 = batch_1.union(jamb_corner.translate((400,0,0)))
        batch_1 = batch_1.union(jamb_corner.translate((0,200,0)))
        batch_1 = batch_1.union(jamb_middle.translate((200,200,0)))
        batch_1 = batch_1.union(jamb_corner.translate((400,200,0)))

        stringer_flat = rib_stringer.rotate((1,0,0),(0,0,0),90)
        ledger_flat   = rib_ledger.rotate((0,0,0),(0,0,1),90).rotate((1,0,0),(0,0,0),90)
        #show_object(ledger_flat,name="stringer",options={"alpha":0.2,"color":(255,170,0)})
        batch_2 = stringer_flat.translate((0,0,0))
        batch_2 = batch_2.union(stringer_flat.translate((0,150,0)))
        batch_2 = batch_2.union(stringer_flat.translate((0,300,0)))
        batch_2 = batch_2.union(stringer_flat.translate((0,450,0)))
        batch_2 = batch_2.union(ledger_flat.translate((0,600,0)))
        batch_2 = batch_2.union(ledger_flat.translate((0,750,0)))
        batch_2 = batch_2.union(ledger_flat.translate((0,900,0)))

        batch_3 = duckboard.rotate((0,0,0),(0,1,0),180)

        exporters.export(batch_1.val().scale(0.1), 'docs/batch_1.stl', exporters.ExportTypes.STL)
        exporters.export(batch_2.val().scale(0.1), 'docs/batch_2.stl', exporters.ExportTypes.STL)
        exporters.export(batch_3.val().scale(0.1), 'docs/batch_3.stl', exporters.ExportTypes.STL)

        #show_object(batch_2,name="batch_1",options={"alpha":0.2,"color":(255,170,0)})

        self.model = bed
        return

    def bom(self) -> None:
        jl   = self.measures["jamb.length"]
        js   = self.measures["jamb.side"]
        jt   = self.measures["jamb.thickness"]
        rl_1 = self.measures["rib.length.1"]
        rl_2 = self.measures["rib.length.2"]
        rw   = self.measures["rib.width"]
        rt   = self.measures["rib.thickness"]
        sl   = self.measures["stringer.length"]
        sw   = self.measures["stringer.width"]
        st   = self.measures["stringer.thickness"]
        ll   = self.measures["ledger.length"]
        lw   = self.measures["ledger.width"]
        lt   = self.measures["ledger.thickness"]
        bl   = self.measures["batten.length"]
        bw   = self.measures["batten.width.3"]
        bt   = self.measures["batten.thickness"]
        jamb_broad  = f"12,JB,jamb broad,beech,{jl} x {js} x {jt},,diy-store\n"
        jamb_small  = f"12,JS,jamb small,beech,{jl} x {js-2*jt} x {jt},,diy-store\n"
        rib_long    = f"4,RL,rib long,beech,{rl_2} x {rw} x {rt},,diy-store\n"
        rib_short   = f"3,RS,rib short,beech,{rl_1} x {rw} x {rt},,diy-store\n"
        stringer    = f"4,S,stringer,beech,{sl} x {sw} x {st},,diy-store\n"
        ledger      = f"3,L,ledger,beech,{ll} x {lw} x {lt},,diy-store\n"
        batten      = f"11,B,batten,beech,{bl} x {bw} x {bt},,diy-store\n"
        screw_long  = f"24,SL,screw long,steel A2,M6 x 65,1102706065,www.frantos.com\n"
        screw_short = f"50,SS,screw short,steel A2,M6 x 35,1102706035,www.frantos.com\n"
        insert      = f"74,IS,insert SKD330,steel zinc plated,M6 x 18,420618001,www.rampa.com\n"
        with open("docs/bom.csv", "w", encoding="ascii") as f:
            header =f"QTY,REF-DSG,NAME,MATERIAL,DIMENSIONS,MPN,URL\n"
            f.write(header)
            f.write(jamb_broad)
            f.write(jamb_small)
            f.write(rib_long)
            f.write(rib_short)
            f.write(stringer)
            f.write(ledger)
            f.write(batten)
            f.write(screw_long)
            f.write(screw_short)
            f.write(insert)
        return

    def jamb_broad(self) -> None:
        jl  = self.measures["jamb.length"]
        js  = self.measures["jamb.side"]
        jt  = self.measures["jamb.thickness"]
        jcw = self.measures["jamb.cut.width"]
        jcd = self.measures["jamb.cut.depth"]
        xo = 0.5*(jl-jcd)+2.5
        jamb_outer = cq.Workplane("XY").rect(10+jl+10,10+js+10)                # outer
        jamb_inner = cq.Workplane("XY").rect(jl,js)                            # inner
        jamb_cut   = cq.Workplane("XY").rect(jcd+5,jcw).translate((-xo,0,0))   # cut
        #show_object(jamb_outer,name="jamb_outer",options={"alpha":0.2,"color":(255,170,0)})
        #show_object(jamb_inner,name="jamb_inner",options={"alpha":0.2,"color":(255,170,0)})
        #show_object(jamb_cut,name="jamb_cut",options={"alpha":0.2,"color":(255,170,0)})
        jamb_broad = cq.Assembly()
        jamb_broad.add(jamb_outer,name="outer",color=cq.Color("blue"))
        jamb_broad.add(jamb_inner,name="inner",color=cq.Color("black"))
        jamb_broad.add(jamb_cut,name="cut",color=cq.Color("red"))
        #show_object(jamb_broad,name="jamb_broad",options={"alpha":0.2,"color":(255,170,0)})
        show_object(jamb_broad,name="jamb_broad",options={"alpha":0.2,"color":(255,170,0)})

        #exporters.export(jamb_broad,"docs/object.dxf",opt={"doc_units":4})

        return
    
    def jamb_small(self) -> None:
        return

    def jamb_jig(self) -> None:
        return

    def rib_short(self) -> None:
        return    

    pass

def main() -> None:
    simple_bed = SimpleBed(measures)
    return

if __name__ == "__main__" or __name__ == "temp":
    main()