import numba
numba.config.THREADING_LAYER='omp'
# numba.config.NUMBA_NUM_THREADS=2
print(f"{numba.config.THREADING_LAYER=}")
print(f"{numba.config.NUMBA_NUM_THREADS=}")

@numba.jit(nopython=True, parallel=True)
def omp():
    # numba.
    for i in numba.prange(4):
        print(f"[i={i}] thread {numba.get_thread_id()}/{numba.get_num_threads()}")
    

if __name__ == "__main__":
    omp()