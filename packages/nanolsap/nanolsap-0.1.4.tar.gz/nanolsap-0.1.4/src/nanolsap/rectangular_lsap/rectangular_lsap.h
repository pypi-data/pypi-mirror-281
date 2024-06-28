/*
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:

1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above
   copyright notice, this list of conditions and the following
   disclaimer in the documentation and/or other materials provided
   with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived
   from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#ifndef RECTANGULAR_LSAP_H
#define RECTANGULAR_LSAP_H

#define RECTANGULAR_LSAP_INFEASIBLE -1
#define RECTANGULAR_LSAP_INVALID -2
#define RECTANGULAR_LSAP_SUBSCRIPT_INVALID -3
#define RECTANGULAR_LSAP_DTYPE_INVALID -4

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>

int solve_rectangular_linear_sum_assignment(intptr_t nr, intptr_t nc,
                                            double* input_cost, bool maximize,
                                            int64_t* a, int64_t* b);

enum LSAP_TYPES {
   LSAP_BOOL=0,
   LSAP_BYTE, LSAP_UBYTE,
   LSAP_SHORT, LSAP_USHORT,
   LSAP_INT, LSAP_UINT,
   LSAP_LONG, LSAP_ULONG,
   LSAP_LONGLONG, LSAP_ULONGLONG,
   LSAP_FLOAT, LSAP_DOUBLE, LSAP_LONGDOUBLE,

   LSAP_INVALID = 0xFFFF,
};

int solve_rectangular_linear_sum_assignment_dtype(
    intptr_t nr, intptr_t nc, void* input_cost, intptr_t dtype, bool maximize,
    const intptr_t *subrows, intptr_t n_subrows, const intptr_t *subcols, intptr_t n_subcols,
    int64_t* a, int64_t* b);

#ifdef __cplusplus
}
#endif

#endif
