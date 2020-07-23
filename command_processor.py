import phasor
import cmath
import re
import string

PRECISION = 5 #Digits after 0 for angle in radian

def isnum(value):
    '''Returns true if 'value' can be converted into a float'''
    try:
        float(value)
        return True
    except ValueError:
        return False

def valid_phasor_name(name):
    if isnum(name[0]):
        return False

    allowed_chs = string.ascii_letters + string.digits + '_'
    for c in name:
        if c not in allowed_chs:
            return False

    return True

def get_std_command(raw_command):
    '''Returns standard command where complex number in polar forms are expressed as 'rANGthetaR'
        e.g. '5ANG1R' where 'theta' a number between 'ANG' and 'R' represents angles in radian and
        a number 'r' preceeding 'ANG' represents magnitude

        raw_command: RHS of an expression provided by user
        '''
    raw_command = raw_command.replace(' ','').replace('arg','ang').replace('pi','cmath.pi')

    cc = raw_command[:] #carbon copy of raw_command to mutate

    #Covert angle in degrees (evaluating it if it is reprented as an expresion), which appears before 'd' into angle in radians, appearing before 'r', mutate cc
    d_result = re.findall('ang(.+?)d', cc)
    for exp in d_result:
        ang_index = cc.find('ang')
        d_index = cc[ang_index:].find('d') + ang_index
        cc = cc[:ang_index] + 'ang' + str(round((eval(exp))*cmath.pi/180, PRECISION)) + 'r'+ cc[d_index+1:]

    #The angle if represented as an expression, is evaluated and stored as " 'ANG'<float>'R' ", digits after decimal point in <float> is controlled by PRECISION
    result = re.findall('ang(.+?)r', cc)
    for exp in result:
        ang_index = cc.find('ang')
        r_index = cc[ang_index:].find('r') + ang_index
        cc = cc[:ang_index] + 'ANG' + str(round(eval(exp), PRECISION)) + 'R'+ cc[r_index+1:]
        
    return cc

def eval_std_command(cc):
    '''Evaluates standard command cc to and returns a (possibly) complex no. of evaluation, otherwise returns a string showing error'''
    
    final_command = cc[:]
    
    #Angles in radian might still contain preceeding '-', to separate it from operators specifying different terms, replace it temporarily with '!'
    for i, c in enumerate(cc):
        if c == '-':
            if 'ANG' in cc[i-4:i]:
                cc = cc[:i]+'!'+cc[i+1:]

    #This line replaces term separators (+-*/) by comma, separating them into different operands AND at the end, re-replaces '!' with '-'
    cc = cc.replace('+',',').replace('-',',').replace('*',',').replace('/',',').replace('(','').replace(')','').replace('!','-') #Caution: The last replace should change '!' to '-', other replacments should preceed it

    #Create Phasor objects for each separate term
    operands_list = cc.split(',')
    operand_dict = {} #operand (as it appears in standard command) -> complex number
    
    #Assign a Phasor object to each operand
    for operand in operands_list:
        if operand in phasor.Phasor.phasor_dict:
            operand_dict[operand] = phasor.Phasor.phasor_dict[operand].cnumber
            final_command = final_command.replace(operand, operand_dict[operand])
        else: #New phasor has to be constructed, supported formats : 'rANGthetaR, a, ja, aj'
            if 'ANG' in operand: #Operand is in ' rANGthetaR ' form
                _operand_split = operand.split('ANG')
                _operand_r = float(_operand_split[0])
                _operand_theta = float(_operand_split[1][:-1]) #drop the last R
                _operand_cnumber = _operand_r*cmath.cos(_operand_theta) +  _operand_r*cmath.sin(_operand_theta)*1j
                final_command = final_command.replace(operand, str(_operand_cnumber))
                
            elif 'j' in operand or 'i' in operand:
                operand = operand.replace('i','j').replace('j*','j')#For users who can't read instructions and type j*b instead of jb
                _j_index = operand.find('j')
                if _j_index == 0: #j is in beginning
                    _operand_r = float(operand[1:])
                else: #assuming j in end
                    _operand_r = float(operand[:-1])
                print(_operand_r)
                _operand_theta = cmath.pi/2
                _operand_cnumber = _operand_r*cmath.cos(_operand_theta) +  _operand_r*cmath.sin(_operand_theta)*1j
                final_command = final_command.replace(operand, str(_operand_cnumber))

            elif not isnum(operand):
                final_command = final_command.replace(operand, 'ERROR: Couldn\'t find phasor named '+operand)

    try:
        result = eval(final_command)
    except SyntaxError:
        return 'ERROR: Command entered either has phasor name which was not found, or has an invalid syntax, please check and try again. Make sure you spelled phasor name correctly.'
    except ValueError:
        return 'ERROR: Couldn\'t calculate value of entered expression on the RHS.'
    except NameError:
        return 'ERROR: Either phasor name was not found or polar form was incorrectly entered.'
    
    if type(result) == type(1) or type(result) == type(1.1) or type(result) == type(1+2j):
        return result
    else:
        return 'ERROR: Evaluation of command didn\'t result into number.'

#TODO
def process_input(command):
    '''Process the user input'''

    if '=' in command:
        parameters = command.split('=')
        if valid_phasor_name(parameters[0]):
            _phasor_name = parameters[0]
            _std_command = get_std_command(parameters[1])
            _phasor_cnumber = eval_std_command(_std_command)
            if type(_phasor_cnumber ) == type('a'):
                return _phasor_cnumber
            else:
                phasor.Phasor(_phasor_cnumber.real, _phasor_cnumber.imag, True, _phasor_name, True)
                return True

    if 'del' in command:
        _phasor_name = command.split(' ')[0]
        try:
            phasor.Phasor.phasor_dict.pop(_phasor_name)
            return True
        except KeyError:
            return 'No such phasor.'

     


            
