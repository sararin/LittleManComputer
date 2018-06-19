class Parse:
  def __init__(self, codeToParse):
    self.codeToParse = codeToParse
    self.replace = {'ADD':"1", 'SUB':"2", 'STA':"3", 'LDA':"5", 'BRA':"6", 'BRZ':"7", 'BRP': "8", 'INP': "9", 'DAT': "0"}

  def _createDict(self, code):
    repl = {}
    for y, x  in enumerate(code):
      if len(x) == 3:
        repl[x.pop(0)] = str(y)
    return repl

  def _useDict(self, dct, code):
    for x in code:
      if x[-1] in dct:
        x[-1] = dct[x[-1]]
    return code

  def _replaceOpcodes(self, code):
    for x in code:
      x[0] = self.replace[x[0]]
      if len(x[1]) < 2:
        x[1] = "0"+x[1]
    return code

  def _parse(self, code):
    code = code.split('\n')
    code = list( map(lambda x: x.split(' '), code) )
    code = self._replaceOpcodes( self._useDict( self._createDict(code), code) )
    final = ' '.join(map(''.join, code))
    return final.split(' ')
  
  def getResult(self):
    return self._parse(self.codeToParse)

class LMC:
  def __init__(self, memory):
    self.memory = memory
    self.PC = 0
    self.acc = 0
    self.opcodes = {"1": self._ADD, "2": self._SUB, "5": self._LDA, "6": self._BRA, "7": self._BRZ, "8": self._BRP}

  def _ADD(self, b):
    return int(self.acc) + int(self.memory[b])

  def _SUB(self, b):
    return self.acc - self.memory[b]

  def _LDA(self, b): #same thing as BRA
    return self.memory[b]

  def _BRA(self, b):
    return b

  def _BRZ(self, b):
    if int(self.acc) == 0:
      return b
    else:
      return self.PC +1

  def _BRP(self, b):
    if int(self.acc) != 0:
      return b
    else:
      return self.PC + 1

  def interpret(self):
    while True:
      instruction = self.memory[self.PC][0]
      memAddress = int( ''.join(self.memory[self.PC][1:]) )
      print(self.memory)
      if instruction in "125": # ADD SUB LDA
        self.acc = self.opcodes[instruction](memAddress)
      elif instruction == "3": #STA
        self.memory[memAddress] = self.acc
        self.acc = 0
      elif instruction in "04": #HLT
        break
      elif instruction in "678": #BRA BRZ BRP
        self.PC = self.opcodes[instruction](memAddress) - 1
      elif instruction == "9": #IN and OUT
        if memAddress == 1:
          self.acc = input(">").rjust(3, "0")[-3:]
        else:
          print(self.acc)
      else: #everything else
        raise NameError("Unknown instruction "+self.instruction+" at "+self.PC+" address") #all bugs go here
      self.PC += 1

def openCode(file):
  with open(file, "r") as f:
    data = f.read()
  return data

def writeToMemory(code):
  howMuchAdd = abs(len(code) - 100)
  code += ["000"]*howMuchAdd
  return code

if __name__ == "__main__":
  from sys import argv
  script, first = argv
  co = openCode(first)
  parser = Parse(co)
  mashine = LMC(  writeToMemory(parser.getResult()) )
  mashine.interpret()
