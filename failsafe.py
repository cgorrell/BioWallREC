import sqlite3 as lite
import sys
import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu


conx = lite.connect('pi.db')

with conx:
    cur = conx.cursor()
    Modbus_address = cur.execute("SELECT Value FROM Modbus WHERE Name = ?;", ('Modbus_address', )).fetchone()[0]
    baudrate = cur.execute("SELECT Value FROM Modbus WHERE Name = ?;", ('Baudrate', )).fetchone()[0]
    bits = cur.execute("SELECT Value FROM Modbus WHERE Name = ?;", ('Register_bit_length', )).fetchone()[0]
    Starting_input = cur.execute("SELECT Value FROM Modbus WHERE Name = ?;", ('Starting_input', )).fetchone()[0]
    Qty_inputs = cur.execute("SELECT Value FROM Modbus WHERE Name = ?;", ('Qty_inputs', )).fetchone()[0]
    Starting_output = cur.execute("SELECT Value FROM Modbus WHERE Name = ?;", ('Starting_output', )).fetchone()[0]
    Qty_outputs = cur.execute("SELECT Value FROM Modbus WHERE Name = ?;", ('Qty_outputs', )).fetchone()[0]
    Fertigator_address = cur.execute("SELECT Address FROM Outputs WHERE Alias = ?;", ('Fertigator', )).fetchone()[0]
    Supply_address = cur.execute("SELECT Address FROM Outputs WHERE Alias = ?;", ('Solenoid', )).fetchone()[0]
try:
    wall = modbus_rtu.RtuMaster(serial.Serial(port='/dev/rfxcom', baudrate= baudrate, bytesize=8, parity='N', stopbits=1, xonxoff=0))
    wall.set_timeout(5.0)
except :
    pass

def Fail_safe():
    safe_outputs = []
    for x in range(Qty_outputs):
        safe_outputs += [0]
    try:
        #wall.execute(1, cst.WRITE_SINGLE_REGISTER, Supply_address, output_value=0)
        #wall.execute(1, cst.WRITE_SINGLE_REGISTER, Fertigator_address, output_value=0)
        wall.execute(1, cst.WRITE_MULTIPLE_REGISTERS, Starting_output, output_value=safe_outputs)
    except modbus_tk.modbus.ModbusError, e:
        print("%s- Code=%d" % (e, e.get_exception_code()))
    except modbus_tk.modbus.ModbusInvalidResponseError, e:
        print("%s" % (e))
    except lite.Error as e:
        print "An error occurred:", e.args[0]
    except :
        print "Device Communicaion Error: Failed to execute fail safe"
if __name__=='__main__':
    Fail_safe()
