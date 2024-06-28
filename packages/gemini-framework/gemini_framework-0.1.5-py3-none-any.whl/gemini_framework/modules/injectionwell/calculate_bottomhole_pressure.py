from gemini_framework.abstract.unit_module_abstract import UnitModuleAbstract
from gemini_model.well.vertical_lift_curve import VLP
from gemini_model.fluid.pvt_water_stp import PVTConstantSTP
import numpy as np


class CalculateBottomholePressure(UnitModuleAbstract):

    def __init__(self, unit):
        super().__init__(unit)

        self.model = VLP()

        self.link_input('measured', 'injectionwell_flow')
        self.link_input('measured', 'injectionwell_wellhead_pressure')
        self.link_input('measured', 'injectionwell_wellhead_temperature')
        self.link_output('calculated', 'injectionwell_bottomhole_pressure')

    def step(self, loop):
        self.loop = loop
        self.loop.start_time = self.get_output_last_data_time('injectionwell_bottomhole_pressure')
        self.loop.compute_n_simulation()

        well_param = dict()
        well_traj = self.unit.parameters['injectionwell_trajectory_table']
        depth = []
        diameter = []
        angle = []
        for ii in range(1, len(well_traj)):
            MD = well_traj[ii]['MD'] - well_traj[ii - 1]['MD']
            TVD = well_traj[ii]['TVD'] - well_traj[ii - 1]['TVD']

            depth.append(MD)
            diameter.append(well_traj[ii]['ID'])
            angle.append(np.round(90 - np.arccos(TVD / MD) * 180 / np.pi, 2))

        well_param['diameter'] = np.array(diameter)  # well diameter in [m]
        well_param['depth'] = np.array(depth)  # well depth in [m]
        well_param['angle'] = np.array(angle)  # well angle in [degree]

        self.model.update_parameters(well_param)
        self.model.PVT = PVTConstantSTP()

        time, injectionwell_flow = self.get_input_data('injectionwell_flow')
        time, injectionwell_wellhead_pressure = self.get_input_data(
            'injectionwell_wellhead_pressure')
        time, injectionwell_wellhead_temperature = self.get_input_data(
            'injectionwell_wellhead_temperature')

        u = dict()
        injectionwell_bottomhole_pressure = []
        for ii in range(1, self.loop.n_step):
            try:
                u['mass_flowrate'] = injectionwell_flow[ii]
                u['pressure_input'] = injectionwell_wellhead_pressure[ii]
                u['temperature_input'] = injectionwell_wellhead_temperature[ii]
                u['direction'] = 'down'
                u['temperature_ambient'] = float(
                    self.unit.parameters['injectionwell_soil_temperature'])

                x = []
                self.model.calculate_output(u, x)

                y = self.model.get_output()

                injectionwell_bottomhole_pressure.append(y['pressure_output'])
            except Exception as e:
                print("ERROR:" + repr(e))
                injectionwell_bottomhole_pressure.append(None)

        if injectionwell_bottomhole_pressure:
            self.write_output_data('injectionwell_bottomhole_pressure', time,
                                   injectionwell_bottomhole_pressure)
