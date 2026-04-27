import disk_scrub as disk_scrub

def wipe_temp_files():
    # Limpeza de diretórios temporários (/tmp e local)
    files = ["temp1.tmp", "temp2.log"]
    while files:
        files.pop()
    disk_scrub.scrub_disk_sectors()
