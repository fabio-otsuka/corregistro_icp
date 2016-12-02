#from __future__ import print_function
import vtk
from vtk import *
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

a=[]
b=[]
e=[]

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
pointCount = 4
for index in range(pointCount):
    point = [0, 0, 0]
    sourcePoints.GetPoint(index, point)
    print("source point[%s]=%s" % (index, point))

# ============ create target points ==============
print("Creating target points...")
targetPoints = vtk.vtkPoints()
targetVertices = vtk.vtkCellArray()

id = targetPoints.InsertNextPoint(9.0,127.0,76.0)
targetVertices.InsertNextCell(1)
targetVertices.InsertCellPoint(id)

id = targetPoints.InsertNextPoint(157.0,134.0,73.0)  ##
targetVertices.InsertNextCell(1)
targetVertices.InsertCellPoint(id)

id = targetPoints.InsertNextPoint(86.0,33.0,98.0)
targetVertices.InsertNextCell(1)
targetVertices.InsertCellPoint(id)

id = targetPoints.InsertNextPoint(85.0,220.0,84.0)
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
# icp.DebugOn()
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