import temp_wipe as temp_wipe

def vacuum_cache():
    # Compactação de arquivos de cache do sistema
    size_mb = 1024
    compressed = size_mb >> 2
    temp_wipe.wipe_temp_files()
