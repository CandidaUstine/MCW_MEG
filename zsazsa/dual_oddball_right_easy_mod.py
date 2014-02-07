def copyfile(source, dest, buffer_size=1024*1024):
    if not hasattr(source, 'read'):
        source = OrgFile
    if not hasattr(dest, 'write'):
        dest = OutputFile
    while 1:
        copy_buffer = source.read(buffer_size)
        if copy_buffer:
            dest.write(copy_buffer)
        else:
            break
    source.close
    dest.close

OrgFile = open ('run05_dual_oddball_right_raw.eve', 'rb')
OutputFile = open('run05_dual_oddball_right_raw' + '_mod' + '.eve', 'wb')


def simple_modify_file(file_name_in):
    sd_list = []
    resp_list = []
    seq_num = -1

    with open(file_name_in, 'r') as input_file_obj:
            lines = input_file_obj.readlines()

    for line in lines:
        magic_part = line.strip().split()
        tagnum = int(magic_part[3])
        if tagnum == 102:
            sd_list.append(0)  # 0 = standard block
            resp_list.append(0)
            seq_num += 1
        elif tagnum == 202:
            sd_list.append(1) # 1 = deviant block
            resp_list.append(0)
            seq_num += 1
        elif tagnum > 16410 and tagnum < 16420:
            resp_list[seq_num] = 1 # 1 = answered yes to hearing deviant
        elif tagnum == 32768:
            resp_list[seq_num] = 2 # 2 = answered no to hearing deviant

    seq_num = -1
    insequence = False
    with open('run05_dual_oddball_right_raw_mod.eve', 'w') as output_file_obj:
        for line in lines:
            magic_part = line.strip().split()
            newtagnum = int(magic_part[3])
            output_file_obj.write(magic_part[0] + ' ')
            output_file_obj.write(magic_part[1] + ' ')
            output_file_obj.write(magic_part[2] + ' ')

            if newtagnum == 102 or newtagnum == 202:
                seq_num += 1
                insequence = True
                
            newtagnum2 = newtagnum
            if insequence:
                if newtagnum >= 99 and newtagnum <= 120: # standard sequence 
                    if sd_list[seq_num] == 0:
                        if resp_list[seq_num] == 2:
                            newtagnum2 = 100 # answered no to hearing deviant and is incorrect 
                        elif resp_list[seq_num] == 1:
                            newtagnum2 = 200 # answered yes to hearing deviant and is correct 

                elif newtagnum >= 200 and newtagnum <= 220: # deviant sequence
                    if sd_list[seq_num] == 1:
                        if resp_list[seq_num] == 2:
                            newtagnum2 = 500 # answered no to hearing deviant and is correct 
                        elif resp_list[seq_num] == 1:
                            newtagnum2 = 400 # answered yes to hearing deviant and is incorrect 
                        
                elif newtagnum == 3:
                    if sd_list[seq_num] == 1:
                        if resp_list[seq_num] == 1:
                            newtagnum2 = 3 # 3 = correctly heard deviant 
                        elif resp_list[seq_num] == 2:
                                newtagnum2 = 4 # 4 = incorrectly heard deviant
                        elif resp_list[seq_num] == 0:
                            newtagnum2 = 5 # 5 = no response
            else:
                if newtagnum < 1000:
                    newtagnum2 = 0

            if newtagnum == 120 or newtagnum == 220:
                    insequence = False
                    
            output_file_obj.write(str(newtagnum2) + "\n")                   
                
        output_file_obj.close()

copyfile(OrgFile,OutputFile)
OrgFile.close()
OutputFile.close()  
simple_modify_file('run05_dual_oddball_right_raw_mod.eve')
