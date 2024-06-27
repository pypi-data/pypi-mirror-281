
import cv2
import pyacvd
import pyvista as pv

import numpy as np

import vtk
from vtk.util import numpy_support


class MeshPyvista(object):
    def __init__(self, contour=None, spacing=None, origin=None, dimensions=None, create_mask=False):
        self.contour = contour
        self.spacing = spacing
        self.origin = origin
        self.dimensions = dimensions

        self.mask = None
        self.mesh = None

        self.window_sinc_settings = {'Iterations': 20, 'Passband': 0.001, 'Angle': 60}

        if create_mask:
            self.compute_mask()

    def set_from_image(self, image):
        self.mask = np.asarray(self.image).ravel()
        self.spacing = image.GetSpacing()
        self.origin = image.GetOrigin()
        self.dimensions = image.GetSize()

    def set_mask(self, mask):
        self.mask = mask

    def set_spacing(self, spacing):
        self.spacing = spacing

    def set_origin(self, origin):
        self.origin = origin

    def set_dimensions(self, dimensions):
        self.dimensions = dimensions

    def set_mesh(self, mesh):
        self.mesh = mesh

    def update_window_sinc_settings(self, iterations=None, passband=None, angle=None):
        if iterations is not None:
            self.window_sinc_settings['Iterations'] = iterations

        if passband is not None:
            self.window_sinc_settings['Passband'] = passband

        if angle is not None:
            self.window_sinc_settings['Angle'] = angle

    def compute_mask(self):
        if self.contour and self.dimensions and self.spacing and self.origin:
            slice_check = np.zeros(self.dimensions[2])
            hold_mask = np.zeros([self.dimensions[2], self.dimensions[0], self.dimensions[1]], dtype=np.uint8)
            for c in self.contour:
                slice_num = int(np.round((c[0][2] - self.origin[2]) / float(self.spacing[2])))

                contour_indexing = np.round(np.abs((c - self.origin) / self.spacing))
                contour_stacked = np.vstack((contour_indexing[:, 0:2], contour_indexing[0, 0:2]))
                new_contour = np.array([contour_stacked], dtype=np.int32)
                image = np.zeros([self.dimensions[0], self.dimensions[1]], dtype=np.uint8)
                cv2.fillPoly(image, new_contour, 1)

                if slice_check[slice_num] == 0:
                    hold_mask[slice_num, :, :] = image
                    slice_check[slice_num] = 1
                else:
                    hold_mask[slice_num, :, :] = hold_mask[slice_num, :, :] + image
            self.mask = (hold_mask > 0).astype(np.uint8)
        else:
            if not self.contour:
                ValueError('No contour')
            if not self.dimensions:
                ValueError('No dimensions')
            if not self.spacing:
                ValueError('No spacing')
            if not self.origin:
                ValueError('No origin')

    def compute_mesh(self):
        if self.mask.any() and self.dimensions and self.spacing and self.origin:
            label = numpy_support.numpy_to_vtk(num_array=np.asarray(self.mask).ravel(), deep=True, array_type=vtk.VTK_FLOAT)
            img_vtk = vtk.vtkImageData()
            # img_vtk.Set
            img_vtk.SetDimensions([self.dimensions[1], self.dimensions[0], self.dimensions[2]])
            img_vtk.SetSpacing(self.spacing)
            img_vtk.SetOrigin(self.origin)
            img_vtk.GetPointData().SetScalars(label)

            vtk_mesh = vtk.vtkDiscreteMarchingCubes()
            vtk_mesh.SetInputData(img_vtk)
            vtk_mesh.GenerateValues(1, 1, 1)
            vtk_mesh.Update()

            self.mesh = pv.PolyData(vtk_mesh.GetOutput())
        else:
            if not self.mask:
                ValueError('No mask')
            if not self.dimensions:
                ValueError('No dimensions')
            if not self.spacing:
                ValueError('No spacing')
            if not self.origin:
                ValueError('No origin')

    # noinspection PyArgumentList
    def compute_smooth(self, window_sinc=True):
        if window_sinc:
            smoother = vtk.vtkWindowedSincPolyDataFilter()
            smoother.SetInputData(self.mesh)
            smoother.SetNumberOfIterations(self.window_sinc_settings['Iterations'])
            smoother.BoundarySmoothingOff()
            smoother.FeatureEdgeSmoothingOff()
            smoother.SetFeatureAngle(self.window_sinc_settings['Angle'])
            smoother.SetPassBand(self.window_sinc_settings['Passband'])
            smoother.NonManifoldSmoothingOn()
            smoother.NormalizeCoordinatesOff()
            smoother.Update()

            self.mesh = pv.PolyData(smoother.GetOutput())

    def compute_cluster(self, points=2500):
        clus = pyacvd.Clustering(self.mesh)
        clus.cluster(points)
        self.mesh = clus.create_mesh()
