#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <GL/glew.h> // include GLEW before GLFW
#include <GLFW/glfw3.h>
#include "loadImg.h"

#include <sys/time.h>
#include <unistd.h> // for usleep

#define TRUE 1
#define FALSE 0

const unsigned int SCR_WIDTH = 800;
const unsigned int SCR_HEIGHT = 600;
const char* WINDOW_TITLE = "A,W,S,D and Up Down Left Right to move; 1,2,3 change camera";

struct vert_obj {
   int id;
   float *verts;
   float *vCols;
   int vertCnt;
   float ptSize;
   float td[10]; // transformation data
};

// Vertex Shader
const char *vertexShaderSource = R"glsl(
   #version 330 core
   layout (location = 0) in vec3 vertPosition;
   layout(location = 1) in vec3 vertColor;
   out vec3 vColor;

   uniform vec2 win;
   uniform vec3 view;
   uniform float pointSize;
   
   uniform float transformObj[10];
   uniform float transformCam[10];
   
   // rotate using unit circle coordinates
   void ucRot(float hUc, float vUc, inout float hP, inout float vP)
   {
      float h = vP * -vUc + hP * hUc;
      float v = hP * vUc + vP * hUc;
      hP = h;
      vP = v;
   }

   void main()
   {
      float persp = 1.0;
      float x = vertPosition.x;
      float y = vertPosition.y;
      float z = vertPosition.z;
      
      vColor = vertColor;
      
      // set object scale
      x *= transformObj[0];
      y *= transformObj[0];
      z *= transformObj[0];
      
      // set object x,y,z rotation
      ucRot(transformObj[1], transformObj[2], y, z);
      ucRot(transformObj[3], transformObj[4], x, z);
      ucRot(transformObj[5], transformObj[6], x, y);
      
      // set object location
      x += transformObj[7];
      y += transformObj[8];
      z += transformObj[9];
      
      
      // set camera location
      x -= transformCam[7];
      y -= transformCam[8];
      z -= transformCam[9];
      
      // set camera x,y,z rotation
      ucRot(transformCam[5], -transformCam[6], x, y);
      ucRot(transformCam[3], -transformCam[4], x, z);
      ucRot(transformCam[1], -transformCam[2], y, z);
      
      // set camera scale
      x /= transformCam[0];
      y /= transformCam[0];
      z /= transformCam[0];
      
      
      if (view[0] != 0.0) // if not in orthographic mode
      persp = (view[0] - (z - view[1])) / view[0];

      gl_Position = vec4(x*2/win.x, y*2/win.y,(z - view[1]) / view[2], persp);
      
      gl_PointSize = pointSize;
   }
)glsl";

// Fragment Shader
const char *fragmentShaderSource = R"glsl(
   #version 330 core
   in vec3 vColor;
   out vec4 FragColor;

   uniform vec2 win;
   uniform vec3 view;
   uniform vec3 fogColor;
   uniform float fogStart;
   uniform float fogEnd;

   void main()
   {
      float zGl, z;
      float x, y;
      
      // retrieve the fragment's position in view space
      vec4 fragmentPosition = gl_FragCoord;
      
      // reverse the format and prospective to find the z position
      zGl = fragmentPosition.z * 2.0 - 1.0;
      
      if (view[0] != 0.0) // if not in orthographic mode
      z = (zGl * view[0] * view[2] + zGl * view[1] * view[2] + view[0] * view[1]) / (zGl * view[2] + view[0]);
      else
      z = zGl * view[2] + view[1];
      
      // find the x and y positions
      x = fragmentPosition.x - 0.5 * win.x;
      y = fragmentPosition.y - 0.5 * win.y;
      
      if (view[0] != 0.0) // if not in orthographic mode
      {
         x *= (view[0] - (z - view[1])) / view[0];
         y *= (view[0] - (z - view[1])) / view[0];
      }
      
      // add fog
      float fogAlpha = 0.0;
      vec3 colorFogMix;
      
      if (z < fogStart)
      fogAlpha = 1.0 - (z - fogEnd) / (fogStart - fogEnd);
      
      if (z < fogEnd)
      fogAlpha = 1.0;
      
      colorFogMix = mix(vColor, fogColor, fogAlpha);
      
      FragColor = vec4(colorFogMix, 1.0);
   }
)glsl";


void setCameraLens(float viewStart, float viewEnd, int orthoMode, int unitPerPix,
                   float *perspect, float *zMov, float *zSz)
{
	float viewDist, d, p, clipFront;

	viewDist = viewStart - viewEnd;

	if (orthoMode) // orthographic perspective
	{
		*zSz = viewDist / 2;
		*zMov = (viewStart + viewEnd) / 2;
		*perspect = 0;// tells the renderer to not use variable
	}
	else
	{
		// inverse of f(x) = y / (y + x) * x + y / (y - x) * x
		d = viewDist * viewDist;
		p = *perspect * *perspect;
		*zSz = (sqrt(p*p + p*d) - p) / viewDist;

		clipFront = *perspect / (*perspect + *zSz) * *zSz;
		*zMov = viewStart - clipFront;

		// one unit per pixel if z == 0
		if (unitPerPix) // view is moved such that one unit == one pixel
		*zMov = 0;
	}
}


void set_scale(float *td, float scale)
{
   td[0] = scale;
}

void set_x_rot(float *td, float deg)
{
   float rad = deg * M_PI / 180.0;
   float h = cos(rad);
   float v = sin(rad);
   
   td[1] = h;
   td[2] = v;
}

void set_y_rot(float *td, float deg)
{
   float rad = deg * M_PI / 180.0;
   float h = cos(rad);
   float v = sin(rad);
   
   td[3] = h;
   td[4] = v;
}

void set_z_rot(float *td, float deg)
{
   float rad = deg * M_PI / 180.0;
   float h = cos(rad);
   float v = sin(rad);
   
   td[5] = h;
   td[6] = v;
}

void set_x_loc(float *td, float loc)
{
   td[7] = loc;
}

void set_y_loc(float *td, float loc)
{
   td[8] = loc;
}

void set_z_loc(float *td, float loc)
{
   td[9] = loc;
}


float get_scale(float *td)
{
   return td[0];
}
float get_x_rot(float *td)
{
   if (td[2] > 0)
   return acos(td[1]) * 180.0 / M_PI;
   else
   return -acos(td[1]) * 180.0 / M_PI;
}
float get_y_rot(float *td)
{
   if (td[4] > 0)
   return acos(td[3]) * 180.0 / M_PI;
   else
   return -acos(td[3]) * 180.0 / M_PI;
}
float get_z_rot(float *td)
{
   if (td[6] > 0)
   return acos(td[5]) * 180.0 / M_PI;
   else
   return -acos(td[5]) * 180.0 / M_PI;
}
float get_x_loc(float *td)
{
   return td[7];
}
float get_y_loc(float *td)
{
   return td[8];
}
float get_z_loc(float *td)
{
   return td[9];
}


// rotate using unit circle coordinates
void ucRot(float hUc, float vUc, float *hP, float *vP)
{
   float h = *vP * -vUc + *hP * hUc;
   float v = *hP * vUc + *vP * hUc;
   *hP = h;
   *vP = v;
}

void rotate(float *verts, int cnt, float x, float y, float z)
{
   int i;
   float xh, xv, yh, yv, zh, zv;

   x *= M_PI / 180.0;
   xh = cos(x);
   xv = sin(x);
   
   for (i=0; i < cnt; i+=3)
   ucRot(xh, xv, &verts[i+1], &verts[i+2]);

   y *= M_PI / 180.0;
   yh = cos(y);
   yv = sin(y);
   
   for (i=0; i < cnt; i+=3)
   ucRot(yh, yv, &verts[i+0], &verts[i+2]);

   z *= M_PI / 180.0;
   zh = cos(z);
   zv = sin(z);
   
   for (i=0; i < cnt; i+=3)
   ucRot(zh, zv, &verts[i+0], &verts[i+1]);
}


// shader compilation helper
GLuint compileShader(GLenum type, const char* source, const char* shaderName)
{
   GLuint shader = glCreateShader(type);
   glShaderSource(shader, 1, &source, NULL);
   glCompileShader(shader);
   
   int success;
   char infoLog[512];
   glGetShaderiv(shader, GL_COMPILE_STATUS, &success);
   if (!success)
   {
      glGetShaderInfoLog(shader, 512, NULL, infoLog);
      fprintf(stderr, "SHADER ERROR: %s, COMPILATION FAILED\n%s\n", shaderName, infoLog);
      glDeleteShader(shader);
      return 0;
   }
   
   return shader;
}

// shader program linking helper
GLuint linkShaderProgram(GLuint vertexShader, GLuint fragmentShader)
{
   GLuint shaderProgram = glCreateProgram();
   glAttachShader(shaderProgram, vertexShader);
   glAttachShader(shaderProgram, fragmentShader);
   glLinkProgram(shaderProgram);
   
   int success;
   char infoLog[512];
   glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
   if (!success)
   {
      glGetProgramInfoLog(shaderProgram, 512, NULL, infoLog);
      fprintf(stderr, "PROGRAM ERROR: LINKING FAILED\n%s\n", infoLog);
      glDeleteProgram(shaderProgram);
      return 0;
   }
   
   return shaderProgram;
}

// GLFW error callback
void error_callback(int error, const char* description)
{
   fprintf(stderr, "GLFW Error %d: %s\n", error, description);
}

// GLFW framebuffer size callback
void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
   glViewport(0, 0, width, height);
}


int main()
{
   // initialize GLFW
   glfwSetErrorCallback(error_callback);
   if (!glfwInit())
   {
      fprintf(stderr, "Failed to initialize GLFW\n");
      return -1;
   }
   glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
   glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
   glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

   // create window
   GLFWwindow* window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, WINDOW_TITLE, NULL, NULL);
   if (window == NULL)
   {
      fprintf(stderr, "Failed to create GLFW window\n");
      glfwTerminate();
      return -1;
   }
   glfwMakeContextCurrent(window);
   glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

   // initialize GLEW
   GLenum err = glewInit();
   if (GLEW_OK != err)
   {
      fprintf(stderr, "Error initializing GLEW: %s\n", glewGetErrorString(err));
      glfwTerminate();
      return -1;
   }
   printf("OpenGL Version: %s\n", glGetString(GL_VERSION));

   // compile and link shaders
   GLuint vertexShader = compileShader(GL_VERTEX_SHADER, vertexShaderSource, "VERTEX");
   GLuint fragmentShader = compileShader(GL_FRAGMENT_SHADER, fragmentShaderSource, "FRAGMENT");
   if (vertexShader == 0 || fragmentShader == 0)
   {
      glfwTerminate();
      return -1;
   }
   GLuint shaderProgram = linkShaderProgram(vertexShader, fragmentShader);
   glDeleteShader(vertexShader);
   glDeleteShader(fragmentShader);
   if (shaderProgram == 0)
   {
      glfwTerminate();
      return -1;
   }

   // configure OpenGL state
	glClearDepth(-1.0);
	glDepthFunc(GL_GEQUAL);
   glEnable(GL_DEPTH_TEST);
   glEnable(GL_PROGRAM_POINT_SIZE);

   // setup shader variables
   GLint viewMemLoc = glGetUniformLocation(shaderProgram, "view");
   GLint winMemLoc = glGetUniformLocation(shaderProgram, "win");
   GLint fogStartMemLoc = glGetUniformLocation(shaderProgram, "fogStart");
   GLint fogEndMemLoc = glGetUniformLocation(shaderProgram, "fogEnd");
   GLint fogColorMemLoc = glGetUniformLocation(shaderProgram, "fogColor");
   GLuint transformCamLoc = glGetUniformLocation(shaderProgram, "transformCam");
   GLuint transformObjLoc = glGetUniformLocation(shaderProgram, "transformObj");
   GLint pointSizeMemLoc = glGetUniformLocation(shaderProgram, "pointSize");

   
   // load 3D objects
   int i;
   int vObjCnt = 7;
   char *vObjs_filename[] = {
   "highStreetA.jpeg",
   "highStreetB.jpeg",
   "highStreetC.jpeg",
   "highStreetD.jpeg",
   "cameraA.png",
   "cameraB.png",
   "cameraC.png"};
   struct vert_obj vObjs[7] = {0};
   struct vert_obj *camImg = &vObjs[4];
   GLuint VAO[7], VBO_vertices[7], VBO_colors[7];
   
   // load image data
   for (i=0; i < vObjCnt; i++)
   {
      loadImg(vObjs_filename[i], &vObjs[i].verts, &vObjs[i].vCols, &vObjs[i].vertCnt);
      vObjs[i].id = i;
      vObjs[i].ptSize = 1;
      set_scale(vObjs[i].td, 1.0);
      set_x_rot(vObjs[i].td, 0.0);
      set_y_rot(vObjs[i].td, 0.0);
      set_z_rot(vObjs[i].td, 0.0);
   }
   
   // rotate the cameras to point forwards
   rotate(vObjs[4].verts, vObjs[4].vertCnt*3, 0.0, 90.0, 0.0);
   rotate(vObjs[5].verts, vObjs[5].vertCnt*3, 0.0, 90.0, 0.0);
   rotate(vObjs[6].verts, vObjs[6].vertCnt*3, 0.0, 90.0, 0.0);
   
   // send data to the graphics processor
   for (i=0; i < vObjCnt; i++)
   {
      glGenVertexArrays(1, &VAO[i]); // generate and bind Vertex Array Object
      glBindVertexArray(VAO[i]); // set configuration for this VAO

      glGenBuffers(1, &VBO_vertices[i]);// Vertex Buffer Object (VBO) for positions
      glBindBuffer(GL_ARRAY_BUFFER, VBO_vertices[i]); // Bind the buffer
      
      // copy vertex data into the buffer's memory
      glBufferData(GL_ARRAY_BUFFER, vObjs[i].vertCnt*3*sizeof(float), vObjs[i].verts, GL_STATIC_DRAW);
      glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
      glEnableVertexAttribArray(0); // enable the vertex attribute

      glGenBuffers(1, &VBO_colors[i]); // Vertex Buffer Object (VBO) for colors
      glBindBuffer(GL_ARRAY_BUFFER, VBO_colors[i]); // bind the buffer
      
      // copy color data into the buffer's memory
      glBufferData(GL_ARRAY_BUFFER, vObjs[i].vertCnt*3*sizeof(float), vObjs[i].vCols, GL_STATIC_DRAW);
      glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
      glEnableVertexAttribArray(1); // enable the vertex attribute
      
      glBindBuffer(GL_ARRAY_BUFFER, 0); // unbind the VBO
      glBindVertexArray(0); // unbind the VAO
   }
   
   
   // set up camera transformation data
   float camera_td[10] = {0};
   set_scale(camera_td, 1.0);
   set_x_rot(camera_td, 0.0);
   set_y_rot(camera_td, 0.0);
   set_z_rot(camera_td, 0.0);
   
   // set view clipping, perspective, fog
   int width, height;
   float viewStart = 600;
   float viewEnd = -600;
   float persp = 410;
   int orth = FALSE;
   int unitPerPix = TRUE; // will move the lens until "1 unit" == "1 pixel"
   float zMov, zSz;
   
   float fogColor[3] = {0.0, 0.0, 0.0};
   float fogStart = 100.0;
   float fogEnd = -1000.0;
   
   setCameraLens(viewStart, viewEnd, orth, unitPerPix, &persp, &zMov, &zSz);
   
   
   // place objects in environment
   set_z_loc(vObjs[0].td, 800);
   set_z_loc(vObjs[1].td, -800);

   set_y_rot(vObjs[2].td, 90);
   set_y_rot(vObjs[3].td, 90);
   set_x_loc(vObjs[2].td, 800);
   set_x_loc(vObjs[3].td, -800);

   set_x_loc(vObjs[4].td, -200);
   set_x_loc(vObjs[6].td, 200);
   
   // set FPS timer variables
   #define FPS_SETTING 20
   struct timeval start, end;
   int frameCount = 0;
   gettimeofday(&start, NULL); // get the initial time
   int sleep_time = 1000000 / FPS_SETTING; // convert to microseconds
   
   // rendering loop
   while (!glfwWindowShouldClose(window))
   {
      glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
      
      // activate shader program
      glUseProgram(shaderProgram);
      
      // window settings
      glfwGetWindowSize(window, &width, &height);
      glUniform2f(winMemLoc, width, height);
      
      // view settings
      glUniform3f(viewMemLoc, persp, zMov, zSz);
      
      // fog settings
      glUniform3fv(fogColorMemLoc, 1, fogColor);
      glUniform1f(fogStartMemLoc, fogStart);
      glUniform1f(fogEndMemLoc, fogEnd);
      
      // set point size
      glUniform1f(pointSizeMemLoc, 1.0);
   
   
      // keyboard input
      if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS) // exit
      glfwSetWindowShouldClose(window, GL_TRUE);
      
      
      if (glfwGetKey(window, GLFW_KEY_1) == GLFW_PRESS)
      camImg = &vObjs[4];
      
      if (glfwGetKey(window, GLFW_KEY_2) == GLFW_PRESS)
      camImg = &vObjs[5];
      
      if (glfwGetKey(window, GLFW_KEY_3) == GLFW_PRESS)
      camImg = &vObjs[6];
      
      
      float turnUpDwn = get_x_rot(camImg->td);
      float turnLR = get_y_rot(camImg->td);
      float moveFwdBwd = 0.0;
      float moveLR = 0.0;
      float xTravDist, yTravDist, zTravDist;
      
      if (glfwGetKey(window, GLFW_KEY_LEFT) == GLFW_PRESS)
      turnLR -= 6.8;
      
      if (glfwGetKey(window, GLFW_KEY_RIGHT) == GLFW_PRESS)
      turnLR += 6.8;

      if (glfwGetKey(window, GLFW_KEY_UP) == GLFW_PRESS)
      turnUpDwn += 4.5;
      
      if (glfwGetKey(window, GLFW_KEY_DOWN) == GLFW_PRESS)
      turnUpDwn -= 4.5;
      
      if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)
      moveFwdBwd = 15.8;
      
      if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS)
      moveFwdBwd = -15.8;

      if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS)
      moveLR = -15.8;
      
      if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS)
      moveLR = 15.8;
      

      // animate the camera moving or moving toward a camera image
      float camImg_rot = get_y_rot(camImg->td);
      
      // correction for when the rotation goes over 180 degrees 
      if ((get_y_rot(camImg->td) < 0) && (get_y_rot(camera_td) > 90))
      camImg_rot += 360;
      
      // correction for when the rotation goes under -180 degrees 
      if ((get_y_rot(camImg->td) > 0) && (get_y_rot(camera_td) < -90))
      camImg_rot -= 360;
      
      set_y_rot(camera_td, (camImg_rot - get_y_rot(camera_td))*0.15 + get_y_rot(camera_td));
      set_x_loc(camera_td, (get_x_loc(camImg->td) - get_x_loc(camera_td))*0.2 + get_x_loc(camera_td));
      set_z_loc(camera_td, (get_z_loc(camImg->td) - get_z_loc(camera_td))*0.2 + get_z_loc(camera_td));
   
      camImg_rot = get_x_rot(camImg->td);
      
      // correction for when the rotation goes over 180 degrees 
      if ((get_x_rot(camImg->td) < 0) && (get_x_rot(camera_td) > 90))
      camImg_rot += 360;
      
      // correction for when the rotation goes under -180 degrees 
      if ((get_x_rot(camImg->td) > 0) && (get_x_rot(camera_td) < -90))
      camImg_rot -= 360;
      
      set_x_rot(camera_td, (camImg_rot - get_x_rot(camera_td))*0.15 + get_x_rot(camera_td));
      set_y_loc(camera_td, (get_y_loc(camImg->td) - get_y_loc(camera_td))*0.2 + get_y_loc(camera_td));
   
      
      set_x_rot(camImg->td, turnUpDwn);
      
      yTravDist = moveFwdBwd * sin(turnUpDwn * (M_PI / 180.0));
      set_y_loc(camImg->td, get_y_loc(camImg->td) + yTravDist);
      
      // shortend the surface travel distance by the up/down rotation amount
      moveFwdBwd *= cos(turnUpDwn * (M_PI / 180.0));
      ///////////////////////////////////////////////////////////
      
      
      // find the travel distance that can be added to the current location
      xTravDist = moveFwdBwd * sin(turnLR * (M_PI / 180.0));
      zTravDist = -moveFwdBwd * cos(turnLR * (M_PI / 180.0));
      
      set_x_loc(camImg->td, get_x_loc(camImg->td) + xTravDist);
      set_z_loc(camImg->td, get_z_loc(camImg->td) + zTravDist);
      
      // move left and right
      turnLR += 90;
      xTravDist = moveLR * sin(turnLR * (M_PI / 180.0));
      zTravDist = -moveLR * cos(turnLR * (M_PI / 180.0));
      turnLR -= 90;
      
      set_x_loc(camImg->td, get_x_loc(camImg->td) + xTravDist);
      set_z_loc(camImg->td, get_z_loc(camImg->td) + zTravDist);
      
      // rotate object to the direction of travel
      set_y_rot(camImg->td, turnLR);
      
      // add camera transformation data
      glUniform1fv(transformCamLoc, 10, camera_td);
      
      for (i=0; i < vObjCnt; i++)
      {
         glUniform1fv(transformObjLoc, 10, vObjs[i].td); // add object transformation data
         
         glBindVertexArray(VAO[i]); // bind the VAO
         glDrawArrays(GL_POINTS, 0, vObjs[i].vertCnt);
         glBindVertexArray(0); // unbind the VAO
      }

      glfwSwapBuffers(window); // swap buffers
      glfwPollEvents(); // poll events
      

      usleep(sleep_time); // FPS limiter
      
      // calculate the elapsed time in seconds
      frameCount++;
      gettimeofday(&end, NULL); // get the current time
      double elapsedTime = (end.tv_sec - start.tv_sec) + 
                           (end.tv_usec - start.tv_usec) / 1000000.0;

      // update FPS every second
      if (elapsedTime >= 1.0)
      {
         printf("FPS: %d\n", frameCount);
         printf("\033[A"); // move cursor up one line
         frameCount = 0;
         start = end; // reset start time
      }
   }

   
   for (i=0; i < vObjCnt; i++)
   {
      glDeleteVertexArrays(1, &VAO[i]);
      glDeleteBuffers(1, &VBO_vertices[i]);
      glDeleteBuffers(1, &VBO_colors[i]);
      freeImg(vObjs[i].verts, vObjs[i].vCols);
   }
   
   glDeleteProgram(shaderProgram);

   glfwDestroyWindow(window);
   glfwTerminate();
   return 0;
}