import cmath

class Phasor():
    phasor_id = 0
    phasor_dict = {} #phasor_id - > Phasor object, only phasors created by user shall be entered
    _max_x = 1
    _max_y = 1
    
    def __init__(self, x, y, user_created = False, name='', todraw = False):
        self._x = x
        self._y = y
        self.cnumber = self._x+self._y*1j
        self._mag = abs(self.cnumber)
        self._phase = cmath.phase(self.cnumber)
        self._id = Phasor.phasor_id
        self._user_created = user_created
        self._name = ''
        self._todraw = todraw
    
        if self._user_created:
            self._name = name
            Phasor.phasor_dict[self._name] = self
            self._todraw = True
            
        Phasor.phasor_id += 1           

    @classmethod
    def draw_all_phasors(cls):
        for phasor in cls.phasor_dict:
            if cls.phasor_dict[phasor]._todraw:
                if abs(cls.phasor_dict[phasor]._x) > cls._max_x:
                    cls._max_x = abs(cls.phasor_dict[phasor]._x)
                if abs(cls.phasor_dict[phasor]._y) > cls._max_y:
                    cls._max_y = abs(cls.phasor_dict[phasor]._y)
                    
        print(cls._max_x)
        print(cls._max_y)
        phasordrawdata = {}
        i = 0;
        for phasor in cls.phasor_dict:
            if cls.phasor_dict[phasor]._todraw:
                cls.phasor_dict[phasor]._xpx = (cls.phasor_dict[phasor]._x * 295)/cls._max_x #we want largest phasor to be of 295 px
                cls.phasor_dict[phasor]._ypx = (cls.phasor_dict[phasor]._y * 295)/cls._max_y

                phasordrawdata[i] = {'name':cls.phasor_dict[phasor]._name, 'x':cls.phasor_dict[phasor]._xpx, 'y':cls.phasor_dict[phasor]._ypx}
                i += 1             
        
        return phasordrawdata
            #send data now

            

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
    a = Phasor(3, 4, True, 'a', True)
    b = Phasor(4, 3, True, 'b', True)
    c = Phasor(1, 1, True, 'c', True)
    print('a :',a)
    print('b :',b)
    print('c :',c)
    Phasor.draw_all_phasors();
