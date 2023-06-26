// push constant 3030
    @3030
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// pop pointer 0
    @SP  // Get data in the stack
    M = M - 1
    A = M
    D = M
    @3
    M = D
// push constant 3040
    @3040
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// pop pointer 1
    @SP  // Get data in the stack
    M = M - 1
    A = M
    D = M
    @4
    M = D
// push constant 32
    @32
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// pop this 2
    @2  // address = segment + index
    D = A
    @THIS
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
// push constant 46
    @46
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// pop that 6
    @6  // address = segment + index
    D = A
    @THAT
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
// push pointer 0
    @3
    D = M
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push pointer 1
    @4
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
// push this 2
    @2
    D = A
    @THIS
    A = D + M
    D = M
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
// push that 6
    @6
    D = A
    @THAT
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
