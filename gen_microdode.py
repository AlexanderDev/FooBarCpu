# Logism seven segments indicator
#  0 1 2 3 4 5 6 7 - bits
# |G|F|A|B|E|D|C|DB|

SEGMENT_CODE = {
	'A':2,
	'B':3,
	'C':6,
	'D':5,
	'E':4,
	'F':1,
	'G':0,
	'DB':7
}

DIGIT_CODE = {
	0:[],
	1:['B', 'C'],
	2:['A', 'B', 'D', 'E', 'G'],
	3:['A', 'B', 'C', 'D', 'G'],
	4:['B', 'C', 'F', 'G'],
	5:['A', 'C', 'D', 'F', 'G'],
	6:['A', 'C', 'D', 'E', 'F', 'G'],
	7:['A', 'B', 'C'],
	8:['A', 'B', 'C', 'D', 'E', 'F', 'G'],
	9:['A', 'B', 'C', 'D', 'F', 'G'],
}

def seven_seg_code(seg_list):
	code = 0
	for segname in seg_list:
		code+=(1<<SEGMENT_CODE[segname])
	return code


def digit_code(d):
	return seven_seg_code(DIGIT_CODE[d])


# OPCODES
OPCODE_LEN = 9
MUX_POS = 5
def output(code):
	r = 1 << (OPCODE_LEN-1)
	return lambda : {'instr':r+code}

def goto(addr):
	r = 0x1 << MUX_POS
	return lambda : {'instr':r+(addr&0x1F)}

# Define commands
def commands(funcs):
	commands = []
	for f in funcs:
		commands.append(format(f()['instr'], '02x'))
	return commands

microprogramm = commands([
	output(digit_code(0)),
	output(digit_code(1)),
	output(digit_code(2)),
	output(digit_code(3)),
	output(digit_code(4)),
	output(digit_code(5)),
	output(digit_code(6)),
	output(digit_code(7)),
	output(digit_code(8)),
	output(digit_code(9)),
	goto(0)
	])


def rom2file(filename, opcodes):
	with open(filename, 'w') as f:
		f.write('v2.0 raw\n')
		f.write(' '.join(opcodes))
		f.write('\n')

rom2file('/tmp/rom', microprogramm)