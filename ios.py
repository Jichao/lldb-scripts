import lldb

#assume 32-bit address
def va2fa(debugger, command, result, dict):
    va = int(command, 0)
    target = debugger.GetSelectedTarget()
    sbaddr = lldb.SBAddress()
    sbaddr.SetLoadAddress(va, target)
    fa = sbaddr.GetFileAddress()
    print "va: ", hex(va),  " fa: ", hex(fa)

def fa2va(debugger, command, result, dict):
    #assume fa in the first module.
    fa = int(command , 0)
    module = debugger.GetSelectedTarget().GetModuleAtIndex(0)
    sbaddr = lldb.SBAddress(module.GetObjectFileHeaderAddress())
    offset = sbaddr.GetLoadAddress(debugger.GetSelectedTarget()) - sbaddr.GetFileAddress()
    va = fa + offset
    print "fa: ", hex(fa), " va: ", hex(va)

def __lldb_init_module (debugger, dict):
  debugger.HandleCommand('command script add -f ios.va2fa va2fa')
  debugger.HandleCommand('command script add -f ios.fa2va fa2va')
