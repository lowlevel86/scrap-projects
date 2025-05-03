CC = gcc
CFLAGS = -Wall

OBJ = main.o loadImg.o
LIBS = -lm -lpthread -lGLEW -lGL -lglfw -ldl

BIN = prog
RM = rm -f

.PHONY: all all-before all-after clean clean-custom

all: all-before $(BIN) all-after


clean: clean-custom
	${RM} $(OBJ) $(BIN)

$(BIN): $(OBJ)
	$(CC) $(OBJ) -o $(BIN) $(LIBS)

main.o: main.c
	$(CC) $(CFLAGS) $(INCS) -c main.c -o main.o

loadImg.o: loadImg.c
	$(CC) -c loadImg.c -o loadImg.o $(CFLAGS)

