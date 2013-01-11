from __future__ import division
from numpy import *
from Tkinter import *
import treeregress
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def reDraw(tolS,tolN):
  reDraw.f.clf()
  reDraw.a = reDraw.f.add_subplot(111)
  if chkBtnVar.get():
    if tolN < 2:
      tolN = 2
    myTree=treeregress.createTree(reDraw.rawDat, treeregress.modelLeaf,\
      treeregress.modelErr, (tolS,tolN))
    yHat = treeregress.createForeCast(myTree, reDraw.testDat, \
      treeregress.modelTreeEval)
  else:
    myTree=treeregress.createTree(reDraw.rawDat, ops=(tolS,tolN))
    yHat = treeregress.createForecast(myTree, reDraw.testDat)
  reDraw.a.scatter(reDraw.rawDat[:,0], reDraw.rawDat[:,1], s=5)
  reDraw.a.plot(reDraw.testDat, yHat, linewidth=2.0)
  reDraw.canvas.show()

def getInputs():
  try: 
    tolN = int(tolNentry.get())
  except:
    tolN = 10
    print "enter Integer for tolN"
    tolNentry.delete(0, END)
    tolNentry.insert(0,'10')
  try: 
    tolS = float(tolSentry.get())
  except:
    tolS = 1.0
    print "enter Float for tolS"
    tolSentry.delete(0, END)
    tolSentry.insert(0,'1.0')
  return tolN,tolS

def drawNewTree():
  tolN,tolS = getInputs()
  reDraw(tolS,tolN)

root=Tk()

#Label(root, text="Plot Place Holder").grid(row=0, columnspan=3)
reDraw.f = Figure(figsize=(5,4), dpi=100)
reDraw.canvas = FigureCanvasTkAgg(reDraw.f, master=root)
reDraw.canvas.show()
reDraw.canvas.get_tk_widget().grid(row=0, columnspan=3)

Label(root, text="tolN").grid(row=1, column=0)
tolNentry = Entry(root)
tolNentry.grid(row=1, column=1)
tolNentry.insert(0, '10')
Label(root, text="tolS").grid(row=2, column=0)
tolSentry = Entry(root)
tolSentry.grid(row=2, column=1)
tolSentry.insert(0, '1.0')
Button(root, text="ReDraw", command=drawNewTree).grid(row=1, column=2, rowspan=3)
chkBtnVar = IntVar()
chkBtn = Checkbutton(root, text="Model Tree", variable = chkBtnVar)
chkBtn.grid(row=3, column=0, columnspan=2)
reDraw.rawDat = mat(treeregress.loadDataSet('sine.txt'))
reDraw.testDat = arange(min(reDraw.rawDat[:,0]),\
max(reDraw.rawDat[:,0]),0.01)
reDraw(1.0, 10)
root.mainloop()
