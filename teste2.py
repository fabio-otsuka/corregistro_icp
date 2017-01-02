#from __future__ import print_function
import vtk
from vtk import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from math import sqrt

a=[]
b=[]
e=[]

S = [[-129.5,-48.4,-43.8],[-105.3,94.8,-30.9],[-16.6,3.6,-48.5],[-190.0,33.9,15.8]]
Simagem = [[9.0,127.0,76.0],[157.0,134.0,73.0],[86.0,33.0,98.0],[85.0,220.0,84.0]]


p1 = np.array(S[0])
p2 = np.array(S[1])
p3 = np.array(S[2])
p4 = np.array(S[3])
img1 = np.array(Simagem[0])
img2 = np.array(Simagem[1])
img3 = np.array(Simagem[2])
img4 = np.array(Simagem[3])

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
Ninv = M.I


ponto1 = np.array(img1)
ponto1.shape = (3,1)
ponto1 = np.matrix(ponto1.copy())

ponto2 = np.matrix(img2)
ponto2.shape = (3,1)
ponto2 = np.matrix(ponto2.copy())

ponto3 = np.matrix(img3)
ponto3.shape = (3,1)
ponto3 = np.matrix(ponto3.copy())

ponto4 = np.matrix(img4)
ponto4.shape = (3,1)
ponto4 = np.matrix(ponto4.copy())

imagem1 = np.array(q1 + (Minv * N) * (ponto1 - q2))
imagem2 = np.array(q1 + (Minv * N) * (ponto2 - q2))
imagem3 = np.array(q1 + (Minv * N) * (ponto3 - q2))
imagem4 = np.array(q1 + (Minv * N) * (ponto4 - q2))




# ============ create source points ==============
print "Creating source points..."
sourcePoints = vtk.vtkPoints()
sourceVertices = vtk.vtkCellArray()

id = sourcePoints.InsertNextPoint(-129.5,-48.4,-43.8)
sourceVertices.InsertNextCell(1)
sourceVertices.InsertCellPoint(id)

id = sourcePoints.InsertNextPoint(-105.3,94.8,-30.9)
sourceVertices.InsertNextCell(1)
sourceVertices.InsertCellPoint(id)

id = sourcePoints.InsertNextPoint(-16.6,3.6,-48.5)
sourceVertices.InsertNextCell(1)
sourceVertices.InsertCellPoint(id)

id = sourcePoints.InsertNextPoint(-190.6,33.9,15.8)
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
pointCount = 4
for index in range(pointCount):
    point = [0, 0, 0]
    sourcePoints.GetPoint(index, point)
    src.append(point)
    print("source point[%s]=%s" % (index, point))

# ============ create target points ==============
print("Creating target points...")
targetPoints = vtk.vtkPoints()
targetVertices = vtk.vtkCellArray()

id = targetPoints.InsertNextPoint(imagem1)
targetVertices.InsertNextCell(1)
targetVertices.InsertCellPoint(id)

id = targetPoints.InsertNextPoint(imagem2)  ##
targetVertices.InsertNextCell(1)
targetVertices.InsertCellPoint(id)

id = targetPoints.InsertNextPoint(imagem3)
targetVertices.InsertNextCell(1)
targetVertices.InsertCellPoint(id)

id = targetPoints.InsertNextPoint(imagem4)
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
pointCount = 4
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
pointCount = 4
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

for i in range(0,3):
    tsource[i][0] = tsource[i][0] - distx
    tsource[i][1] = tsource[i][1] - disty
    tsource[i][2] = tsource[i][2] - distz

# ======================= error =========================
ED1=np.sqrt((((tgt[0][0]-tsource[0][0])**2) + ((tgt[0][1]-tsource[0][1])**2) +((tgt[0][2]-tsource[0][2])**2)))
ED2=np.sqrt((((tgt[1][0]-tsource[1][0])**2) + ((tgt[1][1]-tsource[1][1])**2) +((tgt[1][2]-tsource[1][2])**2)))
ED3=np.sqrt((((tgt[2][0]-tsource[2][0])**2) + ((tgt[2][1]-tsource[2][1])**2) +((tgt[2][2]-tsource[2][2])**2)))
ED4=np.sqrt((((tgt[3][0]-tsource[3][0])**2) + ((tgt[3][1]-tsource[3][1])**2) +((tgt[3][2]-tsource[3][2])**2)))

FRE = float(np.sqrt((ED1**2 + ED2**2 + ED3**2 + ED4**2)/4))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = [tgt[0][0],tgt[1][0],tgt[2][0],tgt[3][0]]
y = [tgt[0][1],tgt[1][1],tgt[2][1],tgt[3][1]]
z = [tgt[0][2],tgt[1][2],tgt[2][2],tgt[3][2]]

ax.scatter(x[0], y[0], z[0], c='r', marker='o')
ax.scatter(x[1], y[1], z[1], c='g', marker='o')
ax.scatter(x[2], y[2], z[2], c='b', marker='o')
ax.scatter(x[3], y[3], z[3], c='black', marker='o')

ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

x = [tsource[0][0],tsource[1][0],tsource[2][0],tsource[3][0]]
y = [tsource[0][1],tsource[1][1],tsource[2][1],tsource[3][1]]
z = [tsource[0][2],tsource[1][2],tsource[2][2],tsource[3][2]]

ax.scatter(x[0], y[0], z[0], c='r', marker='x')
ax.scatter(x[1], y[1], z[1], c='g', marker='x')
ax.scatter(x[2], y[2], z[2], c='b', marker='x')
ax.scatter(x[3], y[3], z[3], c='black', marker='x')

plt.show()

print FRE
