// function Sys.init 0
    (Sys.init)
    
// push constant 4000
    @4000
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
// push constant 5000
    @5000
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
// call Sys.main 0
    @Sys.init$ret.1     // push return-address
    D = A
    @SP
    A = M
    M = D
    @LCL        // push LCL
    D = M
    @SP
    M = M + 1
    A = M
    M = D
    @ARG        // push ARG
    D = M
    @SP
    M = M + 1
    A = M
    M = D
    @THIS        // push THIS
    D = M
    @SP
    M = M + 1
    A = M
    M = D
    @THAT        // push THAT
    D = M
    @SP
    M = M + 1
    A = M
    M = D
    @SP         // ARG = SP - n - 5
    M = M + 1
    D = M
    @5
    D = D - A
    @0
    D = D - A
    @ARG
    M = D
    @SP         // LCL = SP
    D = M
    @LCL
    M = D
    @Sys.main // goto f
    0;JMP
    (Sys.init$ret.1)
// pop temp 1
    @1  // address = 5 + index
    D = A
    @5
    D = D + A
    @R13 
    M = D
    @SP  // Get data in the stack
    M = M - 1
    A = M
    D = M
    @R13
    A = M
    M = D
// label LOOP
    (Sys.init$LOOP)
// goto LOOP
    @Sys.init$LOOP
    0;JMP
// function Sys.main 5
    (Sys.main)
    @SP
	A=M
	M=0
	@SP
	M=M+1
	A=M
	M=0
	@SP
	M=M+1
	A=M
	M=0
	@SP
	M=M+1
	A=M
	M=0
	@SP
	M=M+1
	A=M
	M=0
	@SP
	M=M+1
// push constant 4001
    @4001
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
// push constant 5001
    @5001
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
// push constant 200
    @200
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// pop local 1
    @1  // address = segment + index
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
// push constant 40
    @40
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// pop local 2
    @2  // address = segment + index
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
// push constant 6
    @6
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// pop local 3
    @3  // address = segment + index
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
// push constant 123
    @123
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// call Sys.add12 1
    @Sys.main$ret.1     // push return-address
    D = A
    @SP
    A = M
    M = D
    @LCL        // push LCL
    D = M
    @SP
    M = M + 1
    A = M
    M = D
    @ARG        // push ARG
    D = M
    @SP
    M = M + 1
    A = M
    M = D
    @THIS        // push THIS
    D = M
    @SP
    M = M + 1
    A = M
    M = D
    @THAT        // push THAT
    D = M
    @SP
    M = M + 1
    A = M
    M = D
    @SP         // ARG = SP - n - 5
    M = M + 1
    D = M
    @5
    D = D - A
    @1
    D = D - A
    @ARG
    M = D
    @SP         // LCL = SP
    D = M
    @LCL
    M = D
    @Sys.add12 // goto f
    0;JMP
    (Sys.main$ret.1)
// pop temp 0
    @0  // address = 5 + index
    D = A
    @5
    D = D + A
    @R13 
    M = D
    @SP  // Get data in the stack
    M = M - 1
    A = M
    D = M
    @R13
    A = M
    M = D
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
// push local 2
    @2
    D = A
    @LCL
    A = D + M
    D = M
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push local 3
    @3
    D = A
    @LCL
    A = D + M
    D = M
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push local 4
    @4
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
    @R14        // LCL=*(FRAME-4)
    M = M - 1
    A = M
    D = M
    @LCL
    M = D
    @R15        // goto RET
    A = M
    0;JMP
// function Sys.add12 0
    (Sys.add12)
    
// push constant 4002
    @4002
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
// push constant 5002
    @5002
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
// push constant 12
    @12
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
    @R14        // LCL=*(FRAME-4)
    M = M - 1
    A = M
    D = M
    @LCL
    M = D
    @R15        // goto RET
    A = M
    0;JMP
