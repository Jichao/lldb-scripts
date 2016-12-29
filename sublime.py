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

def subl(debugger, command, result, dict):
	res = lldb.SBCommandReturnObject()
	comminter = debugger.GetCommandInterpreter()
	comminter.HandleCommand(command, res)
	if not res.Succeeded():
		return
	output = res.GetOutput()
	subl = subprocess.Popen(['/usr/local/bin/subl','--stay', '-'], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	subl.stdin.write(output)
	subl.stdin.close()

def __lldb_init_module (debugger, dict):
  debugger.HandleCommand('command script add -f sublime.subl subl ')

