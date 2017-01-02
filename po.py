import lldb

def print_to_file(debugger, command, result, dict):
  #Change the output file to a path/name of your choice
  f=open("/Users/user/temp.txt","w")
  debugger.SetOutputFileHandle(f,True);
  #Change command to the command you want the output of
  command = "po self"
  debugger.HandleCommand(command)

def __lldb_init_module (debugger, dict):
  debugger.HandleCommand('command script add -f po.print_to_file print_to_file ')

