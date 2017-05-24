'''
Created on 10-Mar-2016

@author: deepa
'''
'''
Created on 11-May-2015

@author: deepa
'''

import numpy
import copy
from OCC.BRepAlgoAPI import BRepAlgoAPI_Cut


class BeamWebBeamWeb(object):
  
    def __init__(self, column, beam, notch, angle, nut_bolt_array):
        self.column = column
        self.beam = beam
        self.notch = notch
        self.angle = angle
        self.angleLeft = copy.deepcopy(angle)
        self.nut_bolt_array = nut_bolt_array
        self.columnModel = None
        self.beamModel = None
        self.angleModel = None
        self.angleLeftModel = None
        self.clearDist = 20.0  # This distance between edge of the column web/flange and beam cross section
        
    def create_3dmodel(self):
        self.create_column_geometry()
        self.create_beam_geometry()
        self.create_angle_geometry()
        self.create_nut_bolt_array()

        # Call for create_model
        self.columnModel = self.column.create_model()
        self.beamModel = self.beam.create_model()
        self.angleModel = self.angle.create_model()
        self.angleLeftModel = self.angleLeft.create_model()
        self.nutboltArrayModels = self.nut_bolt_array.create_model()
#         self.notchModel = self.notch.create_model()
#         return self.beamModel
    
#     def create_column_geometry(self):
#         column_origin = numpy.array([0, 0, 0])
#         column_u_dir = numpy.array([1.0, 0, 0])
#         wDir1 = numpy.array([0.0, 1.0, 0.0])
#         self.column.place(column_origin, column_u_dir, wDir1)
#         
#     def create_beam_geometry(self):
#         uDir = numpy.array([0, 1.0, 0])
#         wDir = numpy.array([1.0, 0, 0.0])
#         shiftOrigin = (self.column.D/2 - self.beam.D/2)
#         origin2 = self.column.sec_origin + (-shiftOrigin) * self.column.vDir + (self.column.t/2 * self.column.uDir) + (self.column.length/2 * self.column.wDir) + (self.clearDist * self.column.uDir)
#         self.beam.place(origin2, uDir, wDir)
        
    def create_column_geometry(self):

        column_origin = numpy.array([0, 0, 0])
        column_u_dir = numpy.array([1.0, 0, 0])
        wDir1 = numpy.array([0.0, -1.0, 0.0])
        self.column.place(column_origin, column_u_dir, wDir1)
         
    def create_beam_geometry(self):
        beam_origin = ((self.column.sec_origin + self.column.D / 2 - self.beam.D / 2) * (self.column.vDir)) + ((self.column.t / 2 + 20) * self.column.uDir) + (self.column.length / 2 * (self.column.wDir))
        uDir = numpy.array([0.0, 1.0, 0])
        wDir = numpy.array([1.0, 0.0, 0.0])
        self.beam.place(beam_origin, uDir, wDir)
        
#     def createNotchGeometry(self):
#         notchOrigin = (self.beam.sec_origin)*(self.beam.wDir)
#         uDir = numpy.array([-1.0, 0.0, 0])
#         wDir = numpy.array([0.0, 1.0, 0.0])
#         self.notch.place(notchOrigin,uDir,wDir)
    
    def create_angle_geometry(self):
        angle0_origin = (self.beam.sec_origin + (self.beam.D / 2.0 - self.notch.height - self.angle.L)
                         * (self.beam.vDir) - (self.beam.t / 2 * self.beam.uDir) + self.clearDist
                         * (-self.beam.wDir))
        # (self.beam.sec_origin + (self.beam.D / 2.0 - self.beam.T - self.beam.R1 - 5)
        #  * self.beam.vDir + (self.beam.t / 2 * self.beam.uDir) +
        #  self.clearDist * (-self.beam.wDir))
        # uDir0 = numpy.array([1.0, 0.0, 0])
        # wDir0 = numpy.array([0.0, -1.0, 0])
        uDir0 = numpy.array([0, -1.0, 0])
        wDir0 = numpy.array([0.0, 0, 1.0])
        # uDir0 = numpy.array([0, 1.0, 0])
        # wDir0 = numpy.array([0, 0, 1.0])
        self.angleLeft.place(angle0_origin, uDir0, wDir0)

        angle1_origin = (self.beam.sec_origin + (self.beam.D / 2.0 - self.notch.height)
                         * (self.beam.vDir) + (self.beam.t / 2 * self.beam.uDir) + self.clearDist
                         * (-self.beam.wDir))
        # uDir1 = numpy.array([1.0, 0.0, 0])
        # wDir1 = numpy.array([0.0, 1.0, 0])
        uDir1 = numpy.array([0, 1.0, 0])
        wDir1 = numpy.array([0, 0, -1.0])
        self.angle.place(angle1_origin, uDir1, wDir1)

    def create_nut_bolt_array(self):
        nut_bolt_array_origin = self.angleLeft.sec_origin
        nut_bolt_array_origin = nut_bolt_array_origin + self.angleLeft.T * self.angleLeft.uDir
        nut_bolt_array_origin = nut_bolt_array_origin + self.angleLeft.A * self.angleLeft.vDir

        gauge_dir = self.angleLeft.vDir
        pitch_dir = self.angleLeft.wDir
        bolt_dir = -self.angleLeft.uDir

        # c_nutbolt_array_origin = self.angle.sec_origin
        # c_nutbolt_array_origin = c_nutbolt_array_origin + self.angle.T * self.angle.uDir
        # c_nutbolt_array_origin = c_nutbolt_array_origin + self.angle.B * self.angle.wDir
        #
        # c_gauge_dir = self.angle.wDir
        # c_pitch_dir = self.angle.vDir
        # c_bolt_dir = -self.angle.uDir
        c_nutbolt_array_origin = self.angle.sec_origin
        c_nutbolt_array_origin = c_nutbolt_array_origin + self.angle.T * self.angle.vDir
        c_nutbolt_array_origin = c_nutbolt_array_origin + self.angle.B * self.angle.uDir

        c_gauge_dir = self.angle.uDir
        c_pitch_dir = self.angle.wDir
        c_bolt_dir = -self.angle.vDir

        # c_nutbolt_array_origin1 = self.angleLeft.sec_origin
        # c_nutbolt_array_origin1 = c_nutbolt_array_origin1 + self.angle.T * self.angle.uDir
        # c_nutbolt_array_origin1 = c_nutbolt_array_origin - (self.beam.t + self.angle.B) * self.angle.wDir
        # c_nutbolt_array_origin1 = c_nutbolt_array_origin1 + (self.angle.L * self.angle.vDir)
        #
        # c_gauge_dir1 = self.angle.wDir
        # c_pitch_dir1 = self.angle.vDir
        # c_bolt_dir1 = -self.angle.uDir
        c_nutbolt_array_origin1 = self.angleLeft.sec_origin
        c_nutbolt_array_origin1 = c_nutbolt_array_origin1 + self.angle.T * self.angle.vDir
        c_nutbolt_array_origin1 = c_nutbolt_array_origin - (self.beam.t + self.angle.B) * self.angle.uDir
        c_nutbolt_array_origin1 = c_nutbolt_array_origin1 + (self.angle.L * self.angle.wDir)

        c_gauge_dir1 = self.angle.uDir
        c_pitch_dir1 = self.angle.wDir
        c_bolt_dir1 = -self.angle.vDir
        
        self.nut_bolt_array.place(nut_bolt_array_origin, -gauge_dir, pitch_dir, bolt_dir, c_nutbolt_array_origin, -c_gauge_dir, c_pitch_dir, c_bolt_dir,
                                  c_nutbolt_array_origin1, c_gauge_dir1, c_pitch_dir1, c_bolt_dir1)

    def get_models(self):
        '''Returning 3D models
        '''
        return [self.columnModel, self.beamModel, self.angleModel] + self.nut_bolt_array.get_model()
             
    def get_nutboltmodels(self):
        
        return self.nut_bolt_array.get_models()
        # return self.nut_bolt_array.getboltModels()
         
    def get_beamModel(self):
        final_beam = self.beamModel
        nut_bolt_list = self.nut_bolt_array.get_models()
        for bolt in nut_bolt_list[0:(len(nut_bolt_list) // 2)]:
            final_beam = BRepAlgoAPI_Cut(final_beam, bolt).Shape()
        return final_beam


    def get_columnModel(self):
        final_beam = self.columnModel
        nut_bolt_list = self.nut_bolt_array.get_models()
        for bolt in nut_bolt_list[:]:
            final_beam = BRepAlgoAPI_Cut(final_beam, bolt).Shape()
        return final_beam
