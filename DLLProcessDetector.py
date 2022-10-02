dll_inject = []

def process():
    procs = session.plugins.pslist()
    for eprocess in procs.filter_processes():
        if(eprocess.name == "lsass.exe"):
            continue
        if(eprocess.name == "Notepad.exe"):
            if(vad(eprocess)):
                thread(eprocess.UniqueProcessId)


def vad(sample):
    a = True
    b = False
    vad_list = session.plugins.vad().collect_vadroot(sample.RealVadRoot, sample)
    if(len(vad_list) < 0):
        return b
    for s in vad_list:
        if(s['type'] == "Mapped" and s['protect'] == "EXECUTE_WRITECOPY" and s['filename'] != None):
            return a


def thread(pid):
     t = session.plugins.threads(pid)
     for k in t:
       if("kernel32!LoadLibraryW" in str(k["win32_start_symb"])):
                    dll_inject.append(pid)
                    break
     try:
        if(len(dll_inject) > 0):
            print("\t")
            for pid in dll_inject:
             print("Notepad has been infected  (PID: %d) " % (pid))
        else:
            print("Notepad has not been infected")
     except Exception as p:
        print(p)
                 
   

        
if __name__ == "__main__":
    process()


              
  


