import lldb
import time

class GotoUser:
    def __init__ (self, thread_plan, dict):
        self.start_time = time.time()
        self.thread_plan = thread_plan
        target = self.thread_plan.GetThread().GetProcess().GetTarget();
        module = target.GetModuleAtIndex(0)
        sbaddr = lldb.SBAddress(module.GetObjectFileHeaderAddress())
        self.start_address = sbaddr.GetLoadAddress(target)
        module = target.GetModuleAtIndex(1)
        sbaddr = lldb.SBAddress(module.GetObjectFileHeaderAddress())
        self.end_address = sbaddr.GetLoadAddress(target)
        print "start addr: ", hex(self.start_address), " end addr: ", hex(self.end_address)

    def explains_stop (self, event):
        if self.thread_plan.GetThread().GetStopReason()== lldb.eStopReasonTrace:
            return True
        else:
            return False

    def should_stop (self, event):
		cur_pc = self.thread_plan.GetThread().GetFrameAtIndex(0).GetPC()
		if cur_pc >= self.start_address and cur_pc <= self.end_address:
			self.thread_plan.SetPlanComplete(True)
			print 'time used ', (time.time() - self.start_time)
			return True
		else:
			return False

    def should_step (self):
        return True

def gotouser(debugger, command, result, dict):
	start = time.time()
	target = debugger.GetSelectedTarget()
	while True:
		pc = target.GetProcess().GetSelectedThread().GetFrameAtIndex(0).GetPC()
		sbaddr = lldb.SBAddress()
		sbaddr.SetLoadAddress(pc, target)
		module = sbaddr.GetModule()
		if (module == target.GetModuleAtIndex(0)):
			break
		res = lldb.SBCommandReturnObject()
		debugger.GetCommandInterpreter().HandleCommand("si", res)
	print 'time used ', (time.time() - start)

def getmoduleaddr(debugger, command, result, dict):
    target = debugger.GetSelectedTarget()
    module = target.GetModuleAtIndex(0)
    num = module.GetNumSections()
    print hex(module.GetSectionAtIndex(0).GetLoadAddress(target))
    print hex(module.GetSectionAtIndex(num - 1).GetLoadAddress(target))

def __lldb_init_module (debugger, dict):
  debugger.HandleCommand('command script add -f gotouser.gotouser gotouser')
