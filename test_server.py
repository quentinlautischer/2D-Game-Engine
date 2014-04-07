import sys, serial

# Some little helper functions to help ease readability
def initialize_serial(port, speed):
    ser = serial.Serial(port, speed)
    return ser

init_established = 0

if __name__ == "__main__":
	print("yo")
	ser = initialize_serial("Port_#0001.Hub_#0005", 9600)
    
	while 1:
		user_input = ser.read()
		print(user_input)
		keyStroke = user_input.decode(encoding='UTF-8')
		print(keyStroke)
		if keyStroke == 'D':
			print("Yes")
