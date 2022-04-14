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
D1 = 12.7 * 1000 #Checked
D2 = 25.4 * 1000 #Checked
D3 = 9.53 * 1000 #SSMA = 9.53 #1.85 =  5.84
D4 = 2.79 * 1000 #Checked
D5 = 1.27 * 1000 #SSMA = 1.27mm #1.85 = 0.762mm  #Checked
D6 = 0.25 * 1000 #SSMA = 0.25 #1.86 = 0.25 #Checked
D7 =  0.2794 * 1000 #Checked
D8  = 0.61 * 1000 #Checked
D9  = 0.3 * 1000 #Checked 
D10 = 0.0762 * 1000 #Chekced
D11 = 0.3302 * 1000 #Checked
D12 = 1.0 * 1000 #Checked
D13 = 0.6 * 1000 #Checked
D14 = 0.15 #Checked
D16 = 5.0 * 1000 #None, 2,5,10mm #Checked
D17 = 2.06 #SSMA = 1.98 #1.85 = 2.06 #Checked
D18 = 0.4064 * 1000 #y dim GND cutout #1.85 = no antipad #SSMA = 0.4064 #Checked
D19 =  0.508 * 1000   #x dim GND Cutout #1.85 = no antipad #SSMA = 0.508 #Checked

D30 = 3.0 * 1000 #Cutout width #Checked
D31 = 1.2 * 1000 #Cutout overlapf #Checked


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


#### Tkinter Guy ####
window = tk.Tk()
window.geometry("690x690")
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

butt = tk.Button(text ="Generate", command = overwrite)
butt.grid(row = 20, column = 0)

mirror_bool = tk.IntVar()
tk.Checkbutton(window, text="mirror?", variable=mirror_bool).grid(row=24)
double_via_bool = tk.IntVar(value=1)
tk.Checkbutton(window, text="double via row?", variable=double_via_bool).grid(row=25)

canvas = tk.Canvas(window, width = 1500, height = 3000) 
canvas.grid(column = 3, row = 0, columnspan=300, rowspan=300)
img = tk.PhotoImage(file="ref.png")     
canvas.create_image(20,20, anchor=tk.NW, image=img)   

window.mainloop()

#trace parsing 
Seg_types = np.array([0]) #0 is straight, 1 is right turn, -1 is left turn
Seg_dims  = np.array([D2/1000]) #Straight length, Turn radius
Seg_lengths = Seg_dims+(np.pi/2-1)*np.absolute(Seg_types)*Seg_dims #

Trace_cumlength = np.cumsum(Seg_lengths)
Trace_numvias = 2*(math.floor((Trace_cumlength[-1])/(D13/1000)-0.5))-1
Tracer_disfirstvia = ((Trace_cumlength[-1])-(((Trace_numvias+1)/2-1)*(D13/1000)))/2
print(Tracer_disfirstvia)
Trace_viapos = np.array(range(Trace_numvias))*(D13/2000) + Tracer_disfirstvia #even indices are closest row, odd indices are farther row

def allow_ground_via(x,y,Seg_types,Seg_dims,Seg_lengths,Tracer_x_passed,Tracer_y_passed,Tracer_dir_passed,Exclusion_width):
    allow_via = True
    Tracer_x = Tracer_x_passed
    Tracer_y = Tracer_y_passed
    Tracer_dir = Tracer_dir_passed
    for seg_idx,seg_type in enumerate(Seg_types):
        if Seg_types[seg_idx]==0:
            x1=Tracer_x-Exclusion_width/2*np.sin(Tracer_dir)
            x2=Tracer_x+Exclusion_width/2*np.sin(Tracer_dir)+Seg_dims[seg_idx]*np.cos(Tracer_dir)
            y1=Tracer_y-Exclusion_width/2*np.cos(Tracer_dir)
            y2=Tracer_y+Exclusion_width/2*np.cos(Tracer_dir)+Seg_dims[seg_idx]*np.sin(Tracer_dir)
            if ((x-x1)*(x-x2)<0) and ((y-y1)*(y-y2)<0):
                allow_via = False
        elif Seg_types[seg_idx]==1:
            arc_center_x=Tracer_x+np.cos(Tracer_dir-np.pi/2)*Seg_dims[seg_idx]
            arc_center_y=Tracer_y+np.sin(Tracer_dir-np.pi/2)*Seg_dims[seg_idx]
            seg1=np.array([Tracer_x-arc_center_x,Tracer_y-arc_center_y])
            end_x=Tracer_x+np.cos(Tracer_dir-np.pi/4)*np.sqrt(2)*Seg_dims[seg_idx]
            end_y=Tracer_y+np.sin(Tracer_dir-np.pi/4)*np.sqrt(2)*Seg_dims[seg_idx]
            seg2=np.array([end_x-arc_center_x,end_y-arc_center_y])
            seg=np.array([x-arc_center_x,y-arc_center_y])
            if (np.dot(seg,seg1)>=0) and (np.dot(seg,seg2)>=0): #outisde this quarter plane there is no exclusion
                rad_dist = np.sqrt(seg[0]**2+seg[1]**2)
                if abs(rad_dist-Seg_dims[seg_idx])<Exclusion_width/2:
                       allow_via = False
        else:
            arc_center_x=Tracer_x+np.cos(Tracer_dir+np.pi/2)*Seg_dims[seg_idx]
            arc_center_y=Tracer_y+np.sin(Tracer_dir+np.pi/2)*Seg_dims[seg_idx]
            seg1=np.array([Tracer_x-arc_center_x,Tracer_y-arc_center_y])
            end_x=Tracer_x+np.cos(Tracer_dir+np.pi/4)*np.sqrt(2)*Seg_dims[seg_idx]
            end_y=Tracer_y+np.sin(Tracer_dir+np.pi/4)*np.sqrt(2)*Seg_dims[seg_idx]
            seg2=np.array([end_x-arc_center_x,end_y-arc_center_y])
            seg=np.array([x-arc_center_x,y-arc_center_y])
            if (np.dot(seg,seg1)>=0) and (np.dot(seg,seg2)>=0): #outisde this quarter plane there is no exclusion
                rad_dist = np.sqrt(seg[0]**2+seg[1]**2)
                if abs(rad_dist-Seg_dims[seg_idx])<Exclusion_width/2:
                       allow_via = False
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
    return allow_via

def allow_holes_via(x,y,Exclusion_dist):
        #valid for D17 in inches, once conversion has happened
        allow_via = True
        h1 = [(D1-D3)/2, D4]
        h1 = [h1[0]/1000, h1[1]/1000]
        h2 = [h1[0]+(D3/1000), h1[1]]
        h3 = [h1[0], h1[1]+((D2-D4-D4)/1000)]
        h4 = [h2[0], h3[1]]
        for h in [h1,h2,h3,h4]:
            if np.sqrt((x-h[0])**2+(y-h[1])**2)<D17/2*25.4+Exclusion_dist:
                allow_via = False
        return allow_via

def allow_opens_via(x,y,Exclusion_dist):
        allow_via = True
        length_cut = (D16/1000 + (2*D30/1000) - (2*D31/1000) + 2*Exclusion_dist)
        point_cut_1 = [(D1/2000)-(length_cut/2), (D2/2000)-(D16/2000)-Exclusion_dist]
        point_cut_2 = [point_cut_1[0], point_cut_1[1]+D16/1000+2*Exclusion_dist]
        point_cut_3 = [point_cut_2[0]+D30/1000+2*Exclusion_dist, point_cut_2[1]]
        if ((x-point_cut_1[0])*(x-point_cut_3[0])<0) and ((y-point_cut_1[1])*(y-point_cut_3[1])<0):
            allow_via = False
        point_cut_1=[D1/1000-point_cut_1[0],point_cut_1[1]]
        point_cut_3=[D1/1000-point_cut_3[0],point_cut_3[1]]
        if ((x-point_cut_1[0])*(x-point_cut_3[0])<0) and ((y-point_cut_1[1])*(y-point_cut_3[1])<0):
            allow_via = False
        return allow_via

Seg_endnumvia=np.zeros_like(Seg_types)
Via_coords=[]
Tracer_x=D1/2000 #This is a trace start parameter
Tracer_y=0 #This is a trace start parameter
Tracer_dir=np.pi/2 #This is a trace start parameter
Via_last_type=1 #This is a via start parameter

for seg_idx,seg_type in enumerate(Seg_types):
    Seg_endnumvia[seg_idx] = np.searchsorted(Trace_viapos,Trace_cumlength[seg_idx])
print(Seg_endnumvia)
Seg_endnumvia[1:] = Seg_endnumvia[1:]-Seg_endnumvia[:-1]
print(Seg_endnumvia)

for seg_idx,seg_type in enumerate(Seg_types):
    #generate positions for this segment
    for via_idx in range(Seg_endnumvia[seg_idx]):
        via_type= (Via_last_type+1+via_idx) % 2
        if Seg_types[seg_idx]==0:
            x=Tracer_x+(Tracer_disfirstvia+via_idx*(D13/2000))*np.cos(Tracer_dir)
            y=Tracer_y+(Tracer_disfirstvia+via_idx*(D13/2000))*np.sin(Tracer_dir)
            ang=Tracer_dir+np.pi/2
            Via_coords = Via_coords+[[x,y,ang,via_type]]
        elif Seg_types[seg_idx]==1:
            arc_center_x=Tracer_x+np.cos(Tracer_dir-np.pi/2)*Seg_dims[seg_idx]
            arc_center_y=Tracer_y+np.sin(Tracer_dir-np.pi/2)*Seg_dims[seg_idx]
            arc_startangle=Tracer_dir+np.pi/2
            ang=arc_startangle-(Tracer_disfirstvia+via_idx*(D13/2000))/Seg_lengths[seg_idx]*np.pi/2
            x=arc_center_x+Seg_dims[seg_idx]*np.cos(ang)
            y=arc_center_y+Seg_dims[seg_idx]*np.sin(ang)
            Via_coords = Via_coords+[[x,y,ang,via_type]]
        else:
            arc_center_x=Tracer_x+np.cos(Tracer_dir+np.pi/2)*Seg_dims[seg_idx]
            arc_center_y=Tracer_y+np.sin(Tracer_dir+np.pi/2)*Seg_dims[seg_idx]
            arc_startangle=Tracer_dir-np.pi/2
            ang=arc_startangle+(Tracer_disfirstvia+via_idx*(D13/2000))/Seg_lengths[seg_idx]*np.pi/2
            x=arc_center_x+Seg_dims[seg_idx]*np.cos(ang)
            y=arc_center_y+Seg_dims[seg_idx]*np.sin(ang)
            Via_coords = Via_coords+[[x,y,ang,via_type]]
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
    Tracer_disfirstvia=(D13/2000)-Seg_lengths[seg_idx]+(Tracer_disfirstvia+(Seg_endnumvia[seg_idx]-1)*(D13/2000))
    Via_last_type=via_type

#Reinitialise for later use in functions
Tracer_x=D1/2000 #This is a trace start parameter
Tracer_y=0 #This is a trace start parameter
Tracer_dir=np.pi/2 #This is a trace start parameter
Via_last_type=1 #This is a via start parameter

end = "M02*"

def featurelayer(laynam): #Layer with Traces e.g Top and Bottom Layer

        def draw(point, light): #Draws a polygon from a point array
                print("X%dY%d%s*"%(point[0],point[1], light))
                file.write("X%dY%d%s*\n"%(point[0],point[1], light))

        ### Initialize File ###
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
        


        file = open(basename+laynam, "w+")
        file.truncate(0)

        print(init)
        file.write(init)
        ### Initialize File END ###

        ###left side (GND PLANE)###
        p1 = [0,0]
        p2 = [p1[0], p1[1] + D2]
        p3 = [p2[0]+(D1/2)-(D8/2), p2[1] + 0]
        p4 = [(D1/2)-(D8/2),(D2/2)+(D16/2)+D9]
        p5 = [p4[0]+((D8-D7)/2), p4[1]-D9]
        p6 = [p5[0]+0,p5[1]-D16]
        p7 = [p4[0], p4[1]-D16-(2*D9)]
        p8 = [p7[0], 0]
        points =  [p1,p2,p3,p4,p5,p6,p7,p8,p1]
        
        print("G36*\n")
        file.write("G36*\n")

        draw(p1, "D02")
        for x in points:
                draw(x, "D01")
        print("G37*\n")
        file.write("G37*\n")
        ###left side (GND PLANE) END###
        
        ###right side (GND PLANE)###
        print("G36*\n")
        file.write("G36*\n")   
        pointsr = []
        middle = D1/2
        middle2 = D2/2
        for x in points: # Mirror Left side on middle line
                pointsr.append([(middle-x[0])+middle, x[1]])

        draw(pointsr[0], "D02")
        for x in pointsr:
                draw(x, "D01")
        print("G37*\n")
        file.write("G37*\n") 
        ###right side (GND PLANE) END###

        ### Trace Drawing ###

        # Define Points of bottom left quarter 
        pm1 = [(D1/2)-(D6/2), 0]
        pm2 = [pm1[0], D5]
        pm3 = [(D1/2)-(D7/2), D5]
        pm4 = [pm3[0], (D2/2)-(D16/2)-D9]
        pm5 = [(D1/2)-(D10/2), (D2/2)-(D16/2)]
        pm6 = [pm5[0], (D2/2)]
        pm7 = [D1/2, D2/2]
        pm8 = [D1/2, 0]
        pointsm = [pm1,pm2,pm3,pm4,pm5,pm6,pm7,pm8,pm1]
        
        print("G36*\n")
        file.write("G36*\n")
        
        draw(pointsm[0], "D02") #Draw bottom left quarter
        for x in pointsm:
                draw(x, "D01")

        print("G37*\n")
        file.write("G37*\n")
        
        print("G36*\n")
        file.write("G36*\n")
        pointsmr = []
        for x in pointsm: # Create Points for bottom right quarter
                pointsmr.append([(middle-x[0])+middle, x[1]])

        draw(pointsmr[0], "D02") # Draw bottom right quarter
        for x in pointsmr:
                draw(x, "D01")

        print("G37*\n")
        file.write("G37*\n")
        
        print("G36*\n")
        file.write("G36*\n")
        pointsmu = []
        for x in pointsm: # Create Points for top right quarter
                pointsmu.append([x[0],(middle2-x[1])+middle2])

        draw(pointsmu[0], "D02") # Draw top right quarter
        for x in pointsmu:
                draw(x, "D01")

        print("G37*\n")
        file.write("G37*\n")
       
        print("G36*\n")
        file.write("G36*\n")
        pointsmur = []
        for x in pointsm: # Create Points for top left quarter
                pointsmur.append([(middle-x[0])+middle,(middle2-x[1])+middle2])

        draw(pointsmur[0], "D02") # Draw top left quarter
        for x in pointsmur:
                draw(x, "D01")

        print("G37*\n")
        file.write("G37*\n")

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

def drillfiles():
        global D14
        global D17
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

        Exclusion_width =  D12/1000+(1+1*double_via_bool.get())*np.sqrt(3)*D13/1000
        Exclusion_dist = np.sqrt(3)*D13/2000
        
        lattice_a = 2*D13/1000
        V1=np.flip(np.arange(D2/2000-np.sqrt(3)*lattice_a/4,Exclusion_dist,-np.sqrt(3)*lattice_a/2))
        V2=np.arange(D2/2000+np.sqrt(3)*lattice_a/4,D2/1000-Exclusion_dist,np.sqrt(3)*lattice_a/2)
        V=np.concatenate((V1,V2))
        for via_ind,via_y in enumerate(V):
            H1=np.flip(np.arange(D1/2000+((via_ind % 2)/2-1)*lattice_a,Exclusion_dist,-lattice_a))
            H2=np.arange(D1/2000+(via_ind % 2)/2*lattice_a,D1/1000-Exclusion_dist,lattice_a)
            H=np.concatenate((H1,H2))
            for via_x in H:
                allow_via=allow_ground_via(via_x,via_y,Seg_types,Seg_dims,Seg_lengths,Tracer_x,Tracer_y,Tracer_dir,Exclusion_width)
                allow_via=allow_via and allow_holes_via(via_x, via_y, Exclusion_dist)
                allow_via=allow_via and allow_opens_via(via_x, via_y, Exclusion_dist)
                if allow_via:
                    file.write("""X%sY%s\n"""%(toinchtz2(via_x),toinchtz2(via_y)))

        if double_via_bool.get():
            Via_selected=Via_coords
        else:
            Via_selected=Via_coords[::2]
        for via_idx,via_coord in enumerate(Via_selected):
                via_x=via_coord[0]-np.cos(via_coord[2])*(D12/2000+via_coord[3]*np.sqrt(3)/2*D13/1000)
                via_y=via_coord[1]-np.sin(via_coord[2])*(D12/2000+via_coord[3]*np.sqrt(3)/2*D13/1000)
                print("via L" + str(via_idx) + "-------------> " + str(via_x) + ", " + str(via_y))
                #print("before--->" + str(via_x))
                #print("after----> " + str(toinchtz2(via_x)))
                file.write("""X%sY%s\n"""%(toinchtz2(via_x),toinchtz2(via_y)))
                print("X%sY%s"%(toinchtz2(via_x),toinchtz2(via_y)))
                via_x=via_coord[0]+np.cos(via_coord[2])*(D12/2000+via_coord[3]*np.sqrt(3)*D13/2000)
                via_y=via_coord[1]+np.sin(via_coord[2])*(D12/2000+via_coord[3]*np.sqrt(3)*D13/2000)
                print("via R" + str(via_idx) + "-------------> " + str(via_x) + ", " + str(via_y))
                file.write("""X%sY%s\n"""%(toinchtz2(via_x),toinchtz2(via_y)))
                print("X%sY%s"%(toinchtz2(via_x),toinchtz2(via_y)))

        h1 = [(D1-D3)/2, D4]
        h1 = [h1[0]/1000, h1[1]/1000]
        h2 = [h1[0]+(D3/1000), h1[1]]
        h3 = [h1[0], h1[1]+((D2-D4-D4)/1000)]
        h4 = [h2[0], h3[1]]
        #print(h1, h2, h3, h4)

        #coordinates
        file.write("T02\n")
        file.write("""X%sY%s\n"""%(toinchtz2(h1[0]),toinchtz2(h1[1])))
        file.write("""X%sY%s\n"""%(toinchtz2(h2[0]),toinchtz2(h2[1])))
        file.write("""X%sY%s\n"""%(toinchtz2(h3[0]),toinchtz2(h3[1])))
        file.write("""X%sY%s\n"""%(toinchtz2(h4[0]),toinchtz2(h4[1])))
        #print("Vias--> " + str(len(Via_coords)))
        file.write("M30")
        file.close()

drillfiles()


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
G04 Layer_Physical_Order=4*
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

####Mirror_Check#####
if mirror_bool.get():
        featurelayer(".gbl")
        left_side_plane = []
        right_side_plane = []
else:
        groundplane(basename + ".gbl")
        
featurelayer(".gtl")

###GND PLANE 1###
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
###GND PLANE 1 END###

###GND PLANE 2###
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
###GND PLANE 2 END###


### Create Solder Maks planes(EMPTY)###
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
### Create Solder Maks planes(EMPTY) END###

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

        length_cut = (D16 + (2*D30) - (2*D31))
        point_cut_1 = [(D1/2)-(length_cut/2), (D2/2)-(D16/2)]
        point_cut_2 = [point_cut_1[0], point_cut_1[1]+D16]
        point_cut_3 = [point_cut_2[0]+D30, point_cut_2[1]]
        point_cut_4 = [point_cut_3[0], point_cut_3[1]-D16]

        points_cut = [point_cut_1,point_cut_2,point_cut_3,point_cut_4,point_cut_1]

        file.write("X%dY%d%s*\n"%(point_cut_1[0],point_cut_1[1], "D02"))
        for x in points_cut:

                file.write("X%dY%d%s*\n"%(x[0],x[1], "D01"))
                file.write("X%dY%d%s*\n"%(x[0],x[1], "D02"))

        points_cut_mirror =[]

        for x in points_cut:
                points_cut_mirror.append([D1-x[0], x[1]])

        file.write("X%dY%d%s*\n"%(points_cut_mirror[0][0],points_cut_mirror[0][1], "D02"))

        for x in points_cut_mirror:

                file.write("X%dY%d%s*\n"%(x[0],x[1], "D01"))
                file.write("X%dY%d%s*\n"%(x[0],x[1], "D02"))


        #file.write("X0Y0D01*\n")
        file.write(end)
        file.close()


###Create mechanical layer(Outline)###
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
###Create mechanical layer(Outline) END###

### Create Gerber Zip for production ###
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
### Create Gerber Zip for production END###


print("Succesfully Created Gerber Files")