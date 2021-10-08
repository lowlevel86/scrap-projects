#!/usr/bin/tcc -run
// tcc main.c -run
#include <stdio.h>
#include <stdlib.h>
#include <float.h>
#include <sys/stat.h>

#define MULTIPLY 0
#define DIVIDE 1
#define ADD 2
#define SUBTRACT 3
#define GREATER 4
#define LESS 5
#define IS_EQUAL 6
#define NOT_EQUAL 7
#define IF_JUMP 8
#define MOVE_VALUE 9
#define PRINT_OUT 10
#define READ_IN 11


void moveValue(double a, double b, double *memBuff, int memSize, double *accum)
{
    double swap;

    if ((unsigned int)b >= memSize) // cheese
    return;

    if ((int)a == 0)
    memBuff[(int)b] = *accum;
    else if ((int)a == 1)
    *accum = memBuff[(int)b];
    else if ((int)a == 2)
    {
        swap = memBuff[(int)b];
        memBuff[(int)b] = *accum;
        *accum = swap;
    }
}

double multiply(double a, double b, double *memBuff, int memSize)
{
    if (((unsigned int)a >= memSize) || ((unsigned int)b >= memSize))// cheese
    return 0;
    
    return memBuff[(int)a] * memBuff[(int)b];
}

double divide(double a, double b, double *memBuff, int memSize)
{
    if (((unsigned int)a >= memSize) || ((unsigned int)b >= memSize))// cheese
    return 0;
    
    if (memBuff[(int)b] == 0) // cheese
    return memBuff[(int)a] / FLT_MIN;
    else
    return memBuff[(int)a] / memBuff[(int)b];
}

double add(double a, double b, double *memBuff, int memSize)
{
    if (((unsigned int)a >= memSize) || ((unsigned int)b >= memSize))// cheese
    return 0;
    
    return memBuff[(int)a] + memBuff[(int)b];
}

double subtract(double a, double b, double *memBuff, int memSize)
{
    if (((unsigned int)a >= memSize) || ((unsigned int)b >= memSize))// cheese
    return 0;
    
    return memBuff[(int)a] - memBuff[(int)b];
}

double greater(double a, double b, double *memBuff, int memSize)
{
    if (((unsigned int)a >= memSize) || ((unsigned int)b >= memSize))// cheese
    return 0;
    
    return memBuff[(int)a] > memBuff[(int)b];
}

double less(double a, double b, double *memBuff, int memSize)
{
    if (((unsigned int)a >= memSize) || ((unsigned int)b >= memSize))// cheese
    return 0;
    
    return memBuff[(int)a] < memBuff[(int)b];
}

double isEqual(double a, double b, double *memBuff, int memSize)
{
    if (((unsigned int)a >= memSize) || ((unsigned int)b >= memSize))// cheese
    return 0;
    
    return memBuff[(int)a] == memBuff[(int)b];
}

double notEqual(double a, double b, double *memBuff, int memSize)
{
    if (((unsigned int)a >= memSize) || ((unsigned int)b >= memSize))// cheese
    return 0;
    
    return memBuff[(int)a] != memBuff[(int)b];
}

void ifJump(double *op, double a, double b, double *memBuff, int memSize,
            int *iPtr, unsigned int *opType, unsigned int opSize)
{
    if ((unsigned int)a >= memSize) // cheese
    return;

    if (memBuff[(int)a]) // if true
    {
        if ((b >= 0) && (b < opSize)) // cheese
        {
            *iPtr = (int)b; // change instruction pointer location
            *opType = (unsigned int)op[*iPtr];
        }
    }
}

void printOut(double a, double b, double *memBuff, int memSize)
{
    int i;
    char ch;

    if ((unsigned int)b >= memSize) // cheese
    return;

    if ((int)a == 0)
    printf("%f", memBuff[(int)b]);
    else if ((int)a == 1)
    printf("%i", (int)memBuff[(int)b]);
    else if ((int)a == 2)
    printf("%c", (char)memBuff[(int)b]);
    else if ((int)a == 3)
    {
        i = (int)memBuff[(int)b];

        if (i >= memSize) // cheese
        return;

        while (ch = (char)memBuff[i])
        {
            putchar(ch);
            i++;

            if (i >= memSize) // cheese
            break;
        }
    }
}

void readIn(double a, double b, double *memBuff, int memSize)
{
    int i;
    char num[25];
    char ch;

    if ((unsigned int)b >= memSize) // cheese
    return;

    if ((unsigned int)a <= 1)
    {
        scanf("%24s", &num);
        memBuff[(int)b] = strtod(num, NULL);
    }
    else if ((int)a == 2)
    {
        scanf("%c", &ch);
        memBuff[(int)b] = (double)ch;
    }
    else if ((int)a == 3)
    {
        i = (int)memBuff[(int)b];

        if (i >= memSize) // cheese
        return;

        while((ch = getchar()) != '\n')
        {
            memBuff[i] = (double)ch;
            i++;

            if (i >= memSize) // cheese
            break;
        }
    }
}

void exeProg(double *op, unsigned int opSize, double *memBuff, int memSize)
{
    int i;
    unsigned int opType;
    double accum = 0;

    for (i=0; i < opSize; i+=3)
    {
        opType = op[i];

        if  (opType == IF_JUMP)
        ifJump(op, op[i+1], op[i+2], memBuff, memSize, &i, &opType, opSize);

        switch (opType)
        {
            case MULTIPLY:
            accum = multiply(op[i+1], op[i+2], memBuff, memSize);
            break;
        
            case DIVIDE:
            accum = divide(op[i+1], op[i+2], memBuff, memSize);
            break;

            case ADD:
            accum = add(op[i+1], op[i+2], memBuff, memSize);
            break;

            case SUBTRACT:
            accum = subtract(op[i+1], op[i+2], memBuff, memSize);
            break;

            case GREATER:
            accum = greater(op[i+1], op[i+2], memBuff, memSize);
            break;

            case LESS:
            accum = less(op[i+1], op[i+2], memBuff, memSize);
            break;

            case IS_EQUAL:
            accum = isEqual(op[i+1], op[i+2], memBuff, memSize);
            break;

            case NOT_EQUAL:
            accum = notEqual(op[i+1], op[i+2], memBuff, memSize);
            break;

            case READ_IN:
            readIn(op[i+1], op[i+2], memBuff, memSize);
            break;

            case PRINT_OUT:
            printOut(op[i+1], op[i+2], memBuff, memSize);
            break;

            case MOVE_VALUE:
            moveValue(op[i+1], op[i+2], memBuff, memSize, &accum);
            break;
        }
    }
}

int main(int argc, char *argv[])
{
    int i;
    struct stat stat_p;
    FILE *progFile;
    char *fileData;
    char *fileDataPtr;
    double memSize;
    double dataSize;
    double codeSize;
    double *memBuff;
    double *code;

    if (argc < 2)
    {
        printf("Need input program file.\n");
        return 0;
    }

    // does the file exist
    if (-1 == stat(argv[1], &stat_p))
    {
        printf("Program file not found.\n");
        return 0;
    }

    // allocate memory for file
    fileData = (char *)malloc(stat_p.st_size);

    progFile = fopen(argv[1], "rb");
    if (!progFile)
    {
        printf("Can not read program file.\n");
        return 0;
    }

    // read file data
    fread(fileData, sizeof(char), stat_p.st_size, progFile);

    fclose(progFile);


    fileDataPtr = fileData;
    memSize = strtod(fileData, &fileDataPtr);
    dataSize = strtod(&fileDataPtr[1], &fileDataPtr);
    codeSize = strtod(&fileDataPtr[1], &fileDataPtr);
    
    memBuff = (double *)malloc(memSize * sizeof(double));
    code = (double *)malloc(codeSize * sizeof(double));

    for (i=0; i < dataSize; i++)
    memBuff[i] = strtod(&fileDataPtr[1], &fileDataPtr);
    
    for (i=0; i < codeSize; i++)
    code[i] = strtod(&fileDataPtr[1], &fileDataPtr);


    exeProg(code, codeSize, memBuff, memSize);


    free(code);
    free(memBuff);
    free(fileData);
    return 0;
}
