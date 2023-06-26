// init code
	@256
	D=A
	@SP
	M=D
// call Sys.init 0
    @$ret.1     // push return-address
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
    @Sys.init // goto f
    0;JMP
    ($ret.1)
// function Class2.set 0
    (Class2.set)
    
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
// pop static 0
    @SP  // Get data in the stack
    M = M - 1
    A = M
    D = M
    @Class2.0
    M = D
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
// pop static 1
    @SP  // Get data in the stack
    M = M - 1
    A = M
    D = M
    @Class2.1
    M = D
// push constant 0
    @0
    D = A
    @SP
    A = M
    M = D
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
// function Class2.get 0
    (Class2.get)
    
// push static 0
    @Class2.0
    D = M
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push static 1
    @Class2.1
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
// init code
	@256
	D=A
	@SP
	M=D
// call Sys.init 0
    @$ret.1     // push return-address
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
    @Sys.init // goto f
    0;JMP
    ($ret.1)
// function Class1.set 0
    (Class1.set)
    
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
// pop static 0
    @SP  // Get data in the stack
    M = M - 1
    A = M
    D = M
    @Class1.0
    M = D
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
// pop static 1
    @SP  // Get data in the stack
    M = M - 1
    A = M
    D = M
    @Class1.1
    M = D
// push constant 0
    @0
    D = A
    @SP
    A = M
    M = D
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
// function Class1.get 0
    (Class1.get)
    
// push static 0
    @Class1.0
    D = M
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push static 1
    @Class1.1
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
// init code
	@256
	D=A
	@SP
	M=D
// call Sys.init 0
    @$ret.1     // push return-address
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
    @Sys.init // goto f
    0;JMP
    ($ret.1)
// function Sys.init 0
    (Sys.init)
    
// push constant 6
    @6
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push constant 8
    @8
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// call Class1.set 2
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
    @2
    D = D - A
    @ARG
    M = D
    @SP         // LCL = SP
    D = M
    @LCL
    M = D
    @Class1.set // goto f
    0;JMP
    (Sys.init$ret.1)
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
// push constant 23
    @23
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// push constant 15
    @15
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// call Class2.set 2
    @Sys.init$ret.2     // push return-address
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
    @2
    D = D - A
    @ARG
    M = D
    @SP         // LCL = SP
    D = M
    @LCL
    M = D
    @Class2.set // goto f
    0;JMP
    (Sys.init$ret.2)
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
// call Class1.get 0
    @Sys.init$ret.3     // push return-address
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
    @Class1.get // goto f
    0;JMP
    (Sys.init$ret.3)
// call Class2.get 0
    @Sys.init$ret.4     // push return-address
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
    @Class2.get // goto f
    0;JMP
    (Sys.init$ret.4)
// label WHILE
    (Sys.init$WHILE)
// goto WHILE
    @Sys.init$WHILE
    0;JMP
