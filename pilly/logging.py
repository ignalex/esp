import os
import time 

class LOG (object):
        "logger keeping N logs"
        def __init__(self,*args, **kargs):
            for k,v in kargs.items():
                setattr(self,k,v)
            if not hasattr(self,'log'): self.log = True
            if not hasattr(self,'keep'): self.keep = 3
            self.check_files()
            self.name = 'log0.txt'
            
        def __call__(self, *args, **kargs): 
            if len(args)>=1: 
                print(args[0]) 
                with open(self.name,'a') as f: 
                    f.write(str(time.time()).split('.')[0] + ' ' + args[0] + '\n')
                    
        def check_files(self): 
            for t in range(self.keep + 1, 0, -1): 
                ft = 'log'+str(t)+'.txt'
                fc = 'log'+str(t-1)+'.txt'
                if os.path.exists(ft): 
                    os.remove(ft)
                    print (f'{ft} removed')
                if os.path.exists(fc):
                    os.rename(fc,ft)
        def read(self): 
            if os.path.exists('log0.txt'): 
                for f in open('log0.txt', 'r').readlines(): 
                    print(f)
                
        
lg = LOG()