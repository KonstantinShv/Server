import asyncio
import serial

async def handle_echo(reader, writer):
    
    global answer
    global flag
    global message
    while True:
        t = 0
        data = await reader.read(100)
        flag = 1
        message = data.decode()
        client_socket, addr = writer.get_extra_info('peername')
        if message == '':
            flag = 0
            print(f"Client {addr!r} unexpectedly disconnected")
            break           
            
        else:

            print(f"Received {message!r} from {addr!r}")
            while t == 0:
                try:            
#                     a = str(answer)
#                     b = '\n'
#                     c = a + b
#                     response = c.encode()
                    b = '\n'
                    almost_final_answer = answer + b
                    final_answer = almost_final_answer.encode()
                    print(f"Send: {answer!r}")
                    writer.write(final_answer)
                    await writer.drain()
                    t = 1
                    flag = 0
                    del answer
                
                except NameError:                
                    await asyncio.sleep(0.1)
                
            
            
async def counter():
    global answer
    global flag
    global message
    import serial
    import time
    flag = 0
      
    ser = serial.Serial(
    port ='COM1',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
        timeout=1)
    ser.close()
    ser.setRTS(0)

# Черт его знает, зачем оно здесь
    # first_channel = []
    # second_channel = []
    # third_channel = []
    # fourth_channel = []
    # fifth_channel = []
    # sixth_channel = [] 
    
    # Строки непрерывного чтения значения с теркона
    first_channel_values = '' 
    second_channel_values = ''
    third_channel_values = ''
    fourth_channel_values = ''
    fifth_channel_values = ''
    sixth_channel_values = ''

    # Строки чтения значений по запросу
    read_first_channel_values = ''
    read_second_channel_values = ''
    read_third_channel_values = ''
    read_fourth_channel_values = ''
    read_fifth_channel_values = ''
    read_sixth_channel_values = ''
    
    #Счетчики количества считаных значений
    count_1 = 0
    count_2 = 0
    count_3 = 0
    count_4 = 0
    count_5 = 0
    count_6 = 0
    
    
    while True:
                            
                
        await asyncio.sleep(0.1)
        ser.open()
        time.sleep(0.8)
        com_response = ser.readline(26) # Считываем значение с COM-порта
        ser.close()
        com_response_str = com_response.decode() # Переводим полученное значение из байтовой строки в обычную
        # Прибор посылает значения с каналов парами: 1-2, 3-4, 5-6. Мы читаем сразу два значения и разбиваем 
        # его на каналы. 
        com_response_num_ch_odd = com_response_str[1] # Определяем номер нечетного канала в паре канал, с которого получено значение
        com_response_num_ch_even = com_response_str[14] # Определяем номер четного канала в паре канал, с которого получено значение

        # Заполняем строки непрерывного чтения первым значением в ответе прибора
        if com_response_num_ch_odd == '1':
            first_channel_values = first_channel_values + com_response_str[3:12]
            count_1 += 1
            
        elif com_response_num_ch_odd == '2':
            second_channel_values = second_channel_values + com_response_str[3:12]
            count_2 += 1
            
        elif com_response_num_ch_odd == '3':
            third_channel_values = third_channel_values + com_response_str[3:12]
            count_3 += 1
            
        elif com_response_num_ch_odd == '4':
            fourth_channel_values = fourth_channel_values + com_response_str[3:12]
            count_4 += 1
            
        elif com_response_num_ch_odd == '5':
            fifth_channel_values = fifth_channel_values + com_response_str[3:12]
            count_5 += 1
            
        elif com_response_num_ch_odd == '6':
            sixth_channel_values = sixth_channel_values + com_response_str[3:12]
            count_6 += 1
        

        # Заполняем строки непрерывного чтения вторым значением в ответе прибора
        if com_response_num_ch_even == '1':
            first_channel_values = first_channel_values + com_response_str[16:25]
            count_1 += 1
            
        elif com_response_num_ch_even == '2':
            second_channel_values = second_channel_values + com_response_str[16:25]
            count_2 += 1
            
        elif com_response_num_ch_even == '3':
            third_channel_values = third_channel_values + com_response_str[16:25]
            count_3 += 1
            
        elif com_response_num_ch_even == '4':
            fourth_channel_values = fourth_channel_values + com_response_str[16:25]
            count_4 += 1
            
        elif com_response_num_ch_even == '5':
            fifth_channel_values = fifth_channel_values + com_response_str[16:25]
            count_5 += 1
            
        elif com_response_num_ch_even == '6':
            sixth_channel_values = sixth_channel_values + com_response_str[16:25]
            count_6 += 1
            
        
            
            
        # Если в строке записано 150 значений - обнуляем строку    
        if count_1 == 150:
            first_channel_values = ''
            count_1 = 0
            
        elif count_2 == 150:
            second_channel_values = ''
            count_2 = 0
            
        elif count_3 == 150:
            third_channel_values = ''
            count_3 = 0
            
        elif count_4 == 150:
            fourth_channel_values = ''
            count_4 = 0
            
        elif count_5 == 150:
            fifth_channel_values = ''
            count_5 = 0
            
        elif count_6 == 150:
            sixth_channel_values = ''
            count_6 = 0
            
        
        
        # Если пришел запрос от клиента - обрабатываем
        if flag == 1:
            
            decode_message = message
            
            # Обнуление строк непрерывного чтения
            if decode_message == 'reset\n':
                first_channel_values = ''
                second_channel_values = ''
                third_channel_values = ''
                fourth_channel_values = ''
                fifth_channel_values = ''
                sixth_channel_values = ''
                answer = 'Done!'

            #  Получение значений с определенного канала из строки непрерывного чтения   
            elif decode_message == 'get_ch1_values\n':
                answer = first_channel_values
                
            elif decode_message == 'get_ch2_values\n':
                answer = second_channel_values
                
            elif decode_message == 'get_ch3_values\n':
                answer = third_channel_values
                
            elif decode_message == 'get_ch4_values\n':
                answer = fourth_channel_values
                
            elif decode_message == 'get_ch5_values\n':
                answer = fifth_channel_values
                
            elif decode_message == 'get_ch6_values\n':
                answer = sixth_channel_values

            # Получение заданного числа значений с определенного канала в реальном времени    
            elif decode_message[0:8] == 'read_ch1': #пример - read_ch1_030_values
                i_1 = int(decode_message[9:12]) # Определяем количесвто запрошенных значений
                j_1 = 0
                while j_1 != i_1: # Считываем значения с прибора, пока не наберется необходимое количество значений с нужного канала
                    await asyncio.sleep(0.1)
                    ser.open()
                    time.sleep(0.8)
                    read_com_1 = ser.readline(26) # Получаем значение с прибора
                    ser.close()
                    read_com_1_str = read_com_1.decode() # Переводим из байтовой строки в обычную
                    read_com_1_num_ch_odd = read_com_1_str[1] # Определяем номер канала
                    read_com_1_num_ch_even = read_com_1_str[14]

                    # Записываем в строку значения только с нужного канала
                    if read_com_1_num_ch_odd == '1':
                        read_first_channel_values = read_first_channel_values + read_com_1_str[3:12]
                        j_1 +=1

                    elif read_com_1_num_ch_even == '1':
                        read_first_channel_values = read_first_channel_values + read_com_1_str[16:25]
                        j_1 +=1 
                    
                answer = read_first_channel_values # Передаем строку для отправки клиенту
                time.sleep(0.1)
                read_first_channel_values = ''
                
            elif decode_message[0:8] == 'read_ch2': #пример - read_ch1_030_values
                i_2 = int(decode_message[9:12])
                j_2 = 0
                while j_2 != i_2:
                    await asyncio.sleep(0.1)
                    ser.open()
                    time.sleep(0.8)
                    read_com_2 = ser.readline(26)
                    ser.close()
                    read_com_2_str = read_com_2.decode()
                    read_com_2_num_ch_odd = read_com_2_str[1] # Определяем номер канала
                    read_com_2_num_ch_even = read_com_2_str[14]
        
                    if read_com_2_num_ch_odd == '2':
                        read_second_channel_values = read_second_channel_values + read_com_2_str[3:12]
                        j_2 +=1
                    elif read_com_2_num_ch_even == '2':
                        read_second_channel_values = read_second_channel_values + read_com_2_str[16:25]
                        j_2 +=1
                    
                answer = read_second_channel_values
                time.sleep(0.1)
                read_second_channel_values = ''
            
            elif decode_message[0:8] == 'read_ch3': #пример - read_ch1_030_values
                i_3 = int(decode_message[9:12])
                j_3 = 0
                while j_3 != i_3:
                    await asyncio.sleep(0.1)
                    ser.open()
                    time.sleep(0.8)
                    read_com_3 = ser.readline(26)
                    ser.close()
                    read_com_3_str = read_com_3.decode()
                    read_com_3_num_ch_odd = read_com_3_str[1]
                    read_com_3_num_ch_even = read_com_3_str[14]
        
                    if read_com_3_num_ch_odd == '3':
                        read_third_channel_values = read_third_channel_values + read_com_3_str[3:12]
                        j_3 +=1
                    if read_com_3_num_ch_even == '3':
                        read_third_channel_values = read_third_channel_values + read_com_3_str[16:25]
                        j_3 +=1    
                    
                answer = read_third_channel_values
                time.sleep(0.1)
                read_third_channel_values = ''
                
            elif decode_message[0:8] == 'read_ch4': #пример - read_ch1_030_values
                i_4 = int(decode_message[9:12])
                j_4 = 0
                while j_4 != i_4:
                    await asyncio.sleep(0.1)
                    ser.open()
                    time.sleep(0.8)
                    read_com_4 = ser.readline(26)
                    ser.close()
                    read_com_4_str = read_com_4.decode()
                    read_com_4_num_ch_odd = read_com_4_str[1]
                    read_com_4_num_ch_even = read_com_4_str[14]
        
                    if read_com_4_num_ch_odd == '4':
                        read_fourth_channel_values = read_fourth_channel_values + read_com_4_str[3:12]
                        j_4 +=1
                    elif read_com_4_num_ch_even == '4':
                        read_fourth_channel_values = read_fourth_channel_values + read_com_4_str[16:25]
                        j_4 +=1
                    
                answer = read_fourth_channel_values
                time.sleep(0.1)
                read_fourth_channel_values = ''
            
            
            elif decode_message[0:8] == 'read_ch5': #пример - read_ch1_030_values
                i_5 = int(decode_message[9:12])
                j_5 = 0
                while j_5 != i_5:
                    await asyncio.sleep(0.1)
                    ser.open()
                    time.sleep(0.8)
                    read_com_5 = ser.readline(26)
                    ser.close()
                    read_com_5_str = read_com_5.decode()
                    read_com_5_num_ch_odd = read_com_5_str[1]
                    read_com_5_num_ch_even = read_com_5_str[14]
        
                    if read_com_5_num_ch_odd == '5':
                        read_fifth_channel_values = read_fifth_channel_values + read_com_5_str[3:11]
                        j_5 +=1
                    if read_com_5_num_ch_even == '5':
                        read_fifth_channel_values = read_fifth_channel_values + read_com_5_str[16:25]
                        j_5 +=1
                    
                answer = read_fifth_channel_values
                time.sleep(0.1)
                read_fifth_channel_values = ''
            
            elif decode_message[0:8] == 'read_ch6': #пример - read_ch1_030_values
                i_6 = int(decode_message[9:12])
                j_6 = 0
                while j_6 != i_6:
                    await asyncio.sleep(0.1)
                    ser.open()
                    time.sleep(0.8)
                    read_com_6 = ser.readline(26)
                    ser.close()
                    read_com_6_str = read_com_6.decode()
                    read_com_6_num_ch_odd = read_com_6_str[1]
                    read_com_6_num_ch_even = read_com_6_str[14]
        
                    if read_com_6_num_ch_odd == '6':
                        read_sixth_channel_values = read_sixth_channel_values + read_com_6_str[3:11]
                        j_6 +=1
                    if read_com_6_num_ch_even == '6':
                        read_sixth_channel_values = read_sixth_channel_values + read_com_6_str[16:25]
                        j_6 +=1
                    
                answer = read_sixth_channel_values
                time.sleep(0.1)
                read_sixth_channel_values = ''
                
            

            else:
                answer = 'incorrect input arguments'
                       
            
            flag = 0
            
loop = asyncio.get_event_loop()
asyncio.ensure_future(counter())
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
#print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()

