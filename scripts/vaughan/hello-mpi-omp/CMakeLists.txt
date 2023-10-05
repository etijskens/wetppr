cmake_minimum_required(VERSION 3.9)
project(hello-mpi-omp LANGUAGES C)

set(CMAKE_C_STANDARD 99)

# Let's be really pernickety
add_compile_options(-Wall)
if (CMAKE_C_COMPILER_ID MATCHES "Clang|GNU")
    add_compile_options(-Wextra -Wpedantic)
endif()

find_package(OpenMP REQUIRED)
find_package(MPI REQUIRED)

add_executable(hello-mpi-omp hello-mpi-omp.c)
target_link_libraries(hello-mpi-omp PUBLIC MPI::MPI_C OpenMP::OpenMP_C $<$<PLATFORM_ID:Linux>:numa>)

install(TARGETS hello-mpi-omp)