'''
Basic Calc module
Includes funtions related to 
   Show parameters
   Draw curves
   Some electrical calculations

History:
   6/10/2017 : First version
   3/03/2018 : Added compatibility with Python 3
   5/03/2018 : Added "grid" parameter to plot functions
   9/03/2018 : Added plotHist
  13/03/2018 : Added version string 
  14/03/2018 : Added f2s and decimal formatting in printVar and printR
               Add plot support in Google Colaboratory
  15/03/2018 : Change parameter useSci for sci in print functions  
               Correction on f2s  
               Elimination of electronics functions that now belong to 
               the 'electronicsDC' module
   7/04/2018 : Add getVar and named parameters in plot functions 
  13/04/2018 : Corrected error in plot1n and plotnn   
  15/04/2018 : Add hook to plot functions
   2/07/2018 : Add interactive plots
'''

# Python 2.7 compatibility
from __future__ import print_function
from __future__ import division

import numpy as np               # Import numpy for numeric calculations
import pylab as pl               # Import pylab
import matplotlib.pyplot as plt

import inspect

version = '2/7/2018B'

# Define normal mode outside colaboratory
colaboratory = False

# Interactive plot not enabled by default
iplots = False   

#########################################################################################
# PRINTING CODE                                                                         #
#########################################################################################

def f2s(v,nd=None):
    """
    f2s (float2string)
    Takes one float value and converts it to string
    If greater or equal than 1000, uses two decimal places
    If greater than one, uses three decimal places
    if less than one, uses three significant decimal places
    The optional parameter can fix the number of significant digits
    """
    # Base number of decimals
    a = abs(v)
    if nd == None:
        ndec = 3
        if (a>=1000): ndec = 2
        if (a<1): ndec = int(np.floor(3-np.log10(a)))
    else:
        ndec = nd
        if (a<1): ndec = int(np.floor(nd-np.log10(a)))

    # Check for significance
    v2 = np.floor(v*10**ndec)/(10**ndec)
    for i in range(0,ndec):
        if np.floor(v2) == v2:
            ndec = i+1
            break
        v2 = v2*10.0    
    
    # Return string
    return ('{0:.%df}' % ndec).format(v)
   
def f2sci(v,unit='',nd=3,prefix=True):
    """
    Takes one float and converts it to scientific notation
    Required parameters
       v : Number to convert
    Optional parameters
        unit : Unit to show
          nd : Number of decimal places (Default to 3) 
      prefix : Use standard prefixes for powers of 10 up to +/-18
    """
    potH=['k','M','G','T','P','E']
    potL=['m','u','n','p','f','a']
    a = abs(v)
    ndec = int(np.floor(np.log10(a)))
    pot = int(np.floor(ndec/3))
    exp = 3*pot
    base = v/(10.0**exp)
    s = f2s(base,nd)
    if pot==0: 
        return s + ' ' + unit
      
    if (prefix):
        if 1 <= pot <=6:
            s = s + ' ' + potH[pot-1] + unit
            return s
        if 1 <= -pot <=6:
            s = s + ' '+ potL[-pot-1] + unit
            return s
    
    s = s + 'E' + ('{:+d}').format(exp) + ' ' + unit
    return s    
    
def printVar(name,value,unit="",sci=True,prefix=True):
    """
    Print a variable name, value and units
    """
    if sci:
        print(name + " = " + f2sci(value,unit,prefix=prefix))
    else:
        print(name + " = " + f2s(value) + " " + unit)
           
def printTitle(title):
    """
    Print a title with blank lines after and before
    """ 
    print()
    print(title)
    print()

# Getvar ################################################################################

def getVar(name,level=1):
    """
    Get a variable from its name
    Level indicates stack level
    Level 1 is appropiate if this function is called from the target context
    """
    # Get caller globals and locals
    caller_globals = dict(inspect.getmembers(inspect.stack()[level][0]))["f_globals"]
    caller_locals = dict(inspect.getmembers(inspect.stack()[level][0]))["f_locals"]
    # Get variable
    var = eval(name,caller_globals,caller_locals)
    # Return variable
    return var    
    
#########################################################################################
# JUPYTER DRAWING CODE                                                                  #
#########################################################################################

def interactivePlots(flag=True):
    """
    ----------------------------------------------------------------
    interactivePlots(flag)
    Activates interactive plotting on Jypyter
    Requires also setting the magic '%matplotlib notebook'
    Using the optinal parameter to False, return to inline mode
    
    Optional parametres:
        flag : Set interactive mode (defaults to True)
    
    Included in slab.py
    ----------------------------------------------------------------
    """
    global iplots
    if flag:
        iplots = True
        print("Plots are now interactive")
        print("Remember to also set '%matplotlib notebook' in Jupyter")
    else:
        iplots = False
        print("Plots are static now")
        print("Remember to also set '%matplotlib inline' in Jupyter")     
    
#########################################################################################
# COLABORATORY DRAWING CODE                                                             #
#########################################################################################    

'''
These are the same normal plot functions but optimized to be used in
Google Colaboratory
'''
# COLABORATORY FLAG FOR PLOTTING #####################################################

def setColaboratory(flag=True):
    """
    @setColaboratory
    setColaboratory(flag=True)
    Indicates that we are in Colaboartory
    Don't return anything
    """  
    global colaboratory
    colaboratory = flag   

# Internal functions ####################################################################

'''
_jplotStart
Starts a new plot
Paramenters:
  title : Title of the plot (defaults to none)
  xt    : x label of the plot (defaults to none)
  yt    : y label of the plot (defaults to none)
  grid  : Determines if there is grid (defaults to True)
Returns:
  fig : Figure object
  ax  : Axes object  
'''
def _jplotStart(title="",xt="",yt="",grid=True,xlim=None,ylim=None):
    fig=plt.figure()
    if xlim != None:
        plt.xlim(xlim[0],xlim[1])
    if ylim != None:
        plt.ylim(ylim[0],ylim[1])      
    ax = fig.add_subplot(111)
    ax.set_facecolor("white")
    ax.set_title(title)
    ax.set_xlabel(xt)
    ax.set_ylabel(yt)
    if (grid):
        plt.grid(True,color="lightgrey",linestyle='--')
    return fig,ax

'''
_jplotEnd
Ends a previously started plot
Paramenters:
  fig      : Figure object obtained from plotStart
  ax       : Axes obtained from plotStart
  labels   : List of labels for the curves (defaults to none)
  location : Location for labels (defaults to 'best')
Returns nothing  
'''    
def _jplotEnd(fig,ax,labels=[],location='best'):
    if not labels == []:
        pl.legend(loc=location)
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    ax.axvline(x=xmin,linewidth=2, color='black')
    ax.axvline(x=xmax,linewidth=2, color='black')
    ax.axhline(y=ymin,linewidth=2, color='black')
    ax.axhline(y=ymax,linewidth=2, color='black')
    plt.show()

'''
_jplotXY
Plot two magnitudes using log if needed
Used by the plot11, plot1n and plotnn commands
'''
def _jplotXY(x,y,label="",logx=False,logy=False):
    if not logx and not logy:
        pl.plot(x,y,label=label)
        return
    if logx and not logy:
        pl.semilogx(x,y,label=label)
        return
    if logy and not logx:
        pl.semilogy(x,y,label=label)
        return
    if logx and logy:
        pl.loglog(x,y,label=label)
        return
     
# Public functions ######################################################################
     
def jplot11(x,y,title="",xt="",yt="",logx=False,logy=False,grid=True,hook=None,xlim=None,ylim=None):
       
    fig,ax = _jplotStart(title,xt,yt,grid,xlim,ylim)

    _jplotXY(x,y,logx=logx,logy=logy)
    
    if not hook is None:
        hook() 
    
    _jplotEnd(fig,ax)
    
def jplot1n(x,ylist,title="",xt="",yt="",labels=[],location='best',logx=False,logy=False
           ,grid=True,hook=None,xlim=None,ylim=None):
    
    fig,ax=_jplotStart(title,xt,yt,grid,xlim,ylim)
    
    if labels == []:
        for y in ylist:
            _jplotXY(x,y,logx=logx,logy=logy)
    else:
        for y,lbl in zip(ylist,labels):
            _jplotXY(x,y,label=lbl,logx=logx,logy=logy)

    if not hook is None:
        hook()        
            
    _jplotEnd(fig,ax,labels,location)   
  
def jplotnn(xlist,ylist,title="",xt="",yt="",labels=[],location='best',logx=False,logy=False
           ,grid=True,hook=None,xlim=None,ylim=None):

    fig,ax=_jplotStart(title,xt,yt,grid,xlim,ylim)
    
    if labels == []:
        for x,y in zip(xlist,ylist):
            _jplotXY(x,y,logx=logx,logy=logy)
    else:
        for x,y,lbl in zip(xlist,ylist,labels):
            _jplotXY(x,y,label=lbl,logx=logx,logy=logy)
            
    if not hook is None:
        hook()        
            
    _jplotEnd(fig,ax,labels,location)  
    
def jplotHist(v,bins=10,title="",xt="",yt="",grid=True,hook=None):

    fig,ax = _jplotStart(title,xt,yt,grid)

    plt.hist(v,bins)
    
    if not hook is None:
        hook()
    
    _jplotEnd(fig,ax)       
    
     
#########################################################################################
# DRAWING CODE                                                                          #
#########################################################################################

'''
Plot two magnitudes using log if needed
Used by the plot11, plot1n and plotnn commands
'''
def plotXY(x,y,label="",logx=False,logy=False):
    if not logx and not logy:
        pl.plot(x,y,label=label)
        return
    if logx and not logy:
        pl.semilogx(x,y,label=label)
        return
    if logy and not logx:
        pl.semilogy(x,y,label=label)
        return
    if logx and logy:
        pl.loglog(x,y,label=label)
        return
        
'''
@plot11@
plot11(x,y,title,xt,yt,logx,logy,grid,hook,xlim,ylim)
Plot one input against one output
If x is an empty list [], a sequence number
will be used for the x axis

Required parameters:
  x : Horizontal vector (string calls eval)
  y : Vertical vector (string calls eval)
  
Optional parameters:
  title : Plot title (Defaults to none)
     xt : Label for x axis (Defaults to none or x string)
     yt : Label for y axis (Defaults to none or y string)
   logx : Use logarithmic x axis (Defaults to False)
   logy : Use logarithmic x axis (Defaults to False)
   grid : Draw a grid (Defaults to true) 
   hook : Function to be executed before showing the graph
   xlim : Tuple (min,max) with Limits for x axis
   ylim : Tuple (min,max) with Limits for y axis     

Returns nothing
'''
def plot11(x,y,title="",xt="",yt="",logx=False,logy=False,grid=True,hook=None,xlim=None,ylim=None):
    # Check for x, y given as strings
    if type(x)==str:
        if xt=='': xt=x
        x = getVar(x,level=2)
    if type(y)==str:
        if yt=='': yt=y
        y = getVar(y,level=2)
 
    # Generate sequence if x is not provided
    if x == []:
        x = np.arange(0,len(y))      
                
    # Check colaboratory    
    if colaboratory:
        jplot11(x,y,title,xt,yt,logx,logy,grid,hook,xlim,ylim)
        return
 
    plt.figure(facecolor="white")   # White border
    if xlim != None:
        plt.xlim(xlim[0],xlim[1])
    if ylim != None:
        plt.ylim(ylim[0],ylim[1])    
    plotXY(x,y,logx=logx,logy=logy)
    pl.xlabel(xt)
    pl.ylabel(yt)
    pl.title(title)
    if grid:
        pl.grid()
    if not hook is None:
        hook()    
    if not iplots:    
        pl.show()
        pl.close()
    
'''
@plot1n@
plot1n(x,ylist,title,xt,yt,labels,location,logx,logy,grid,hook,xlim,ylim)
Plot one input against several outputs
If x is an empty list [], a sequence number
will be used for the x axis

Required parameters:
      x : Horizontal vector (string calls eval)
  ylist : List of vertical vectors (list of strings calls eval)
  
Optional parameters:
    title : Plot title (Defaults to none)
       xt : Label for x axis (Defaults to none or x string)
       yt : Label for y axis (Defaults to none)
   labels : List of legend labels (Defaults to none or ylist strings)
 location : Location for legend (Defaults to 'best')
     logx : Use logarithmic x axis (Defaults to False)
     logy : Use logarithmic x axis (Defaults to False)
     grid : Draw a grid (Defaults to true)
     hook : Function to be executed before showing the graph     
     xlim : Tuple (min,max) with Limits for x axis
     ylim : Tuple (min,max) with Limits for y axis 

Returns nothing
'''
def plot1n(x,ylist,title="",xt="",yt="",labels=[],location='best'
            ,logx=False,logy=False,grid=True,hook=None,xlim=None,ylim=None):
    # Check for x, y given as strings
    if type(x)==str:
        if xt=='': xt=x
        x = getVar(x,level=2)
    if type(ylist[0])==str and (labels==[]): 
        labels=ylist
    ylist2 = []
    for element in ylist:
        if type(element) == str:
            ylist2.append(getVar(element,level=2))
        else:
            ylist2.append(element)
    ylist=ylist2        

    # Generate sequence is x is not provided
    if x == []:
        x = np.arange(0,len(ylist[0]))          
    
    # Check if we are in colaboratory
    if colaboratory:
        jplot1n(x,ylist,title,xt,yt,labels,location,logx,logy,grid,hook,xlim,ylim)
        return    
        
    plt.figure(facecolor="white")   # White border
    if xlim != None:
        plt.xlim(xlim[0],xlim[1])
    if ylim != None:
        plt.ylim(ylim[0],ylim[1])      
    if labels == []:
        for y in ylist:
            plotXY(x,y,logx=logx,logy=logy)
            #pl.plot(x,y)
    else:
        for y,lbl in zip(ylist,labels):
            plotXY(x,y,label=lbl,logx=logx,logy=logy)
            #pl.plot(x,y,label=lbl)
    pl.xlabel(xt)
    pl.ylabel(yt)
    pl.title(title)
    if grid:
        pl.grid()
    if not labels == []:
        pl.legend(loc=location)
    if not hook is None:
        hook()    
    if not iplots:    
        pl.show()
        pl.close()   
  
'''
@plotnn@
plotnn(xlist,ylist,title,xt,yt,labels,location,logx,logy,grid,hook,xlim,ylim)
Plot several curves with different inputs and outputs

Required parameters:
  xlist : List of horizontal vector (list of strings calls eval)
  ylist : List of vertical vectors (list of strings calls eval)
  
Optional parameters:
    title : Plot title (Defaults to none)
       xt : Label for x axis (Defaults to none or first string of xlist)
       yt : Label for y axis (Defaults to none)
   labels : List of legend labels (Defaults to none or ylist strings)
 location : Location for legend (Defaults to 'best')
     logx : Use logarithmic x axis (Defaults to False)
     logy : Use logarithmic x axis (Defaults to False)
     grid : Draw a grid (Defaults to true)
     hook : Function to be executed before showing the graph     
     xlim : Tuple (min,max) with Limits for x axis
     ylim : Tuple (min,max) with Limits for y axis  

Returns nothing
'''
def plotnn(xlist,ylist,title="",xt="",yt="",labels=[],location='best'
           ,logx=False,logy=False,grid=True,hook=None,xlim=None,ylim=None):
    # Check for x, y given as strings
    if type(xlist[0])==str:
        if xt=='': xt=xlist[0]
    if type(ylist[0])==str and (labels==[]): 
        labels=ylist
        
    xlist2 = []
    for element in xlist:
        if type(element) == str:
            xlist2.append(getVar(element,level=2))
        else:
            xlist2.append(element)
    xlist=xlist2  
    
    ylist2 = []
    for element in ylist:
        if type(element) == str:
            ylist2.append(getVar(element,level=2))
        else:
            ylist2.append(element)
    ylist=ylist2    
        
    # Check if we are in colaboratory
    if colaboratory:
        jplotnn(xlist,ylist,title,xt,yt,labels,location,logx,logy,grid,hook,xlim,ylim)
        return

    plt.figure(facecolor="white")   # White border
    if xlim != None:
        plt.xlim(xlim[0],xlim[1])
    if ylim != None:
        plt.ylim(ylim[0],ylim[1])      
    if labels == []:
        for x,y in zip(xlist,ylist):
            plotXY(x,y,logx=logx,logy=logy)
    else:
        for x,y,lbl in zip(xlist,ylist,labels):
            plotXY(x,y,label=lbl,logx=logx,logy=logy)
    pl.xlabel(xt)
    pl.ylabel(yt)
    pl.title(title)
    pl.grid()
    if not labels == []:
        pl.legend(loc=location)
    if not hook is None:
        hook()
    if not iplots:    
        pl.show()
        pl.close()  
  
'''
@plotHist@
plotHist(v,bins=10,title="",xt="",yt="",grid)
Plot an histagram from provided data

Required parameters:
  v : Data vector (string calls eval)
  
Optional parameters:
     bins : Number of bins for the histogram (Defaults to 10)
    title : Plot title (Defaults to none)
       xt : Label for x axis (Defaults to none or x string)
       yt : Label for y axis (Defaults to none or 'Frequency' if v is string)
     grid : Use grid (Default to True)     
     
Returns nothing   
'''    
def plotHist(v,bins=10,title="",xt="",yt="",grid=True):
    # Check for v given as strings
    if type(v)==str:
        if xt=='': xt=v
        v = getVar(v,level=2)
        if yt=='': yt='Frequency'
        
    # Check colaboratory 
    if colaboratory:
        jplotHist(v,bins=bins,title=title,xt=xt,yt=yt,grid=grid)
        return  
      
    plt.figure(facecolor="white")   # White border
    
    plt.hist(v,bins)
    
    pl.xlabel(xt)
    pl.ylabel(yt)
    pl.title(title)
    if grid:
        pl.grid()
    if not iplots:    
        pl.show()
        pl.close()
   
  
#########################################################################################
# DIFFERENTIAL EQUATIONS CODE                                                           #
#########################################################################################      
    
'''
Calculates the Euler solution of a dynamical system
System is defined as:
 dx/dt = f(x,t)
Parameters:
   x : State variable or vector 
   t : Current time
   f : function f(x,t)
   h : time step interval
Returns:
   xNew : New value of x at time t+h
'''
def euler(x, t, f, h):
    xNew = x + h * f(x,t)
    return xNew
    
'''
Calculates the 4th order Runge-Kutta approximation for a dynamical system
System is defined as:
 dx/dt = f(x,t)
Parameters:
   x : State variable or vector 
   t : Current time
   f : function f(x,t)
   h : time step interval
Returns:
   xNew : New value of x at time t+h
'''    
def rk4(x, t, f, h): 
    k1 = h * f(x,t)
    k2 = h * f(x + k1/2.0 , t + h/2.0)
    k3 = h * f(x + k2/2.0 , t + h/2.0)
    k4 = h * f(x + k3     , t + h)
    xNew = x + ( k1/6 + k2/3 + k3/3 + k4/6 )
    return xNew
    
#########################################################################################
# GEOMETRIC CODE                                                                        #
#########################################################################################     

'''
Normalize a line that passes thorugh two points
 Generates line as y = Ax + B
Parameters:
  x1 : First point x
  y1 : First point y
  x2 : Second point x
  y2 : Second point y
Return:
  A : Slope
  B : Zero cross  
'''
def normalizeLine(x1,y1,x2,y2):
    a = (y2*1.0 - y1*1.0)/(x2*1.0 - x1*1.0)
    b = (y1*1.0 - a*x1)
    return a,b
