#define PY_SSIZE_T_CLEAN

#include <stdio.h>
#include <math.h>
#include <Python.h>

#include "numpy/ndarraytypes.h"
#include "numpy/ufuncobject.h"
#include "numpy/npy_3kcompat.h"

/*
 * wordle_partition.c
 *
 * Details explaining the Python-C API can be found under
 * 'Extending and Embedding' and 'Python/C API' at
 * docs.python.org .
 */

static PyMethodDef LogitMethods[] = {
    {NULL, NULL, 0, NULL}
};

/* The loop definition must precede the PyMODINIT_FUNC. */

/*
 * Partition ufunc signature: 
 *   (n_query_words,n_word_length),(n_active_words,n_word_length),(n_active_words,n_total_letters)->(n_query_words)
 *
 * Inputs:
 *   - Query pool , with each possible query word represented as a vector containing the letters of the query word
 *   - Active solution words, with each (remaining) possible solution represented as a vector containing the letters of the potential solution
 *   - Active solutions letter counts, containing counts of each of the letters in the possible solution word (array indexed by letter ordinal)
 * 
 * Output:
 *   - Vector containing the score of each of the query words
 */
static void wordle_partition_score(char **args, const npy_intp *dimensions,
                                   const npy_intp *steps, void *data)
{
    npy_ubyte* in_query_words = (npy_ubyte*)args[0];
    npy_ubyte* in_active_words = (npy_ubyte*)args[1];
    npy_ubyte* in_active_lcnts = (npy_ubyte*)args[2];
    npy_ubyte* out_scores = (npy_ubyte*)args[3];
    
    npy_intp n_total = dimensions[0];
    npy_intp n_query_words = dimensions[1];
    npy_intp n_word_length = dimensions[2];
    npy_intp n_active_words = dimensions[3];
    npy_intp n_total_letters = dimensions[4];

    npy_intp s_query_words_outer = steps[0];
    npy_intp s_active_words_outer = steps[1];
    npy_intp s_active_lcnts_outer = steps[2];
    npy_intp s_scores_outer = steps[3];
    npy_intp s_query_words_inner = steps[4];
    npy_intp s_query_words_letter = steps[5];
    npy_intp s_active_words_inner = steps[6];
    npy_intp s_active_words_letter = steps[7];
    npy_intp s_active_lcnts_inner = steps[8];
    npy_intp s_active_lcnts_letter = steps[9];

    noy_intp i_total;
    npy_intp i_query_word;
    npy_intp i_active_word;
    npy_intp i_word_pos:
    npy_intp i_partition;
    
    npy_ubyte* letter_counts = (npy_ubyte*)malloc(sizeof(npy_ubyte)*(n_total_letters+1));
    npy_int32* partitions = (npy_int32*)malloc(sizeof(npy_int32)*pow(3,5));
    
    for (i_total = 0; i_total < n_total; ++i_total) {

        for (i_query_word = 0; i_query_word < n_query_words; ++i_query_word) {        
            
            char* pos_query_words = in_query_words;
            char* pos_active_words = in_active_words;
            char* pos_active_lcnts = in_active_lcnts;

            memset(partitions, 0, sizeof(npy_int32)*pow(3,5));

            for (i_active_word = 0; i_active_word < n_active_words; ++i_active_word) {
                memset(letter_counts, 0, sizeof(npy_ubyte)*(n_total_letters+1));

                in_query_words = pos_query_words;

                npy_uint32 partition_idx_green = 0;
                for (i_word_pos = 0; i_word_pos < n_word_length; ++i_word_pos) {
                    partition_idx_green *= 3
                    partition_idx_green += (*in_query_words == *in_active_words) * 2;
                    
                    letter_counts[(*in_query_words == *in_active_words) * (1 + *in_query_words)] += 1;
                    in_query_words += s_query_words_letter;
                    in_active_words += s_active_words_letter;
                }

                in_query_words = pos_query_words;

                npy_unit32 partition_idx_yellow = 0;
                for (i_word_pos = 0; i _word_pos < n_word_length; ++i_word_pos) {
                    partition_idx_yellow *= 3;
                    partition_idx_yellow += (npy_uint32)((letter_counts[1 + *in_query_words] < 
                                                        *(in_active_lcnts + s_active_lcnts_letter * (*in_query_words)));
                    
                    letter_counts[1 + *in_query_words] += 1;
                    in_query_words += s_query_words_letter;
                }

                partitions[partition_idx_green + partition_idx_yellow] += 1;

                in_active_lcnts += s_active_lcnts_inner;
            }

            npy_double t = (npy_double)n_active_words;
            f = filter(lambda x: x>0, partitions)
            score = reduce(lambda h,n: h - (float(n)/t)*math.log2(float(n)/t), f, 0)
            t = float(np.sum(partitions))
            score = reduce(lambda h,n: h - (float(n)/t)*math.log2(float(n)/t), partitions[partitions>0], 0)

            # prefer words in active set in case score is tied
            if (score > best_score) or (score == best_score and word in active_set): 
                best_word, best_score = word, score

            in_query_words = pos_query_words + s_query_words_inner;
            in_active_words = pos_active_words;
            in_active_lcnts = pos_active_lcnts;
        }

        free(letter_counts);
        free(partitions);
    }
}
/* This a pointer to the above function */
PyUFuncGenericFunction funcs[1] = {&double_logit};

/* These are the input and return dtypes of logit.*/
static char types[2] = {NPY_DOUBLE, NPY_DOUBLE};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "npufunc",
    NULL,
    -1,
    LogitMethods,
    NULL,
    NULL,
    NULL,
    NULL
};

PyMODINIT_FUNC PyInit_npufunc(void)
{
    PyObject *m, *logit, *d;
    m = PyModule_Create(&moduledef);
    if (!m) {
        return NULL;
    }

    import_array();
    import_umath();

    logit = PyUFunc_FromFuncAndData(funcs, NULL, types, 1, 1, 1,
                                    PyUFunc_None, "logit",
                                    "logit_docstring", 0);

    d = PyModule_GetDict(m);

    PyDict_SetItemString(d, "logit", logit);
    Py_DECREF(logit);

    return m;
}