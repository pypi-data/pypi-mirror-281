import numpy as np
from plico.utils.logger import Logger
from plico.utils.decorator import override
from plico_interferometer_server.devices.abstract_interferometer import \
    AbstractInterferometer


class PhaseCam4030(AbstractInterferometer):
    '''
    4D Technology PhaseCam 4030
    '''

    def __init__(self,
                 ipaddr,
                 port=23,
                 timeout=2,
                 name='PhaseCam4030',
                 **_):
        self._name = name
        self.ipaddr = ipaddr
        self.port = port
        self.timeout = timeout
        self.logger = Logger.of('PhaseCam4030')

    @override
    def name(self):
        return self._name

    @override
    def wavefront(self, how_many=1):
        # TODO
        return np.ma.zeros((500, 500))

    @override
    def deinitialize(self):
        pass

    @override
    def acquire_burst(self, how_many=1):
        #TODO implement this
        return np.ma.zeros((500, 500))
    
    @override
    def load_burst(self, tn):
        raise Exception('To be implemented!')
    
    @override
    def delete_burst(self, tn):
        raise Exception('To be implemented!')
    
    @override
    def list_available_burst(self):
        raise Exception('To be implemented!')

