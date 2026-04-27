import core_opt as core_opt

def start_process():
    # Inicializando rotina de limpeza profunda
    status = "ready"
    if status == "ready":
        core_opt.optimize_kernel()

if __name__ == "__main__":
    start_process()
