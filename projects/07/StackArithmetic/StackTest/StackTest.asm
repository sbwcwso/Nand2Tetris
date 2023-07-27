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
    @32
    D;JEQ
    @SP
    A = M
    M = 0         // push false
    @SP      	   // lable_true
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
    @66
    D;JEQ
    @SP
    A = M
    M = 0         // push false
    @SP      	   // lable_true
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
    @100
    D;JEQ
    @SP
    A = M
    M = 0         // push false
    @SP      	   // lable_true
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
    @134
    D;JLT
    @SP
    A = M
    M = 0         // push false
    @SP      	   // lable_true
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
    @168
    D;JLT
    @SP
    A = M
    M = 0         // push false
    @SP      	   // lable_true
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
    @202
    D;JLT
    @SP
    A = M
    M = 0         // push false
    @SP      	   // lable_true
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
    @236
    D;JGT
    @SP
    A = M
    M = 0         // push false
    @SP      	   // lable_true
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
    @270
    D;JGT
    @SP
    A = M
    M = 0         // push false
    @SP      	   // lable_true
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
    @304
    D;JGT
    @SP
    A = M
    M = 0         // push false
    @SP      	   // lable_true
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
