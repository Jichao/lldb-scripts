import lldb
import time

class SimpleStep:
    def __init__ (self, thread_plan, dict):
		self.start_time = time.time()
		self.thread_plan = thread_plan
		self.start_address = thread_plan.GetThread().GetFrameAtIndex(0).GetPC()

    def explains_stop (self, event):
        if self.thread_plan.GetThread().GetStopReason()== lldb.eStopReasonTrace:
            return True
        else:
            return False

    def should_stop (self, event):
		cur_pc = self.thread_plan.GetThread().GetFrameAtIndex(0).GetPC()
		sbaddr = lldb.SBAddress()
		target = self.thread_plan.GetThread().GetProcess().GetTarget()
		sbaddr.SetLoadAddress(cur_pc, target)
		if sbaddr.GetModule() == target.GetModuleAtIndex(0):
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
