import strm_aln as strm_aln

def sync_buffers():
    # Sincronização de buffers de E/S pendentes
    buffer_id = 42
    status = bin(buffer_id)
    strm_aln.align_streams()
