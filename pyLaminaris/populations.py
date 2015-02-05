__author__ = 'mccolgan'
import neurons as _neurons
import numpy as np


class NMNeuronPopulation:
    def __init__(self, size=100, side='ipsi', record=True):
        self.side = side
        self.size = size
        self.x_offset = 4500.
        self.x_spread = 200.
        self.record = record
        self.neurons = [
            _neurons.NMNeuron(root_point=self.x_offset + self.x_spread * np.random.rand(), record=self.record) for n in
            range(size)]

    def set_stimulation(self, stimtype='mod_click', freq=4000.):
        #TODO: make this take more than a single stimtype
        import helper

        def mod_click(t):
            return (0.1
                    + 2.9 * np.exp(np.sin(4 * 2 * np.pi * t) - 1. - 16 * (t - 10) ** 2)
                    + 1.5 * np.exp(np.sin(4 * 2 * np.pi * t) - 1. - 16 * (t - 11) ** 2)
                    - 0.1 * np.exp(-16 * (t - 10.5) ** 2))

        def pulse(t):
            return (0.1
                    + 2.9 * np.exp(-16 * (t - 10.) ** 2))

        if stimtype == 'mod_click':
            fun = mod_click
        elif stimtype == 'pulse':
            fun = pulse
        else:
            raise NameError, "Unknown stimulation type"

        for n in self.neurons:
            n.set_spiketimes(helper.inhom_poisson(fun, 20., 0., 6.))

    def nodes_imem_loc(self):
        imem = []
        iloc = []
        for n in self.neurons:
            imem_n, iloc_n = n.nodes_imem_loc()
            imem.append(imem_n)
            iloc.append(iloc_n)
        imem = np.vstack(imem)
        iloc = np.vstack(iloc)
        if self.side == 'contra':
            iloc[:, 0] = 2 * (self.x_offset + self.x_spread) - iloc[:, 0]
        return imem, iloc