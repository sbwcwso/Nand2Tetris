// function SimpleFunction.test 2
    (SimpleFunction.test)
    @SP
	A=M
	M=0
	@SP
	M=M+1
	A=M
	M=0
	@SP
	M=M+1
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
// push local 1
    @1
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
// not
    @SP
    M = M - 1
    A = M
    M = !M // push (not y)
    @SP
    M = M + 1
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
// push argument 1
    @1
    D = A
    @ARG
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
// return
    @LCL        // FRAME(R14) = LCL
    D = M
    @R14
    M = D
    @5          // RET(R15) = *(FRAME - 5)
    D = A
    @R14
    A = M - D  
    D = M
    @R15
    M = D
    @SP         // *ARG = pop()
    M = M - 1
    A = M
    D = M
    @ARG
    A = M
    M = D
    @ARG        // SP = ARG + 1
    D = M + 1
    @SP
    M = D
    @R14        // THAT=*(FRAME-1)
    M = M - 1
    A = M
    D = M
    @THAT
    M = D
    @R14        // THIS=*(FRAME-2)
    M = M - 1
    A = M
    D = M
    @THIS
    M = D
    @R14        // ARG=*(FRAME-3)
    M = M - 1
    A = M
    D = M
    @ARG
    M = D
    @R14        // LCL=*(FRAME-1)
    M = M - 1
    A = M
    D = M
    @LCL
    M = D
    @R15        // goto RET
    A = M
    0;JMP
