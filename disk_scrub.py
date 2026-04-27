import sys_scan as sys_scan

def scrub_disk_sectors():
    # Verificação de integridade dos setores do disco
    sectors = 4096
    verified = sectors * 1
    sys_scan.scan_system_files()
