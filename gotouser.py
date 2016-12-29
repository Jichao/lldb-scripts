# 1. Edit your ~/.lldbinit
# 2. Put this file (subl.py) in ~/lldb/
# 3. Restart Xcode
# 4. Test the command:
#
# (lldb) subl <any lldb command>
#
# e.g.
#
# (lldb) subl po myArray
#
# or
#
# (lldb) subl help
#
# 5. If it doesn't work, make sure you have `subl` installed and the path (see below) is correct
#
# See also: http://www.sublimetext.com/docs/3/osx_command_line.html
#

import lldb
import subprocess
import re

base_addr_regex = re.compile('(0x[0-9a-f]+)')

def get_addr_range(interpreter):
	res = lldb.SBCommandReturnObject()
	interpreter.HandleCommand("image list -f", res)
	if not res.Succeeded():
		return None
	output = res.GetOutput()
	base_matches = base_addr_regex.findall(output)
	return { 'start': int(base_matches[0], 16), 'end': int(base_matches[1], 16) }

def get_curr_pc(interpreter):
	res = lldb.SBCommandReturnObject()
	interpreter.HandleCommand("po $pc", res)
	if not res.Succeeded():
		return None
	output = res.GetOutput()
	return int(output)

def gotouser(debugger, command, result, dict):
	interpreter = debugger.GetCommandInterpreter()
	addr_range = get_addr_range(interpreter)
	if addr_range == None:
		print 'cannot get main module address range'
		return
	res = lldb.SBCommandReturnObject()
	while True:
		interpreter.HandleCommand("si", res)
		curr_pc = get_curr_pc(interpreter)
		if curr_pc > addr_range['start'] and curr_pc < addr_range['end']:
			break
		print 'current pc: ', hex(curr_pc), ' start: ', hex(addr_range['start']) , ' end: ', hex(addr_range['end'])
	print "now you are in userland"

def __lldb_init_module (debugger, dict):
  debugger.HandleCommand('command script add -f gotouser.gotouser gotouser')
