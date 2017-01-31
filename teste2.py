#from __future__ import print_function
import vtk
from vtk import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from math import sqrt
from math import factorial

a=[]
b=[]
e=[]
c=[]
group = []

S = [[-129.5,-48.4,-43.8],[-105.3,94.8,-30.9],[-16.6,3.6,-48.5],[-190.0,33.9,15.8]]
Simagem = [[9.0,127.0,76.0],[157.0,134.0,73.0],[86.0,33.0,98.0],[85.0,220.0,84.0]]

# This test first makes a combination of the four points, making 4 groups of 3 points
# After that, for each group, the ICP is applied and then the FRE is calculated for each group

n=len(S)
N = factorial(n)
P = factorial(3)
NP = factorial(n - 3)
C = N / (P * NP)
l=0
for i in range(0,C-2):
    for j in range (i+1,C-1):
        for k in range(j+1,C):
            a.insert(l,[S[i],S[j],S[k]])
            b.insert(l,[Simagem[i],Simagem[j],Simagem[k]])
            group.insert(l,l+1)
            l=l+1

print a[0]
for i in range(0,C):
    #Fiduciais da img
    #self.M, self.q1, self.Minv = db.base_creation(a[i][0],
    #                                           a[i][1],
    #                                           a[i][2])
    #FIducias do rastreador
    #self.N, self.q2, self.Ninv = db.base_creation(b[i][0],
    #                                           b[i][1],
    #                                           b[i][2])

    p1 = np.array(a[i][0])
    p2 = np.array(a[i][1])
    p3 = np.array(a[i][2])
    img1 = np.array(b[i][0])
    img2 = np.array(b[i][1])
    img3 = np.array(b[i][2])

    sub1 = p2 - p1
    sub2 = p3 - p1
    sub3 = img2 - img1
    sub4 = img3 - img1
    lamb1 = (sub1[0] * sub2[0] + sub1[1] * sub2[1] + sub1[2] * sub2[2]) / np.dot(sub1, sub1)
    lamb2 = (sub3[0] * sub4[0] + sub3[1] * sub4[1] + sub3[2] * sub4[2]) / np.dot(sub3, sub3)

    q1 = p1 + lamb1 * sub1
    q2 = img1 + lamb2 * sub3
    g1 = p1 - q1
    g2 = p3 - q1
    gimg1 = img1 - q2
    gimg2 = img3 - q2

    if not g1.any():
        g1 = p2 - q1

    g3 = np.cross(g2, g1)
    gimg3 = np.cross(gimg2, gimg1)

    g1 = g1 / sqrt(np.dot(g1, g1))
    g2 = g2 / sqrt(np.dot(g2, g2))
    g3 = g3 / sqrt(np.dot(g3, g3))

    gimg1 = gimg1 / sqrt(np.dot(gimg1, gimg1))
    gimg2 = gimg2 / sqrt(np.dot(gimg2, gimg2))
    gimg3 = gimg3 / sqrt(np.dot(gimg3, gimg3))

    M = np.matrix([[g1[0], g1[1], g1[2]],
                    [g2[0], g2[1], g2[2]],
                    [g3[0], g3[1], g3[2]]])

    N = np.matrix([[gimg1[0], gimg1[1], gimg1[2]],
                    [gimg2[0], gimg2[1], gimg2[2]],
                    [gimg3[0], gimg3[1], gimg3[2]]])

    q1.shape = (3, 1)
    q2.shape = (3, 1)
    q1 = np.matrix(q1.copy())
    q2 = np.matrix(q2.copy())
    Minv = M.I
    Ninv = N.I


    ponto1 = np.array(p1)
    ponto1.shape = (3,1)
    ponto1 = np.matrix(ponto1.copy())
    ponto2 = np.matrix(p2)
    ponto2.shape = (3,1)
    ponto2 = np.matrix(ponto2.copy())
    ponto3 = np.matrix(p3)
    ponto3.shape = (3,1)
    ponto3 = np.matrix(ponto3.copy())

    ponto1 = np.array(q2 + (Ninv * M) * (ponto1 - q1))
    ponto2 = np.array(q2 + (Ninv * M) * (ponto2 - q1))
    ponto3 = np.array(q2 + (Ninv * M) * (ponto3 - q1))


# ============ create source points ==============
    print "Creating source points..."
    sourcePoints = vtk.vtkPoints()
    sourceVertices = vtk.vtkCellArray()

    id = sourcePoints.InsertNextPoint(ponto1)
    sourceVertices.InsertNextCell(1)
    sourceVertices.InsertCellPoint(id)

    id = sourcePoints.InsertNextPoint(ponto2)
    sourceVertices.InsertNextCell(1)
    sourceVertices.InsertCellPoint(id)

    id = sourcePoints.InsertNextPoint(ponto3)
    sourceVertices.InsertNextCell(1)
    sourceVertices.InsertCellPoint(id)

    source = vtk.vtkPolyData()
    source.SetPoints(sourcePoints)
    source.SetVerts(sourceVertices)
    if vtk.VTK_MAJOR_VERSION <= 5:
        source.Update()

    print("Displaying source points...")
# ============ display source points ==============
    src = []
    pointCount = 3
    for index in range(pointCount):
        point = [0, 0, 0]
        sourcePoints.GetPoint(index, point)
        src.append(point)
        print("source point[%s]=%s" % (index, point))

# ============ create target points ==============
    print("Creating target points...")
    targetPoints = vtk.vtkPoints()
    targetVertices = vtk.vtkCellArray()

    id = targetPoints.InsertNextPoint(img1)
    targetVertices.InsertNextCell(1)
    targetVertices.InsertCellPoint(id)

    id = targetPoints.InsertNextPoint(img2)  ##
    targetVertices.InsertNextCell(1)
    targetVertices.InsertCellPoint(id)

    id = targetPoints.InsertNextPoint(img3)
    targetVertices.InsertNextCell(1)
    targetVertices.InsertCellPoint(id)

    target = vtk.vtkPolyData()
    target.SetPoints(targetPoints)
    target.SetVerts(targetVertices)
    if vtk.VTK_MAJOR_VERSION <= 5:
        target.Update()

# ============ display target points ==============
    tgt = []
    print("Displaying target points...")
    pointCount = 3
    for index in range(pointCount):
        point = [0, 0, 0]
        targetPoints.GetPoint(index, point)
        tgt.append(point)
        print("target point[%s]=%s" % (index, point))

    print("Running ICP ----------------")
# ============ run ICP ==============
    icp = vtk.vtkIterativeClosestPointTransform()
    icp.SetSource(source)
    icp.SetTarget(target)
    icp.GetLandmarkTransform().SetModeToRigidBody()
    icp.DebugOn()
    icp.SetMaximumNumberOfIterations(20)
    icp.StartByMatchingCentroidsOn()
    icp.Modified()
    icp.Update()

    icpTransformFilter = vtk.vtkTransformPolyDataFilter()
    if vtk.VTK_MAJOR_VERSION <= 5:
        icpTransformFilter.SetInput(source)
    else:
        icpTransformFilter.SetInputData(source)

    icpTransformFilter.SetTransform(icp)
    icpTransformFilter.Update()

    transformedSource = icpTransformFilter.GetOutput()

# ============ display transformed points ==============
    pointCount = 3
    tsource=[]
    for index in range(pointCount):
        point = [0, 0, 0]
        transformedSource.GetPoint(index, point)
        tsource.append(point)
        print("transformed source point[%s]=%s" % (index, point))
#print tsource[0][0]


    distx = tsource[0][0] - tgt[0][0]
    disty = tsource[0][1] - tgt[0][1]
    distz = tsource[0][2] - tgt[0][2]

    for t in range(0,3):
        tsource[t][0] = tsource[t][0] - distx
        tsource[t][1] = tsource[t][1] - disty
        tsource[t][2] = tsource[t][2] - distz

# ======================= error =========================
    ED1=np.sqrt((((tgt[0][0]-tsource[0][0])**2) + ((tgt[0][1]-tsource[0][1])**2) +((tgt[0][2]-tsource[0][2])**2)))
    ED2=np.sqrt((((tgt[1][0]-tsource[1][0])**2) + ((tgt[1][1]-tsource[1][1])**2) +((tgt[1][2]-tsource[1][2])**2)))
    ED3=np.sqrt((((tgt[2][0]-tsource[2][0])**2) + ((tgt[2][1]-tsource[2][1])**2) +((tgt[2][2]-tsource[2][2])**2)))

    FRE = float(np.sqrt((ED1**2 + ED2**2 + ED3**2)/3))
    e.insert(i,[FRE])

# Done the calculation of the FREs, then it is time to ordenate the groups in terms of the FRE
# the algorith uses a iterative method that compares each term, placing them in ordem from the least FRE
# to the biggest FRE

for i in range(0,C):
    for j in range(0,C-1):
        if e[j] > e[j+1]:
            aux=e[j+1]
            e[j+1] = e[j]
            e[j]= aux

            aux = a[j + 1]
            a[j+1] = a[j]
            a[j] = aux

            aux = b[j + 1]
            b[j+1] = b[j]
            b[j] = aux

            aux = group[j+1]
            group[j+1] = group[j]
            group[j] = aux

print 'Group %s:' %group[0]
print 'FRE: %s \n' %e[0]

print 'Group %s:' %group[1]
print 'FRE: %s \n' %e[1]

print 'Group %s:' %group[2]
print 'FRE: %s \n' %e[2]

print 'Group %s:' %group[3]
print 'FRE: %s \n' %e[3]
