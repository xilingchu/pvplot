from abc import ABC, abstractmethod

class pvScript(ABC):
    '''
    Basic Paraview Script:
    A paraview script can be divided into four parts: import, filter, render, and output.
    '''
    def __init__(self):
        pass

    @abstractmethod
    def _import(self):
        pass
        
    @abstractmethod
    def _filter(self):
        pass

    @abstractmethod
    def _render(self):
        pass
        
    @abstractmethod
    def _output(self):
        pass
