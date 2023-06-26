// push constant 0
    @0
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// pop local 0
    @0  // address = segment + index
    D = A
    @LCL
    D = D + M
    @R13
    M = D
    @SP  // Get data in the stack
    M = M - 1
    A = M
    D = M
    @R13  // RAM[address] = data
    A = M
    M = D
// label LOOP_START
    ($LOOP_START)
// push argument 0
    @0
    D = A
    @ARG
    A = D + M
    D = M
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push local 0
    @0
    D = A
    @LCL
    A = D + M
    D = M
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
// pop local 0
    @0  // address = segment + index
    D = A
    @LCL
    D = D + M
    @R13
    M = D
    @SP  // Get data in the stack
    M = M - 1
    A = M
    D = M
    @R13  // RAM[address] = data
    A = M
    M = D
// push argument 0
    @0
    D = A
    @ARG
    A = D + M
    D = M
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push constant 1
    @1
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
// pop argument 0
    @0  // address = segment + index
    D = A
    @ARG
    D = D + M
    @R13
    M = D
    @SP  // Get data in the stack
    M = M - 1
    A = M
    D = M
    @R13  // RAM[address] = data
    A = M
    M = D
// push argument 0
    @0
    D = A
    @ARG
    A = D + M
    D = M
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// if-goto LOOP_START
    @SP
    M = M - 1
    A = M
    D = M
    @$LOOP_START
    D;JNE
// push local 0
    @0
    D = A
    @LCL
    A = D + M
    D = M
    @SP
    A = M
    M = D
    @SP
    M = M + 1
