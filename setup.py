import sqlite3 as lite
import pyonep
import logging
from pyonep import onep
from pyonep.provision import Provision
from pyonep.onep import OnepV1
from pyonep.exceptions import ProvisionException
from pyonep.exceptions import OneException
#import RPi.GPIO as GPIO
Setup_logger= logging.getLogger("exosite.setup")
con = lite.connect('pi.db')
prompt = '> '
o = onep.OnepV1()
provision = Provision('m2.exosite.com', https=True, port=443,  manage_by_cik=False, verbose=False,  raise_api_exceptions=True)


def Wall_config():       
    print "What would you like to configure? \n1=Modbus \n 2=Gateway \n 3=Sensors \n 4=Outputs \n 5=Timers \n 6=Setpoints \n 0=Exit"
    selection = int(raw_input(prompt))
    if selection == 1:
        Modbus_config()
    elif selection == 2:
        Gateway_config()
    elif selection == 3:
        Sensors_config()
    elif selection == 4:
        Outputs_config()
    elif selection == 5:
        Timers_config()
    elif selection == 6:
        Setpoints_config()

def Modbus_config():
    while True:
        print "We will begin with Preparing the Modbus Device Connection. Please respond to every prompt. \n"

        print "What is the Modbus Device Address (0-255?) [T34A0 = 01]"
        Modbus_address = int(raw_input(prompt))

        print "What is the Modbus Device Baudrate?  Usually 9600 or 19200."
        Baudrate = int(raw_input(prompt))

        print "What is the register bit length for your input registers? (usually 8 or *12)"
        Register_bit_length = int(raw_input(prompt))

        print "What is the Starting INPUT register address on your modbus device? [T34A0 = 190]"
        Starting_input = int(raw_input(prompt))

        print "How many consecutive inputs would you like to read? [T34A0 = 10]"
        Qty_inputs = int(raw_input(prompt))

        print "What is the Starting OUPUT register address on your modbus device? [T34A0 = 100]"
        Starting_ouput = int(raw_input(prompt))

        print "How many consecutive outputs would you like to read? [T34A0 = 8]"
        Qty_outputs = int(raw_input(prompt))

        print "Is everything correct (y/n)? \n Modbus_address = %r \n Baudrate = %r \n Register_bit_length = %r \n Starting_input = %r \n Qty_inputs = %r \n Starting_ouput = %r \n Qty_outputs = %r \n" % (Modbus_address, Baudrate,  Register_bit_length, Starting_input, Qty_inputs, Starting_ouput, Qty_outputs)
        if raw_input(prompt) == 'y':
            with con:
                cur = con.cursor()
                cur.execute("INSERT INTO Modbus(Name, Value) VALUES ('Baudrate', ?);", (Baudrate,))
                cur.execute("INSERT INTO Modbus(Name, Value) VALUES ('Modbus_address', ?);", (Modbus_address,))
                cur.execute("INSERT INTO Modbus(Name, Value) VALUES ('Starting_input', ?);",(Starting_input,))
                cur.execute("INSERT INTO Modbus(Name, Value) VALUES ('Qty_inputs', ?);", (Qty_inputs,))
                cur.execute("INSERT INTO Modbus(Name, Value) VALUES ('Register_bit_length', ?);", (Register_bit_length,))
                cur.execute("INSERT INTO Modbus(Name, Value) VALUES ('Starting_output', ?);", (Starting_ouput,))
                cur.execute("INSERT INTO Modbus(Name, Value) VALUES ('Qty_outputs', ?);", (Qty_outputs,))
            Setup_logger.info("Modbus table updated with: \n Modbus_address = %r \n Baudrate = %r \n Register_bit_length = %r \n Starting_input = %r \n Qty_inputs = %r \n Starting_ouput = %r \n Qty_outputs = %r \n" % (Modbus_address, Baudrate,  Register_bit_length, Starting_input, Qty_inputs, Starting_ouput, Qty_outputs))
            break
        print "let's try again."

def Gateway_config():
    while True:
        print "We will begin with Preparing the Gateway Device Connection. Please respond to every prompt. \n"

        print "What is the Alias of your gateway? (must be a Unique wall name should match Exosite Alias)"
        Device_alias = raw_input(prompt)
        
        print "What is your Device Serial Number? (from exosite)"
        Serial_number = str(raw_input(prompt))
        
        print "Is everything correct (y/n)? \n Device_alias %r \n Serial number= %r \n" % (Device_alias, Serial_number)
        if raw_input(prompt) == 'y':
            with con:
                cur = con.cursor()
                cur.execute("INSERT INTO Gateway(Name, Value) VALUES ('Device_alias', ?);", (Device_alias, ))
                cur.execute("INSERT INTO Gateway(Name, Value) VALUES ('Portal_cik', ?);", ('YOUR CIK HERE', ))
                cur.execute("INSERT INTO Gateway(Name, Value) VALUES ('Vendor_token', ?);", ('YOUR TOKEN HERE', ))
                cur.execute("INSERT INTO Gateway(Name, Value) VALUES ('Vendor_name', ?);", ('furbish', ))
                cur.execute("INSERT INTO Gateway(Name, Value) VALUES ('Model', ?);", ('BioWallREC', ))
            	cur.execute("INSERT INTO Gateway(Name, Value) VALUES ('Serial', ?);", (Serial_number, ))
            	Status_check()	
            Setup_logger.info(" Gateway table updated with: \n Device_alias %r \n Serial number= %r \n" % (Device_alias, Serial_number))
            break
        print "let's try again."

def Sensors_config():
    while True:
        print "We will begin with Preparing the Sensors for your device. \n"

        print "What is the modbus register address of your PH sensor?"
        PH_address = int(raw_input(prompt))

        print "What is the Digital to Analog Conversion Numerator of your PH sensor ? (10)"
        PH_DACN = float(raw_input(prompt))

        print "What is the slope for your PH Voltage conversion?"
        PH_slope = float(raw_input(prompt))

        print "What is the intercept for your PH Voltage conversion?"
        PH_intercept = float(raw_input(prompt))

        print "What is the modbus register address of your EC sensor?"
        EC_address = int(raw_input(prompt))

        print "What is the Digital to Analog Conversion Numerator of your EC sensor? (10)"
        EC_DACN = float(raw_input(prompt))

        print "What is the slope for your EC Voltage conversion?"
        EC_slope = float(raw_input(prompt))

        print "What is the intercept for your EC Voltage conversion?"
        EC_intercept = float(raw_input(prompt))

        print "What is the modbus register address of your Pressure sensor?"
        Pressure_address = int(raw_input(prompt))

        print "What is the Digital to Analog Conversion Numerator of your Pressure sensor? (10)"
        Pressure_DACN = float(raw_input(prompt))

        print "What is the slope for your Pressure Voltage conversion?"
        Pressure_slope = float(raw_input(prompt))

        print "What is the intercept for your Pressure Voltage conversion?"
        Pressure_intercept = float(raw_input(prompt))

        print "What is the modbus register address of your Flow sensor?"
        Flow_address = int(raw_input(prompt))

        print "What is the Digital to Analog Conversion Numerator of your Flow sensor? (10)"
        Flow_DACN = float(raw_input(prompt))

        print "What is the slope for your Flow Voltage conversion?"
        Flow_slope = float(raw_input(prompt))

        print "What is the intercept for your Flow Voltage conversion?"
        Flow_intercept = float(raw_input(prompt))

        print "What is the modbus register address of your Level sensor?"
        Level_address = int(raw_input(prompt))

        print "What is the Digital to Analog Conversion Numerator of your Level sensor? (10000)"
        Level_DACN = float(raw_input(prompt))

        print "What is the length of your Wema Level sensor (in inches)?"
        Level_height = float(raw_input(prompt))

        print "What is the offset of the sensor from the bottom of the tank (in inches)?"
        Level_offset = float(raw_input(prompt))

        print "What is the modbus register address of your Leak sensor?"
        Leak_address = float(raw_input(prompt))

        print "What is the Digital to Analog Conversion Numerator of your Leak sensor? (10000)"
        Leak_DACN = float(raw_input(prompt))

        print "What is the slope for your Leak Voltage conversion?"
        Leak_slope = int(raw_input(prompt))

        print "What is the intercept for your Leak Voltage conversion?"
        Leak_intercept = raw_input(prompt)

        print "Is everything correct (y/n)? \n PH_address = %r \n PH_DACN = %r \n PH_slope = %r \n PH_intercept = %r \n EC_address = %r \n EC_DACN = %r \n EC_slope = %r \n EC_intercept = %r \n Pressure_address = %r \n Pressure_DACN = %r \n Pressure_slope = %r \n Pressure_intercept = %r \n Flow_address = %r \n Flow_DACN = %r \n Flow_slope = %r \n Flow_intercept = %r \n Level_address = %r \n Level_DACN = %r \n Level_height = %r \n Level_offset = %r \n Leak_address = %r \n Leak_DACN = %r \n  Leak_slope = %r \n Leak_intercept = %r \n " % (PH_address, PH_DACN, PH_slope, PH_intercept, EC_address, EC_DACN, EC_slope, EC_intercept, Pressure_address, Pressure_DACN, Pressure_slope, Pressure_intercept, Flow_address, Flow_DACN, Flow_slope, Flow_intercept, Level_address, Level_DACN, Level_height, Level_offset, Leak_address, Leak_DACN, Leak_slope, Leak_intercept)
        if raw_input(prompt) == 'y':
            
            Level_slope = -Level_height/(240-33)
            Level_intercept = 0 - Level_slope*240 + Level_offset
            with con:
                cur = con.cursor()
                cur.execute("INSERT INTO Sensors(Alias, Address, DACN, Slope, Intercept) VALUES ('PH', ?, ?, ?, ?);", (PH_address, PH_DACN, PH_slope, PH_intercept, ))
                cur.execute("INSERT INTO Sensors(Alias, Address, DACN, Slope, Intercept) VALUES ('EC', ?, ?, ?, ?);", (EC_address, EC_DACN, EC_slope, EC_intercept,  ))
                cur.execute("INSERT INTO Sensors(Alias, Address, DACN, Slope, Intercept) VALUES ('Pressure', ?, ?, ?, ?);", (Pressure_address, Pressure_DACN, Pressure_slope, Pressure_intercept,  ))
                cur.execute("INSERT INTO Sensors(Alias, Address, DACN, Slope, Intercept) VALUES ('Flow', ?, ?, ?, ?);", (Flow_address, Flow_DACN, Flow_slope, Flow_intercept,  ))
                cur.execute("INSERT INTO Sensors(Alias, Address, DACN, Slope, Intercept) VALUES ('Leak', ?, ?, ?, ?);", (Leak_address, Leak_DACN, Leak_slope, Leak_intercept,  ))
                cur.execute("INSERT INTO Sensors(Alias, Address, DACN, Slope, Intercept) VALUES ('Level', ?, ?, ?, ?);", (Level_address, Level_DACN, Level_slope, Level_intercept,  ))
            Setup_logger.info("Sensor table updated with: \n PH_address = %r \n PH_DACN = %r \n PH_slope = %r \n PH_intercept = %r \n EC_address = %r \n EC_DACN = %r \n EC_slope = %r \n EC_intercept = %r \n Pressure_address = %r \n Pressure_DACN = %r \n Pressure_slope = %r \n Pressure_intercept = %r \n Flow_address = %r \n Flow_DACN = %r \n Flow_slope = %r \n Flow_intercept = %r \n Level_address = %r \n Level_DACN = %r \n Level_slope = %r \n Level_intercept = %r \n Leak_address = %r \n Leak_DACN = %r \n  Leak_slope = %r \n Leak_intercept = %r \n " % (PH_address, PH_DACN, PH_slope, PH_intercept, EC_address, EC_DACN, EC_slope, EC_intercept, Pressure_address, Pressure_DACN, Pressure_slope, Pressure_intercept, Flow_address, Flow_DACN, Flow_slope, Flow_intercept, Level_address, Level_DACN, Level_slope, Level_intercept, Leak_address, Leak_DACN, Leak_slope, Leak_intercept))
            break
        print "Let's try again."
          
def Outputs_config():
    while True:
        print "We will begin with Preparing the Outputs for your device. \n"

        print "What is the modbus register address of your make up water solenoid?"
        Solenoid_address = int(raw_input(prompt))

        print "What is Dataport DACN of your make up water solenoid? (Future application put 1 for now)"
        Solenoid_DACN = raw_input(prompt)

        print "What is the modbus register address of your fertigator pump?"
        Fertigator_address = int(raw_input(prompt))

        print "What is Dataport DACN of your fertigator pump? (Future application put 1 for now)"
        Fertigator_DACN = raw_input(prompt)

        print "What is the modbus register address of your Pump?"
        Pump_address = int(raw_input(prompt))

        print "What is Dataport DACN of your Pump? (Future application put 1 for now)"
        Pump_DACN = raw_input(prompt)

        print "What is the modbus register address of your Fill Solenoid?"
        Fill_address = int(raw_input(prompt))

        print "What is Dataport DACN of your Fill Solenoid? (Future application put 1 for now)"
        Fill_DACN = raw_input(prompt)

        print "Is everything correct (y/n)? \n Solenoid_address = %r \n Solenoid_DACN = %r \n Fertigator_address = %r \n Fertigator_DACN = %r \n Pump_address = %r \n Pump_DACN = %r \n Fill_address = %r \n Fill_DACN = %r \n" % (Solenoid_address, Solenoid_DACN, Fertigator_address, Fertigator_DACN, Pump_address, Pump_DACN, Fill_address, Fill_DACN)
        
        if raw_input(prompt) == 'y':
            with con:
                cur = con.cursor()
                cur.execute("INSERT INTO Outputs(Alias, Address, DACN) VALUES ('Solenoid', ?, ?);", (Solenoid_address, Solenoid_DACN, ))
                cur.execute("INSERT INTO Outputs(Alias, Address, DACN) VALUES ('Fertigator', ?, ?);", (Fertigator_address, Fertigator_DACN, ))
                cur.execute("INSERT INTO Outputs(Alias, Address, DACN) VALUES ('Pump', ?, ?);", (Pump_address, Pump_DACN, ))
                cur.execute("INSERT INTO Outputs(Alias, Address, DACN) VALUES ('Fill', ?, ?);", (Fill_address, Fill_DACN, ))
            Setup_logger.info(" Output table updated with: \n Solenoid_address = %r \n Solenoid_DACN = %r \n Fertigator_address = %r \n Fertigator_DACN = %r \n Pump_address = %r \n Pump_DACN = %r \n Fill_address = %r \n Fill_DACN = %r \n" % (Solenoid_address, Solenoid_DACN, Fertigator_address, Fertigator_DACN, Pump_address, Pump_DACN, Fill_address, Fill_DACN))
            break
        print "Let's try again."

def Timers_config():
    while True:
        print "We will begin with Preparing the Timers for your device.  All timers are counted in seconds. \n"

        print "What is the total cycle time for your circulating pump?"
        Pump_cycle = float(raw_input(prompt))

        print "What is the run time for your circulating pump per cycle. (should be less than last response)"
        Pump_timer = float(raw_input(prompt))

        print "What is the per dosing duration for the fertigator? (should be less than last reponse)"
        Fertigator_timer = float(raw_input(prompt))

        print "What is delay between data transmissions to exosite? (read/write frequency should be greater than 15 seconds)"
        Relay = float(raw_input(prompt))

        print "Is everything correct (y/n)? \n Pump_cycle %r seconds \n Pump_timer every %r seconds \n Fertigator every %r seconds \n Relay every %r seconds \n" % (Pump_cycle, Pump_timer, Fertigator_timer, Relay)

        if raw_input(prompt) == 'y':
			with con:
				cur = con.cursor()
				cur.execute("INSERT INTO Timers(Name, Length) VALUES ('Pump_timer', ?);", (Pump_timer, ))
				cur.execute("INSERT INTO Timers(Name, Length) VALUES ('Pump_cycle', ?);", (Pump_cycle, ))
				cur.execute("INSERT INTO Timers(Name, Length) VALUES ('Fertigator_timer', ?);", (Fertigator_timer, ))
				cur.execute("INSERT INTO Timers(Name, Length) VALUES ('Relay', ?);", (Relay, ))
			Setup_logger.info("Timers table updated with: \n Pump_cycle %r seconds \n Pump_timer every %r seconds \n Fertigator every %r seconds \n Relay every %r seconds \n" % (Pump_cycle, Pump_timer, Fertigator_timer, Relay))
			break
        print "Let's try again."

def Setpoints_config():
    while True:
        print "We will begin with Preparing the Setpoints for your device. \n"

        print "What is the high water setpoint for your recirculating system? (in inches)"
        Water_high_setpoint = float(raw_input(prompt))

        print "What is the low water setpoint for your recirculating system? (in inches)"
        Water_low_setpoint = float(raw_input(prompt))

        print "What is the high EC setpoint for your recirculating system? (in PPM)"
        EC_high_setpoint = float(raw_input(prompt))

        print "What is the low EC setpoint for your recirculating system? (in PPM)"
        EC_low_setpoint = float(raw_input(prompt))

        print "Is everything correct (y/n)? \n Water_high_setpoint= %r inches \n Water_low_setpoint= %r inches \n EC_high_setpoint= %r \n EC_low_setpoint= %r \n" % (Water_high_setpoint, Water_low_setpoint, EC_high_setpoint, EC_low_setpoint)
        if raw_input(prompt) == 'y':
            with con:
                Manual_fill = 0
                cur = con.cursor()
                cur.execute("INSERT INTO Setpoints(Name, Value) VALUES ('Water_high_setpoint', ?);", (Water_high_setpoint, ))
                cur.execute("INSERT INTO Setpoints(Name, Value) VALUES ('Water_low_setpoint', ?);", (Water_low_setpoint, ))
                cur.execute("INSERT INTO Setpoints(Name, Value) VALUES ('EC_high_setpoint', ?);", (EC_high_setpoint, ))
                cur.execute("INSERT INTO Setpoints(Name, Value) VALUES ('EC_low_setpoint', ?);", (EC_low_setpoint, ))
                cur.execute("INSERT INTO Setpoints(Name, Value) VALUES ('Manual_fill', ?);", (Manual_fill, ))
            Setup_logger.info("Setpoints table updated with: \n Water_high_setpoint= %r \n Water_low_setpoint= %r \n" % (Water_high_setpoint, Water_low_setpoint))
            break
        print "Let's try again."

def Status_check():
	try:
		with con:
			cur = con.cursor()
			vendorname = cur.execute("SELECT Value FROM Gateway WHERE Name = ?;", ('Vendor_name', )).fetchone()[0]
			model = cur.execute("SELECT Value FROM Gateway WHERE Name = ?;", ('Model', )).fetchone()[0]
			sn1 = cur.execute("SELECT Value FROM Gateway WHERE Name = ?;", ('Serial', )).fetchone()[0]
			vendortoken = cur.execute("SELECT Value FROM Gateway WHERE Name = ?;", ('Vendor_token', )).fetchone()[0]
		Active_check = provision.serialnumber_info(vendortoken, model, sn1).body
		Active_check_list = Active_check.split(",")
		status = Active_check_list[0]
		with con:
			cur = con.cursor()
			if cur.execute("SELECT EXISTS(SELECT 1 FROM Gateway WHERE Name = ? LIMIT 1);", ("Status", )).fetchone()[0] != True:
				cur.execute("INSERT INTO Gateway(Name, Value) VALUES ('Status', ?);", (status, ))
			else:
				cur.execute("UPDATE Gateway SET Value =? WHERE Name=?;", (status, "Status",  ))
		return status
	except :
		print "status error"
		return "statuserror"

def Activate_device():
	print "Activating Device"
	with con:
		cur = con.cursor()
		vendorname = cur.execute("SELECT Value FROM Gateway WHERE Name = ?;", ('Vendor_name', )).fetchone()[0]
		model = cur.execute("SELECT Value FROM Gateway WHERE Name = ?;", ('Model', )).fetchone()[0]
		sn1 = cur.execute("SELECT Value FROM Gateway WHERE Name = ?;", ('Serial', )).fetchone()[0]
		vendortoken = cur.execute("SELECT Value FROM Gateway WHERE Name = ?;", ('Vendor_token', )).fetchone()[0]
	return provision.serialnumber_activate(model, sn1, vendorname).body

def Setup_timers(Device_CIK):
	vals_to_write = []
	with con:
		cur = con.cursor()
		cur.execute("SELECT Name, Length FROM Timers")
		Timers = cur.fetchall()
	for row in Timers:
		Dataport_alias = row[0].encode('ascii', 'ignore')
		Dataport_value = row[1]
		vals_to_write += [[{'alias': Dataport_alias}, Dataport_value]]
	try:
		o.writegroup(
			Device_CIK,
			vals_to_write)
	except OneException, exct:
		print exct

def Setup_setpoints(Device_CIK):
    vals_to_write = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT Name, Value FROM Setpoints")
        Timers = cur.fetchall()
    for row in Timers:
        Dataport_alias = row[0].encode('ascii', 'ignore')
        Dataport_value = row[1]
        vals_to_write += [[{'alias': Dataport_alias}, Dataport_value]]
    try:
        o.writegroup(
            Device_CIK,
            vals_to_write)
    except OneException, exct:
        print exct

def Startup():
	with con:
		cur = con.cursor()
		cur.execute("CREATE TABLE IF NOT EXISTS Modbus(Id INTEGER PRIMARY KEY, Name TEXT, Value INT)")
		cur.execute("CREATE TABLE IF NOT EXISTS Gateway(Id INTEGER PRIMARY KEY, Name TEXT, Value TEXT)")
		cur.execute("CREATE TABLE IF NOT EXISTS Sensors(Id INTEGER PRIMARY KEY, Alias TEXT, Address INT, DACN INT, Slope REAL, Intercept REAL)")
		cur.execute("CREATE TABLE IF NOT EXISTS Outputs(Id INTEGER PRIMARY KEY, Alias TEXT, Address INT, DACN INT)")
		cur.execute("CREATE TABLE IF NOT EXISTS Timers(Id INTEGER PRIMARY KEY, Name TEXT, Length REAL)")
        cur.execute("CREATE TABLE IF NOT EXISTS Setpoints(Id INTEGER PRIMARY KEY, Name TEXT, Value REAL)")

	while True:
		with con:
			cur = con.cursor()
			cur.execute("SELECT * FROM Modbus")
			if len(cur.fetchall()) > 1:
				Modbus_check = 1
			else:
				Modbus_check = 0
            
			cur.execute("SELECT * FROM Gateway")
			if len(cur.fetchall()) > 1:
				Gateway_check =1
			else:
				Gateway_check = 0

			cur.execute("SELECT * FROM Sensors")
			if len(cur.fetchall()) > 1:
				Sensors_check =1
			else:
				Sensors_check = 0

			cur.execute("SELECT * FROM Outputs")
			if len(cur.fetchall()) > 1:
				Outputs_check =1
			else:
				Outputs_check = 0
            
			cur.execute("SELECT * FROM Timers")
			if len(cur.fetchall()) > 1:
				Timers_check =1
			else:
				Timers_check = 0

			cur.execute("SELECT * FROM Setpoints")
			if len(cur.fetchall()) > 1:
				Setpoints_check =1
			else:
				Setpoints_check = 0

		if Modbus_check != 1 or Gateway_check != 1 or Sensors_check != 1 or Outputs_check != 1 or Timers_check != 1 or Setpoints_check != 1:# or GPIO.input(23) == 1:
			print "\nModbus config = %r \n Gateway config = %r \n Sensors config = %r \n Outputs config = %r \n Timers config = %r \n Setpoints config = %r" % (Modbus_check, Gateway_check, Sensors_check, Outputs_check, Timers_check, Setpoints_check)
			raw_input("Press Enter to continue...")
			Wall_config()
		else:
			if Status_check() == 'notactivated':
				Device_CIK = Activate_device()
				with con:
					cur = con.cursor()
					if cur.execute("SELECT EXISTS(SELECT 1 FROM Gateway WHERE Name = ? LIMIT 1);", ("Device_cik", )).fetchone()[0] != True:
						cur.execute("INSERT INTO Gateway(Name, Value) VALUES ('Device_cik', ?);", (Device_CIK, ))
					else:
						 cur.execute("UPDATE Gateway SET Value = ? WHERE Name = ?;", (Device_CIK,"Device_cik", ))
				Setup_timers(Device_CIK)
				Setup_setpoints(Device_CIK)
			break

if __name__ == '__main__':
	Startup()
# Todo list

# add in challenge to make sure entries are of the proper length
