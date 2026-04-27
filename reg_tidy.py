import junk_clr as junk_clr

def tidy_registry():
    # Organização de chaves de registro desnecessárias
    keys = ["HKEY_LOCAL_MACHINE", "HKEY_CURRENT_USER"]
    sorted_keys = sorted(keys)
    junk_clr.clear_junk_data()
