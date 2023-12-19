import sys

class BofStatVariable:
    def __init__(self):
        self._reset()
        
    def _reset(self)->None:
        self.crt=0
        self.min=sys.maxsize
        self.max=-sys.maxsize-1
        self.mean=0
        self.mean_acc=0
        self.nb_sample=0
    
    def Bof_ResetStatVar(self)->None:    
        self._reset()
        
    def Bof_UpdateStatVar(self, val:int)->None:
        self.crt = val
        if (self.nb_sample == 0):
            self.min = val
            self.max = val
        else:
            if (val < self.min):
                self.min = val
            if (val > self.max):
                self.max = val
        self._Bof_UpdateStatMean()

    def _Bof_UpdateStatMean(self)->None:
        temp_accumulator = self.mean_acc + self.crt
        roll_over = (temp_accumulator > sys.maxsize)
        if not roll_over:
            self.mean_acc = temp_accumulator
            self.nb_sample = self.nb_sample + 1
            roll_over = (self.nb_sample == 0)
  
        if roll_over:
            self.mean_acc = self.mean
            self.nb_sample = 1
            
        self.mean = self.mean_acc / self.nb_sample