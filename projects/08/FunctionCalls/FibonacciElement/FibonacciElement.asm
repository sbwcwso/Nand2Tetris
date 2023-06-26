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
// function Main.fibonacci 0
    (Main.fibonacci)
    
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
// push constant 2
    @2
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
    @Main.fibonacci$true.1
    D;JLT
    @SP
    A = M
    M = 0          // push false
    (Main.fibonacci$true.1)   // lable_true
    @SP      	   
    M = M + 1
// if-goto IF_TRUE
    @SP
    M = M - 1
    A = M
    D = M
    @Main.fibonacci$IF_TRUE
    D;JNE
// goto IF_FALSE
    @Main.fibonacci$IF_FALSE
    0;JMP
// label IF_TRUE
    (Main.fibonacci$IF_TRUE)
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
// label IF_FALSE
    (Main.fibonacci$IF_FALSE)
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
// push constant 2
    @2
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
// call Main.fibonacci 1
    @Main.fibonacci$ret.1     // push return-address
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
    @Main.fibonacci // goto f
    0;JMP
    (Main.fibonacci$ret.1)
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
// call Main.fibonacci 1
    @Main.fibonacci$ret.2     // push return-address
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
    @Main.fibonacci // goto f
    0;JMP
    (Main.fibonacci$ret.2)
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
    
// push constant 4
    @4
    D = A
    @SP
    A = M
    M = D
    @SP
    M = M + 1
// call Main.fibonacci 1
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
    @1
    D = D - A
    @ARG
    M = D
    @SP         // LCL = SP
    D = M
    @LCL
    M = D
    @Main.fibonacci // goto f
    0;JMP
    (Sys.init$ret.1)
// label WHILE
    (Sys.init$WHILE)
// goto WHILE
    @Sys.init$WHILE
    0;JMP
