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
                if self.log:  
                    with open(self.name,'a') as f: 
                        f.write(str(time.time()).split('.')[0] + ' ' + args[0] + '\n')
                    f.close()
                    
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
                with open('log0.txt', 'r') as f: 
                    for l in f.readlines(): 
                        print(l)
                f.close()
                
if __name__ == '__main__':         
    lg = LOG(log=False)
    #lg('test1')