# Unit test for the FEM module

# ***************************************************************************
# *   Copyright (c) 2015 - FreeCAD Developers                               *
# *   Author: Przemo Firszt <przemo@firszt.eu>                              *
# *                                                                         *
# *   This file is part of the FreeCAD CAx development system.              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   FreeCAD is distributed in the hope that it will be useful,            *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with FreeCAD; if not, write to the Free Software        *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************/

import Fem
from femtools import ccxtools
import femresult.resulttools as resulttools
import FreeCAD
import ObjectsFem
import femsolver.run
import tempfile
import unittest
import os

mesh_name = 'Mesh'
stat_types = ["U1", "U2", "U3", "Uabs", "Sabs", "MaxPrin", "MidPrin", "MinPrin", "MaxShear", "Peeq", "Temp", "MFlow", "NPress"]

home_path = FreeCAD.getHomePath()
temp_dir = tempfile.gettempdir() + '/FEM_unittests/'
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
test_file_dir = home_path + 'Mod/Fem/femtest/testfiles/ccx/'
test_file_dir_elmer = home_path + 'Mod/Fem/femtest/testfiles/elmer/'

# define some locations fot the analysis tests
# since they are also used in the helper def which create results they should stay global for the module
static_base_name = 'cube_static'
static_analysis_dir = temp_dir + 'FEM_ccx_static/'
static_save_fc_file = static_analysis_dir + static_base_name + '.fcstd'
static_analysis_inp_file = test_file_dir + static_base_name + '.inp'
static_expected_values = test_file_dir + "cube_static_expected_values"

frequency_base_name = 'cube_frequency'
frequency_analysis_dir = temp_dir + 'FEM_ccx_frequency/'
frequency_save_fc_file = frequency_analysis_dir + frequency_base_name + '.fcstd'
frequency_analysis_inp_file = test_file_dir + frequency_base_name + '.inp'
frequency_expected_values = test_file_dir + "cube_frequency_expected_values"

thermomech_base_name = 'spine_thermomech'
thermomech_analysis_dir = temp_dir + 'FEM_ccx_thermomech/'
thermomech_save_fc_file = thermomech_analysis_dir + thermomech_base_name + '.fcstd'
thermomech_analysis_inp_file = test_file_dir + thermomech_base_name + '.inp'
thermomech_expected_values = test_file_dir + "spine_thermomech_expected_values"

Flow1D_thermomech_base_name = 'Flow1D_thermomech'
Flow1D_thermomech_analysis_dir = temp_dir + 'FEM_ccx_Flow1D_thermomech/'
Flow1D_thermomech_save_fc_file = Flow1D_thermomech_analysis_dir + Flow1D_thermomech_base_name + '.fcstd'
Flow1D_thermomech_analysis_inp_file = test_file_dir + Flow1D_thermomech_base_name + '.inp'
Flow1D_thermomech_expected_values = test_file_dir + "Flow1D_thermomech_expected_values"

solverframework_analysis_dir = temp_dir + 'FEM_solverframework/'
solverframework_save_fc_file = solverframework_analysis_dir + static_base_name + '.fcstd'


class FemTest(unittest.TestCase):
    def setUp(self):
        try:
            FreeCAD.setActiveDocument("FemTest")
        except:
            FreeCAD.newDocument("FemTest")
        finally:
            FreeCAD.setActiveDocument("FemTest")
        self.active_doc = FreeCAD.ActiveDocument

    def test_mesh_seg2_python(self):
        seg2 = Fem.FemMesh()
        seg2.addNode(0, 0, 0, 1)
        seg2.addNode(2, 0, 0, 2)
        seg2.addNode(4, 0, 0, 3)
        seg2.addEdge([1, 2])
        seg2.addEdge([2, 3], 2)

        node_data = [seg2.NodeCount, seg2.Nodes]
        edge_data = [seg2.EdgeCount, seg2.Edges[0], seg2.getElementNodes(seg2.Edges[0]), seg2.Edges[1], seg2.getElementNodes(seg2.Edges[1])]
        expected_nodes = [3, {1: FreeCAD.Vector(0.0, 0.0, 0.0), 2: FreeCAD.Vector(2.0, 0.0, 0.0), 3: FreeCAD.Vector(4.0, 0.0, 0.0)}]
        expected_edges = [2, 1, (1, 2), 2, (2, 3)]
        self.assertEqual(node_data, expected_nodes, "Nodes of Python created seg2 element are unexpected")
        self.assertEqual(edge_data, expected_edges, "Edges of Python created seg2 element are unexpected")

    def test_mesh_seg3_python(self):
        seg3 = Fem.FemMesh()
        seg3.addNode(0, 0, 0, 1)
        seg3.addNode(1, 0, 0, 2)
        seg3.addNode(2, 0, 0, 3)
        seg3.addNode(3, 0, 0, 4)
        seg3.addNode(4, 0, 0, 5)
        seg3.addEdge([1, 3, 2])
        seg3.addEdge([3, 5, 4], 2)

        node_data = [seg3.NodeCount, seg3.Nodes]
        edge_data = [seg3.EdgeCount, seg3.Edges[0], seg3.getElementNodes(seg3.Edges[0]), seg3.Edges[1], seg3.getElementNodes(seg3.Edges[1])]
        expected_nodes = [5, {1: FreeCAD.Vector(0.0, 0.0, 0.0), 2: FreeCAD.Vector(1.0, 0.0, 0.0), 3: FreeCAD.Vector(2.0, 0.0, 0.0), 4: FreeCAD.Vector(3.0, 0.0, 0.0), 5: FreeCAD.Vector(4.0, 0.0, 0.0)}]
        expected_edges = [2, 1, (1, 3, 2), 2, (3, 5, 4)]
        self.assertEqual(node_data, expected_nodes, "Nodes of Python created seg3 element are unexpected")
        self.assertEqual(edge_data, expected_edges, "Edges of Python created seg3 element are unexpected")

    def test_unv_save_load(self):
        tetra10 = Fem.FemMesh()
        tetra10.addNode(6, 12, 18, 1)
        tetra10.addNode(0, 0, 18, 2)
        tetra10.addNode(12, 0, 18, 3)
        tetra10.addNode(6, 6, 0, 4)

        tetra10.addNode(3, 6, 18, 5)
        tetra10.addNode(6, 0, 18, 6)
        tetra10.addNode(9, 6, 18, 7)

        tetra10.addNode(6, 9, 9, 8)
        tetra10.addNode(3, 3, 9, 9)
        tetra10.addNode(9, 3, 9, 10)
        tetra10.addVolume([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        unv_file = temp_dir + '/tetra10_mesh.unv'
        tetra10.write(unv_file)
        newmesh = Fem.read(unv_file)
        expected = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        self.assertEqual(newmesh.getElementNodes(1), expected, "Nodes order of quadratic volume element is unexpected")

    def test_writeAbaqus_precision(self):
        # https://forum.freecadweb.org/viewtopic.php?f=18&t=22759#p176669
        # ccx reads only F20.0 (i. e. Fortran floating point field 20 chars wide)
        # thus precision is set to 13 in writeAbaqus
        seg2 = Fem.FemMesh()
        seg2.addNode(0, 0, 0, 1)
        #            1234567890123456789012  1234567890123456789012  123456789012345678901234567
        seg2.addNode(-5000000000000000000.1, -1.123456789123456e-14, -0.1234567890123456789e-101, 2)
        seg2.addEdge([1, 2])

        inp_file = temp_dir + '/seg2_mesh.inp'
        seg2.writeABAQUS(inp_file, 1, False)

        read_file = open(inp_file, 'r')
        read_node_line = 'line was not found'
        for l in read_file:
            l = l.strip()
            if l.startswith('2, -5'):
                read_node_line = l
        read_file.close()

        #                  1234567  12345678901234567890  12345678901234567890
        expected_win = '2, -5e+018, -1.123456789123e-014, -1.234567890123e-102'
        expected_lin = '2, -5e+18, -1.123456789123e-14, -1.234567890123e-102'
        expected = [expected_lin, expected_win]
        self.assertTrue(True if read_node_line in expected else False,
                        "Problem in test_writeAbaqus_precision, \n{0}\n{1}".format(read_node_line, expected))

    def test_read_frd_massflow_networkpressure(self):
        # read data from frd file
        frd_file = test_file_dir + 'Flow1D_thermomech.frd'
        import feminout.importCcxFrdResults as importCcxFrdResults
        frd_content = importCcxFrdResults.readResult(frd_file)

        # do something with the read data
        frd_content_len = []
        for key in sorted(frd_content.keys()):
            frd_content_len.append(len(frd_content[key]))
        print('read data')
        print(frd_content_len)
        print(sorted(frd_content.keys()))
        # print(frd_content)
        read_mflow = frd_content['Results'][12]['mflow']
        read_npressure = frd_content['Results'][12]['npressure']
        res_len = [
            len(read_mflow),
            len(read_npressure)
        ]
        print(res_len)
        print(read_mflow)
        print(read_npressure)

        # create the expected data
        print('\nexpected data')
        efc = {}  # expected frd content
        efc['Nodes'] = {
            2: FreeCAD.Vector(0.0, 0.0, -50.0),
            3: FreeCAD.Vector(0.0, 0.0, -4300.0),
            4: FreeCAD.Vector(4950.0, 0.0, -4300.0),
            5: FreeCAD.Vector(5000.0, 0.0, -4300.0),
            6: FreeCAD.Vector(8535.53, 0.0, -7835.53),
            7: FreeCAD.Vector(8569.88, 0.0, -7870.88),
            8: FreeCAD.Vector(12105.4, 0.0, -11406.4),
            9: FreeCAD.Vector(12140.8, 0.0, -11441.8),
            10: FreeCAD.Vector(13908.5, 0.0, -13209.5),
            11: FreeCAD.Vector(13943.9, 0.0, -13244.9),
            12: FreeCAD.Vector(15047.0, 0.0, -14348.0),
            13: FreeCAD.Vector(15047.0, 0.0, -7947.97),
            15: FreeCAD.Vector(0.0, 0.0, 0.0),
            16: FreeCAD.Vector(0.0, 0.0, -2175.0),
            17: FreeCAD.Vector(2475.0, 0.0, -4300.0),
            18: FreeCAD.Vector(4975.0, 0.0, -4300.0),
            19: FreeCAD.Vector(6767.77, 0.0, -6067.77),
            20: FreeCAD.Vector(8552.71, 0.0, -7853.21),
            21: FreeCAD.Vector(10337.6, 0.0, -9638.64),
            22: FreeCAD.Vector(12123.1, 0.0, -11424.1),
            23: FreeCAD.Vector(13024.6, 0.0, -12325.6),
            24: FreeCAD.Vector(13926.2, 0.0, -13227.2),
            25: FreeCAD.Vector(14495.4, 0.0, -13796.4),
            26: FreeCAD.Vector(15047.0, 0.0, -11148.0),
            27: FreeCAD.Vector(15047.0, 0.0, -7897.97)
        }
        efc['Seg2Elem'] = {
            1: (15, 2),
            13: (13, 27)
        }
        efc['Seg3Elem'] = {}
        '''   deleted during reading because of the inout file
        efc['Seg3Elem'] = {
            2: (2, 16, 3),
            3: (3, 17, 4),
            4: (4, 18, 5),
            5: (5, 19, 6),
            6: (6, 20, 7),
            7: (7, 21, 8),
            8: (8, 22, 9),
            9: (9, 23, 10),
            10: (10, 24, 11),
            11: (11, 25, 12),
            12: (12, 26, 13)
        }
        '''
        efc['Tria3Elem'] = efc['Tria6Elem'] = efc['Quad4Elem'] = efc['Quad8Elem'] = {}  # faces
        efc['Tetra4Elem'] = efc['Tetra10Elem'] = efc['Hexa8Elem'] = efc['Hexa20Elem'] = efc['Penta6Elem'] = efc['Penta15Elem'] = {}  # volumes
        efc['Results'] = [
            {'time': 0.00390625},
            {'time': 0.0078125},
            {'time': 0.0136719},
            {'time': 0.0224609},
            {'time': 0.0356445},
            {'time': 0.0554199},
            {'time': 0.085083},
            {'time': 0.129578},
            {'time': 0.19632},
            {'time': 0.296432},
            {'time': 0.446602},
            {'time': 0.671856},
            {
                'number': 0,
                'time': 1.0,
                'mflow': {
                    1: 78.3918,  # added during reading because of the inout file
                    2: 78.3918,
                    3: 78.3918,
                    4: 78.3918,
                    5: 78.3918,
                    6: 78.3918,
                    7: 78.3918,
                    8: 78.3918,
                    9: 78.3918,
                    10: 78.3918,
                    11: 78.3918,
                    12: 78.3918,
                    13: 78.3918,
                    15: 78.3918,
                    16: 78.3918,
                    17: 78.3918,
                    18: 78.3918,
                    19: 78.3918,
                    20: 78.3918,
                    21: 78.3918,
                    22: 78.3918,
                    23: 78.3918,
                    24: 78.3918,
                    25: 78.3918,
                    26: 78.3918,
                    27: 78.3918,
                    28: 78.3918  # added during reading because of the inout file
                },
                'npressure': {
                    1: 0.1,  # added during reading because of the inout file
                    2: 0.1,
                    3: 0.134840,
                    4: 0.128261,
                    5: 0.127949,
                    6: 0.155918,
                    7: 0.157797,
                    8: 0.191647,
                    9: 0.178953,
                    10: 0.180849,
                    11: 0.161476,
                    12: 0.162658,
                    13: 0.1,
                    15: 0.1,
                    16: 0.117420,
                    17: 0.131551,
                    18: 0.128105,
                    19: 0.141934,
                    20: 0.156857,
                    21: 0.174722,
                    22: 0.185300,
                    23: 0.179901,
                    24: 0.171162,
                    25: 0.162067,
                    26: 0.131329,
                    27: 0.1,
                    28: 0.1  # added during reading because of the inout file
                }
            }
        ]
        expected_frd_content = efc

        # do something with the expected data
        expected_frd_content_len = []
        for key in sorted(expected_frd_content.keys()):
            expected_frd_content_len.append(len(expected_frd_content[key]))
        print(expected_frd_content_len)
        print(sorted(expected_frd_content.keys()))
        # expected results
        expected_mflow = expected_frd_content['Results'][12]['mflow']
        expected_npressure = expected_frd_content['Results'][12]['npressure']
        expected_res_len = [
            len(expected_mflow),
            len(expected_npressure)
        ]
        print(expected_res_len)
        print(expected_mflow)
        print(expected_npressure)

        # tests
        self.assertEqual(frd_content_len, expected_frd_content_len, "Length's of read frd data values are unexpected")
        self.assertEqual(frd_content['Nodes'], expected_frd_content['Nodes'], "Values of read node data are unexpected")
        self.assertEqual(frd_content['Seg2Elem'], expected_frd_content['Seg2Elem'], "Values of read Seg2 data are unexpected")
        self.assertEqual(frd_content['Seg3Elem'], expected_frd_content['Seg3Elem'], "Values of read Seg3 data are unexpected")
        self.assertEqual(res_len, expected_res_len, "Length's of read result data values are unexpected")
        self.assertEqual(read_mflow, expected_mflow, "Values of read mflow result data are unexpected")
        self.assertEqual(read_npressure, expected_npressure, "Values of read npressure result data are unexpected")

    def test_femobjects_make(self):
        doc = self.active_doc
        analysis = ObjectsFem.makeAnalysis(doc)

        analysis.addObject(ObjectsFem.makeConstraintBearing(doc))
        analysis.addObject(ObjectsFem.makeConstraintBodyHeatSource(doc))
        analysis.addObject(ObjectsFem.makeConstraintContact(doc))
        analysis.addObject(ObjectsFem.makeConstraintDisplacement(doc))
        analysis.addObject(ObjectsFem.makeConstraintElectrostaticPotential(doc))
        analysis.addObject(ObjectsFem.makeConstraintFixed(doc))
        analysis.addObject(ObjectsFem.makeConstraintFlowVelocity(doc))
        analysis.addObject(ObjectsFem.makeConstraintFluidBoundary(doc))
        analysis.addObject(ObjectsFem.makeConstraintForce(doc))
        analysis.addObject(ObjectsFem.makeConstraintGear(doc))
        analysis.addObject(ObjectsFem.makeConstraintHeatflux(doc))
        analysis.addObject(ObjectsFem.makeConstraintInitialFlowVelocity(doc))
        analysis.addObject(ObjectsFem.makeConstraintInitialTemperature(doc))
        analysis.addObject(ObjectsFem.makeConstraintPlaneRotation(doc))
        analysis.addObject(ObjectsFem.makeConstraintPressure(doc))
        analysis.addObject(ObjectsFem.makeConstraintPulley(doc))
        analysis.addObject(ObjectsFem.makeConstraintSelfWeight(doc))
        analysis.addObject(ObjectsFem.makeConstraintTemperature(doc))
        analysis.addObject(ObjectsFem.makeConstraintTransform(doc))

        analysis.addObject(ObjectsFem.makeElementFluid1D(doc))
        analysis.addObject(ObjectsFem.makeElementGeometry1D(doc))
        analysis.addObject(ObjectsFem.makeElementGeometry2D(doc))
        analysis.addObject(ObjectsFem.makeElementRotation1D(doc))

        analysis.addObject(ObjectsFem.makeMaterialFluid(doc))
        mat = analysis.addObject(ObjectsFem.makeMaterialSolid(doc))[0]
        analysis.addObject(ObjectsFem.makeMaterialMechanicalNonlinear(doc, mat))

        msh = analysis.addObject(ObjectsFem.makeMeshGmsh(doc))[0]
        analysis.addObject(ObjectsFem.makeMeshBoundaryLayer(doc, msh))
        analysis.addObject(ObjectsFem.makeMeshGroup(doc, msh))
        analysis.addObject(ObjectsFem.makeMeshRegion(doc, msh))
        analysis.addObject(ObjectsFem.makeMeshNetgen(doc))
        analysis.addObject(ObjectsFem.makeMeshResult(doc))

        analysis.addObject(ObjectsFem.makeResultMechanical(doc))

        analysis.addObject(ObjectsFem.makeSolverCalculixCcxTools(doc))
        analysis.addObject(ObjectsFem.makeSolverCalculix(doc))
        sol = analysis.addObject(ObjectsFem.makeSolverElmer(doc))[0]
        analysis.addObject(ObjectsFem.makeSolverZ88(doc))

        analysis.addObject(ObjectsFem.makeEquationElasticity(doc, sol))
        analysis.addObject(ObjectsFem.makeEquationElectrostatic(doc, sol))
        analysis.addObject(ObjectsFem.makeEquationFlow(doc, sol))
        analysis.addObject(ObjectsFem.makeEquationFluxsolver(doc, sol))
        analysis.addObject(ObjectsFem.makeEquationHeat(doc, sol))
        # TODO the equations show up twice on Tree (on solver and on analysis), if they are added to the analysis group

        doc.recompute()
        self.assertEqual(len(analysis.Group), get_defmake_count() - 1)  # because of the analysis itself count -1

    def test_femobjects_type(self):
        doc = self.active_doc

        from femtools.femutils import typeOfObj
        self.assertEqual('Fem::FemAnalysis', typeOfObj(ObjectsFem.makeAnalysis(doc)))
        self.assertEqual('Fem::ConstraintBearing', typeOfObj(ObjectsFem.makeConstraintBearing(doc)))
        self.assertEqual('Fem::ConstraintBodyHeatSource', typeOfObj(ObjectsFem.makeConstraintBodyHeatSource(doc)))
        self.assertEqual('Fem::ConstraintContact', typeOfObj(ObjectsFem.makeConstraintContact(doc)))
        self.assertEqual('Fem::ConstraintDisplacement', typeOfObj(ObjectsFem.makeConstraintDisplacement(doc)))
        self.assertEqual('Fem::ConstraintElectrostaticPotential', typeOfObj(ObjectsFem.makeConstraintElectrostaticPotential(doc)))
        self.assertEqual('Fem::ConstraintFixed', typeOfObj(ObjectsFem.makeConstraintFixed(doc)))
        self.assertEqual('Fem::ConstraintFlowVelocity', typeOfObj(ObjectsFem.makeConstraintFlowVelocity(doc)))
        self.assertEqual('Fem::ConstraintFluidBoundary', typeOfObj(ObjectsFem.makeConstraintFluidBoundary(doc)))
        self.assertEqual('Fem::ConstraintForce', typeOfObj(ObjectsFem.makeConstraintForce(doc)))
        self.assertEqual('Fem::ConstraintGear', typeOfObj(ObjectsFem.makeConstraintGear(doc)))
        self.assertEqual('Fem::ConstraintHeatflux', typeOfObj(ObjectsFem.makeConstraintHeatflux(doc)))
        self.assertEqual('Fem::ConstraintInitialFlowVelocity', typeOfObj(ObjectsFem.makeConstraintInitialFlowVelocity(doc)))
        self.assertEqual('Fem::ConstraintInitialTemperature', typeOfObj(ObjectsFem.makeConstraintInitialTemperature(doc)))
        self.assertEqual('Fem::ConstraintPlaneRotation', typeOfObj(ObjectsFem.makeConstraintPlaneRotation(doc)))
        self.assertEqual('Fem::ConstraintPressure', typeOfObj(ObjectsFem.makeConstraintPressure(doc)))
        self.assertEqual('Fem::ConstraintPulley', typeOfObj(ObjectsFem.makeConstraintPulley(doc)))
        self.assertEqual('Fem::ConstraintSelfWeight', typeOfObj(ObjectsFem.makeConstraintSelfWeight(doc)))
        self.assertEqual('Fem::ConstraintTemperature', typeOfObj(ObjectsFem.makeConstraintTemperature(doc)))
        self.assertEqual('Fem::ConstraintTransform', typeOfObj(ObjectsFem.makeConstraintTransform(doc)))
        self.assertEqual('Fem::FemElementFluid1D', typeOfObj(ObjectsFem.makeElementFluid1D(doc)))
        self.assertEqual('Fem::FemElementGeometry1D', typeOfObj(ObjectsFem.makeElementGeometry1D(doc)))
        self.assertEqual('Fem::FemElementGeometry2D', typeOfObj(ObjectsFem.makeElementGeometry2D(doc)))
        self.assertEqual('Fem::FemElementRotation1D', typeOfObj(ObjectsFem.makeElementRotation1D(doc)))
        materialsolid = ObjectsFem.makeMaterialSolid(doc)
        self.assertEqual('Fem::Material', typeOfObj(ObjectsFem.makeMaterialFluid(doc)))
        self.assertEqual('Fem::Material', typeOfObj(materialsolid))
        self.assertEqual('Fem::MaterialMechanicalNonlinear', typeOfObj(ObjectsFem.makeMaterialMechanicalNonlinear(doc, materialsolid)))
        mesh = ObjectsFem.makeMeshGmsh(doc)
        self.assertEqual('Fem::FemMeshGmsh', typeOfObj(mesh))
        self.assertEqual('Fem::FemMeshBoundaryLayer', typeOfObj(ObjectsFem.makeMeshBoundaryLayer(doc, mesh)))
        self.assertEqual('Fem::FemMeshGroup', typeOfObj(ObjectsFem.makeMeshGroup(doc, mesh)))
        self.assertEqual('Fem::FemMeshRegion', typeOfObj(ObjectsFem.makeMeshRegion(doc, mesh)))
        self.assertEqual('Fem::FemMeshShapeNetgenObject', typeOfObj(ObjectsFem.makeMeshNetgen(doc)))
        self.assertEqual('Fem::FemMeshResult', typeOfObj(ObjectsFem.makeMeshResult(doc)))
        self.assertEqual('Fem::FemResultMechanical', typeOfObj(ObjectsFem.makeResultMechanical(doc)))
        solverelmer = ObjectsFem.makeSolverElmer(doc)
        self.assertEqual('Fem::FemSolverCalculixCcxTools', typeOfObj(ObjectsFem.makeSolverCalculixCcxTools(doc)))
        self.assertEqual('Fem::FemSolverObjectCalculix', typeOfObj(ObjectsFem.makeSolverCalculix(doc)))
        self.assertEqual('Fem::FemSolverObjectElmer', typeOfObj(solverelmer))
        self.assertEqual('Fem::FemSolverObjectZ88', typeOfObj(ObjectsFem.makeSolverZ88(doc)))
        self.assertEqual('Fem::FemEquationElmerElasticity', typeOfObj(ObjectsFem.makeEquationElasticity(doc, solverelmer)))
        self.assertEqual('Fem::FemEquationElmerElectrostatic', typeOfObj(ObjectsFem.makeEquationElectrostatic(doc, solverelmer)))
        self.assertEqual('Fem::FemEquationElmerFlow', typeOfObj(ObjectsFem.makeEquationFlow(doc, solverelmer)))
        self.assertEqual('Fem::FemEquationElmerFluxsolver', typeOfObj(ObjectsFem.makeEquationFluxsolver(doc, solverelmer)))
        self.assertEqual('Fem::FemEquationElmerHeat', typeOfObj(ObjectsFem.makeEquationHeat(doc, solverelmer)))
        # TODO: equation linear missing, equation nonlinear missing, use different type for fluid and solid material

    def test_femobjects_isoftypenew(self):
        doc = self.active_doc

        from femtools.femutils import isOfTypeNew
        self.assertTrue(isOfTypeNew(ObjectsFem.makeAnalysis(doc), 'Fem::FemAnalysis'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintBearing(doc), 'Fem::ConstraintBearing'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintBodyHeatSource(doc), 'Fem::ConstraintBodyHeatSource'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintContact(doc), 'Fem::ConstraintContact'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintDisplacement(doc), 'Fem::ConstraintDisplacement'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintElectrostaticPotential(doc), 'Fem::ConstraintElectrostaticPotential'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintFixed(doc), 'Fem::ConstraintFixed'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintFlowVelocity(doc), 'Fem::ConstraintFlowVelocity'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintFluidBoundary(doc), 'Fem::ConstraintFluidBoundary'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintForce(doc), 'Fem::ConstraintForce'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintGear(doc), 'Fem::ConstraintGear'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintHeatflux(doc), 'Fem::ConstraintHeatflux'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintInitialFlowVelocity(doc), 'Fem::ConstraintInitialFlowVelocity'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintInitialTemperature(doc), 'Fem::ConstraintInitialTemperature'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintPlaneRotation(doc), 'Fem::ConstraintPlaneRotation'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintPressure(doc), 'Fem::ConstraintPressure'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintPulley(doc), 'Fem::ConstraintPulley'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintSelfWeight(doc), 'Fem::ConstraintSelfWeight'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintTemperature(doc), 'Fem::ConstraintTemperature'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeConstraintTransform(doc), 'Fem::ConstraintTransform'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeElementFluid1D(doc), 'Fem::FemElementFluid1D'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeElementGeometry1D(doc), 'Fem::FemElementGeometry1D'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeElementGeometry2D(doc), 'Fem::FemElementGeometry2D'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeElementRotation1D(doc), 'Fem::FemElementRotation1D'))
        materialsolid = ObjectsFem.makeMaterialSolid(doc)
        self.assertTrue(isOfTypeNew(ObjectsFem.makeMaterialFluid(doc), 'Fem::Material'))
        self.assertTrue(isOfTypeNew(materialsolid, 'Fem::Material'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeMaterialMechanicalNonlinear(doc, materialsolid), 'Fem::MaterialMechanicalNonlinear'))
        mesh = ObjectsFem.makeMeshGmsh(doc)
        self.assertTrue(isOfTypeNew(mesh, 'Fem::FemMeshGmsh'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeMeshBoundaryLayer(doc, mesh), 'Fem::FemMeshBoundaryLayer'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeMeshGroup(doc, mesh), 'Fem::FemMeshGroup'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeMeshRegion(doc, mesh), 'Fem::FemMeshRegion'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeMeshNetgen(doc), 'Fem::FemMeshShapeNetgenObject'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeMeshResult(doc), 'Fem::FemMeshResult'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeResultMechanical(doc), 'Fem::FemResultMechanical'))
        solverelmer = ObjectsFem.makeSolverElmer(doc)
        self.assertTrue(isOfTypeNew(ObjectsFem.makeSolverCalculixCcxTools(doc), 'Fem::FemSolverCalculixCcxTools'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeSolverCalculix(doc), 'Fem::FemSolverObjectCalculix'))
        self.assertTrue(isOfTypeNew(solverelmer, 'Fem::FemSolverObjectElmer'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeSolverZ88(doc), 'Fem::FemSolverObjectZ88'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeEquationElasticity(doc, solverelmer), 'Fem::FemEquationElmerElasticity'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeEquationElectrostatic(doc, solverelmer), 'Fem::FemEquationElmerElectrostatic'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeEquationFlow(doc, solverelmer), 'Fem::FemEquationElmerFlow'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeEquationFluxsolver(doc, solverelmer), 'Fem::FemEquationElmerFluxsolver'))
        self.assertTrue(isOfTypeNew(ObjectsFem.makeEquationHeat(doc, solverelmer), 'Fem::FemEquationElmerHeat'))

    def test_femobjects_derivedfromfem(self):
        doc = self.active_doc

        from femtools.femutils import isDerivedFrom as isDerivedFromFem
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeAnalysis(doc), 'Fem::FemAnalysis'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintBearing(doc), 'Fem::ConstraintBearing'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintBodyHeatSource(doc), 'Fem::ConstraintBodyHeatSource'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintContact(doc), 'Fem::ConstraintContact'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintDisplacement(doc), 'Fem::ConstraintDisplacement'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintElectrostaticPotential(doc), 'Fem::ConstraintElectrostaticPotential'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintFixed(doc), 'Fem::ConstraintFixed'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintFlowVelocity(doc), 'Fem::ConstraintFlowVelocity'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintFluidBoundary(doc), 'Fem::ConstraintFluidBoundary'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintForce(doc), 'Fem::ConstraintForce'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintGear(doc), 'Fem::ConstraintGear'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintHeatflux(doc), 'Fem::ConstraintHeatflux'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintInitialFlowVelocity(doc), 'Fem::ConstraintInitialFlowVelocity'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintInitialTemperature(doc), 'Fem::ConstraintInitialTemperature'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintPlaneRotation(doc), 'Fem::ConstraintPlaneRotation'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintPressure(doc), 'Fem::ConstraintPressure'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintPulley(doc), 'Fem::ConstraintPulley'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintSelfWeight(doc), 'Fem::ConstraintSelfWeight'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintTemperature(doc), 'Fem::ConstraintTemperature'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeConstraintTransform(doc), 'Fem::ConstraintTransform'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeElementFluid1D(doc), 'Fem::FemElementFluid1D'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeElementGeometry1D(doc), 'Fem::FemElementGeometry1D'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeElementGeometry2D(doc), 'Fem::FemElementGeometry2D'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeElementRotation1D(doc), 'Fem::FemElementRotation1D'))
        materialsolid = ObjectsFem.makeMaterialSolid(doc)
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeMaterialFluid(doc), 'Fem::Material'))
        self.assertTrue(isDerivedFromFem(materialsolid, 'Fem::Material'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeMaterialMechanicalNonlinear(doc, materialsolid), 'Fem::MaterialMechanicalNonlinear'))
        mesh = ObjectsFem.makeMeshGmsh(doc)
        self.assertTrue(isDerivedFromFem(mesh, 'Fem::FemMeshGmsh'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeMeshBoundaryLayer(doc, mesh), 'Fem::FemMeshBoundaryLayer'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeMeshGroup(doc, mesh), 'Fem::FemMeshGroup'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeMeshRegion(doc, mesh), 'Fem::FemMeshRegion'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeMeshNetgen(doc), 'Fem::FemMeshShapeNetgenObject'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeMeshResult(doc), 'Fem::FemMeshResult'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeResultMechanical(doc), 'Fem::FemResultMechanical'))
        solverelmer = ObjectsFem.makeSolverElmer(doc)
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeSolverCalculixCcxTools(doc), 'Fem::FemSolverCalculixCcxTools'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeSolverCalculix(doc), 'Fem::FemSolverObjectCalculix'))
        self.assertTrue(isDerivedFromFem(solverelmer, 'Fem::FemSolverObjectElmer'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeSolverZ88(doc), 'Fem::FemSolverObjectZ88'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeEquationElasticity(doc, solverelmer), 'Fem::FemEquationElmerElasticity'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeEquationElectrostatic(doc, solverelmer), 'Fem::FemEquationElmerElectrostatic'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeEquationFlow(doc, solverelmer), 'Fem::FemEquationElmerFlow'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeEquationFluxsolver(doc, solverelmer), 'Fem::FemEquationElmerFluxsolver'))
        self.assertTrue(isDerivedFromFem(ObjectsFem.makeEquationHeat(doc, solverelmer), 'Fem::FemEquationElmerHeat'))

    def test_femobjects_derivedfromstd(self):
        doc = self.active_doc

        self.assertTrue(ObjectsFem.makeAnalysis(doc).isDerivedFrom('Fem::FemAnalysis'))
        self.assertTrue(ObjectsFem.makeConstraintBearing(doc).isDerivedFrom('Fem::ConstraintBearing'))
        self.assertTrue(ObjectsFem.makeConstraintBodyHeatSource(doc).isDerivedFrom('Fem::ConstraintPython'))
        self.assertTrue(ObjectsFem.makeConstraintContact(doc).isDerivedFrom('Fem::ConstraintContact'))
        self.assertTrue(ObjectsFem.makeConstraintDisplacement(doc).isDerivedFrom('Fem::ConstraintDisplacement'))
        self.assertTrue(ObjectsFem.makeConstraintElectrostaticPotential(doc).isDerivedFrom('Fem::ConstraintPython'))
        self.assertTrue(ObjectsFem.makeConstraintFixed(doc).isDerivedFrom('Fem::ConstraintFixed'))
        self.assertTrue(ObjectsFem.makeConstraintFlowVelocity(doc).isDerivedFrom('Fem::ConstraintPython'))
        self.assertTrue(ObjectsFem.makeConstraintFluidBoundary(doc).isDerivedFrom('Fem::ConstraintFluidBoundary'))
        self.assertTrue(ObjectsFem.makeConstraintForce(doc).isDerivedFrom('Fem::ConstraintForce'))
        self.assertTrue(ObjectsFem.makeConstraintGear(doc).isDerivedFrom('Fem::ConstraintGear'))
        self.assertTrue(ObjectsFem.makeConstraintHeatflux(doc).isDerivedFrom('Fem::ConstraintHeatflux'))
        self.assertTrue(ObjectsFem.makeConstraintInitialFlowVelocity(doc).isDerivedFrom('Fem::ConstraintPython'))
        self.assertTrue(ObjectsFem.makeConstraintInitialTemperature(doc).isDerivedFrom('Fem::ConstraintInitialTemperature'))
        self.assertTrue(ObjectsFem.makeConstraintPlaneRotation(doc).isDerivedFrom('Fem::ConstraintPlaneRotation'))
        self.assertTrue(ObjectsFem.makeConstraintPressure(doc).isDerivedFrom('Fem::ConstraintPressure'))
        self.assertTrue(ObjectsFem.makeConstraintPulley(doc).isDerivedFrom('Fem::ConstraintPulley'))
        self.assertTrue(ObjectsFem.makeConstraintSelfWeight(doc).isDerivedFrom('Fem::ConstraintPython'))
        self.assertTrue(ObjectsFem.makeConstraintTemperature(doc).isDerivedFrom('Fem::ConstraintTemperature'))
        self.assertTrue(ObjectsFem.makeConstraintTransform(doc).isDerivedFrom('Fem::ConstraintTransform'))
        self.assertTrue(ObjectsFem.makeElementFluid1D(doc).isDerivedFrom('Fem::FeaturePython'))
        self.assertTrue(ObjectsFem.makeElementGeometry1D(doc).isDerivedFrom('Fem::FeaturePython'))
        self.assertTrue(ObjectsFem.makeElementGeometry2D(doc).isDerivedFrom('Fem::FeaturePython'))
        self.assertTrue(ObjectsFem.makeElementRotation1D(doc).isDerivedFrom('Fem::FeaturePython'))
        materialsolid = ObjectsFem.makeMaterialSolid(doc)
        self.assertTrue(ObjectsFem.makeMaterialFluid(doc).isDerivedFrom('App::MaterialObjectPython'))
        self.assertTrue(materialsolid.isDerivedFrom('App::MaterialObjectPython'))
        self.assertTrue(ObjectsFem.makeMaterialMechanicalNonlinear(doc, materialsolid).isDerivedFrom('Fem::FeaturePython'))
        mesh = ObjectsFem.makeMeshGmsh(doc)
        self.assertTrue(mesh.isDerivedFrom('Fem::FemMeshObjectPython'))
        self.assertTrue(ObjectsFem.makeMeshBoundaryLayer(doc, mesh).isDerivedFrom('Fem::FeaturePython'))
        self.assertTrue(ObjectsFem.makeMeshGroup(doc, mesh).isDerivedFrom('Fem::FeaturePython'))
        self.assertTrue(ObjectsFem.makeMeshRegion(doc, mesh).isDerivedFrom('Fem::FeaturePython'))
        self.assertTrue(ObjectsFem.makeMeshNetgen(doc).isDerivedFrom('Fem::FemMeshShapeNetgenObject'))
        self.assertTrue(ObjectsFem.makeMeshResult(doc).isDerivedFrom('Fem::FemMeshObjectPython'))
        self.assertTrue(ObjectsFem.makeResultMechanical(doc).isDerivedFrom('Fem::FemResultObjectPython'))
        solverelmer = ObjectsFem.makeSolverElmer(doc)
        self.assertTrue(ObjectsFem.makeSolverCalculixCcxTools(doc).isDerivedFrom('Fem::FemSolverObjectPython'))
        self.assertTrue(ObjectsFem.makeSolverCalculix(doc).isDerivedFrom('Fem::FemSolverObjectPython'))
        self.assertTrue(solverelmer.isDerivedFrom('Fem::FemSolverObjectPython'))
        self.assertTrue(ObjectsFem.makeSolverZ88(doc).isDerivedFrom('Fem::FemSolverObjectPython'))
        self.assertTrue(ObjectsFem.makeEquationElasticity(doc, solverelmer).isDerivedFrom('App::FeaturePython'))
        self.assertTrue(ObjectsFem.makeEquationElectrostatic(doc, solverelmer).isDerivedFrom('App::FeaturePython'))
        self.assertTrue(ObjectsFem.makeEquationFlow(doc, solverelmer).isDerivedFrom('App::FeaturePython'))
        self.assertTrue(ObjectsFem.makeEquationFluxsolver(doc, solverelmer).isDerivedFrom('App::FeaturePython'))
        self.assertTrue(ObjectsFem.makeEquationHeat(doc, solverelmer).isDerivedFrom('App::FeaturePython'))

    def test_adding_refshaps(self):
        doc = self.active_doc
        slab = doc.addObject("Part::Plane", "Face")
        slab.Length = 500.00
        slab.Width = 500.00
        cf = ObjectsFem.makeConstraintFixed(doc)
        ref_eles = []
        # FreeCAD list property seam not to support append, thus we need some workaround, which is on many elements even much faster
        for i, face in enumerate(slab.Shape.Edges):
            ref_eles.append("Edge%d" % (i + 1))
        cf.References = [(slab, ref_eles)]
        doc.recompute()
        expected_reflist = [(slab, ('Edge1', 'Edge2', 'Edge3', 'Edge4'))]
        assert_err_message = 'Adding reference shapes did not result in expected list ' + str(cf.References) + ' != ' + str(expected_reflist)
        self.assertEqual(cf.References, expected_reflist, assert_err_message)

    def test_pyimport_all_FEM_modules(self):
        # we're going to try to import all python modules from FreeCAD Fem
        pymodules = []

        # collect all Python modules in Fem
        pymodules += collect_python_modules('')  # Fem main dir
        pymodules += collect_python_modules('feminout')
        pymodules += collect_python_modules('femmesh')
        pymodules += collect_python_modules('femresult')
        pymodules += collect_python_modules('femtest')
        pymodules += collect_python_modules('femobjects')
        if FreeCAD.GuiUp:
            pymodules += collect_python_modules('femcommands')
            pymodules += collect_python_modules('femguiobjects')
        pymodules += collect_python_modules('femsolver')
        pymodules += collect_python_modules('femsolver/elmer')
        pymodules += collect_python_modules('femsolver/elmer/equations')
        pymodules += collect_python_modules('femsolver/z88')
        pymodules += collect_python_modules('femsolver/calculix')

        # import all collected modules
        # fcc_print(pymodules)
        for mod in pymodules:
            fcc_print('Try importing {0} ...'.format(mod))
            try:
                im = __import__('{0}'.format(mod))
            except:
                im = False
            if not im:
                __import__('{0}'.format(mod))  # to get an error message what was going wrong
            self.assertTrue(im, 'Problem importing {0}'.format(mod))

    def tearDown(self):
        FreeCAD.closeDocument("FemTest")
        pass


class FemCcxAnalysisTest(unittest.TestCase):

    def setUp(self):
        try:
            FreeCAD.setActiveDocument("FemTest")
        except:
            FreeCAD.newDocument("FemTest")
        finally:
            FreeCAD.setActiveDocument("FemTest")
        self.active_doc = FreeCAD.ActiveDocument

    def test_static_freq_analysis(self):
        # static
        fcc_print('--------------- Start of FEM tests ---------------')
        box = self.active_doc.addObject("Part::Box", "Box")
        fcc_print('Checking FEM new analysis...')
        analysis = ObjectsFem.makeAnalysis(self.active_doc, 'Analysis')
        self.assertTrue(analysis, "FemTest of new analysis failed")

        fcc_print('Checking FEM new solver...')
        solver_object = ObjectsFem.makeSolverCalculixCcxTools(self.active_doc, 'CalculiX')
        solver_object.GeometricalNonlinearity = 'linear'
        solver_object.ThermoMechSteadyState = False
        solver_object.MatrixSolverType = 'default'
        solver_object.IterationsControlParameterTimeUse = False
        solver_object.EigenmodesCount = 10
        solver_object.EigenmodeHighLimit = 1000000.0
        solver_object.EigenmodeLowLimit = 0.0
        self.assertTrue(solver_object, "FemTest of new solver failed")
        analysis.addObject(solver_object)

        fcc_print('Checking FEM new material...')
        material_object = ObjectsFem.makeMaterialSolid(self.active_doc, 'MechanicalMaterial')
        mat = material_object.Material
        mat['Name'] = "Steel-Generic"
        mat['YoungsModulus'] = "200000 MPa"
        mat['PoissonRatio'] = "0.30"
        mat['Density'] = "7900 kg/m^3"
        material_object.Material = mat
        self.assertTrue(material_object, "FemTest of new material failed")
        analysis.addObject(material_object)

        fcc_print('Checking FEM new fixed constraint...')
        fixed_constraint = self.active_doc.addObject("Fem::ConstraintFixed", "FemConstraintFixed")
        fixed_constraint.References = [(box, "Face1")]
        self.assertTrue(fixed_constraint, "FemTest of new fixed constraint failed")
        analysis.addObject(fixed_constraint)

        fcc_print('Checking FEM new force constraint...')
        force_constraint = self.active_doc.addObject("Fem::ConstraintForce", "FemConstraintForce")
        force_constraint.References = [(box, "Face6")]
        force_constraint.Force = 40000.0
        force_constraint.Direction = (box, ["Edge5"])
        self.active_doc.recompute()
        force_constraint.Reversed = True
        self.active_doc.recompute()
        self.assertTrue(force_constraint, "FemTest of new force constraint failed")
        analysis.addObject(force_constraint)

        fcc_print('Checking FEM new pressure constraint...')
        pressure_constraint = self.active_doc.addObject("Fem::ConstraintPressure", "FemConstraintPressure")
        pressure_constraint.References = [(box, "Face2")]
        pressure_constraint.Pressure = 1000.0
        pressure_constraint.Reversed = False
        self.assertTrue(pressure_constraint, "FemTest of new pressure constraint failed")
        analysis.addObject(pressure_constraint)

        fcc_print('Checking FEM new mesh...')
        from .testfiles.ccx.cube_mesh import create_nodes_cube
        from .testfiles.ccx.cube_mesh import create_elements_cube
        mesh = Fem.FemMesh()
        ret = create_nodes_cube(mesh)
        self.assertTrue(ret, "Import of mesh nodes failed")
        ret = create_elements_cube(mesh)
        self.assertTrue(ret, "Import of mesh volumes failed")
        mesh_object = self.active_doc.addObject('Fem::FemMeshObject', mesh_name)
        mesh_object.FemMesh = mesh
        self.assertTrue(mesh, "FemTest of new mesh failed")
        analysis.addObject(mesh_object)

        self.active_doc.recompute()

        fea = ccxtools.FemToolsCcx(analysis, solver_object, test_mode=True)
        fcc_print('Setting up working directory {}'.format(static_analysis_dir))
        fea.setup_working_dir(static_analysis_dir)
        self.assertTrue(True if fea.working_dir == static_analysis_dir else False,
                        "Setting working directory {} failed".format(static_analysis_dir))

        fcc_print('Checking FEM inp file prerequisites for static analysis...')
        error = fea.check_prerequisites()
        self.assertFalse(error, "ccxtools check_prerequisites returned error message: {}".format(error))

        fcc_print('Checking FEM inp file write...')

        fcc_print('Setting analysis type to \'static\"')
        fea.set_analysis_type("static")
        self.assertTrue(True if fea.analysis_type == 'static' else False, "Setting analysis type to \'static\' failed")

        fcc_print('Writing {}/{}.inp for static analysis'.format(static_analysis_dir, mesh_name))
        error = fea.write_inp_file()
        self.assertFalse(error, "Writing failed")

        fcc_print('Comparing {} to {}/{}.inp'.format(static_analysis_inp_file, static_analysis_dir, mesh_name))
        ret = compare_inp_files(static_analysis_inp_file, static_analysis_dir + mesh_name + '.inp')
        self.assertFalse(ret, "ccxtools write_inp_file test failed.\n{}".format(ret))

        fcc_print('Setting up working directory to {} in order to read simulated calculations'.format(test_file_dir))
        fea.setup_working_dir(test_file_dir)
        self.assertTrue(True if fea.working_dir == test_file_dir else False,
                        "Setting working directory {} failed".format(test_file_dir))

        fcc_print('Setting base name to read test {}.frd file...'.format('cube_static'))
        fea.set_base_name(static_base_name)
        self.assertTrue(True if fea.base_name == static_base_name else False,
                        "Setting base name to {} failed".format(static_base_name))

        fcc_print('Setting inp file name to read test {}.frd file...'.format('cube_static'))
        fea.set_inp_file_name()
        self.assertTrue(True if fea.inp_file_name == static_analysis_inp_file else False,
                        "Setting inp file name to {} failed".format(static_analysis_inp_file))

        fcc_print('Checking FEM frd file read from static analysis...')
        fea.load_results()
        self.assertTrue(fea.results_present, "Cannot read results from {}.frd frd file".format(fea.base_name))

        fcc_print('Reading stats from result object for static analysis...')
        ret = compare_stats(fea, static_expected_values, 'CalculiX_static_results')
        self.assertFalse(ret, "Invalid results read from .frd file")

        fcc_print('Save FreeCAD file for static analysis to {}...'.format(static_save_fc_file))
        self.active_doc.saveAs(static_save_fc_file)

        # frequency
        fcc_print('Reset Statik analysis')
        fea.reset_all()
        fcc_print('Setting analysis type to \'frequency\"')
        fea.set_analysis_type("frequency")
        self.assertTrue(True if fea.analysis_type == 'frequency' else False, "Setting analysis type to \'frequency\' failed")

        fcc_print('Setting up working directory to {} in order to write frequency calculations'.format(frequency_analysis_dir))
        fea.setup_working_dir(frequency_analysis_dir)
        self.assertTrue(True if fea.working_dir == frequency_analysis_dir else False,
                        "Setting working directory {} failed".format(frequency_analysis_dir))

        fcc_print('Checking FEM inp file prerequisites for frequency analysis...')
        error = fea.check_prerequisites()
        self.assertFalse(error, "ccxtools check_prerequisites returned error message: {}".format(error))

        fcc_print('Writing {}/{}.inp for frequency analysis'.format(frequency_analysis_dir, mesh_name))
        error = fea.write_inp_file()
        self.assertFalse(error, "Writing failed")

        fcc_print('Comparing {} to {}/{}.inp'.format(frequency_analysis_inp_file, frequency_analysis_dir, mesh_name))
        ret = compare_inp_files(frequency_analysis_inp_file, frequency_analysis_dir + mesh_name + '.inp')
        self.assertFalse(ret, "ccxtools write_inp_file test failed.\n{}".format(ret))

        fcc_print('Setting up working directory to {} in order to read simulated calculations'.format(test_file_dir))
        fea.setup_working_dir(test_file_dir)
        self.assertTrue(True if fea.working_dir == test_file_dir else False,
                        "Setting working directory {} failed".format(test_file_dir))

        fcc_print('Setting base name to read test {}.frd file...'.format(frequency_base_name))
        fea.set_base_name(frequency_base_name)
        self.assertTrue(True if fea.base_name == frequency_base_name else False,
                        "Setting base name to {} failed".format(frequency_base_name))

        fcc_print('Setting inp file name to read test {}.frd file...'.format('cube_frequency'))
        fea.set_inp_file_name()
        self.assertTrue(True if fea.inp_file_name == frequency_analysis_inp_file else False,
                        "Setting inp file name to {} failed".format(frequency_analysis_inp_file))

        fcc_print('Checking FEM frd file read from frequency analysis...')
        fea.load_results()
        self.assertTrue(fea.results_present, "Cannot read results from {}.frd frd file".format(fea.base_name))

        fcc_print('Reading stats from result object for frequency analysis...')
        ret = compare_stats(fea, frequency_expected_values, 'CalculiX_frequency_mode_1_results')
        self.assertFalse(ret, "Invalid results read from .frd file")

        fcc_print('Save FreeCAD file for frequency analysis to {}...'.format(frequency_save_fc_file))
        self.active_doc.saveAs(frequency_save_fc_file)
        fcc_print('--------------- End of FEM tests static and frequency analysis ---------------')

    def test_thermomech_analysis(self):
        fcc_print('--------------- Start of FEM tests ---------------')
        box = self.active_doc.addObject("Part::Box", "Box")
        box.Height = 25.4
        box.Width = 25.4
        box.Length = 203.2
        fcc_print('Checking FEM new analysis...')
        analysis = ObjectsFem.makeAnalysis(self.active_doc, 'Analysis')
        self.assertTrue(analysis, "FemTest of new analysis failed")

        fcc_print('Checking FEM new solver...')
        solver_object = ObjectsFem.makeSolverCalculixCcxTools(self.active_doc, 'CalculiX')
        solver_object.AnalysisType = 'thermomech'
        solver_object.GeometricalNonlinearity = 'linear'
        solver_object.ThermoMechSteadyState = True
        solver_object.MatrixSolverType = 'default'
        solver_object.IterationsThermoMechMaximum = 2000
        solver_object.IterationsControlParameterTimeUse = True
        self.assertTrue(solver_object, "FemTest of new solver failed")
        analysis.addObject(solver_object)

        fcc_print('Checking FEM new material...')
        material_object = ObjectsFem.makeMaterialSolid(self.active_doc, 'MechanicalMaterial')
        mat = material_object.Material
        mat['Name'] = "Steel-Generic"
        mat['YoungsModulus'] = "200000 MPa"
        mat['PoissonRatio'] = "0.30"
        mat['Density'] = "7900 kg/m^3"
        mat['ThermalConductivity'] = "43.27 W/m/K"  # SvdW: Change to Ansys model values
        mat['ThermalExpansionCoefficient'] = "12 um/m/K"
        mat['SpecificHeat'] = "500 J/kg/K"  # SvdW: Change to Ansys model values
        material_object.Material = mat
        self.assertTrue(material_object, "FemTest of new material failed")
        analysis.addObject(material_object)

        fcc_print('Checking FEM new fixed constraint...')
        fixed_constraint = self.active_doc.addObject("Fem::ConstraintFixed", "FemConstraintFixed")
        fixed_constraint.References = [(box, "Face1")]
        self.assertTrue(fixed_constraint, "FemTest of new fixed constraint failed")
        analysis.addObject(fixed_constraint)

        fcc_print('Checking FEM new initial temperature constraint...')
        initialtemperature_constraint = self.active_doc.addObject("Fem::ConstraintInitialTemperature", "FemConstraintInitialTemperature")
        initialtemperature_constraint.initialTemperature = 300.0
        self.assertTrue(initialtemperature_constraint, "FemTest of new initial temperature constraint failed")
        analysis.addObject(initialtemperature_constraint)

        fcc_print('Checking FEM new temperature constraint...')
        temperature_constraint = self.active_doc.addObject("Fem::ConstraintTemperature", "FemConstraintTemperature")
        temperature_constraint.References = [(box, "Face1")]
        temperature_constraint.Temperature = 310.93
        self.assertTrue(temperature_constraint, "FemTest of new temperature constraint failed")
        analysis.addObject(temperature_constraint)

        fcc_print('Checking FEM new heatflux constraint...')
        heatflux_constraint = self.active_doc.addObject("Fem::ConstraintHeatflux", "FemConstraintHeatflux")
        heatflux_constraint.References = [(box, "Face3"), (box, "Face4"), (box, "Face5"), (box, "Face6")]
        heatflux_constraint.AmbientTemp = 255.3722
        heatflux_constraint.FilmCoef = 5.678
        self.assertTrue(heatflux_constraint, "FemTest of new heatflux constraint failed")
        analysis.addObject(heatflux_constraint)

        fcc_print('Checking FEM new mesh...')
        from .testfiles.ccx.spine_mesh import create_nodes_spine
        from .testfiles.ccx.spine_mesh import create_elements_spine
        mesh = Fem.FemMesh()
        ret = create_nodes_spine(mesh)
        self.assertTrue(ret, "Import of mesh nodes failed")
        ret = create_elements_spine(mesh)
        self.assertTrue(ret, "Import of mesh volumes failed")
        mesh_object = self.active_doc.addObject('Fem::FemMeshObject', mesh_name)
        mesh_object.FemMesh = mesh
        self.assertTrue(mesh, "FemTest of new mesh failed")
        analysis.addObject(mesh_object)

        self.active_doc.recompute()

        fea = ccxtools.FemToolsCcx(analysis, test_mode=True)
        fcc_print('Setting up working directory {}'.format(thermomech_analysis_dir))
        fea.setup_working_dir(thermomech_analysis_dir)
        self.assertTrue(True if fea.working_dir == thermomech_analysis_dir else False,
                        "Setting working directory {} failed".format(thermomech_analysis_dir))

        fcc_print('Setting analysis type to \'thermomech\"')
        fea.set_analysis_type("thermomech")
        self.assertTrue(True if fea.analysis_type == 'thermomech' else False, "Setting analysis type to \'thermomech\' failed")

        fcc_print('Checking FEM inp file prerequisites for thermo-mechanical analysis...')
        error = fea.check_prerequisites()
        self.assertFalse(error, "ccxtools check_prerequisites returned error message: {}".format(error))

        fcc_print('Checking FEM inp file write...')

        fcc_print('Writing {}/{}.inp for thermomech analysis'.format(thermomech_analysis_dir, mesh_name))
        error = fea.write_inp_file()
        self.assertFalse(error, "Writing failed")

        fcc_print('Comparing {} to {}/{}.inp'.format(thermomech_analysis_inp_file, thermomech_analysis_dir, mesh_name))
        ret = compare_inp_files(thermomech_analysis_inp_file, thermomech_analysis_dir + mesh_name + '.inp')
        self.assertFalse(ret, "ccxtools write_inp_file test failed.\n{}".format(ret))

        fcc_print('Setting up working directory to {} in order to read simulated calculations'.format(test_file_dir))
        fea.setup_working_dir(test_file_dir)
        self.assertTrue(True if fea.working_dir == test_file_dir else False,
                        "Setting working directory {} failed".format(test_file_dir))

        fcc_print('Setting base name to read test {}.frd file...'.format('spine_thermomech'))
        fea.set_base_name(thermomech_base_name)
        self.assertTrue(True if fea.base_name == thermomech_base_name else False,
                        "Setting base name to {} failed".format(thermomech_base_name))

        fcc_print('Setting inp file name to read test {}.frd file...'.format('spine_thermomech'))
        fea.set_inp_file_name()
        self.assertTrue(True if fea.inp_file_name == thermomech_analysis_inp_file else False,
                        "Setting inp file name to {} failed".format(thermomech_analysis_inp_file))

        fcc_print('Checking FEM frd file read from thermomech analysis...')
        fea.load_results()
        self.assertTrue(fea.results_present, "Cannot read results from {}.frd frd file".format(fea.base_name))

        fcc_print('Reading stats from result object for thermomech analysis...')
        ret = compare_stats(fea, thermomech_expected_values, 'CalculiX_thermomech_results')
        self.assertFalse(ret, "Invalid results read from .frd file")

        fcc_print('Save FreeCAD file for thermomech analysis to {}...'.format(thermomech_save_fc_file))
        self.active_doc.saveAs(thermomech_save_fc_file)

        fcc_print('--------------- End of FEM tests thermomech analysis ---------------')

    def test_Flow1D_thermomech_analysis(self):
        fcc_print('--------------- Start of 1D Flow FEM tests ---------------')
        import Draft
        p1 = FreeCAD.Vector(0, 0, 50)
        p2 = FreeCAD.Vector(0, 0, -50)
        p3 = FreeCAD.Vector(0, 0, -4300)
        p4 = FreeCAD.Vector(4950, 0, -4300)
        p5 = FreeCAD.Vector(5000, 0, -4300)
        p6 = FreeCAD.Vector(8535.53, 0, -7835.53)
        p7 = FreeCAD.Vector(8569.88, 0, -7870.88)
        p8 = FreeCAD.Vector(12105.41, 0, -11406.41)
        p9 = FreeCAD.Vector(12140.76, 0, -11441.76)
        p10 = FreeCAD.Vector(13908.53, 0, -13209.53)
        p11 = FreeCAD.Vector(13943.88, 0, -13244.88)
        p12 = FreeCAD.Vector(15046.97, 0, -14347.97)
        p13 = FreeCAD.Vector(15046.97, 0, -7947.97)
        p14 = FreeCAD.Vector(15046.97, 0, -7847.97)
        p15 = FreeCAD.Vector(0, 0, 0)
        p16 = FreeCAD.Vector(0, 0, -2175)
        p17 = FreeCAD.Vector(2475, 0, -4300)
        p18 = FreeCAD.Vector(4975, 0, -4300)
        p19 = FreeCAD.Vector(6767.765, 0, -6067.765)
        p20 = FreeCAD.Vector(8552.705, 0, -7853.205)
        p21 = FreeCAD.Vector(10337.645, 0, -9638.645)
        p22 = FreeCAD.Vector(12123.085, 0, -11424.085)
        p23 = FreeCAD.Vector(13024.645, 0, -12325.645)
        p24 = FreeCAD.Vector(13926.205, 0, -13227.205)
        p25 = FreeCAD.Vector(14495.425, 0, -13796.425)
        p26 = FreeCAD.Vector(15046.97, 0, -11147.97)
        p27 = FreeCAD.Vector(15046.97, 0, -7897.97)
        points = [p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26, p27]
        line = Draft.makeWire(points, closed=False, face=False, support=None)
        fcc_print('Checking FEM new analysis...')
        analysis = ObjectsFem.makeAnalysis(self.active_doc, 'Analysis')
        self.assertTrue(analysis, "FemTest of new analysis failed")

        fcc_print('Checking FEM new solver...')
        solver_object = ObjectsFem.makeSolverCalculixCcxTools(self.active_doc, 'CalculiX')
        solver_object.AnalysisType = 'thermomech'
        solver_object.GeometricalNonlinearity = 'linear'
        solver_object.ThermoMechSteadyState = True
        solver_object.MatrixSolverType = 'default'
        solver_object.IterationsThermoMechMaximum = 2000
        solver_object.IterationsControlParameterTimeUse = False
        self.assertTrue(solver_object, "FemTest of new solver failed")
        analysis.addObject(solver_object)

        fcc_print('Checking FEM new material...')
        material_object = ObjectsFem.makeMaterialFluid(self.active_doc, 'FluidMaterial')
        mat = material_object.Material
        mat['Name'] = "Water"
        mat['Density'] = "998 kg/m^3"
        mat['SpecificHeat'] = "4.182 J/kg/K"
        mat['DynamicViscosity'] = "1.003e-3 kg/m/s"
        mat['VolumetricThermalExpansionCoefficient'] = "2.07e-4 m/m/K"
        mat['ThermalConductivity'] = "0.591 W/m/K"
        material_object.Material = mat
        self.assertTrue(material_object, "FemTest of new material failed")
        analysis.addObject(material_object)

        fcc_print('Checking FEM Flow1D inlet constraint...')
        Flow1d_inlet = ObjectsFem.makeElementFluid1D(self.active_doc, "ElementFluid1D")
        Flow1d_inlet.SectionType = 'Liquid'
        Flow1d_inlet.LiquidSectionType = 'PIPE INLET'
        Flow1d_inlet.InletPressure = 0.1
        Flow1d_inlet.References = [(line, "Edge1")]
        self.assertTrue(Flow1d_inlet, "FemTest of new Flow1D inlet constraint failed")
        analysis.addObject(Flow1d_inlet)

        fcc_print('Checking FEM new Flow1D entrance constraint...')
        Flow1d_entrance = ObjectsFem.makeElementFluid1D(self.active_doc, "ElementFluid1D")
        Flow1d_entrance.SectionType = 'Liquid'
        Flow1d_entrance.LiquidSectionType = 'PIPE ENTRANCE'
        Flow1d_entrance.EntrancePipeArea = 31416.00
        Flow1d_entrance.EntranceArea = 25133.00
        Flow1d_entrance.References = [(line, "Edge2")]
        self.assertTrue(Flow1d_entrance, "FemTest of new Flow1D entrance constraint failed")
        analysis.addObject(Flow1d_entrance)

        fcc_print('Checking FEM new Flow1D manning constraint...')
        Flow1d_manning = ObjectsFem.makeElementFluid1D(self.active_doc, "ElementFluid1D")
        Flow1d_manning.SectionType = 'Liquid'
        Flow1d_manning.LiquidSectionType = 'PIPE MANNING'
        Flow1d_manning.ManningArea = 31416
        Flow1d_manning.ManningRadius = 50
        Flow1d_manning.ManningCoefficient = 0.002
        Flow1d_manning.References = [(line, "Edge3"), (line, "Edge5")]
        self.assertTrue(Flow1d_manning, "FemTest of new Flow1D manning constraint failed")
        analysis.addObject(Flow1d_manning)

        fcc_print('Checking FEM new Flow1D bend constraint...')
        Flow1d_bend = ObjectsFem.makeElementFluid1D(self.active_doc, "ElementFluid1D")
        Flow1d_bend.SectionType = 'Liquid'
        Flow1d_bend.LiquidSectionType = 'PIPE BEND'
        Flow1d_bend.BendPipeArea = 31416
        Flow1d_bend.BendRadiusDiameter = 1.5
        Flow1d_bend.BendAngle = 45
        Flow1d_bend.BendLossCoefficient = 0.4
        Flow1d_bend.References = [(line, "Edge4")]
        self.assertTrue(Flow1d_bend, "FemTest of new Flow1D bend constraint failed")
        analysis.addObject(Flow1d_bend)

        fcc_print('Checking FEM new Flow1D enlargement constraint...')
        Flow1d_enlargement = ObjectsFem.makeElementFluid1D(self.active_doc, "ElementFluid1D")
        Flow1d_enlargement.SectionType = 'Liquid'
        Flow1d_enlargement.LiquidSectionType = 'PIPE ENLARGEMENT'
        Flow1d_enlargement.EnlargeArea1 = 31416.00
        Flow1d_enlargement.EnlargeArea2 = 70686.00
        Flow1d_enlargement.References = [(line, "Edge6")]
        self.assertTrue(Flow1d_enlargement, "FemTest of new Flow1D enlargement constraint failed")
        analysis.addObject(Flow1d_enlargement)

        fcc_print('Checking FEM new Flow1D manning constraint...')
        Flow1d_manning1 = ObjectsFem.makeElementFluid1D(self.active_doc, "ElementFluid1D")
        Flow1d_manning1.SectionType = 'Liquid'
        Flow1d_manning1.LiquidSectionType = 'PIPE MANNING'
        Flow1d_manning1.ManningArea = 70686.00
        Flow1d_manning1.ManningRadius = 75
        Flow1d_manning1.ManningCoefficient = 0.002
        Flow1d_manning1.References = [(line, "Edge7")]
        self.assertTrue(Flow1d_manning1, "FemTest of new Flow1D manning constraint failed")
        analysis.addObject(Flow1d_manning1)

        fcc_print('Checking FEM new Flow1D contraction constraint...')
        Flow1d_contraction = ObjectsFem.makeElementFluid1D(self.active_doc, "ElementFluid1D")
        Flow1d_contraction.SectionType = 'Liquid'
        Flow1d_contraction.LiquidSectionType = 'PIPE CONTRACTION'
        Flow1d_contraction.ContractArea1 = 70686
        Flow1d_contraction.ContractArea2 = 17671
        Flow1d_contraction.References = [(line, "Edge8")]
        self.assertTrue(Flow1d_contraction, "FemTest of new Flow1D contraction constraint failed")
        analysis.addObject(Flow1d_contraction)

        fcc_print('Checking FEM new Flow1D manning constraint...')
        Flow1d_manning2 = ObjectsFem.makeElementFluid1D(self.active_doc, "ElementFluid1D")
        Flow1d_manning2.SectionType = 'Liquid'
        Flow1d_manning2.LiquidSectionType = 'PIPE MANNING'
        Flow1d_manning2.ManningArea = 17671.00
        Flow1d_manning2.ManningRadius = 37.5
        Flow1d_manning2.ManningCoefficient = 0.002
        Flow1d_manning2.References = [(line, "Edge11"), (line, "Edge9")]
        self.assertTrue(Flow1d_manning2, "FemTest of new Flow1D manning constraint failed")
        analysis.addObject(Flow1d_manning2)

        fcc_print('Checking FEM new Flow1D gate valve constraint...')
        Flow1d_gate_valve = ObjectsFem.makeElementFluid1D(self.active_doc, "ElementFluid1D")
        Flow1d_gate_valve.SectionType = 'Liquid'
        Flow1d_gate_valve.LiquidSectionType = 'PIPE GATE VALVE'
        Flow1d_gate_valve.GateValvePipeArea = 17671
        Flow1d_gate_valve.GateValveClosingCoeff = 0.5
        Flow1d_gate_valve.References = [(line, "Edge10")]
        self.assertTrue(Flow1d_gate_valve, "FemTest of new Flow1D gate valve constraint failed")
        analysis.addObject(Flow1d_gate_valve)

        fcc_print('Checking FEM new Flow1D enlargement constraint...')
        Flow1d_enlargement1 = ObjectsFem.makeElementFluid1D(self.active_doc, "ElementFluid1D")
        Flow1d_enlargement1.SectionType = 'Liquid'
        Flow1d_enlargement1.LiquidSectionType = 'PIPE ENLARGEMENT'
        Flow1d_enlargement1.EnlargeArea1 = 17671
        Flow1d_enlargement1.EnlargeArea2 = 1e12
        Flow1d_enlargement1.References = [(line, "Edge12")]
        self.assertTrue(Flow1d_enlargement1, "FemTest of new Flow1D enlargement constraint failed")
        analysis.addObject(Flow1d_enlargement1)

        fcc_print('Checking FEM Flow1D outlet constraint...')
        Flow1d_outlet = ObjectsFem.makeElementFluid1D(self.active_doc, "ElementFluid1D")
        Flow1d_outlet.SectionType = 'Liquid'
        Flow1d_outlet.LiquidSectionType = 'PIPE OUTLET'
        Flow1d_outlet.OutletPressure = 0.1
        Flow1d_outlet.References = [(line, "Edge13")]
        self.assertTrue(Flow1d_outlet, "FemTest of new Flow1D inlet constraint failed")
        analysis.addObject(Flow1d_outlet)

        fcc_print('Checking FEM self weight constraint...')
        Flow1d_self_weight = ObjectsFem.makeConstraintSelfWeight(self.active_doc, "ConstraintSelfWeight")
        Flow1d_self_weight.Gravity_x = 0.0
        Flow1d_self_weight.Gravity_y = 0.0
        Flow1d_self_weight.Gravity_z = -1.0
        self.assertTrue(Flow1d_outlet, "FemTest of new Flow1D self weight constraint failed")
        analysis.addObject(Flow1d_self_weight)

        fcc_print('Checking FEM new mesh...')
        from .testfiles.ccx.Flow1D_mesh import create_nodes_Flow1D
        from .testfiles.ccx.Flow1D_mesh import create_elements_Flow1D
        mesh = Fem.FemMesh()
        ret = create_nodes_Flow1D(mesh)
        self.assertTrue(ret, "Import of mesh nodes failed")
        ret = create_elements_Flow1D(mesh)
        self.assertTrue(ret, "Import of mesh volumes failed")
        mesh_object = self.active_doc.addObject('Fem::FemMeshObject', mesh_name)
        mesh_object.FemMesh = mesh
        self.assertTrue(mesh, "FemTest of new mesh failed")
        analysis.addObject(mesh_object)

        self.active_doc.recompute()

        fea = ccxtools.FemToolsCcx(analysis, test_mode=True)
        fcc_print('Setting up working directory {}'.format(Flow1D_thermomech_analysis_dir))
        fea.setup_working_dir(Flow1D_thermomech_analysis_dir)
        self.assertTrue(True if fea.working_dir == Flow1D_thermomech_analysis_dir else False,
                        "Setting working directory {} failed".format(Flow1D_thermomech_analysis_dir))

        fcc_print('Setting analysis type to \'thermomech\"')
        fea.set_analysis_type("thermomech")
        self.assertTrue(True if fea.analysis_type == 'thermomech' else False, "Setting analysis type to \'thermomech\' failed")

        fcc_print('Checking FEM inp file prerequisites for thermo-mechanical analysis...')
        error = fea.check_prerequisites()
        self.assertFalse(error, "ccxtools check_prerequisites returned error message: {}".format(error))

        fcc_print('Checking FEM inp file write...')

        fcc_print('Writing {}/{}.inp for thermomech analysis'.format(Flow1D_thermomech_analysis_dir, mesh_name))
        error = fea.write_inp_file()
        self.assertFalse(error, "Writing failed")

        fcc_print('Comparing {} to {}/{}.inp'.format(Flow1D_thermomech_analysis_inp_file, Flow1D_thermomech_analysis_dir, mesh_name))
        ret = compare_inp_files(Flow1D_thermomech_analysis_inp_file, Flow1D_thermomech_analysis_dir + mesh_name + '.inp')
        self.assertFalse(ret, "ccxtools write_inp_file test failed.\n{}".format(ret))

        fcc_print('Setting up working directory to {} in order to read simulated calculations'.format(test_file_dir))
        fea.setup_working_dir(test_file_dir)
        self.assertTrue(True if fea.working_dir == test_file_dir else False,
                        "Setting working directory {} failed".format(test_file_dir))

        fcc_print('Setting base name to read test {}.frd file...'.format('Flow1D_thermomech'))
        fea.set_base_name(Flow1D_thermomech_base_name)
        self.assertTrue(True if fea.base_name == Flow1D_thermomech_base_name else False,
                        "Setting base name to {} failed".format(Flow1D_thermomech_base_name))

        fcc_print('Setting inp file name to read test {}.frd file...'.format('Flow1D_thermomech'))
        fea.set_inp_file_name()
        self.assertTrue(True if fea.inp_file_name == Flow1D_thermomech_analysis_inp_file else False,
                        "Setting inp file name to {} failed".format(Flow1D_thermomech_analysis_inp_file))

        fcc_print('Checking FEM frd file read from Flow1D thermomech analysis...')
        fea.load_results()
        self.assertTrue(fea.results_present, "Cannot read results from {}.frd frd file".format(fea.base_name))

        fcc_print('Reading stats from result object for Flow1D thermomech analysis...')
        ret = compare_stats(fea, Flow1D_thermomech_expected_values, stat_types, 'CalculiX_thermomech_time_1_0_results')
        self.assertFalse(ret, "Invalid results read from .frd file")

        fcc_print('Save FreeCAD file for thermomech analysis to {}...'.format(Flow1D_thermomech_save_fc_file))
        self.active_doc.saveAs(Flow1D_thermomech_save_fc_file)

        fcc_print('--------------- End of FEM tests FLow 1D thermomech analysis ---------------')

    def tearDown(self):
        FreeCAD.closeDocument("FemTest")
        pass


class SolverFrameWorkTest(unittest.TestCase):

    def setUp(self):
        try:
            FreeCAD.setActiveDocument("FemTest")
        except:
            FreeCAD.newDocument("FemTest")
        finally:
            FreeCAD.setActiveDocument("FemTest")
        self.active_doc = FreeCAD.ActiveDocument

    def test_solver_framework(self):
        fcc_print('--------------- Start of FEM tests  solver frame work ---------------')
        box = self.active_doc.addObject("Part::Box", "Box")
        fcc_print('Checking FEM new analysis...')
        analysis = ObjectsFem.makeAnalysis(self.active_doc, 'Analysis')
        self.assertTrue(analysis, "FemTest of new analysis failed")

        fcc_print('Checking FEM new material...')
        material_object = ObjectsFem.makeMaterialSolid(self.active_doc, 'MechanicalMaterial')
        mat = material_object.Material
        mat['Name'] = "Steel-Generic"
        mat['YoungsModulus'] = "200000 MPa"
        mat['PoissonRatio'] = "0.30"
        mat['Density'] = "7900 kg/m^3"
        material_object.Material = mat
        self.assertTrue(material_object, "FemTest of new material failed")
        analysis.addObject(material_object)

        fcc_print('Checking FEM new fixed constraint...')
        fixed_constraint = self.active_doc.addObject("Fem::ConstraintFixed", "FemConstraintFixed")
        fixed_constraint.References = [(box, "Face1")]
        self.assertTrue(fixed_constraint, "FemTest of new fixed constraint failed")
        analysis.addObject(fixed_constraint)

        fcc_print('Checking FEM new force constraint...')
        force_constraint = self.active_doc.addObject("Fem::ConstraintForce", "FemConstraintForce")
        force_constraint.References = [(box, "Face6")]
        force_constraint.Force = 40000.0
        force_constraint.Direction = (box, ["Edge5"])
        self.active_doc.recompute()
        force_constraint.Reversed = True
        self.active_doc.recompute()
        self.assertTrue(force_constraint, "FemTest of new force constraint failed")
        analysis.addObject(force_constraint)

        fcc_print('Checking FEM new pressure constraint...')
        pressure_constraint = self.active_doc.addObject("Fem::ConstraintPressure", "FemConstraintPressure")
        pressure_constraint.References = [(box, "Face2")]
        pressure_constraint.Pressure = 1000.0
        pressure_constraint.Reversed = False
        self.assertTrue(pressure_constraint, "FemTest of new pressure constraint failed")
        analysis.addObject(pressure_constraint)

        fcc_print('Checking FEM new mesh...')
        from .testfiles.ccx.cube_mesh import create_nodes_cube
        from .testfiles.ccx.cube_mesh import create_elements_cube
        mesh = Fem.FemMesh()
        ret = create_nodes_cube(mesh)
        self.assertTrue(ret, "Import of mesh nodes failed")
        ret = create_elements_cube(mesh)
        self.assertTrue(ret, "Import of mesh volumes failed")
        mesh_object = self.active_doc.addObject('Fem::FemMeshObject', mesh_name)
        mesh_object.FemMesh = mesh
        self.assertTrue(mesh, "FemTest of new mesh failed")
        analysis.addObject(mesh_object)

        self.active_doc.recompute()

        # solver frame work ccx solver
        fcc_print('Checking FEM solver for solver frame work...')
        solver_ccx2_object = ObjectsFem.makeSolverCalculix(self.active_doc, 'SolverCalculiX')
        solver_ccx2_object.GeometricalNonlinearity = 'linear'
        solver_ccx2_object.ThermoMechSteadyState = False
        solver_ccx2_object.MatrixSolverType = 'default'
        solver_ccx2_object.IterationsControlParameterTimeUse = False
        solver_ccx2_object.EigenmodesCount = 10
        solver_ccx2_object.EigenmodeHighLimit = 1000000.0
        solver_ccx2_object.EigenmodeLowLimit = 0.0
        self.assertTrue(solver_ccx2_object, "FemTest of new ccx solver failed")
        analysis.addObject(solver_ccx2_object)

        fcc_print('Checking inpfile writing for solverframework_save_fc_file frame work...')
        if not os.path.exists(solverframework_analysis_dir):  # solver frameworkd does explicit not create a non existing directory
            os.makedirs(solverframework_analysis_dir)

        fcc_print('machine_ccx')
        machine_ccx = solver_ccx2_object.Proxy.createMachine(solver_ccx2_object, solverframework_analysis_dir)
        fcc_print('Machine testmode: ' + str(machine_ccx.testmode))
        machine_ccx.target = femsolver.run.PREPARE
        machine_ccx.start()
        machine_ccx.join()  # wait for the machine to finish.
        fcc_print('Comparing {} to {}/{}.inp'.format(static_analysis_inp_file, solverframework_analysis_dir, mesh_name))
        ret = compare_inp_files(static_analysis_inp_file, solverframework_analysis_dir + mesh_name + '.inp')
        self.assertFalse(ret, "ccxtools write_inp_file test failed.\n{}".format(ret))

        # use solver frame work elmer solver
        solver_elmer_object = ObjectsFem.makeSolverElmer(self.active_doc, 'SolverElmer')
        self.assertTrue(solver_elmer_object, "FemTest of elmer solver failed")
        analysis.addObject(solver_elmer_object)
        solver_elmer_eqobj = ObjectsFem.makeEquationElasticity(self.active_doc, solver_elmer_object)
        self.assertTrue(solver_elmer_eqobj, "FemTest of elmer elasticity equation failed")

        # set ThermalExpansionCoefficient, current elmer seems to need it even on simple elasticity analysis
        mat = material_object.Material
        mat['ThermalExpansionCoefficient'] = "0 um/m/K"  # FIXME elmer elasticity needs the dictionary key, otherwise it fails
        material_object.Material = mat

        mesh_gmsh = ObjectsFem.makeMeshGmsh(self.active_doc)
        mesh_gmsh.CharacteristicLengthMin = "9 mm"
        mesh_gmsh.FemMesh = mesh_object.FemMesh  # elmer needs a GMHS mesh object, FIXME error message on Python solver run
        mesh_gmsh.Part = box
        analysis.addObject(mesh_gmsh)
        self.active_doc.removeObject(mesh_object.Name)

        fcc_print('machine_elmer')
        machine_elmer = solver_elmer_object.Proxy.createMachine(solver_elmer_object, solverframework_analysis_dir, True)
        fcc_print('Machine testmode: ' + str(machine_elmer.testmode))
        machine_elmer.target = femsolver.run.PREPARE
        machine_elmer.start()
        machine_elmer.join()  # wait for the machine to finish.

        '''
        fcc_print('Test writing STARTINFO file')
        fcc_print('Comparing {} to {}'.format(test_file_dir_elmer + 'ELMERSOLVER_STARTINFO', solverframework_analysis_dir + 'ELMERSOLVER_STARTINFO'))
        ret = compare_files(test_file_dir_elmer + 'ELMERSOLVER_STARTINFO', solverframework_analysis_dir + 'ELMERSOLVER_STARTINFO')
        self.assertFalse(ret, "STARTINFO write file test failed.\n{}".format(ret))

        fcc_print('Test writing case file')
        fcc_print('Comparing {} to {}'.format(test_file_dir_elmer + 'case.sif', solverframework_analysis_dir + 'case.sif'))
        ret = compare_files(test_file_dir_elmer + 'case.sif', solverframework_analysis_dir + 'case.sif')
        self.assertFalse(ret, "case write file test failed.\n{}".format(ret))

        fcc_print('Test writing GMSH geo file')
        fcc_print('Comparing {} to {}'.format(test_file_dir_elmer + 'group_mesh.geo', solverframework_analysis_dir + 'group_mesh.geo'))
        ret = compare_files(test_file_dir_elmer + 'group_mesh.geo', solverframework_analysis_dir + 'group_mesh.geo')
        self.assertFalse(ret, "GMSH geo write file test failed.\n{}".format(ret))
        '''

        fcc_print('Save FreeCAD file for static2 analysis to {}...'.format(solverframework_save_fc_file))
        self.active_doc.saveAs(solverframework_save_fc_file)
        fcc_print('--------------- End of FEM tests solver frame work ---------------')

    def tearDown(self):
        FreeCAD.closeDocument("FemTest")
        pass


# helpers
def fcc_print(message):
    FreeCAD.Console.PrintMessage('{} \n'.format(message))


def get_defmake_count():
    '''
    count the def make in module ObjectsFem
    could also be done in bash with
    grep -c  "def make" src/Mod/Fem/ObjectsFem.py
    '''
    name_modfile = home_path + 'Mod/Fem/ObjectsFem.py'
    modfile = open(name_modfile, 'r')
    lines_modefile = modfile.readlines()
    modfile.close()
    lines_defmake = [l for l in lines_modefile if l.startswith('def make')]
    return len(lines_defmake)


def compare_inp_files(file_name1, file_name2):
    file1 = open(file_name1, 'r')
    f1 = file1.readlines()
    file1.close()
    # l.startswith('17671.0,1') is a temporary workaround for python3 problem with 1DFlow input
    # TODO as soon as the 1DFlow result reading is fixed, this should be triggered in the 1DFlow unit test
    lf1 = [l for l in f1 if not (l.startswith('**   written ') or l.startswith('**   file ') or l.startswith('17671.0,1'))]
    lf1 = force_unix_line_ends(lf1)
    file2 = open(file_name2, 'r')
    f2 = file2.readlines()
    file2.close()
    # TODO see comment on file1
    lf2 = [l for l in f2 if not (l.startswith('**   written ') or l.startswith('**   file ') or l.startswith('17671.0,1'))]
    lf2 = force_unix_line_ends(lf2)
    import difflib
    diff = difflib.unified_diff(lf1, lf2, n=0)
    result = ''
    for l in diff:
        result += l
    if result:
        result = "Comparing {} to {} failed!\n".format(file_name1, file_name2) + result
    return result


def compare_files(file_name1, file_name2):
    file1 = open(file_name1, 'r')
    f1 = file1.readlines()
    file1.close()
    # workaraound for compare geos of elmer test and temporary file path (not only names change, path changes with operating system)
    lf1 = [l for l in f1 if not (l.startswith('Merge "') or l.startswith('Save "') or l.startswith('// '))]
    lf1 = force_unix_line_ends(lf1)
    file2 = open(file_name2, 'r')
    f2 = file2.readlines()
    file2.close()
    lf2 = [l for l in f2 if not (l.startswith('Merge "') or l.startswith('Save "') or l.startswith('// '))]
    lf2 = force_unix_line_ends(lf2)
    import difflib
    diff = difflib.unified_diff(lf1, lf2, n=0)
    result = ''
    for l in diff:
        result += l
    if result:
        result = "Comparing {} to {} failed!\n".format(file_name1, file_name2) + result
    return result


def compare_stats(fea, stat_file=None, loc_stat_types=None, res_obj_name=None):
    if not loc_stat_types:
        loc_stat_types = stat_types
    if stat_file:
        sf = open(stat_file, 'r')
        sf_content = []
        for l in sf.readlines():
            for st in loc_stat_types:
                if l.startswith(st):
                    sf_content.append(l)
        sf.close()
        sf_content = force_unix_line_ends(sf_content)
    stats = []
    for s in loc_stat_types:
        if res_obj_name:
            statval = resulttools.get_stats(FreeCAD.ActiveDocument.getObject(res_obj_name), s)
        else:
            print('No result object name given')
            return False
        stats.append("{0}: ({1:.14g}, {2:.14g}, {3:.14g})\n".format(s, statval[0], statval[1], statval[2]))
    if sf_content != stats:
        fcc_print("Expected stats from {}".format(stat_file))
        fcc_print(sf_content)
        fcc_print("Stats read from {}.frd file".format(fea.base_name))
        fcc_print(stats)
        return True
    return False


def force_unix_line_ends(line_list):
    new_line_list = []
    for l in line_list:
        if l.endswith("\r\n"):
            l = l[:-2] + '\n'
        new_line_list.append(l)
    return new_line_list


def collect_python_modules(femsubdir=None):
    if not femsubdir:
        pydir = FreeCAD.ConfigGet("AppHomePath") + 'Mod/Fem/'
    else:
        pydir = FreeCAD.ConfigGet("AppHomePath") + 'Mod/Fem/' + femsubdir + '/'
    collected_modules = []
    fcc_print(pydir)
    for pyfile in sorted(os.listdir(pydir)):
        if pyfile.endswith(".py") and not pyfile.startswith('Init'):
            if not femsubdir:
                collected_modules.append(os.path.splitext(os.path.basename(pyfile))[0])
            else:
                collected_modules.append(femsubdir.replace('/', '.') + '.' + os.path.splitext(os.path.basename(pyfile))[0])
    return collected_modules


def runTestFem():
    '''run FEM unit test
    for more information on how to run a specific test class or a test def see comment at file end
    '''
    import Test
    import sys
    current_module = sys.modules[__name__]
    Test.runTestsFromModule(current_module)


def create_test_results():
    print("run FEM unit tests")
    runTestFem()

    import shutil
    import FemGui

    # static and frequency cube
    FreeCAD.open(static_save_fc_file)
    FemGui.setActiveAnalysis(FreeCAD.ActiveDocument.Analysis)
    fea = ccxtools.FemToolsCcx()

    print("create static result files")
    fea.reset_all()
    fea.run()
    fea.load_results()
    stats_static = []
    for s in stat_types:
        statval = resulttools.get_stats(FreeCAD.ActiveDocument.getObject('CalculiX_static_results'), s)
        stats_static.append("{0}: ({1:.14g}, {2:.14g}, {3:.14g})\n".format(s, statval[0], statval[1], statval[2]))
    static_expected_values_file = static_analysis_dir + 'cube_static_expected_values'
    f = open(static_expected_values_file, 'w')
    for s in stats_static:
        f.write(s)
    f.close()
    frd_result_file = os.path.splitext(fea.inp_file_name)[0] + '.frd'
    dat_result_file = os.path.splitext(fea.inp_file_name)[0] + '.dat'
    frd_static_test_result_file = static_analysis_dir + 'cube_static.frd'
    dat_static_test_result_file = static_analysis_dir + 'cube_static.dat'
    shutil.copyfile(frd_result_file, frd_static_test_result_file)
    shutil.copyfile(dat_result_file, dat_static_test_result_file)

    print("create frequency result files")
    fea.reset_all()
    fea.set_analysis_type('frequency')
    fea.solver.EigenmodesCount = 1  # we should only have one result object
    fea.run()
    fea.load_results()
    stats_frequency = []
    for s in stat_types:
        statval = resulttools.get_stats(FreeCAD.ActiveDocument.getObject('CalculiX_static_mode_1_results'), s)  # FIXME for some reason result obj name has static
        stats_frequency.append("{0}: ({1:.14g}, {2:.14g}, {3:.14g})\n".format(s, statval[0], statval[1], statval[2]))
    frequency_expected_values_file = frequency_analysis_dir + 'cube_frequency_expected_values'
    f = open(frequency_expected_values_file, 'w')
    for s in stats_frequency:
        f.write(s)
    f.close()
    frd_frequency_test_result_file = frequency_analysis_dir + 'cube_frequency.frd'
    dat_frequency_test_result_file = frequency_analysis_dir + 'cube_frequency.dat'
    shutil.copyfile(frd_result_file, frd_frequency_test_result_file)
    shutil.copyfile(dat_result_file, dat_frequency_test_result_file)

    print("create thermomech result files")
    FreeCAD.open(thermomech_save_fc_file)
    FemGui.setActiveAnalysis(FreeCAD.ActiveDocument.Analysis)
    fea = ccxtools.FemToolsCcx()
    fea.reset_all()
    fea.run()
    fea.load_results()
    stats_thermomech = []
    for s in stat_types:
        statval = resulttools.get_stats(FreeCAD.ActiveDocument.getObject('CalculiX_thermomech_results'), s)
        stats_thermomech.append("{0}: ({1:.14g}, {2:.14g}, {3:.14g})\n".format(s, statval[0], statval[1], statval[2]))
    thermomech_expected_values_file = thermomech_analysis_dir + 'spine_thermomech_expected_values'
    f = open(thermomech_expected_values_file, 'w')
    for s in stats_thermomech:
        f.write(s)
    f.close()
    frd_result_file = os.path.splitext(fea.inp_file_name)[0] + '.frd'
    dat_result_file = os.path.splitext(fea.inp_file_name)[0] + '.dat'
    frd_thermomech_test_result_file = thermomech_analysis_dir + 'spine_thermomech.frd'
    dat_thermomech_test_result_file = thermomech_analysis_dir + 'spine_thermomech.dat'
    shutil.copyfile(frd_result_file, frd_thermomech_test_result_file)
    shutil.copyfile(dat_result_file, dat_thermomech_test_result_file)
    print('Results copied to the appropriate FEM test dirs in: ' + temp_dir)

    print("create Flow1D result files")
    FreeCAD.open(Flow1D_thermomech_save_fc_file)
    FemGui.setActiveAnalysis(FreeCAD.ActiveDocument.Analysis)
    fea = ccxtools.FemToolsCcx()
    fea.reset_all()
    fea.run()
    fea.load_results()
    stats_flow1D = []
    for s in stat_types:
        statval = resulttools.get_stats(FreeCAD.ActiveDocument.getObject('CalculiX_thermomech_time_1_0_results'), s)
        stats_flow1D.append("{0}: ({1:.14g}, {2:.14g}, {3:.14g})\n".format(s, statval[0], statval[1], statval[2]))
    Flow1D_thermomech_expected_values_file = Flow1D_thermomech_analysis_dir + 'Flow1D_thermomech_expected_values'
    f = open(Flow1D_thermomech_expected_values_file, 'w')
    for s in stats_flow1D:
        f.write(s)
    f.close()
    frd_result_file = os.path.splitext(fea.inp_file_name)[0] + '.frd'
    dat_result_file = os.path.splitext(fea.inp_file_name)[0] + '.dat'
    frd_Flow1D_thermomech_test_result_file = Flow1D_thermomech_analysis_dir + 'Flow1D_thermomech.frd'
    dat_Flow1D_thermomech_test_result_file = Flow1D_thermomech_analysis_dir + 'Flow1D_thermomech.dat'
    shutil.copyfile(frd_result_file, frd_Flow1D_thermomech_test_result_file)
    shutil.copyfile(dat_result_file, dat_Flow1D_thermomech_test_result_file)
    print('Flow1D thermomech results copied to the appropriate FEM test dirs in: ' + temp_dir)


'''
update the results of FEM unit tests:

import TestFem
TestFem.create_test_results()

copy result files from your_temp_directory/FEM_unittests/   test directories into the src directory
compare the results with git difftool
run make
start FreeCAD and run FEM unit test
if FEM unit test is fine --> commit new FEM unit test results

TODO compare the inp file of the helper with the inp file of FEM unit tests
TODO the better way: move the result creation inside the TestFem and add some preference to deactivate this because it needs ccx


for more information on how to run a specific test class or a test def see
file src/Mod/Test/__init__
https://forum.freecadweb.org/viewtopic.php?f=10&t=22190#p175546

import unittest
mytest = unittest.TestLoader().loadTestsFromName("TestFem.FemTest.test_pyimport_all_FEM_modules")
unittest.TextTestRunner().run(mytest)

'''
