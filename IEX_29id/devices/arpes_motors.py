__all__ = """
    mvx
    mvy
    mvz
    mvth
    mvchi
    mvphi
    mvrx
    mvry
    mvrz
    mvrth
    mvrchi
    mvrphi
    mprint
    mvsample
""".split()



### all the function that moves the manipulator:
### tth, th, phi, chi, x, y, z, sample

  
# RE = bluesky.RunEngine({​​​​​​​​​}​​​​​​​​​)





from bluesky import plan_stubs as bps
import logging
from ophyd import EpicsMotor, EpicsSignal, PVPositionerPC, EpicsSignalRO
from ophyd import Component, Device
from apstools.devices import EpicsDescriptionMixin
#from hkl.geometries import E4CV

#logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)



##### Create class to describe real motors (x,y,z,kphi,kth,kap,tth)

# class EpicsDescriptionMixin(EpicsDescriptionMixin, EpicsMotor):   # adds the .DESC field to EpicsMotor
#     pass

class MyEpicsMotor(EpicsMotor):
    sync = Component(EpicsSignal, ".SYNC")
    desc = Component(EpicsSignalRO,".DESC")



class _ArpesMotors(Device):
    m1  = Component(MyEpicsMotor, "1")    ## x    29idARPES:m1.VAL   29idARPES:m1.RBV
    m2  = Component(MyEpicsMotor, "2")    ## y
    m3  = Component(MyEpicsMotor, "3")    ## z 
    m4  = Component(MyEpicsMotor, "4")    ## th
    m5  = Component(MyEpicsMotor, "5")    ## chi
    m6  = Component(MyEpicsMotor, "6")    ## phi

## Instantiate real motors
arpes_motors = _ArpesMotors("29idKtest:m", name="motors")  # arpes_motors.m1



##### Create class to write to str PVs for troubleshooting

class _Status(Device):
    st1  = Component(EpicsSignal, "1")        
    st2  = Component(EpicsSignal, "2")    
    st3  = Component(EpicsSignal, "3")     
    st4  = Component(EpicsSignal, "4")    

## Instantiate status
status  = _Status("29idKtest:gp:text",name="status")  # =>  status.st1/2/3/4


##### Create class to write to str PVs for troubleshooting

# class _SyncMotors(Device):
#     sync7  = Component(EpicsSignal, "7")        
#     sync8  = Component(EpicsSignal, "8")    
#     sync9  = Component(EpicsSignal, "9")     

# ## Instantiate status
# sync  = _SyncMotors("29idKtest:m",name="sync") 


def _quickmove_plan(value,motor):
    desc  = motor.desc.get()
    yield from bps.mv(motor,value)
    yield from bps.mv(status.st1, f"{desc} = {motor.position}")
    motor.log.logger.info("%s = %d", desc, motor.position)


def _quickmove_rel_plan(value,motor):
    desc  = motor.desc.get()
    yield from bps.mv(status.st2,f"Old {desc} = {motor.position}")
    yield from bps.mvr(motor,value)
    yield from bps.mv(status.st3,f"New {desc} = {motor.position}")
    motor.log.logger.info("%s = %d", desc, motor.position)



def mprint():
    """
    print all motors position
    """
    yield from bps.mv(status.st4, f"{arpes_motors.m1.position},{arpes_motors.m2.position},{arpes_motors.m3.position},{arpes_motors.m4.position},{arpes_motors.m5.position},{arpes_motors.m6.position}")
    # Add the log info


def mvsample(positions=None):
    """
    move diffractometer to a specific position listed as positions=[x,y,z,kphi,kap,kth,tth]
    default positions is st4
    does not move tth
    """
    if not positions:
        positions = status.st4.get()
        positions=[float(s) for s in positions.split(',')]
    x,y,z,th,chi,phi=positions
    yield from bps.mv(arpes_motors.m1,x,arpes_motors.m2,y,arpes_motors.m3,z,
            arpes_motors.m4,th,arpes_motors.m5,chi,arpes_motors.m6,phi)
    # Add the log info




def mvx(value):
    """
    moves x to value 
    """
    yield from _quickmove_plan(value,arpes_motors.m1)


def mvy(value):
    """
    moves y to value 
    """
    yield from _quickmove_plan(value,arpes_motors.m2)


def mvz(value):
    """
    moves z to value 
    """
    yield from _quickmove_plan(value,arpes_motors.m3)


def mvth(value):
    """
    moves kphi to value 
    """
    yield from _quickmove_plan(value,arpes_motors.m4)


def mvchi(value):
    """
    moves kap to value 
    """
    yield from _quickmove_plan(value,arpes_motors.m5)


def mvphi(value):
    """
    moves kth to value 
    """
    yield from _quickmove_plan(value,arpes_motors.m6)



def mvrx(value):
    """
    moves x to value 
    """
    yield from _quickmove_rel_plan(value,arpes_motors.m1)


def mvry(value):
    """
    moves y to value 
    """
    yield from _quickmove_rel_plan(value,arpes_motors.m2)


def mvrz(value):
    """
    moves z to value 
    """
    yield from _quickmove_rel_plan(value,arpes_motors.m3)


def mvrth(value):
    """
    relative move kphi by value 
    """
    yield from _quickmove_rel_plan(value,arpes_motors.m4)


def mvrchi(value):
    """
    moves kap to value 
    """
    yield from _quickmove_rel_plan(value,arpes_motors.m5)


def mvrphi(value):
    """
    moves kth to value 
    """
    yield from _quickmove_rel_plan(value,arpes_motors.m6)



