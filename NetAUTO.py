class AutoNetwork:
    def __init__(self):
        self.os = __import__('os')
        self.dt = __import__('datetime')
        self.outer_f = 'main'
        self.inner_f = ['input_f','output_f']
        self.input_txt = {'#splitNetHost':list(),'#netHostAdd':list(),'#findHostBroad':list()}
        self.main_dir = self.os.getcwd()
        self.def_mask = ('255.0.0.0','255.255.0.0','255.255.255.0')
    def check_dir(self):
        try:
            print(self.os.getcwd())
            self.os.chdir(self.os.path.join(self.main_dir,self.outer_f))
            if self.inner_f == self.os.listdir(self.os.getcwd()):
                return True
            else:
                self.os.chdir(self.os.path.dirname(self.os.getcwd()))
                self.os.rmdir(self.os.path.join(self.os.getcwd(),self.outer_f))
                print(self.outer_f in self.os.listdir(self.os.getcwd()))
                return False
        except FileNotFoundError:
            return False
        
    def set_dir(self):
        self.os.mkdir(self.os.path.join(self.os.getcwd(),self.outer_f))
        self.os.chdir(self.os.path.join(self.os.getcwd(),self.outer_f))
        for i in self.inner_f:
            self.os.mkdir(self.os.path.join(self.os.getcwd(),i))
        self.os.chdir(self.os.path.dirname(self.os.getcwd()))
        print('set_dir--'+self.os.getcwd())
            
    def read_txt(self,txtname,inp_dir):
        switch_inp = [0,0,0]
        with open(self.os.path.join(inp_dir,txtname),'r') as file:
            for i in file.readlines():
                if i.strip() in self.input_txt.keys():
                    switch_inp[list(self.input_txt.keys()).index(i.strip())] += 1
                    continue
                if sum(switch_inp)==1:
                    self.input_txt[list(self.input_txt.keys())[0]].append(i.strip())
                elif sum(switch_inp)==2:
                    self.input_txt[list(self.input_txt.keys())[1]].append(i.strip())
                elif sum(switch_inp) == 3:
                    self.input_txt[list(self.input_txt.keys())[2]].append(i.strip())
        return txtname
                
    def split_netHost(self,main_address):
        if int(main_address.split('.')[0]) in list(range(1,128)):
            return (main_address.split('.')[0],main_address.split('.')[1:])
        elif int(main_address.split('.')[0]) in list(range(128,192)):
            return (main_address.split('.')[:2],main_address.split('.')[2:])
        elif int(main_address.split('.')[0]) in list(range(192,224)):
            return (main_address.split('.')[:3],main_address.split('.')[-1])
    
    def return_netAdd(self,host_add,sub_mask):
        ha = host_add.split('.')
        sm = sub_mask.split('.')
        tmp = ''
        na_d = ''
        for a,b in zip(ha,sm):
            a_f = bin(int(a)).replace('0b','')
            b_f = bin(int(b)).replace('0b','')
            if len(bin(int(a)).replace('0b','')) != 8:
                a_f = ((8-len(bin(int(a)).replace('0b','')))*'0') + bin(int(a)).replace('0b','')
            if len(bin(int(b)).replace('0b','')) != 8:
                b_f = ((8-len(bin(int(b)).replace('0b','')))*'0') + bin(int(b)).replace('0b','')
            for x,y in zip(a_f,b_f):
                if (x == '1') & (y=='1'):
                    tmp += '1'
                else:
                    tmp += '0'
            na_d+=str(int(tmp,2))
            na_d+='.'
            tmp = ''
        return na_d
    
    def return_hostAdd(self,host_add,na_add):
        cm = na_add[:-1].split('.').index('0')
        ha_d = cm*'0.'
        ha_t=''
        for a,i in enumerate(host_add.split('.')[cm:]):
            ha_t += i +'.'
        return ha_d+ha_t

    def default_sm(self,host_add):
        ac = int(host_add.split('.')[0])
        if ac in list(range(1,218)):
            return self.def_mask[0]
        elif ac in list(range(128,192)):
            return self.def_mask[1]
        elif ac in list(range(192,223)):
            return self.def_mask[2]
        
    def ret_hostNet(self,host_add,sub_mask):
        if sub_mask == None:
            sub_mask = self.default_sm(host_add)
        return (self.return_hostAdd(host_add,self.return_netAdd(host_add,sub_mask)), self.return_netAdd(host_add,sub_mask))
    
    def find_hostBroad(self,host_add,sub_mask):
        fhb = []
        for ba in range(0,2):
            ba=str(ba)
            start_split = 0
            slash_tag = 0
            switch = 1
            host_f = ''
            for i in sub_mask.split('.'):
                if i == '255':
                    slash_tag += 8
                else:
                    try:
                        init = (8-len(bin(int(i)).replace('0b','')))*'0' + bin(int(i)).replace('0b','')
                        slash_tag+=init.index('0')
                        break
                    except ValueError:
                        continue
                
            for a,x in enumerate(host_add.split('.')):
                if slash_tag >=8:
                    slash_tag-=8
                    host_f+=x+'{dot}'.format(dot='.' if a != 3 else '')
                elif slash_tag <=0:
                    host_f+='0'+'{dot}'.format(dot='.' if a != 3 else '')
                else:
                    curAd=(8-len(bin(int(x)).replace('0b','')))*'0'+bin(int(x)).replace('0b','')
                    host_f+=str(int(curAd[:slash_tag] + (8-len(curAd[:slash_tag]))*ba,2))+'{dot}'.format(dot='.' if a != 3 else '')
            
            fhb.append(host_f)
            new = ''
            if ba == '0':
                for i in host_f.split('.')[:-1]:
                    new+=i+'.'
                new+= str(int(host_f.split('.')[-1])+1)
            else:
                for i in host_f.split('.')[:-1]:
                    new+=i+'.'
                new+=str(int(host_f.split('.')[-1])-1)
            fhb.append(new)
        return fhb
    
    def rel_output(self,retname,out_dir):
        retname = 'out-{txt}'.format(txt=retname)
        for x in self.input_txt.keys():
            if x == list(self.input_txt.keys())[0]:
                with open(self.os.path.join(out_dir,retname),'a+') as file:
                    file.write(x+'\n')

                if self.input_txt[x] == ['']:
                    continue
                for i in self.input_txt[x]:
                    if i == '':
                        continue
                    with open(self.os.path.join(out_dir,retname),'a+') as file:
                        snh = self.split_netHost(i)
                        file.write('M-Network Address: {na} \nM-Host Address: {ha}\n \n'.format(na=snh[0],ha=snh[1]))
                    
            if x == list(self.input_txt.keys())[1]:
                with open(self.os.path.join(out_dir,retname),'a+') as file:
                    file.write(x+'\n')
                if self.input_txt[x] == ['']:
                    continue
                for i in self.input_txt[x]:
                    if i == '':
                        continue
                    with open(self.os.path.join(out_dir,retname),'a+') as file:
                        try:
                            hana = self.ret_hostNet( i.split(',')[0], i.split(',')[1])
                        except IndexError:
                            hana = self.ret_hostNet(i,None)
                        
                        file.write('Host Address: {ha} \nNetwork Address: {na} \n \n'.format(ha=hana[0],na=hana[1]))
                        
            if x == list(self.input_txt.keys())[2]:
                with open(self.os.path.join(out_dir,retname),'a+') as file:
                    file.write(x+'\n')
                if self.input_txt[x] == ['']:
                    continue
                for i in self.input_txt[x]:
                    if i == '':
                        continue
                    with open(self.os.path.join(out_dir,retname),'a+') as file:
                        hb = self.find_hostBroad(i.split(',')[0],i.split(',')[1])
                        file.write('Network Address(Host=0): {na} \n1st Address: {first} \nLast Address: {last} \nBroadcast Address(Host=1): {ba} \n \n'.format(na=hb[0],first=hb[1],last=hb[3],ba=hb[2]) )

    def main(self):
        inp_dir = self.os.path.join(self.main_dir,self.outer_f + '\\'+self.inner_f[0])
        out_dir = self.os.path.join(self.main_dir,self.outer_f + '\\'+self.inner_f[1])
        if self.check_dir() == False:
            print('Setting up folder workspace...')
            self.set_dir()
        
        while True:
            user_inp = input('Please specify what you would like to do? File upload [0] or direct input[1]? \n')
            if int(user_inp):
                for a,b in zip(self.input_txt.keys(),['a. ','b. ','c. ']):
                    print(b+a)
                user2 = input('Choose what you would like to do?')
                if 'a,b,c'.split(',').index(str(user2).strip()) == 0:
                    address = input('Enter the IP address: \n')
                    snh = self.split_netHost(address)
                    print('M-Network Address: {na} \nM-Host Address: {ha}\n'.format(na=snh[0],ha=snh[1]))
                    
                elif 'a,b,c'.split(',').index(str(user2)) == 1:
                    ha = str(input('Enter Host IP Address: \n'))
                    sm = str(input('Enter Subnet Mask: \n'))
                    if sm == '':
                        hana = self.ret_hostNet(ha,None)
                    hana = self.ret_hostNet(ha,sm)
                    
                    print('Host Address: {ha} \nNetwork Address: {na} \n'.format(ha=hana[0],na=hana[1]))
                elif 'a,b,c'.split(',').index(str(user2)) == 2:
                    ha = str(input('Enter Host IP Address: \n'))
                    sm = str(input('Enter Subnet Mask: \n'))
                    hb = self.find_hostBroad(ha,sm)
                    print(hb)
                    print('Network Address(Host=0): {na} \n1st Address: {first} \nLast Address: {last} \nBroadcast Address(Host=1): {ba} \n'.format(na=hb[0],first=hb[1],last=hb[3],ba=hb[2]) )
            else:
                print('\n')
                for i in self.os.listdir(inp_dir):
                    print(i+'\n')
                txtfile = input('Choose which file to read: \n')
                if txtfile == '':
                    self.main()
                if txtfile not in self.os.listdir(inp_dir):
                    print('File not present.')
                    self.main()
                self.rel_output(self.read_txt(txtfile,inp_dir),out_dir)
                print('Check the output file in: {dest}'.format(dest=out_dir))
                
            
if __name__ == '__main__':
    app = AutoNetwork()
    app.main()
