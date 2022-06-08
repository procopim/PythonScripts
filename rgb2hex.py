def rgb_hex():
  invalid_msg = 'invalid values entered'
  red = int(raw_input('\nenter red value: '))
  if (red > 255 or red < 0):
    print invalid_msg
    return
  green = int(raw_input('\nenter green value: '))
  if (green > 255 or green < 0):
    print invalid_msg
    return
  blue = int(raw_input('\nenter blue value: '))
  if (blue > 255 or blue < 0):
    print invalid_msg
    return
  val = (red << 16)+(green << 8)+(blue)
  print hex(val)[2:].upper() + '\n'

def hex_rgb():
  hex_val = raw_input('\nenter a hexadecimal value\n')
  if (len(hex_val) != 6):
    print 'not a valid hex val'
    return
  else:
    hex_val = int(hex_val,16)

  two_hex_digits = 2**8
  blue = hex_val % two_hex_digits
  hex_val = hex_val >> 8
  green = hex_val % two_hex_digits
  hex_val = hex_val >> 8
  red = hex_val % two_hex_digits

  print "\nRed: %s Green: %s Blue: %s\n" % (red, green, blue)

def convert():
  while True:
    option = raw_input('Enter 1 to convert RGB to HEX. Enter 2 to convert HEX to RGB. Enter X to Exit:\n')
    
    if (option == '1'):
      print 'RGB to Hex...\n'
      rgb_hex()
    elif (option == '2'):
      print 'Hex to RGB...\n'
      hex_rgb()
    elif (option == 'X' or 'x'):
      print 'exit\n'
      break
    else:
      print 'Error'
  
convert()
    

    



  