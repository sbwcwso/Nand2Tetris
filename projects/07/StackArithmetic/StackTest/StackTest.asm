// push constant 17
    @17
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push constant 17
    @17
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// eq
    @SP
    M = M - 1
    @SP
    A = M
    D = M
    @SP
    M = M - 1
    @SP
    A = M
    D = M - D 	    // M = x, D = y, D = x - y
    @SP             // push true(-1) or false(0)
    A = M
    M = -1          // push true
    @$true.1
    D;JEQ
    @SP
    A = M
    M = 0          // push false
    ($true.1)   // lable_true
    @SP      	   
    M = M + 1
// push constant 17
    @17
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push constant 16
    @16
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// eq
    @SP
    M = M - 1
    @SP
    A = M
    D = M
    @SP
    M = M - 1
    @SP
    A = M
    D = M - D 	    // M = x, D = y, D = x - y
    @SP             // push true(-1) or false(0)
    A = M
    M = -1          // push true
    @$true.2
    D;JEQ
    @SP
    A = M
    M = 0          // push false
    ($true.2)   // lable_true
    @SP      	   
    M = M + 1
// push constant 16
    @16
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push constant 17
    @17
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// eq
    @SP
    M = M - 1
    @SP
    A = M
    D = M
    @SP
    M = M - 1
    @SP
    A = M
    D = M - D 	    // M = x, D = y, D = x - y
    @SP             // push true(-1) or false(0)
    A = M
    M = -1          // push true
    @$true.3
    D;JEQ
    @SP
    A = M
    M = 0          // push false
    ($true.3)   // lable_true
    @SP      	   
    M = M + 1
// push constant 892
    @892
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push constant 891
    @891
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// lt
    @SP
    M = M - 1
    @SP
    A = M
    D = M
    @SP
    M = M - 1
    @SP
    A = M
    D = M - D 	    // M = x, D = y, D = x - y
    @SP             // push true(-1) or false(0)
    A = M
    M = -1          // push true
    @$true.4
    D;JLT
    @SP
    A = M
    M = 0          // push false
    ($true.4)   // lable_true
    @SP      	   
    M = M + 1
// push constant 891
    @891
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push constant 892
    @892
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// lt
    @SP
    M = M - 1
    @SP
    A = M
    D = M
    @SP
    M = M - 1
    @SP
    A = M
    D = M - D 	    // M = x, D = y, D = x - y
    @SP             // push true(-1) or false(0)
    A = M
    M = -1          // push true
    @$true.5
    D;JLT
    @SP
    A = M
    M = 0          // push false
    ($true.5)   // lable_true
    @SP      	   
    M = M + 1
// push constant 891
    @891
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push constant 891
    @891
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// lt
    @SP
    M = M - 1
    @SP
    A = M
    D = M
    @SP
    M = M - 1
    @SP
    A = M
    D = M - D 	    // M = x, D = y, D = x - y
    @SP             // push true(-1) or false(0)
    A = M
    M = -1          // push true
    @$true.6
    D;JLT
    @SP
    A = M
    M = 0          // push false
    ($true.6)   // lable_true
    @SP      	   
    M = M + 1
// push constant 32767
    @32767
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push constant 32766
    @32766
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// gt
    @SP
    M = M - 1
    @SP
    A = M
    D = M
    @SP
    M = M - 1
    @SP
    A = M
    D = M - D 	    // M = x, D = y, D = x - y
    @SP             // push true(-1) or false(0)
    A = M
    M = -1          // push true
    @$true.7
    D;JGT
    @SP
    A = M
    M = 0          // push false
    ($true.7)   // lable_true
    @SP      	   
    M = M + 1
// push constant 32766
    @32766
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push constant 32767
    @32767
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// gt
    @SP
    M = M - 1
    @SP
    A = M
    D = M
    @SP
    M = M - 1
    @SP
    A = M
    D = M - D 	    // M = x, D = y, D = x - y
    @SP             // push true(-1) or false(0)
    A = M
    M = -1          // push true
    @$true.8
    D;JGT
    @SP
    A = M
    M = 0          // push false
    ($true.8)   // lable_true
    @SP      	   
    M = M + 1
// push constant 32766
    @32766
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push constant 32766
    @32766
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// gt
    @SP
    M = M - 1
    @SP
    A = M
    D = M
    @SP
    M = M - 1
    @SP
    A = M
    D = M - D 	    // M = x, D = y, D = x - y
    @SP             // push true(-1) or false(0)
    A = M
    M = -1          // push true
    @$true.9
    D;JGT
    @SP
    A = M
    M = 0          // push false
    ($true.9)   // lable_true
    @SP      	   
    M = M + 1
// push constant 57
    @57
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push constant 31
    @31
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push constant 53
    @53
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// add
    @SP
    M = M - 1
    @SP
    A = M
    D = M
    @SP
    M = M - 1
    @SP
    A = M
    M = D + M  // push (M[x] add D[y])
    @SP
    M = M + 1
// push constant 112
    @112
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// sub
    @SP
    M = M - 1
    @SP
    A = M
    D = M
    @SP
    M = M - 1
    @SP
    A = M
    M = M - D  // push (M[x] sub D[y])
    @SP
    M = M + 1
// neg
    @SP
    M = M - 1
    A = M
    M = -M // push (neg y)
    @SP
    M = M + 1
// and
    @SP
    M = M - 1
    @SP
    A = M
    D = M
    @SP
    M = M - 1
    @SP
    A = M
    M = D & M  // push (M[x] and D[y])
    @SP
    M = M + 1
// push constant 82
    @82
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// or
    @SP
    M = M - 1
    @SP
    A = M
    D = M
    @SP
    M = M - 1
    @SP
    A = M
    M = D | M  // push (M[x] or D[y])
    @SP
    M = M + 1
// not
    @SP
    M = M - 1
    A = M
    M = !M // push (not y)
    @SP
    M = M + 1
