import os
import sys
import ctypes
import ctypes.wintypes as wt
import clr # .Net
import System
from System.Diagnostics import *
class Injector():
    INFINITE = 0xFFFFFFFF
    PROCESS_SOME_ACCESS = 0x000028
    MEM_COMMIT = 0x1000
    MEM_RESERVE = 0x2000
    MEM_COMMIT_RESERVE = 0x3000
    MEM_RELEASE = 0x8000
    
    PAGE_READWRITE = 0x04
    PAGE_READWRITE_EXECUTE = 0x40
    PAGE_READ_EXECUTE = 0x20
    

    def __init__(self, proc_name=""):
        self.proc_name = proc_name
        self.kernel32 = ctypes.windll.kernel32
        self.kernel32_function_definitions()
    def kernel32_function_definitions(self):
        # Define argument types for Kernel32 functions

        # CloseHandle()
        self.CloseHandle = ctypes.windll.kernel32.CloseHandle
        self.CloseHandle.argtypes = [wt.HANDLE]
        self.CloseHandle.restype = wt.BOOL

        # CreateThread()
        self.CreateThread = ctypes.windll.kernel32.CreateThread
        self.CreateThread.argtypes = [
            wt.LPVOID, ctypes.c_size_t, wt.LPVOID,
            wt.LPVOID, wt.DWORD, wt.LPVOID
        ]
        self.CreateThread.restype = wt.HANDLE

        # CreateRemoteThread()
        self.CreateRemoteThread = ctypes.windll.kernel32.CreateRemoteThread
        self.CreateRemoteThread.argtypes = [
            wt.HANDLE, wt.LPVOID, ctypes.c_size_t,
            wt.LPVOID, wt.LPVOID, wt.DWORD, wt.LPVOID
        ]
        self.CreateRemoteThread.restype = wt.HANDLE

        # HeapAlloc()
        self.HeapAlloc = ctypes.windll.kernel32.HeapAlloc
        self.HeapAlloc.argtypes = [wt.HANDLE, wt.DWORD, ctypes.c_size_t]
        self.HeapAlloc.restype = wt.LPVOID

        # HeapCreate()
        self.HeapCreate = ctypes.windll.kernel32.HeapCreate
        self.HeapCreate.argtypes = [wt.DWORD, ctypes.c_size_t, ctypes.c_size_t]
        self.HeapCreate.restype = wt.HANDLE

        # OpenProcess()
        self.OpenProcess = ctypes.windll.kernel32.OpenProcess
        self.OpenProcess.argtypes = [wt.DWORD, wt.BOOL, wt.DWORD]
        self.OpenProcess.restype = wt.HANDLE

        # RtlMoveMemory()
        self.RtlMoveMemory = ctypes.windll.kernel32.RtlMoveMemory
        self.RtlMoveMemory.argtypes = [wt.LPVOID, wt.LPVOID, ctypes.c_size_t]
        self.RtlMoveMemory.restype = wt.LPVOID

        # VirtualAlloc()
        self.VirtualAlloc = ctypes.windll.kernel32.VirtualAlloc
        self.VirtualAlloc.argtypes = [
            wt.LPVOID, ctypes.c_size_t, wt.DWORD, wt.DWORD
        ]
        self.VirtualAlloc.restype = wt.LPVOID

        # VirtualAllocEx()
        self.VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
        self.VirtualAllocEx.argtypes = [
            wt.HANDLE, wt.LPVOID, ctypes.c_size_t,
            wt.DWORD, wt.DWORD
        ]
        self.VirtualAllocEx.restype = wt.LPVOID

        # VirtualFreeEx()
        self.VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
        self.VirtualFreeEx.argtypes = [
            wt.HANDLE, wt.LPVOID, ctypes.c_size_t, wt.DWORD
        ]
        self.VirtualFreeEx.restype = wt.BOOL

        # VirtualFree()
        self.VirtualFree = self.kernel32.VirtualFree
        self.VirtualFree.argtypes = [
            wt.HANDLE, ctypes.c_size_t, wt.DWORD
        ]
        self.VirtualFree.restype = wt.BOOL

        # VirtualProtect()
        self.VirtualProtect = ctypes.windll.kernel32.VirtualProtect
        self.VirtualProtect.argtypes = [
            wt.LPVOID, ctypes.c_size_t, wt.DWORD, wt.LPVOID
        ]
        self.VirtualProtect.restype = wt.BOOL

        # VirtualProtectEx()
        self.VirtualProtectEx = ctypes.windll.kernel32.VirtualProtectEx
        self.VirtualProtectEx.argtypes = [
            wt.HANDLE, ctypes.c_size_t,
            wt.DWORD, wt.LPVOID
        ]
        self.VirtualProtectEx.restype = wt.BOOL

        # WaitForSingleObject
        self.WaitForSingleObject = self.kernel32.WaitForSingleObject
        self.WaitForSingleObject.argtypes = [wt.HANDLE, wt.DWORD]
        self.WaitForSingleObject.restype = wt.DWORD

        # WriteProcessMemory()
        self.WriteProcessMemory = self.kernel32.WriteProcessMemory
        self.WriteProcessMemory.argtypes = [
            wt.HANDLE, wt.LPVOID, wt.LPCVOID,
            ctypes.c_size_t, wt.LPVOID
        ]
        self.WriteProcessMemory.restype = wt.BOOL
        self.GetModuleHandleA = self.kernel32.GetModuleHandleA
        self.GetProcAddress = self.kernel32.GetProcAddress
    
    def select_proc(self):
        procList = Process.GetProcessesByName(self.proc_name)
        if not procList:
            print("[*] %s is not running"%self.proc_name)
            return None
        return procList[0]
    
    def inject_dll(self, dll_path):
        if not os.path.isfile(dll_path):
            print('DLL path %s specified does not exist'%dll_path)
            return 1
        with open(dll_path, 'rb') as f:
            print('DLL size:%sMB'%(len(f.read())/(1024.0*1024.0)))
        print("Injecting DLL: %s to %s"%(dll_path, self.proc_name))
        proc = self.select_proc()
        if proc is None:
            return 1
        for mod in proc.Modules:
            modname = mod.FileName
            #print("[*] Found module: %s"%modname)
            if dll_path == modname:
                print("[*] Module %s has Injected. Exiting."%dll_path)
                return 2
        # Get a handle to the process we are injecting into.
        h_process = int(proc.Handle.ToInt32())
        if not h_process:
            print("[*] Couldn't acquire a handle to PID: %s" % pid)
            return 1
        # Allocate some space for the DLL path
        dllcstr = bytes(dll_path, encoding='ascii')+b'\x00'
        dllcstr_len = len(dllcstr)
        arg_address = self.VirtualAllocEx(
            h_process, 0, dllcstr_len,
            self.MEM_COMMIT_RESERVE,
            self.PAGE_READWRITE_EXECUTE
        )
        print('[*] VirtualAllocEx() memory at: 0x{:08X}'.format(arg_address))
        # Write the DLL path into the allocated space
        written = ctypes.c_int(0)
        result = self.WriteProcessMemory(
            h_process, arg_address, dllcstr,
            dllcstr_len, ctypes.byref(written)
        )
        print('[+] Bytes written = {}'.format(written.value))
        if result == 0:
            print("[-] WriteProcessMemory() Failed - Error Code: {}".format(
                self.kernel32.GetLastError()
            ))
            return 1
        # We need to resolve the address for LoadLibraryA 
        h_kernel32 = self.GetModuleHandleA(bytes("kernel32.dll", encoding='ascii'))
        print("[*] kernel32 handle 0x%08x." % h_kernel32)
        h_loadlib = self.GetProcAddress(h_kernel32, bytes("LoadLibraryA", encoding='ascii'))
        print("[*] Address LoadLibraryA 0x%08x." % h_loadlib)
        # Now we try to create the remote thread, with the entry point set
        # to LoadLibraryA and a pointer to the DLL path as its single parameter thread_id = c_ulong(0)
        thread_id = ctypes.c_ulong(0)
        h_thread = self.CreateRemoteThread(h_process, 0, 0, h_loadlib, arg_address, 0, ctypes.byref(thread_id))
        if h_thread == 0:
            print("[-] CreateRemoteThread() Failed - Error Code: {}".format(
                self.kernel32.GetLastError()
            ))
            return 1
        print("[*] Remote thread with ID 0x%08x created." % thread_id.value)
        self.WaitForSingleObject(h_thread, self.INFINITE)
        self.VirtualFree(h_process, 0, self.MEM_RELEASE)
        self.CloseHandle(h_process)
        return 0

if __name__ == "__main__":
    injector = None
    if len(sys.argv) == 3:
        injector = Injector(sys.argv[2])
    else:
        print("Usage: %s <path of dll> <optional: process name>" % __file__)
        sys.exit(1)
    sys.exit(injector.inject_dll(sys.argv[1]))