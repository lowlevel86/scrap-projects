#include "booleans.h"

std::vector<std::string> files;

extern "C"
{
    void boolean_ops(double* pts, int ptSz, int* tris, int triSz, int* labels, int labelSz, double** out_coords, int* out_coordsSz, int** out_tris, int* out_trisSz, int** out_labels, int* out_labelsSz, int booleanOp)
    {
        std::vector<double> in_coords(pts, pts + ptSz);
        std::vector<uint> in_tris(tris, tris + triSz);
        std::vector<uint> in_labels(labels, labels + labelSz);
        std::vector<double> bool_coords;
        std::vector<uint> bool_tris;
        std::vector<std::bitset<NBIT>> bool_labels;

        BoolOp op;
        op = INTERSECTION;
        
        if (booleanOp == 1)
        op = UNION;
        
        if (booleanOp == 2)
        op = SUBTRACTION;
        
        if (booleanOp == 3)
        op = XOR;
        
        booleanPipeline(in_coords, in_tris, in_labels, op, bool_coords, bool_tris, bool_labels);
        
        // Allocate memory for output vector
        *out_coordsSz = bool_coords.size();
        *out_trisSz = bool_tris.size();
        *out_labelsSz = bool_labels.size();
        *out_coords = (double*)malloc(*out_coordsSz * sizeof(double));
        *out_tris = (int*)malloc(*out_trisSz * sizeof(int));
        *out_labels = (int*)malloc(*out_labelsSz * sizeof(int));
        
        for (int i = 0; i < *out_coordsSz; ++i)
        (*out_coords)[i] = bool_coords[i];
        
        for (int i = 0; i < *out_trisSz; ++i)
        (*out_tris)[i] = bool_tris[i];
        
        for (int i = 0; i < *out_labelsSz; ++i)
        (*out_labels)[i] = static_cast<int>(bool_labels[i].to_ulong());
    }

    void free_memory(double* bool_coords, int* bool_tris, int* bool_labels)
    {
        free(bool_coords);
        free(bool_tris);
        free(bool_labels);
    }
}

