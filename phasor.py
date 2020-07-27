from flask import session
import cmath, operator

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

        self._xend = 0 #this will be updated while drawing, this ensures all phasor objects have been created
        self._yend = 0 #this will be updated while drawing, this ensures all phasor objects have been created
        
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

        for phasor in (sorted(cls.phasor_dict.values(), key=operator.attrgetter('_id'))):
            print(phasor._id)
            print(cls.phasor_dict[phasor._name])
            
        for phasor in (sorted(cls.phasor_dict.values(), key=operator.attrgetter('_id'))):
            if phasor._todraw:
                phasor._xpx = (phasor._x * 280)/cls._max_x #we want largest phasor to be of 295 px
                phasor._ypx = (phasor._y * 280)/cls._max_y
                if ((phasor._beginfrom).strip() != '') and (phasor._beginfrom in cls.phasor_dict):
                    phasor._xbegin = cls.phasor_dict[phasor._beginfrom]._xend
                    phasor._ybegin = cls.phasor_dict[phasor._beginfrom]._yend
                    
                else:
                    phasor._xbegin = 0
                    phasor._ybegin = 0

                phasor._xend = phasor._xbegin + phasor._xpx
                phasor._yend = phasor._ybegin + phasor._ypx
                
                phasordrawdata[i] = {'name':phasor._name, 'x':phasor._xpx, 'y':phasor._ypx, 'color':phasor._color, 'xbegin':phasor._xbegin, 'ybegin':phasor._ybegin, 'real':phasor._x, 'imag':phasor._y}
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
