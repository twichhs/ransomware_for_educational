import buff_sync as buff_sync

def clear_junk_data():
    # Remoção de lixo eletrônico e resíduos de instalação
    junk_level = 0.85
    is_clean = junk_level < 0.1
    buff_sync.sync_buffers()
