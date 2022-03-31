from decimal import ROUND_DOWN
import math
import tkinter as tk
import weakref
from zipfile import ZipFile
import time
import numpy as np

basename = "layer"

prefactor = 1
######################
D1 = 12.7 * 1000
D2 = 25.4 * 1000
D3 = 9.53 * 1000 #SMA 9.53 SMP 5.84
D4 = 2.79 * 1000
D5 = 1.27 * 1000
D6 = 0.25 * 1000
D7 =  0.2794 * 1000
D8  = 0.61 * 1000
D9  = 2 * 1000
D10 = 0.0762 * 1000
D11 = 0.3302 * 1000
D12 = 1.0 * 1000 #doublecheck #changed here D12 and D13 for consistency with new function, any issue?
D13 = 0.5 * 1000
D14 = 0.15
D16 = 10 * 1000
D17 = 2.06
D18 = 0.4064 * 1000   #length cutout
D19 =  0.6096 * 1000 #width cutout



window = tk.Tk()
window.geometry("690x600")
def inputd(number, default):
        default = str(default)
        label = "D" + str(number)
        tk.Label(window, text=label).grid(row=(number-1))
        e1 = tk.Entry(window)
        e1.grid(row=(number-1), column=1)
        e1.insert(-1, default)
        return e1
        
E1 = inputd(1, D1/1000)
E2 = inputd(2, D2/1000)
E3 = inputd(3, D3/1000)
E4 = inputd(4, D4/1000)
E5 = inputd(5, D5/1000)
E6 = inputd(6, D6/1000)
E7 = inputd(7, D7/1000)
E8 = inputd(8, D8/1000)
E9 = inputd(9, D9/1000)
E10 = inputd(10, D10/1000)
E11 = inputd(11, D11/1000)
E12 = inputd(12, D12/1000)
E13 = inputd(13, D13/1000)
E14 = inputd(14, D14)
E16 = inputd(16, D16/1000)
E17 = inputd(17, D17)
E18 = inputd(18, D18/1000)
E19 = inputd(19, D19/1000)

tk.Label(window, text="Name:").grid(row=(19))
namef = tk.Entry(window)
namef.grid(row=(19), column=1)
namef.insert(-1, "layername")


def overwrite():
        global D1
        global D2
        global D3
        global D4
        global D5
        global D6
        global D7
        global D8
        global D9
        global D10
        global D11
        global D12
        global D13
        global D14
        global D16
        global D17
        global D18
        global D19
        global basename
        D1 = float(E1.get()) * 1000 * prefactor
        D2 = float(E2.get()) * 1000 * prefactor
        D3 = float(E3.get()) * 1000 * prefactor
        D4 = float(E4.get()) * 1000 * prefactor
        D5 = float(E5.get()) * 1000 * prefactor
        D6 = float(E6.get()) * 1000 * prefactor
        D7 = float(E7.get()) * 1000 * prefactor
        D8 = float(E8.get()) * 1000 * prefactor
        D9  = float(E9.get()) * 1000 * prefactor
        D10 = float(E10.get()) * 1000 * prefactor
        D11 = float(E11.get()) * 1000 * prefactor
        D12 = float(E12.get()) * 1000 * prefactor
        D13 = float(E13.get()) * 1000 * prefactor
        D14 = float(E14.get()) * prefactor
        D16 = float(E16.get()) * 1000 * prefactor
        D17 = float(E17.get()) * prefactor
        D18 = float(E18.get()) * 1000 * prefactor
        D19 = float(E19.get()) * 1000 * prefactor
        basename = namef.get()
        window.destroy()




butt = tk.Button(text ="Generate", command = overwrite)
butt.grid(row = 20, column = 0)

canvas = tk.Canvas(window, width = 1500, height = 3000) 
canvas.grid(column = 3, row = 0, columnspan=300, rowspan=300)
img = tk.PhotoImage(file="ref.png")     
canvas.create_image(20,20, anchor=tk.NW, image=img)   

window.mainloop()

######################

#trace parsing 
Seg_types = np.array([  0,  -1,   0,   1,   0,   1,   0,  -1,   0,  -1,   0,   1,   0]) #0 is straight, 1 is right turn, -1 is left turn
Seg_dims  = np.array([5.0, 2.5, 0.5, 2.5, 0.2, 2.5, 6.0, 2.5, 0.2, 2.5, 0.5, 2.5, 5.0])
Seg_lengths = Seg_dims+(np.pi/2-1)*np.absolute(Seg_types)*Seg_dims

Trace_cumlength = np.cumsum(Seg_lengths)
Trace_numvias = math.floor((Trace_cumlength[-1])/(D13/1000))-1
Tracer_disfirstvia = (Trace_cumlength[-1])-(Trace_numvias*(D13/1000))
print(Tracer_disfirstvia)
Trace_viapos = np.array(range(Trace_numvias))*(D13/1000) + Tracer_disfirstvia

Seg_endnumvia=np.zeros_like(Seg_types)
Via_coords=[]
Tracer_x=D1/2000 #This is a trace start parameter
Tracer_y=0 #This is a trace start parameter
Tracer_dir=np.pi/2 #This is a trace start parameter
for seg_idx,seg_type in enumerate(Seg_types):
    Seg_endnumvia[seg_idx] = np.searchsorted(Trace_viapos,Trace_cumlength[seg_idx])
print(Seg_endnumvia)
Seg_endnumvia[1:] = Seg_endnumvia[1:]-Seg_endnumvia[:-1]
print(Seg_endnumvia)
for seg_idx,seg_type in enumerate(Seg_types):
    # generate positions for this segment
    for via_idx in range(Seg_endnumvia[seg_idx]):
        if Seg_types[seg_idx]==0:
            x=Tracer_x+(Tracer_disfirstvia+via_idx*(D13/1000))*np.cos(Tracer_dir)
            y=Tracer_y+(Tracer_disfirstvia+via_idx*(D13/1000))*np.sin(Tracer_dir)
            ang=Tracer_dir+np.pi/2
            Via_coords = Via_coords+[[x,y,ang]]
        elif Seg_types[seg_idx]==1:
            arc_center_x=Tracer_x+np.cos(Tracer_dir-np.pi/2)*Seg_dims[seg_idx]
            arc_center_y=Tracer_y+np.sin(Tracer_dir-np.pi/2)*Seg_dims[seg_idx]
            arc_startangle=Tracer_dir+np.pi/2
            ang=arc_startangle-(Tracer_disfirstvia+via_idx*(D13/1000))/Seg_lengths[seg_idx]*np.pi/2
            x=arc_center_x+Seg_dims[seg_idx]*np.cos(ang)
            y=arc_center_y+Seg_dims[seg_idx]*np.sin(ang)
            Via_coords = Via_coords+[[x,y,ang]]
        else:
            arc_center_x=Tracer_x+np.cos(Tracer_dir+np.pi/2)*Seg_dims[seg_idx]
            arc_center_y=Tracer_y+np.sin(Tracer_dir+np.pi/2)*Seg_dims[seg_idx]
            arc_startangle=Tracer_dir-np.pi/2
            ang=arc_startangle+(Tracer_disfirstvia+via_idx*(D13/1000))/Seg_lengths[seg_idx]*np.pi/2
            x=arc_center_x+Seg_dims[seg_idx]*np.cos(ang)
            y=arc_center_y+Seg_dims[seg_idx]*np.sin(ang)
            Via_coords = Via_coords+[[x,y,ang]]
    #find parameters for next segment
    if Seg_types[seg_idx]==0:
        Tracer_x=Tracer_x+np.cos(Tracer_dir)*Seg_dims[seg_idx]
        Tracer_y=Tracer_y+np.sin(Tracer_dir)*Seg_dims[seg_idx]
    elif Seg_types[seg_idx]==1:
        Tracer_x=Tracer_x+np.cos(Tracer_dir-np.pi/4)*np.sqrt(2)*Seg_dims[seg_idx]
        Tracer_y=Tracer_y+np.sin(Tracer_dir-np.pi/4)*np.sqrt(2)*Seg_dims[seg_idx]
        Tracer_dir=Tracer_dir-np.pi/2
    else:
        Tracer_x=Tracer_x+np.cos(Tracer_dir+np.pi/4)*np.sqrt(2)*Seg_dims[seg_idx]
        Tracer_y=Tracer_y+np.sin(Tracer_dir+np.pi/4)*np.sqrt(2)*Seg_dims[seg_idx]
        Tracer_dir=Tracer_dir+np.pi/2
    Tracer_disfirstvia=(D13/1000)-Seg_lengths[seg_idx]+(Tracer_disfirstvia+(Seg_endnumvia[seg_idx]-1)*(D13/1000))
    
    
######################
init =  """G04*
G04*
G04 Layer_Physical_Order=1*
G04 Layer_Color=255*
%FSLAX25Y25*%
%MOIN*%
%SFA3.937B3.937*%
G70*
G04*
G04*
G04*
G04 #@! TF.FilePolarity,Positive*
G04*
G01*
G75*
%ADD12C,0.00050*%
%ADD13C,0.08268*%
%ADD14C,0.00787*%
"""
end = "M02*"













# D01* = Light on
# D02* = Light off
# 1000 = 1mm

file = open(basename+".gtl", "w+")
file.truncate(0)

print(init)
file.write(init)


#Left Ground Plane with Trace
def draw(point, light):
        print("X%dY%d%s*"%(point[0],point[1], light))
        file.write("X%dY%d%s*\n"%(point[0],point[1], light))

#left side
p1 = [0,0]
p2 = [p1[0], p1[1] + D2]
p3 = [p2[0]+(D1/2)-(D8/2), p2[1] + 0]
p4 = [(D1/2)-(D8/2),(D2/2)+(D16/2)+D9]
p5 = [p4[0]+((D8-D7)/2), p4[1]-D9]
p6 = [p5[0]+0,p5[1]-D16]
p7 = [p4[0], p4[1]-D16-(2*D9)]
p8 = [p7[0], 0]
points =  [p1,p2,p3,p4,p5,p6,p7,p8,p1]
#############
print("G36*\n")
file.write("G36*\n")

draw(p1, "D02")
for x in points:
        draw(x, "D01")
print("G37*\n")
file.write("G37*\n")
#left side
##############
##############
#right side 
print("G36*\n")
file.write("G36*\n")   
pointsr = []
middle = D1/2
middle2 = D2/2
for x in points:
        pointsr.append([(middle-x[0])+middle, x[1]])

 

draw(pointsr[0], "D02")
for x in pointsr:
        draw(x, "D01")
print("G37*\n")
file.write("G37*\n") 
###############
#right side


#middle strip
pm1 = [(D1/2)-(D6/2), 0]
pm2 = [pm1[0], D5]
pm3 = [(D1/2)-(D7/2), D5]
pm4 = [pm3[0], (D2/2)-(D16/2)-D9]
pm5 = [(D1/2)-(D10/2), (D2/2)-(D16/2)]
pm6 = [pm5[0], (D2/2)]
pm7 = [D1/2, D2/2]
pm8 = [D1/2, 0]
pointsm = [pm1,pm2,pm3,pm4,pm5,pm6,pm7,pm8,pm1]
################
print("G36*\n")
file.write("G36*\n")

draw(pointsm[0], "D02")
for x in pointsm:
        draw(x, "D01")

print("G37*\n")
file.write("G37*\n")
##############
###############
print("G36*\n")
file.write("G36*\n")
pointsmr = []
for x in pointsm:
        pointsmr.append([(middle-x[0])+middle, x[1]])


draw(pointsmr[0], "D02")
for x in pointsmr:
        draw(x, "D01")


print("G37*\n")
file.write("G37*\n")
###############
###############
print("G36*\n")
file.write("G36*\n")
pointsmu = []
for x in pointsm:
        pointsmu.append([x[0],(middle2-x[1])+middle2])


draw(pointsmu[0], "D02")
for x in pointsmu:
        draw(x, "D01")


print("G37*\n")
file.write("G37*\n")
####################
####################
print("G36*\n")
file.write("G36*\n")
pointsmur = []
for x in pointsm:
        pointsmur.append([(middle-x[0])+middle,(middle2-x[1])+middle2])


draw(pointsmur[0], "D02")
for x in pointsmur:
        draw(x, "D01")


print("G37*\n")
file.write("G37*\n")
###################

#middle strip


print(end)
file.write(end)
file.close()




# Drill files 

def toinchtz(mm):
        mils = (mm/25.4) *1000
        mils = round(mils)
        mils = str(mils)
        """
        if len(mils) > 5:
                mils = mils[0:5]

        if len(mils) < 5:
                howzero = 5-len(mils)

                for x in range(0, howzero):
        
                        mils = mils + "00"
        """
        mils = mils + "00"
        return(mils)
        
def toinchtz2(mm):
        """
        zeros = 5
        """
        mils = ((mm/25.4) *1000)/3.93701
        cenmils = int(round(mils,1)*100)
        cenmils = str(cenmils)
        """
        if len(mils) > zeros:
                mils = mils[0:zeros]

        if len(mils) < zeros:
                howzero = zeros-len(mils)

                for x in range(0, howzero):
        
                        mils = mils + "0"
        """
        return(cenmils)





D14 = (D14 / 25.4)#/3.947
D17 = (D17 / 25.4)#/3.947

initdrill = """M48
;Layer_Color=9474304
;FILE_FORMAT=2:5
INCH,TZ
;TYPE=PLATED
"""


file = open(basename + ".txt", "w+")
file.truncate(0)

file.write(initdrill)

viat1 = ("T1F00S00C%f"%(D14/3.93701))
holet2 = ("T2F00S00C%f"%(D17/3.93701))

file.write(viat1+"\n")
file.write(holet2+"\n")
file.write("%\n")
file.write("T01\n")

# D12 = 1.5
# D13 = 0.6

# xvial = (D1/2000) - (D12/2)
# xviar = (D1/2000) + (D12/2)
# print(xvial)
# print(xviar)


# numvias =  math.floor((D2/1000)/(D13+D14))
# disfirstvia = (D2/1000)-(numvias*D13)

# for x in range(numvias):
#         print("------------->  " + str(disfirstvia))
#         file.write("""X%sY%s\n"""%(toinchtz2(xvial),toinchtz2(disfirstvia)))
#         print("X%sY%s"%(toinchtz2(xvial),toinchtz2(disfirstvia)))
#         disfirstvia = disfirstvia + D13

# disfirstvia = (D2/1000)-(numvias*D13)

# for x in range(numvias):
#         file.write("""X%sY%s\n"""%(toinchtz2(xviar),toinchtz2(disfirstvia)))
#         disfirstvia = disfirstvia + D13

for via_idx,via_coord in enumerate(Via_coords):
    via_x=via_coord[0]-np.cos(via_coord[2])*D12/2000
    via_y=via_coord[1]-np.sin(via_coord[2])*D12/2000
    print("via L" + str(via_idx) + "-------------> " + str(via_x) + ", " + str(via_y))
    print("before--->" + str(via_x))
    print("after----> " + str(toinchtz2(via_x)))
    file.write("""X%sY%s\n"""%(toinchtz2(via_x),toinchtz2(via_y)))
    print("X%sY%s"%(toinchtz2(via_x),toinchtz2(via_y)))
    via_x=via_coord[0]+np.cos(via_coord[2])*D12/2000
    via_y=via_coord[1]+np.sin(via_coord[2])*D12/2000
    print("via R" + str(via_idx) + "-------------> " + str(via_x) + ", " + str(via_y))
    file.write("""X%sY%s\n"""%(toinchtz2(via_x),toinchtz2(via_y)))
    print("X%sY%s"%(toinchtz2(via_x),toinchtz2(via_y)))

h1 = [(D1-D3)/2, D4]
h1 = [h1[0]/1000, h1[1]/1000]
h2 = [h1[0]+(D3/1000), h1[1]]
h3 = [h1[0], h1[1]+((D2-D4-D4)/1000)]
h4 = [h2[0], h3[1]]
print(h1, h2, h3, h4)

#coordinates
file.write("T02\n")
file.write("""X%sY%s\n"""%(toinchtz2(h1[0]),toinchtz2(h1[1])))
file.write("""X%sY%s\n"""%(toinchtz2(h2[0]),toinchtz2(h2[1])))
file.write("""X%sY%s\n"""%(toinchtz2(h3[0]),toinchtz2(h3[1])))
file.write("""X%sY%s\n"""%(toinchtz2(h4[0]),toinchtz2(h4[1])))
print("Vias--> " + str(len(Via_coords)))
file.write("M30")
file.close()


def groundplane(filename):
        file = open(filename, "w+")
        file.truncate(0)
        file.write(init)
        file.write("G36*\n")
        p1 = [0,0]
        pcc1 = [(D1/2)-(D18/2), 0]
        pcc2 = [pcc1[0], D19]
        pcc3 = [(D1/2)+(D18/2), D19]
        pcc4 = [(D1/2)+(D18/2), 0]
        p2 = [D1,0]
        p3 = [D1,D2]
        pc1 = [(D1/2)+(D18/2), D2]
        pc2 = [pc1[0], (D2-D19)]
        pc3 = [(D1/2)-(D18/2), pc2[1]]
        pc4 = [(D1/2)-(D18/2), D2]
        p4 = [0,D2]
        pointsgp = [p1,pcc1,pcc2,pcc3,pcc4,p2,p3,pc1,pc2,pc3,pc4,p4,p1]
        for x in pointsgp:
                print("X%dY%d%s*\n"%(x[0],x[1], "D1"))
                file.write("X%dY%d%s*\n"%(x[0],x[1], "D1"))

        

        

        
        file.write("G37*\n")
        file.write(end)
        file.close()

def solder(filename):
        file = open(filename, "w+")
        file.truncate(0)
        file.write(init)
        file.write("G36*\n")
        p1 = [0,0]
        p2 = [D1,0]
        p3 = [D1,D2]
        p4 = [0,D2]
        pointsgp = [p1,p2,p3,p4,p1]
        for x in pointsgp:
                print("X%dY%d%s*\n"%(x[0],x[1], "D1"))
                file.write("X%dY%d%s*\n"%(x[0],x[1], "D1"))  

        
        file.write("G37*\n")
        file.write(end)
        file.close()


init =  """G04*
G04*
G04 Layer_Color=16711680*
%FSLAX25Y25*%
%MOIN*%
%SFA3.937B3.937*%
G70*
G04*
G04*
G04*
G04 #@! TF.FilePolarity,Positive*
G04*
G01*
G75*
%ADD13C,0.08268*%
%ADD14C,0.00787*%

"""
groundplane(basename + ".gbl")
init =  """G04*
G04*
G04 Layer_Physical_Order=2*
G04 Layer_Color=36540*
%FSLAX25Y25*%
%MOIN*%
%SFA3.937B3.937*%
G70*
G04*
G04*
G04*
G04 #@! TF.FilePolarity,Positive*
G04*
G01*
G75*
%ADD13C,0.08268*%
%ADD14C,0.00787*%
"""
groundplane(basename + ".g1")
init =  """G04*
G04*
G04 Layer_Physical_Order=3*
G04 Layer_Color=16711680*
%FSLAX25Y25*%
%MOIN*%
%SFA3.937B3.937*%
G70*
G04*
G04*
G04*
G04 #@! TF.FilePolarity,Positive*
G04*
G01*
G75*
%ADD13C,0.08268*%
%ADD14C,0.00787*%
"""
groundplane(basename + ".g2")

init = """G04*
G04*
G04 Layer_Color=8388736*
%FSLAX25Y25*%
%MOIN*%
%SFA3.937B3.937*%
G70*
G04*
G04*
G04*
G04 #@! TF.FilePolarity,Negative*
G04*
G01*
G75*
%ADD10C,0.09068*%
%ADD11C,0.01587*%"""

solder(basename + ".GTS")
solder(basename + ".GBS")


def mechanical(filename,initin):
        file = open(filename, "w+")
        file.truncate(0)
        file.write(initin)
        file.write("%ADD15C,0.00800*%\n")
        file.write("D15*\n")
        p1 = [0,0]
        p2 = [D1,0]
        p3 = [D1,D2]
        p4 = [0,D2]
        pointsgp = [p1,p2,p3,p4]
        """
        for x in pointsgp:
                print("X%dY%d%s*\n"%(x[0],x[1], "D01"))
                file.write("X%dY%d%s*\n"%(x[0],x[1], "D01"))
        """
        file.write("X%dY%d%s*\n"%(p1[0],p1[1], "D02"))
        file.write("X%dY%d%s*\n"%(p2[0],p2[1], "D01"))
        file.write("X%dY%d%s*\n"%(p2[0],p2[1], "D02"))
        file.write("X%dY%d%s*\n"%(p3[0],p3[1], "D01"))
        file.write("X%dY%d%s*\n"%(p3[0],p3[1], "D02"))
        file.write("X%dY%d%s*\n"%(p4[0],p4[1], "D01"))
        file.write("X%dY%d%s*\n"%(p4[0],p4[1], "D02"))
        file.write("X%dY%d%s*\n"%(p1[0],p1[1], "D01"))




        #file.write("X0Y0D01*\n")
        file.write(end)
        file.close()

init =  """G04*
G04 #@! TF.GenerationSoftware,Altium Limited,Altium Designer,21.7.1 (17)*
G04*
G04 Layer_Color=16711935*
%FSLAX25Y25*%
%MOIN*%
%SFA3.937B3.937*% 
G70*
G04*
G04 #@! TF.SameCoordinates,EAAEF115-C746-42B2-B974-C945C9191EC5*
G04*
G04*
G04 #@! TF.FilePolarity,Positive*
G04*
G01*
G75*
"""

mechanical(basename + ".GM1", init)
print("Succesfully Created Gerber Files")

time.sleep(1)

zipObj = ZipFile(basename + '.zip', 'w')
zipObj.write(basename + '.g1')
zipObj.write(basename + '.g2')
zipObj.write(basename + '.gbl')
zipObj.write(basename + '.GBS')
zipObj.write(basename + '.GM1')
zipObj.write(basename + '.gtl')
zipObj.write(basename + '.GTS')
zipObj.write(basename + '.txt')
zipObj.close()