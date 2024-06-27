# -*- coding: UTF-8 -*-
# Public package
# Private package
# Internal package

class Filler:
    def __init__(self, **argv):
        '''
        fill_block: 填充字符
        fill_loc: 填充位置 ['left', 'l', 'center', 'c', 'right', 'r']
        fill_length: 填充长度 [None:不填充, -1:动态填充, >=0:固定填充]
        '''
        # block
        if ('fill_block' in argv):
            self.block = argv['fill_block']
        else:
            self.block = ' '
        assert (len(self.block) == 1), 'block length must be 1'
        # loc
        if ('fill_loc' in argv):
            if (argv['fill_loc'] in ['center', 'c']):
                self.loc = 'c'
            elif (argv['fill_loc'] in ['left', 'l']):
                self.loc = 'l'
            elif (argv['fill_loc'] in ['right', 'r']):
                self.loc = 'r'
            else:
                raise ValueError("loc must be in ['left', 'l', 'center', 'c', 'right', 'r']")
        else:
            self.loc = 'c'
        # length
        if ('fill_length' in argv):
            self.length = argv['fill_length']
        else:
            self.length = None

    def fill(self, value):
        output = value
        if (self.length is not None):
            if (self.loc in ['left', 'l']):
                while (len(output) < self.length):
                    output = output + self.block
            elif (self.loc in ['right', 'r']):
                while (len(output) < self.length):
                    output = self.block + output
            else:
                while (len(output) < self.length):
                    if (len(output) % 2 == 0):
                        output = self.block + output
                    else:
                        output = output + self.block
            if (self.length < len(output)):
                output = output[:self.length]
        return output
