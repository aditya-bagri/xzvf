#!/usr/bin/env python

import time
import csv
import numpy as np
import pyopencl as cl
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
mpl.rcParams['savefig.dpi'] = 100

from pylab import *

NAME = 'NVIDIA CUDA'
platforms = cl.get_platforms()			#PLATFORM
devices = None
for platform in platforms:
    if platform.name == NAME:
        devices = platform.get_devices()	#DEVICES on each platform

ctx=cl.Context(devices)				#CONTEXT
queue=cl.CommandQueue(ctx)			#COMMAND QUEUE

MAX_PARAM = 50

print "##############################################"
print "Matrix Transpose\n"

#### Defining the Initial Kernel ####

###func0: Naive Implementation ###
					
func0= cl.Program(ctx,"""					
#pragma OPENCL EXTENSION cl_khr_fp64: enable

__kernel void mat_transpose(__global float* A, __global float *A_trans, unsigned int H_A, unsigned int W_A) {
        unsigned int i = get_global_id(0);
        unsigned int j = get_global_id(1);
	A_trans[i*H_A+j]=0;
        A_trans[i*H_A + j]= A[j*W_A +i];
}
""").build().mat_transpose						#KERNEL

""" """
func0.set_scalar_arg_dtypes([None, None, np.uint32, np.uint32])

def trans_op_0(a_buf, atrans_buf, H_A, W_A):
	start = time.time()
	func0(queue, (W_A, H_A), None, a_buf, atrans_buf, np.uint32(H_A), np.uint32(W_A))
    	return time.time()-start

def cl_op_0_trans(a,a_trans,HA,WA):
	a_buf, atrans0_buf = mem_alloc(a, a_trans)
        t=trans_op_0(a_buf,atrans0_buf, HA, WA)
        a_trans0=mem_transfer(a_trans,atrans0_buf)
	return t, a_trans0

###func1: Row Optimisation (All Global)###

func1= cl.Program(ctx,"""
#pragma OPENCL EXTENSION cl_khr_fp64: enable

__kernel void mat_transpose(__global float* A, __global float *A_trans, unsigned int H_A, unsigned int W_A) {
        unsigned int i = get_global_id(0);
        unsigned int j;
	
	for (j=0;j<H_A;j++) {
                A_trans[i*H_A + j]=0.0;
        }

	for (j=0;j<H_A;j++) {
        	A_trans[i*H_A + j]= A[j*W_A +i];
	}
}
""").build().mat_transpose                                              #KERNEL
""" """
func1.set_scalar_arg_dtypes([None, None, np.uint32, np.uint32])

def trans_op_1(a_buf, atrans_buf, H_A, W_A):
    start = time.time()
    func1(queue, (W_A, ), None, a_buf, atrans_buf, np.uint32(H_A), np.uint32(W_A))
    return time.time()-start

def cl_op_1_trans(a,a_trans,HA,WA):
        a_buf, atrans1_buf = mem_alloc(a, a_trans)
        t=trans_op_1(a_buf,atrans1_buf, HA, WA)
        a_trans1=mem_transfer(a_trans,atrans1_buf)
	return t, a_trans1

""" """
###func2: Row Optimisation (Row Private)###

func2= cl.Program(ctx,"""
#pragma OPENCL EXTENSION cl_khr_fp64: enable

__kernel void mat_transpose(__global float* A, __global float *A_trans, unsigned int H_A, unsigned int W_A) {
        unsigned int i = get_global_id(0);
        unsigned int j,k;
	float A_temp[1024];	

	for (k=0;k<H_A;k++) {
                A_temp[k]=A[k*W_A + i];
        }

        for (j=0;j<H_A;j++) {
                A_trans[i*H_A + j]= A_temp[j];
        }

}
""").build().mat_transpose                                              #KERNEL
""" """
func2.set_scalar_arg_dtypes([None, None, np.uint32, np.uint32])

def trans_op_2(a_buf, atrans_buf, H_A, W_A):
    start = time.time()
    func2(queue, (W_A, ), None, a_buf, atrans_buf, np.uint32(H_A), np.uint32(W_A))
    return time.time()-start

def cl_op_2_trans(a,a_trans,HA,WA):
        a_buf, atrans2_buf = mem_alloc(a, a_trans)
        t=trans_op_2(a_buf,atrans2_buf, HA, WA)
        a_trans2=mem_transfer(a_trans,atrans2_buf)
        return t, a_trans2

###func3: Localization (All Local)###

func3= cl.Program(ctx,"""
#pragma OPENCL EXTENSION cl_khr_fp64: enable

__kernel void mat_transpose(__global float* A, __global float *A_trans, unsigned int H_A, unsigned int W_A, __local float* A_temp) {
        unsigned int i = get_global_id(0);
	unsigned int iloc = get_local_id(0);
    	unsigned int nloc = get_local_size(0);
        
	unsigned int j,k;
        //float A_temp[1024];

	for (j=0;j<H_A;j++) {
        	for (k=iloc;k<W_A;k+=nloc) {
                	A_temp[k]=A[j*W_A + k];
        	}
	barrier(CLK_LOCAL_MEM_FENCE);
		for (k=0; k<W_A;k++)
                A_trans[k*H_A + j]= A_temp[k];
        }

}
""").build().mat_transpose                                              #KERNEL

func3.set_scalar_arg_dtypes([None, None, np.uint32, np.uint32, None])

def trans_op_3(a_buf, atrans_buf, H_A, W_A):
	a_col = cl.LocalMemory(np.float32().nbytes*H_A)
    	local_size=32
	start = time.time()
    	func3(queue, (W_A, ), None, a_buf, atrans_buf, np.uint32(H_A), np.uint32(W_A),a_col)
    	return time.time()-start

def cl_op_3_trans(a,a_trans,HA,WA):
        a_buf, atrans3_buf = mem_alloc(a, a_trans)
        t=trans_op_3(a_buf,atrans3_buf, HA, WA)
        a_trans3=mem_transfer(a_trans,atrans3_buf)
        return t, a_trans3




##########################################################################################


def create_arrays(height_A,width_A):
	A=np.random.random((height_A,width_A)).astype(np.float32)
	A_trans=np.zeros((width_A,height_A)).astype(np.float32)
	return A, A_trans

def mem_alloc(A, A_trans):
	mf=cl.mem_flags								#MEMORY_FLAG allocation
	a_buf=cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=A)
	atrans_buf=cl.Buffer(ctx, mf.WRITE_ONLY, A_trans.nbytes)
	init_arr=np.zeros((W_A,H_A)).astype(np.float32)
	cl.enqueue_copy(queue,atrans_buf,init_arr)				#Initializing the Memory of the Output Buffers 
	return a_buf, atrans_buf	

def mem_transfer(A_trans, atrans_buf):
	cl.enqueue_copy(queue,A_trans,atrans_buf)						#Copying Final Data into Python Buffers
	return A_trans

 
def py_trans(A,y):
	start=time.time()
	y=np.transpose(A)
	t= time.time()-start
	return t,y

def py_time(HA,WA,M=4):
	times = []
	A,y=create_arrays(HA,WA)
	for i in xrange(M):
    		t,y=py_trans(A,y)
    		times.append(t)
	#print 'python time:  ', np.average(times)
	return np.average(times)
 
def cl_op0_time(HA, WA, M=4):
	times = []
	a, atrans =create_arrays(HA,WA)
	a_buf, atrans_buf = mem_alloc(a, atrans)
	for i in xrange(M):
		t=trans_op_0(a_buf,atrans_buf, HA, WA)
		times.append(t)
		atrans=mem_transfer(atrans,atrans_buf)
	#print 'opencl op0 time:  ', np.average(times)
	return np.average(times)

def cl_op1_time(HA, WA, M=4):
        times = []
        a, atrans =create_arrays(HA,WA)
        a_buf, atrans_buf = mem_alloc(a, atrans)
        for i in xrange(M):
                t=trans_op_1(a_buf,atrans_buf, HA, WA)
                times.append(t)
                atrans=mem_transfer(atrans,atrans_buf)
        #print 'opencl op1 time:  ', np.average(times)
	return np.average(times)

def cl_op2_time(HA, WA, M=4):
        times = []
        a, atrans =create_arrays(HA,WA)
        a_buf, atrans_buf = mem_alloc(a, atrans)
        for i in xrange(M):
                t=trans_op_2(a_buf,atrans_buf, HA, WA)
                times.append(t)
                atrans=mem_transfer(atrans,atrans_buf)
        #print 'opencl op1 time:  ', np.average(times)
        return np.average(times)

def cl_op3_time(HA, WA, M=4):
        times = []
        a, atrans =create_arrays(HA,WA)
        a_buf, atrans_buf = mem_alloc(a, atrans)
        for i in xrange(M):
                t=trans_op_3(a_buf,atrans_buf, HA, WA)
                times.append(t)
                atrans=mem_transfer(atrans,atrans_buf)
        #print 'opencl op1 time:  ', np.average(times)
        return np.average(times)


######################################################################

### Initialising the parameters ####
H_A=6
W_A=8


a, atrans=create_arrays(H_A,W_A)
#print "A\n", a
a_buf, atrans_buf=mem_alloc(a,atrans)
atrans=mem_transfer(atrans, atrans_buf)


python_time,A_trans_py =py_trans(a, atrans)
#print "A' Python:\n", A_trans_py

### Verifying that the results are equal ###

pyopencl_time0, A_trans_cl0=cl_op_0_trans(a,atrans,H_A,W_A)
#print "A' op0\n",A_trans_cl0
print "op0 equal:\t",np.allclose(A_trans_py,A_trans_cl0)

pyopencl_time1, A_trans_cl1=cl_op_1_trans(a,atrans,H_A,W_A)
#print "A' op1\n",A_trans_cl1
print "op1 equal:\t",np.allclose(A_trans_py,A_trans_cl1)

pyopencl_time2, A_trans_cl2=cl_op_2_trans(a,atrans,H_A,W_A)
#print "A' op2\n",A_trans_cl2
print "op2 equal:\t",np.allclose(A_trans_py,A_trans_cl2)

#pyopencl_time3, A_trans_cl3=cl_op_3_trans(a,atrans,H_A,W_A)
##print "A' op3\n",A_trans_cl3
#print "op3 equal:\t",np.allclose(A_trans_py,A_trans_cl3)


#############################################################################################

### Comparing python & pyopenCL timings ###

python_times=[]
pyopencl_op0_times=[]
pyopencl_op1_times=[]
pyopencl_op2_times=[]
pyopencl_op3_times=[]

param=np.arange(1,201,1).astype(np.int32)

for i in param:
	python_times.append(py_time(i*H_A,i*W_A,4))
	pyopencl_op0_times.append(cl_op0_time(i*H_A,i*W_A,4))
        pyopencl_op1_times.append(cl_op1_time(i*H_A,i*W_A,4))
        pyopencl_op2_times.append(cl_op2_time(i*H_A,i*W_A,4))
#        pyopencl_op3_times.append(cl_op3_time(i*H_A,i*W_A,4))


print "\nDim\t\t", "Python_time\t\t", "Naive_transpose\t\t", "Row Optimisation\t", "Row Optimisation(Row pvt)\t\t" 
for i in param:
	print "(",i*H_A, ",",i*W_A,")\t", python_times[i-1],"\t", pyopencl_op0_times[i-1], "\t", pyopencl_op1_times[i-1], "\t", pyopencl_op2_times[i-1],"\t"#, pyopencl_op3_times[i]

for i in param:
	if pyopencl_op1_times[i-1] < pyopencl_op0_times[i-1]:
		print "\nAt a dimension size of (", i*H_A, ",", i*W_A, "), Row Optimization beats Naive Transpose implementations" 
		break

for i in param:
        if pyopencl_op2_times[i-1] < pyopencl_op0_times[i-1]:
                print "\nAt a dimension size of (", i*H_A, ",", i*W_A, "), Row Privatization beats Naive Transpose implementations"
                break

 
plt.clf()
plt.plot(param*H_A*param*W_A, pyopencl_op0_times, 'r*-',
	 param*H_A*param*W_A, pyopencl_op1_times, 'b*-',
	 param*H_A*param*W_A, pyopencl_op2_times, 'g*-',
	 param*H_A*param*W_A, python_times, 'k*-')

plt.xlabel('# elements in matrix A')
plt.ylabel('$t$')
plt.title('Scaling of Different Implementations')
plt.legend(('op0: Naive', 'op1: Row Work Group', 'op2: Row pvt', 'python'), loc='upper left')
plt.grid(True)
#plt.draw()
plt.savefig('Transpose_scaling.png')


with open('Transpose_scaling.csv', 'w') as f:
    w = csv.writer(f)
    for a_size, b_size,t_op_0, t_op_1, t_op_2, t_py in \
        zip(param*H_A, param*W_A,
            python_times, pyopencl_op0_times, pyopencl_op1_times,
            pyopencl_op2_times):
        w.writerow([a_size, b_size,t_py ,t_op_0, t_op_1, t_op_2])







print "###############################################################"
print "Multiplication of y=A*(B+C)"
print ""

#### Defining the Naive Kernel ####
					
func4= cl.Program(ctx,"""					
#pragma OPENCL EXTENSION cl_khr_fp64: enable

__kernel void mat_transpose(__global float* A, __global float* B, __global float* C, __global float* D, unsigned int SIZE) {
        unsigned int i = get_global_id(0);
        unsigned int j = get_global_id(1);
	unsigned int k;	
	float temp=0.0;

	for (k=0; k<SIZE; k++) {
	
		temp += (A[i*SIZE + k] * (B[k*SIZE + j] + C[k*SIZE+j]));	

	}

	D[i*SIZE + j] = temp;
}
""").build().mat_transpose						#KERNEL
func4.set_scalar_arg_dtypes([None, None, None, None, np.uint32])

def trans_op_4(a_buf, b_buf,c_buf, d_buf, siz):
    start = time.time()
    func4(queue, (siz,siz), None, a_buf, b_buf, c_buf, d_buf, np.uint32(siz))
    return time.time()-start


def cl_op_4_trans(a,b,c,d,siz):
        a_buf,b_buf,c_buf, d_buf = mem_alloc(a,b,c,d)
        t=trans_op_4(a_buf,b_buf,c_buf,d_buf, siz)
        d=mem_transfer(d,d_buf)
        return t, d



#############################################################################################


#### Defining the Tiled Kernel ####

func5= cl.Program(ctx,"""
#pragma OPENCL EXTENSION cl_khr_fp64: enable

__kernel void mat_transpose(__global float* A, __global float* B, __global float* C, __global float* D, unsigned int SIZE, unsigned int m, unsigned int n, unsigned int p) {

    __local float AS[1024];
    __local float BCS[1024];

    int i = get_global_id(1);
    int j = get_global_id(0);
	
    int bx = get_group_id(0);
    int by = get_group_id(1);

    int tx = get_local_id(0);
    int ty = get_local_id(1);

    int aBegin = n* SIZE * by;
    int aEnd   = aBegin + n - 1;
    int aStep  = SIZE;

    int bBegin = SIZE * bx;
    int bStep  = SIZE * p;

    float temp = 0.0f;

    for (int a = aBegin, b = bBegin; a <= aEnd;a += aStep, b += bStep) 
    {

        AS[tx + ty*SIZE] = A[a + n * ty + tx];
        BCS[tx + ty*SIZE] = B[b + p*ty + tx] + C[b + p*ty + tx];

        barrier(CLK_LOCAL_MEM_FENCE);

        for (int k = 0; k < SIZE; ++k)
            temp += AS[ty*SIZE + k] * BCS[k*SIZE + tx];
        barrier(CLK_LOCAL_MEM_FENCE);
    }

    D[i * p + j] = temp;


}
""").build().mat_transpose                                              #KERNEL
func5.set_scalar_arg_dtypes([None, None, None, None, np.uint32, np.uint32, np.uint32, np.uint32])

def trans_op_5(a_buf, b_buf,c_buf, d_buf, siz, m, n, p):
    start = time.time()
    func5(queue, (m,p), (siz,siz), a_buf, b_buf, c_buf, d_buf, np.uint32(siz), np.uint32(m), np.uint32(n), np.uint32(p))
    return time.time()-start


def cl_op_5_trans(a,b,c,d,siz,m,n,p):
        a_buf,b_buf,c_buf, d_buf = mem_alloc(a,b,c,d)
        t=trans_op_5(a_buf,b_buf,c_buf,d_buf, siz, m,n,p)
        d=mem_transfer(d,d_buf)
        return t, d



#############################################################################################



def create_arrays(size):
	A=np.random.random((size,size)).astype(np.float32)
	B=np.random.random((size,size)).astype(np.float32)
	C=np.random.random((size,size)).astype(np.float32)
	D=np.zeros((size,size)).astype(np.float32)
	return A, B, C, D

def create_arrays_2(m,n,p):
	A=np.random.random((m,n)).astype(np.float32)
        B=np.random.random((n,p)).astype(np.float32)
        C=np.random.random((n,p)).astype(np.float32)
        D=np.zeros((m,p)).astype(np.float32)
        return A, B, C, D


def mem_alloc(A, B, C, D):
	mf=cl.mem_flags								#MEMORY_FLAG allocation
	a_buf=cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=A)
	b_buf=cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=B)
	c_buf=cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=C)
	d_buf=cl.Buffer(ctx, mf.WRITE_ONLY, D.nbytes)
	init_arr=np.zeros(D.shape).astype(np.float32)
	cl.enqueue_copy(queue,d_buf,init_arr)				#Initializing the Memory of the Output Buffers 
	return a_buf, b_buf, c_buf, d_buf	



#prg=cl.Program(ctx,kernel).build()					#PROGRAM
#prg.mat_transpose(queue,A_trans.shape,None,a_buf,atrans_buf,np.uint32(height_A),np.uint32(width_A)) 	#KERNEL LAUNCH
def mem_transfer(D, d_buf):
	cl.enqueue_copy(queue,D,d_buf)						#Copying Final Data into Python Buffers
	return D

#print "A\n", A
#print "A_transpose_OpenCL\n", A_trans
#print "A_transpose_python\n", A_trans2
#print 'equal:        ', np.allclose(A_trans, A_trans2)
 
def py_calc(A,B,C,y):
	start=time.time()
	y=np.dot(A,B+C)
	t= time.time()-start
	return t,y

def py_calc_time(siz,M=4):
	times = []
	a, b,c,d =create_arrays(siz)
        a_buf, b_buf, c_buf, d_buf = mem_alloc(a, b, c, d)
	for i in xrange(M):
    		t,y=py_calc(a,b,c,d)
    		times.append(t)
	#print 'python time:  ', np.average(times)
	return np.average(times)
 
def cl_op4_time(siz, M=4):
	times = []
	a, b,c,d =create_arrays(siz)
	a_buf, b_buf, c_buf, d_buf = mem_alloc(a, b, c, d)
	for i in xrange(M):
		t=trans_op_4(a_buf,b_buf, c_buf, d_buf, siz)
		times.append(t)
		d=mem_transfer(d,d_buf)
	#print 'opencl time:  ', np.average(times)
	return np.average(times)

def cl_op5_time(siz,m,n,p, M=4):
        times = []
        a, b,c,d =create_arrays_2(m,n,p)
        a_buf, b_buf, c_buf, d_buf = mem_alloc(a, b, c, d)
        for i in xrange(M):
                t=trans_op_5(a_buf,b_buf, c_buf, d_buf, siz, m, n, p)
                times.append(t)
                d=mem_transfer(d,d_buf)
        #print 'opencl time:  ', np.average(times)
	return np.average(times)


#### Testing & Running the code


### Initialising the parameters ####
SIZE=32
m=SIZE
n=SIZE
p=SIZE

a, b,c,d=create_arrays(SIZE)
#print "A\n", a
#print "B\n", b
#print "C\n", c
a_buf, b_buf, c_buf, d_buf=mem_alloc(a,b,c,d)
d=mem_transfer(d, d_buf)


python_time,D_py =py_calc(a, b, c, d)
#print "D Python:\n", D_py

pyopencl_time4, D_cl4=cl_op_4_trans(a,b,c,d,SIZE)
#print "A' op0\n",A_trans_cl0
print "op4 equal:\t",np.allclose(D_py,D_cl4)

pyopencl_time5, D_cl5=cl_op_5_trans(a,b,c,d,SIZE,m,n,p)
#print "A' op0\n",A_trans_cl0
print "op5 equal:\t",np.allclose(D_py,D_cl5)


#########################################################

### Comparing python & pyopenCL timings ###

python_times=[]
pyopencl_op4_times=[]
pyopencl_op5_times=[]

param=np.arange(1,MAX_PARAM,1).astype(np.int32)

for i in param:
        python_times.append(py_calc_time(i*SIZE,4))
        pyopencl_op4_times.append(cl_op4_time(i*SIZE,4))
        pyopencl_op5_times.append(cl_op5_time(SIZE,i*SIZE,i*SIZE,i*SIZE,4))


print "\nDim\t", "Python_time\t", "Naive_Algorithm\t", "Tiling\t" 
for i in param:
        print "(",i*SIZE, ",",i*SIZE,")\t", python_times[i-1],"\t", pyopencl_op4_times[i-1], "\t", pyopencl_op5_times[i-1], "\t"#, pyopencl_op2_times[i-1],"\t"#, pyopencl_op3_times[i]

for i in param:
	if pyopencl_op5_times[i-1]<python_times[i-1]:
		print "\nFor (", i*SIZE, ",",i*SIZE, ") pyopenCL tiling is faster than python."
		break
for i in param:
	if pyopencl_op4_times[i-1]<python_times[i-1]:
                print "For (", i*SIZE, ",", i*SIZE,") pyopenCL (naive) is faster than python."
                break



plt.clf()
plt.plot(param*SIZE, python_times, 'bo-',
         param*SIZE, pyopencl_op4_times, 'r*-',
         param*SIZE, pyopencl_op5_times, 'go-')

plt.xlabel('# elements in square matrix A,B,C,D')
plt.ylabel('$t$')
plt.title('Scaling of Different Implementations')
plt.legend(('Python', 'Naive A*(B+C)', 'Tiling A*(B+C)'), loc='upper left')
plt.grid(True)
plt.gca().set_xlim((min(param*SIZE), max(param*SIZE)))
plt.gca().set_ylim((0, 1.2*max(python_times)))
#plt.draw()
plt.savefig('Multiplication_scaling.png')

plt.clf()
plt.plot(param*SIZE, pyopencl_op4_times, 'r*-',  
         param*SIZE, pyopencl_op5_times, 'go-')

plt.xlabel('# elements in square matrix A,B,C,D')
plt.ylabel('$t$')
plt.title('Scaling of Different Implementations (ZOOMED)')
plt.legend(('Naive A*(B+C)', 'Tiling A*(B+C)'), loc='upper left')
plt.grid(True)
plt.gca().set_xlim((min(param*SIZE), max(param*SIZE)))
#plt.draw()
plt.savefig('Multiplication_scaling_zoom.png')  


with open('Multiplication_scaling.csv', 'w') as f:
    w = csv.writer(f)
    for a_size, t_op_0, t_op_1, t_op_2 in \
        zip(param*SIZE, 
            python_times, pyopencl_op4_times,
            pyopencl_op5_times):
        w.writerow([a_size, t_op_0, t_op_1, t_op_2])


