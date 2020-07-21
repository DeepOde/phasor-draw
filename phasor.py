import math
import cmath

class Phasor():
    phasor_id = 0
    phasor_dict = {} #phasor_id - > Phasor object, only phasors created by user shall be entered
    def __init__(self, x, y, user_created = False):
        self._x = x
        self._y = y
        self.cnumber = self._x+self._y*1j
        self._mag = abs(self.cnumber)
        self._phase = cmath.phase(self.cnumber)
        self._id = Phasor.phasor_id
        self._user_created = user_created

        if self._user_created:
            Phasor.phasor_dict[self._id] = self

        Phasor.phasor_id += 1           

    
    def __add__(self, other): 
        return Phasor(self._x+other._x, self._y+other._y)
    
    def __sub__(self, other): 
        return Phasor(self._x-other._x, self._y-other._y)
   
    def __mul__(self, other): 
        self._res_num = self.cnumber*other.cnumber
        return Phasor(self._res_num.real, self._res_num.imag)
    
    def __div__(self, other): 
        self._res_num = self.cnumber/other.cnumber
        return Phasor(self._res_num.real, self._res_num.imag)    
        
    def __repr__(self):
        return 'Phasor(' + str(self._x) + ', ' + str(self._y) + ')'

    def __str__(self):
        return str(self.cnumber)

#Test: Prints a few phasors on screen, check operations on them in console.
if __name__ == "__main__":
    a = Phasor(3, 4)
    b = Phasor(4, 3)
    c = Phasor(1, 1)
    print('a :',a)
    print('b :',b)
    print('c :',c)
    
