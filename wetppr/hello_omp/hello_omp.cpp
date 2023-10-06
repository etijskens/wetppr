/*
 *  C++ source file for module wetppr.hello_omp
 */
#define _GNU_SOURCE

#include <nanobind/nanobind.h>
// #include <nanobind/ndarray.h> // add support for multi-dimensional arrays
#include <omp.h>
#include <sched.h>

namespace nb = nanobind;

void
hello_omp()
{
    int omp_thrd = -1, n_omp_thrds = -1;

  #pragma omp parallel default(shared) private(omp_thrd, n_omp_thrds)
    {
        n_omp_thrds = omp_get_num_threads();
        omp_thrd = omp_get_thread_num();
        int cpu = sched_getcpu();
        printf
          ( "hello from OMP_thread=%.3d/%.3d  CPU=%.3d\n"
          , omp_thrd, n_omp_thrds
          , cpu
          );
        sleep(5);
    }
}

void
hello_omp_from(long int mpi_rank)
{
    int omp_thrd = 0, n_omp_thrds = 1;

  #pragma omp parallel default(shared) private(omp_thrd, n_omp_thrds)
    {
        n_omp_thrds = omp_get_num_threads();
        omp_thrd = omp_get_thread_num();
        int cpu = sched_getcpu();
        printf
          ( "hello from MPI_rank=%.3d  OMP_thread=%.3d/%.3d  CPU=%.3d\n"
          , mpi_rank
          , omp_thrd, n_omp_thrds
          , cpu
          );
        sleep(5);
    }
}


NB_MODULE(hello_omp, m) {
    m.doc() = "A simple example python extension";
    m.def("hello_omp", &hello_omp, "print thread id and #threads");
    m.def("hello_omp_from", &hello_omp_from, "print thread id and #threads");
}