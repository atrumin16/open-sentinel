# -*- coding: utf-8 -*-
"""
OpenSentinel Process Management Module
List running processes sorted by RAM/CPU and terminate selected tasks safely.
"""

import psutil

def get_top_processes(limit=30, min_mem_mb=30) -> list:
    """Retorna los procesos activos que consumen más memoria RAM."""
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
        try:
            mem_mb = int(p.info['memory_info'].rss / (1024 * 1024))
            name = p.info['name']
            if mem_mb >= min_mem_mb and name.lower() not in ('system', 'idle', 'registry'):
                procs.append({
                    'pid': p.info['pid'],
                    'name': name,
                    'mem_mb': mem_mb,
                    'cpu': p.info.get('cpu_percent') or 0
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    procs.sort(key=lambda x: x['mem_mb'], reverse=True)
    return procs[:limit]

def kill_process_by_pid(pid: int) -> dict:
    """Finaliza un proceso de Windows por su PID."""
    try:
        p = psutil.Process(pid)
        proc_name = p.name()
        p.terminate()
        return {"success": True, "msg": f"Proceso {proc_name} (PID: {pid}) finalizado con exito"}
    except psutil.NoSuchProcess:
        return {"success": False, "msg": f"El proceso con PID {pid} ya no existe"}
    except psutil.AccessDenied:
        return {"success": False, "msg": f"Permisos insuficientes para finalizar PID {pid}"}
    except Exception as e:
        return {"success": False, "msg": f"Error al finalizar proceso: {e}"}
