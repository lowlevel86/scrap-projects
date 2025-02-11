#!/bin/bash

# replace "" with location of InteractiveAndRobustMeshBooleans-main
ROOTDIR=""

INCS="-I$ROOTDIR/. -I$ROOTDIR/code -I$ROOTDIR/arrangements/code -I$ROOTDIR/arrangements/external/Indirect_Predicates/include -I$ROOTDIR/arrangements/external/abseil-cpp -I$ROOTDIR/arrangements/external/oneTBB -I$ROOTDIR/arrangements/external/Cinolib/include -I$ROOTDIR/arrangements/external/Cinolib/external/eigen -I$ROOTDIR/arrangements/external/Cinolib/external/imgui/include -I$ROOTDIR/arrangements/external/Cinolib/external/imgui -I$ROOTDIR/arrangements/external/Cinolib/external/imgui/glfw/include -I$ROOTDIR/arrangements/external/oneTBB/src/tbb/../../include"

DEFS="-DCINOLIB_USES_OPENGL_GLFW_IMGUI -DCINOLIB_USES_SHEWCHUK_PREDICATES -DGL_SILENCE_DEPRECATION -DTBB_PARALLEL=1"

FLAGS="-O2 -g -DNDEBUG -std=gnu++2a -O2 -Wl,-z,stacksize=8421376 -frounding-math -mavx2"

g++ $DEFS $INCS $FLAGS -fPIC -c main_inputcheck.cpp -o $ROOTDIR/build/CMakeFiles/mesh_booleans_inputcheck.dir/main-inputcheck.cpp.o

/usr/bin/g++ -shared -O2 -g -DNDEBUG $ROOTDIR/build/CMakeFiles/mesh_booleans_inputcheck.dir/main-inputcheck.cpp.o -o mesh_booleans_inputcheck.so -Wl,-rpath,$ROOTDIR/build/gnu_9.4_cxx20_64_relwithdebinfo $ROOTDIR/build/gnu_9.4_cxx20_64_relwithdebinfo/libtbb.so.12.7 /usr/lib/x86_64-linux-gnu/libGL.so $ROOTDIR/build/imgui/libimgui.a $ROOTDIR/build/imgui/glfw/src/libglfw3.a /usr/lib/x86_64-linux-gnu/librt.so -lm -ldl /usr/lib/x86_64-linux-gnu/libX11.so -lpthread $ROOTDIR/build/shewchuk_predicates/libshewchuk_predicates.a

