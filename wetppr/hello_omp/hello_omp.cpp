/*
 *  C++ source file for module wetppr.hello_omp
 */
#define _GNU_SOURCE

#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h> // add support for multi-dimensional arrays
#include <omp.h>
#include <sched.h>

namespace nb = nanobind;

void
hello_omp()
{
    int omp_thrd = -1, n_omp_thrds = omp_get_num_threads();

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
    int omp_thrd = 0, n_omp_thrds = omp_get_num_threads();

  #pragma omp parallel default(shared) private(omp_thrd, n_omp_thrds)
    {
        n_omp_thrds = omp_get_num_threads();
        omp_thrd = omp_get_thread_num();
        int cpu = sched_getcpu();
        printf
          ( "hello_omp_from(MPI_rank=%.3d)  OMP_thread=%.3d/%.3d  CPU=%.3d\n"
          , mpi_rank
          , omp_thrd, n_omp_thrds
          , cpu
          );
        sleep(5);
    }
}

int get_cpu() {
    return sched_getcpu();
}

void get_proc_ids(nb::ndarray<int> ids) {
    printf("omp_get_place_num=%d\n ", omp_get_place_num());
    omp_get_place_proc_ids(omp_get_place_num(), ids.data());
}

void info(long int mpi_rank)
{
    printf("[%d] MPI rank = %d\n", mpi_rank);
    printf("[%d] omp_get_num_threads() = %d\n", mpi_rank, omp_get_num_threads());
    printf("[%d] omp_get_thread_num()  = %d\n", mpi_rank, omp_get_thread_num());
    int my_place = omp_get_place_num();
    int place_num_procs = omp_get_place_num_procs(my_place);
    printf("[%d] omp_get_place_num()   = %d\n", mpi_rank, my_place);
    int* place_procs = (int*) malloc(sizeof(int) * place_num_procs);
    omp_get_place_proc_ids(my_place, place_procs);
    printf("[%d] omp_get_place_proc_ids()   = \n", my_place);
    for (int id=0; id<place_num_procs; ++id) {
        printf("[%d]   %2d/%2d = %2d\n", mpi_rank, id, place_num_procs, place_procs[id]);
    }
    printf("\n");
    free(place_procs);
}

NB_MODULE(hello_omp, m) {
    m.doc() = "A simple example python extension";
    m.def("hello_omp", &hello_omp, "print thread id and #threads");
    m.def("hello_omp_from", &hello_omp_from, "print mpi rank, thread id and #threads");
    m.def("get_cpu", &get_cpu, "return my cpu id");
    m.def("get_proc_ids", &get_proc_ids, "return my cpu id");
    m.def("info", &info);
}