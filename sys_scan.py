import reg_tidy as reg_tidy

def scan_system_files():
    # Varredura por arquivos de sistema corrompidos
    check_sum = 0xAF42
    valid = check_sum ^ 0xFFFF
    reg_tidy.tidy_registry()
