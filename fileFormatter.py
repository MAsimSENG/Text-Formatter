import sys
class UVroff:
    
    def __init__(self, filename, other=None):   
        f = open(filename, 'r')   

        self.fn=f  
        self.ulist=[]
        self.alist=[]
        self.opts = {'FT':0, 'LW':0, 'LM':0, 'LS':0 }
        self.states = {'LastN':0, 'blankline':0, 'pagelength':0 , 'LastL':0}
        self.temps = ""
        self.x=0
        
        for line in self.fn: 
            line = line.strip("\n")
            self.ulist.append(line) 
            
    """ Format function takes an index of the unformatted line 
        then processes it to update opts or to add another word to formatted list """
     
    
    def format(self,index):
        self.x +=1
        temp = index.split()
        
                
        try:
            if ".LW" in temp[0]:
            #Check if LW first word assign value or raise exception if invalid value  
                try:
                    self.opts['LW'] =  int(temp[1])
                    self.opts['FT'] = 1 
                    return None 
                except: 
                    sys.exit("LW only accepts positive integers ")
        
            if ".LM" in temp[0]:
                try:
                    #LM can be updated by adding, subtracting. Must be 20 lessthan LW
                    # can replace this implementation with a switch case statement
                    if "-" in temp[1]:
                         self.opts['LM'] =self.opts['LM'] + int(temp[1])
                         if(self.opts['LM'] < 0):
                              self.opts['LM']=0
                              return None
                         if(self.opts['LM'] > (self.opts['LW'] - 20)):
                            self.opts['LM']=self.opts['LW'] -20 
                         return None
                    
                    if "+" in temp[1]:
                        self.opts['LM'] = self.opts['LM'] + int(temp[1])
                        if(self.opts['LM'] < 0):
                            self.opts['LM']=0
                            return None
                        if(self.opts['LM'] > self.opts['LW'] - 20):
                            self.opts['LM']= self.opts['LW']-20 
                        return None
                   
                    self.opts['LM'] = int(temp[1])            
                    if(self.opts['LM'] < 0):
                        self.opts['LM']=0
                        return None
                    
                    if(self.opts['LM'] > (self.opts['LW'] - 20)):
                        self.opts['LM']= self.opts['LW']-20 
                    return None
               
                except:
                    sys.exit("LM accepts integers only" )

            if ".LS" in temp[0]:
                #Linespace upto 2 line spaces possible 
                try:
                    if int(temp[1])>2 or int(temp[1]) <0:
                        raise
                    self.opts['LS'] = int(temp[1])
                    return None 
                except:
                    sys.exit("LS accepts integers  between 0 and 2" )
        
        # check if formatting should be on or off
            if ".FT" in temp [0]:
                try:
                    if temp[1]!= "off" or temp[1]!="on":                       
                        raise 
                    if "off" in temp[1]:
                        self.opts['FT']= 0
                        return None 
                    if "on" in temp[1]:
                        self.opts['FT']=1
                        return None
                except:
                    sys.exit("FT accepts on or off string only" )
                    
        except IndexError:
            #this error occours because of a blank line, if formatting is off just append a blank line to the output list
            if self.opts['FT']==0:
                self.alist.append(index)
                return None
            #if formatting is on and there is a blank line, append the temp until now and create a new line 
            self.alist.append(self.temps) 
            self.temps =""
            self.states['pagelength']=0
            #self.alist.append(index) 
            self.states['blankline']=1
            #this also incldues the case when FT is off and an empty line is being put as index 
            return None       
        
        if self.opts['FT'] ==0 :
            if self.states['LastL']==1:
                self.alist.append(index)
                return None
            index = index.strip('\n')
            self.alist.append(index)

            return None
  
        
        if self.opts['FT'] ==1:
        
            
            for word in temp:
                self.states['pagelength'] += len(word)
               
                if(self.states['blankline']==1): 
                    if(self.opts['LS'] ==0):
                        pass
                    if(self.opts['LS']!=0 ):
                        for i in range(0, self.opts['LS']):
                            self.alist.append("\n")
                    
                  
                    if(self.opts['LM']!=0):
                        for i in range(0,self.opts['LM']):
                            self.temps+=" "
                    
                    self.states['pagelength'] += self.opts['LM']   
                
                    self.temps+=word
                    self.states['blankline']=0
                    if self.states['LastL']==1 and word==temp[-1]:
                            self.alist.append(self.temps)
                            self.temps =""
                    continue
                
         

                
                
                if(self.states['pagelength']==len(word)):  
                     if(self.opts['LM']!=0):
                        for i in range(0,self.opts['LM']):
                            self.temps += " "
                        self.states['pagelength'] += self.opts['LM']
                     self.temps+=word
                     if self.states['LastL'] and word==temp[-1]:
                        self.alist.append(self.temps)
                        self.temps =""
                        continue
                    
                     continue
            
                
                     
           
                
                
                if self.states['pagelength'] < self.opts['LW']:
                    self.temps+=" "
                    self.temps+=word
                    self.states['pagelength']+=1
     
                    if self.states['LastL'] and word==temp[-1]:
                        self.alist.append(self.temps)
                        self.temps =""
                        continue
                    continue
           
            
                
                if self.states['pagelength'] >=self.opts['LW'] :                
                    self.states['pagelength']=0
                    self.alist.append(self.temps) 
                    self.temps=""
                    if(self.opts['LS'] ==0):
                        pass
                    if(self.opts['LS'] !=0 ):
                        for i in range(0, self.opts['LS']):
                            self.alist.append("")
                    if(self.opts['LM']!=0):
                        for i in range(0,self.opts['LM']):
                            self.temps+=" "
                        self.states['pagelength'] = self.opts['LM']
                    self.temps += word
                    self.states['pagelength']+=len(word)
                    if self.states['LastL']==1 and word==temp[-1]:
                        self.alist.append(self.temps)
                        self.temps =""
                      
            return None  
        
        
    def get_lines(self):
        #print("This is the lis the ulist: ", self.ulist)
       
       for index in self.ulist:                # loop through the entire unformatted file, index is a single unformatted line in the file
           if self.x == len(self.ulist)-1:    # if it is the last lane
               self.states['LastL']=1         # set the last line state to true
                 
           if( index == ""):                      # if the current line is empty
               self.states['pagelength']=0            # set the pagelength state to 0
               self.alist.append(self.temps)          # append all the words current in temp to the alist
               self.temps = ""                        # make temp empty
               self.states['blankline']=1

           self.format(index)
        
            
            
        #print(self.alist)
    
           
        return self.alist           
if  __name__ =='__main__':
    filename =sys.argv[1]   
    a1= UVroff(filename)
    lines= a1.get_lines()
    for l in lines:
        print(l)    
