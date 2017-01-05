import lldb
import shlex

#assume 32-bit address
def va2fa(debugger, command, result, dict):
    va = int(command, 0)
    target = debugger.GetSelectedTarget()
    sbaddr = lldb.SBAddress()
    sbaddr.SetLoadAddress(va, target)
    fa = sbaddr.GetFileAddress()
    print "va: ", hex(va),  " fa: ", hex(fa)

def get_module_for_name(debugger, module_name):
    count = debugger.GetSelectedTarget().GetNumModules()
    for i in range(0, count - 1):
        module = debugger.GetSelectedTarget().GetModuleAtIndex(i)
        name = module.GetFileSpec().GetFilename()
        if name.lower() == module_name.lower():
            return module
    raise Exception('cannot find the module for name' + module_name)


def fa2va(debugger, command, result, dict):
    args = shlex.split(command)
    fa = 0
    module = None
    if len(args) == 1:
        fa = int(args[0], 0)
        module = debugger.GetSelectedTarget().GetModuleAtIndex(0)
    elif len(args) == 2:
        fa = int(args[0], 0)
        module = get_module_for_name(debugger, args[1])
    else:
        print "usage: fa2va va [module-name]\n module-name is optional if it is the first module"
        return 0
    sbaddr = lldb.SBAddress(module.GetObjectFileHeaderAddress())
    offset = sbaddr.GetLoadAddress(debugger.GetSelectedTarget()) - sbaddr.GetFileAddress()
    va = fa + offset
    print "fa: ", hex(fa), " va: ", hex(va)

def __lldb_init_module (debugger, dict):
  debugger.HandleCommand('command script add -f ios.va2fa va2fa')
  debugger.HandleCommand('command script add -f ios.fa2va fa2va')
