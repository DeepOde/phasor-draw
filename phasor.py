from flask import session
import cmath

class Phasor():
    phasor_id = 0
    phasor_dict = {} #phasor_name - > Phasor object, only phasors created by user shall be entered
    _max_x = 1
    _max_y = 1
    
    def __init__(self, x, y, user_created = False, name='', todraw = True, color='red', beginfrom=''):
        print(color)
        self._x = x
        self._y = y
        self._user_created = user_created
        self._todraw = todraw
        self._color = color
        self._name = ''
        self._beginfrom = beginfrom
        
        if self._user_created:
            self._name = name
            Phasor.phasor_dict[self._name] = self
            print("appended to phasor dict, now it is",Phasor.phasor_dict)
        else:
            print("see it was,",self._user_created)
        
        self._xbegin = 0 #this will be updated while drawing, this ensures all phasor objects have been created
        self._ybegin = 0 #this will be updated while drawing, this ensures all phasor objects have been created
        
        self.xpx = x #this can be deleted maybe
        self.ypx = y #this can also be deleted maybe

        self.cnumber = self._x+self._y*1j
        self._mag = abs(self.cnumber)
        self._phase = cmath.phase(self.cnumber)
        self._id = Phasor.phasor_id
                        
        Phasor.phasor_id += 1           

    @classmethod
    def draw_all_phasors(cls):
        cls._max_x = 0
        cls._max_y = 0
        print("operating on pd",cls.phasor_dict)
        for phasor in cls.phasor_dict:
            if cls.phasor_dict[phasor]._todraw:
                if abs(cls.phasor_dict[phasor]._x) > cls._max_x:
                    cls._max_x = abs(cls.phasor_dict[phasor]._x)
                if abs(cls.phasor_dict[phasor]._y) > cls._max_y:
                    cls._max_y = abs(cls.phasor_dict[phasor]._y)
        cls._max_x = max([cls._max_x, cls._max_y])
        print("max",cls._max_x)
        cls._max_y = cls._max_x
        phasordrawdata = {}
        i = 0;
        for phasor in cls.phasor_dict:
            if cls.phasor_dict[phasor]._todraw:
                cls.phasor_dict[phasor]._xpx = (cls.phasor_dict[phasor]._x * 295)/cls._max_x #we want largest phasor to be of 295 px
                cls.phasor_dict[phasor]._ypx = (cls.phasor_dict[phasor]._y * 295)/cls._max_y
                if ((cls.phasor_dict[phasor]._beginfrom).strip() != '') and (cls.phasor_dict[phasor]._beginfrom in cls.phasor_dict):
                    cls.phasor_dict[phasor]._xbegin = (cls.phasor_dict[cls.phasor_dict[phasor]._beginfrom]._x * 280)/cls._max_x
                    cls.phasor_dict[phasor]._ybegin = (cls.phasor_dict[cls.phasor_dict[phasor]._beginfrom]._y * 280)/cls._max_y
                else:
                    cls.phasor_dict[phasor]._xbegin = 0
                    cls.phasor_dict[phasor]._ybegin = 0
                
                phasordrawdata[i] = {'name':cls.phasor_dict[phasor]._name, 'x':cls.phasor_dict[phasor]._xpx, 'y':cls.phasor_dict[phasor]._ypx, 'color':cls.phasor_dict[phasor]._color, 'xbegin':cls.phasor_dict[phasor]._xbegin, 'ybegin':cls.phasor_dict[phasor]._ybegin, 'real':cls.phasor_dict[phasor]._x, 'imag':cls.phasor_dict[phasor]._y}
                i += 1             

        ##Serialise phasor dict to and store in a session, then erase phasor dict
        serialised_copy = {}
        for key, value in cls.phasor_dict.items():
            serialised_copy[key] = value.__dict__
            del serialised_copy[key]['cnumber']

        session['userdict'] = serialised_copy.copy()
        cls.phasor_dict = {}
        ##
        print("i m sendingggggggg this .......", phasordrawdata)
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
        return 'Phasor(' + str(self._x) + ', ' + str(self._y) + ', '+ str(self._user_created)+ ', ' + str(self._name) + ', '+ str(self._todraw) + ', '+ str(self._color) + ', ' + str(self._beginfrom) + ')'

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
