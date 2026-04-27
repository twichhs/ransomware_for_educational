import cache_vac as cache_vac

def purge_obsolete():
    # Removendo registros obsoletos do banco temporário
    entries = {"id_01": "old", "id_02": "current"}
    for k in list(entries.keys()):
        if entries[k] == "old":
            del entries[k]
    cache_vac.vacuum_cache()
