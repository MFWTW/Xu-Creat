import struct 
import serial.tools.list_ports
from time import sleep


  
ser = serial.Serial('COM11', 9600)  
serial_rx_len = 2  

def Serial_Tx(x,y):  
    try:  
        # 打包前先计算校验和：从 0x2C 到 flag 的所有数据
        
        data = struct.pack("<BBBB", 0xFF,x,y,0xFE) 
        
        print("发送数据:", data.hex())
        
        ser.write(data)  
        print(data.hex())  # 打印发送数据的十六进制表示  
    except KeyboardInterrupt:  
        print('KeyboardInterrupt')  
    except Exception as e:  
        print("Exception:", e)  
  
  
if __name__ == '__main__':  
    for i in range(10000):
        Serial_Tx(0,30)
        sleep(1)
        Serial_Tx(1,40)
        sleep(1)
        Serial_Tx(2,50)
        sleep(1)
        Serial_Tx(0,30)
        sleep(1)
        Serial_Tx(1,40)
        sleep(1)
        Serial_Tx(2,50)
        sleep(1)
