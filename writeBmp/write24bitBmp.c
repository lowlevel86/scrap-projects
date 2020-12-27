#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int write24bitBmp(char *filename, void *imgData, int xSize, int ySize,
                  int rowColSwap, int xFlip, int yFlip, int reverseRGB)
{
   int i, x, y, ch;
   int fileSize;
   int imgSize;
   int padSize;
   char *bmpData;
   FILE *bmpFile;
   char (*imgXY)[xSize][ySize][3] = imgData;
   char (*imgYX)[ySize][xSize][3] = imgData;
   
   //  'B',  'M', [      fileSize      ], [reserved], [reserved], [     imgOffset      ], [ header->
   // Size     ], [       width        ], [       height       ], [ planes ], [bits/Px ], [compres->
   // sion     ], [      imgSize       ], [    xResolution     ], [    yResolution     ], [number ->
   // of colors], [  important colors  ]
   char bmpHeader[54] = { 'B',  'M',    0,    0,    0,    0, 0x00, 0x00, 0x00, 0x00, 0x36, 0x00, 0x00, 0x00, 0x28, 0x00,
                         0x00, 0x00,    0,    0,    0,    0,    0,    0,    0,    0, 0x01, 0x00, 0x18, 0x00, 0x00, 0x00,
                         0x00, 0x00,    0,    0,    0,    0, 0xc4, 0x0e, 0x00, 0x00, 0xc4, 0x0e, 0x00, 0x00, 0x00, 0x00,
                         0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
   
   
   // file size
   padSize = xSize % 4;
   imgSize = xSize * ySize * 3 + padSize * ySize;
   fileSize = sizeof(bmpHeader) + imgSize;
   memcpy(&bmpHeader[2], (char *)(&fileSize), 4);
   
   // width
   memcpy(&bmpHeader[18], (char *)(&xSize), 4);
   
   // height
   memcpy(&bmpHeader[22], (char *)(&ySize), 4);
   
   // image size
   memcpy(&bmpHeader[34], (char *)(&imgSize), 4);
   
   bmpData = (char *)malloc(fileSize);
   if (!bmpData)
   {
      printf("Can not allocate memory.\n");
      return 1;
   }
   
   
   // move header to bmp data
   memcpy(bmpData, bmpHeader, sizeof(bmpHeader));
   
   
   // move image data to bmp data
   i = sizeof(bmpHeader);
   
   
   if (rowColSwap)
   {
      if (xFlip)
      {
         if (yFlip)
         {
            if (reverseRGB)
            for (y=ySize-1; y >= 0; y--)
            {
               for (x=xSize-1; x >= 0; x--)
               for (ch=2; ch >= 0; ch--)
               bmpData[i++] = (*imgYX)[y][x][ch];
               
               i += padSize;
            }
            else
            for (y=ySize-1; y >= 0; y--)
            {
               for (x=xSize-1; x >= 0; x--)
               for (ch=0; ch < 3; ch++)
               bmpData[i++] = (*imgYX)[y][x][ch];
               
               i += padSize;
            }
         }
         else
         {
            if (reverseRGB)
            for (y=0; y < ySize; y++)
            {
               for (x=xSize-1; x >= 0; x--)
               for (ch=2; ch >= 0; ch--)
               bmpData[i++] = (*imgYX)[y][x][ch];
               
               i += padSize;
            }
            else
            for (y=0; y < ySize; y++)
            {
               for (x=xSize-1; x >= 0; x--)
               for (ch=0; ch < 3; ch++)
               bmpData[i++] = (*imgYX)[y][x][ch];
               
               i += padSize;
            }
         }
      }
      else
      {
         if (yFlip)
         {
            if (reverseRGB)
            for (y=ySize-1; y >= 0; y--)
            {
               for (x=0; x < xSize; x++)
               for (ch=2; ch >= 0; ch--)
               bmpData[i++] = (*imgYX)[y][x][ch];
               
               i += padSize;
            }
            else
            for (y=ySize-1; y >= 0; y--)
            {
               for (x=0; x < xSize; x++)
               for (ch=0; ch < 3; ch++)
               bmpData[i++] = (*imgYX)[y][x][ch];
               
               i += padSize;
            }
         }
         else
         {
            if (reverseRGB)
            for (y=0; y < ySize; y++)
            {
               for (x=0; x < xSize; x++)
               for (ch=2; ch >= 0; ch--)
               bmpData[i++] = (*imgYX)[y][x][ch];
               
               i += padSize;
            }
            else
            for (y=0; y < ySize; y++)
            {
               for (x=0; x < xSize; x++)
               for (ch=0; ch < 3; ch++)
               bmpData[i++] = (*imgYX)[y][x][ch];
               
               i += padSize;
            }
         }
      }
   }
   else
   {
      if (xFlip)
      {
         if (yFlip)
         {
            if (reverseRGB)
            for (y=ySize-1; y >= 0; y--)
            {
               for (x=xSize-1; x >= 0; x--)
               for (ch=2; ch >= 0; ch--)
               bmpData[i++] = (*imgXY)[x][y][ch];
               
               i += padSize;
            }
            else
            for (y=ySize-1; y >= 0; y--)
            {
               for (x=xSize-1; x >= 0; x--)
               for (ch=0; ch < 3; ch++)
               bmpData[i++] = (*imgXY)[x][y][ch];
               
               i += padSize;
            }
         }
         else
         {
            if (reverseRGB)
            for (y=0; y < ySize; y++)
            {
               for (x=xSize-1; x >= 0; x--)
               for (ch=2; ch >= 0; ch--)
               bmpData[i++] = (*imgXY)[x][y][ch];
               
               i += padSize;
            }
            else
            for (y=0; y < ySize; y++)
            {
               for (x=xSize-1; x >= 0; x--)
               for (ch=0; ch < 3; ch++)
               bmpData[i++] = (*imgXY)[x][y][ch];
               
               i += padSize;
            }
         }
      }
      else
      {
         if (yFlip)
         {
            if (reverseRGB)
            for (y=ySize-1; y >= 0; y--)
            {
               for (x=0; x < xSize; x++)
               for (ch=2; ch >= 0; ch--)
               bmpData[i++] = (*imgXY)[x][y][ch];
               
               i += padSize;
            }
            else
            for (y=ySize-1; y >= 0; y--)
            {
               for (x=0; x < xSize; x++)
               for (ch=0; ch < 3; ch++)
               bmpData[i++] = (*imgXY)[x][y][ch];
               
               i += padSize;
            }
         }
         else
         {
            if (reverseRGB)
            for (y=0; y < ySize; y++)
            {
               for (x=0; x < xSize; x++)
               for (ch=2; ch >= 0; ch--)
               bmpData[i++] = (*imgXY)[x][y][ch];
               
               i += padSize;
            }
            else
            for (y=0; y < ySize; y++)
            {
               for (x=0; x < xSize; x++)
               for (ch=0; ch < 3; ch++)
               bmpData[i++] = (*imgXY)[x][y][ch];
               
               i += padSize;
            }
         }
      }
   }
   
   
   // open file for write
   bmpFile = fopen(filename, "wb");
   if (!bmpFile)
   {
      printf("Can not open file.\n");
      return 1;
   }
   
   fwrite(bmpData, sizeof(char), fileSize, bmpFile);
   
   free(bmpData);
   fclose(bmpFile);
   return 0;
}
