// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Pseudo code:
// At the begining the screen is clear
// prev_key = 0
// current_key = 0
// LOOP:
//     if M[KBD] == 0
//         current_key = 0
//     else:
//         current_key = 1
//     if current_key == prev_key:
//         GOTO LOOP 
//     if current_key == 0
//         GOTO CLEAR 
//     GOTO BLANK

// BLANK:
// prev_key = current_key
// for (i = SCREEN; i < KBD; i++)
//     M[i] = 1
// GOTO LOOP
// CLEAR:
// prev_key = current_key
// for (i = SCREEN; i < KBD; i++)
//     M[i] = 0
// GOTO LOOP
// Put your code here.

@prev_key
M=0
@current_key
M=0
@addr

(LOOP)
    @KBD
    D = M

    @NOT_PRESS
    D;JEQ

    @current_key
    M = 1   // current_key = 1
    @END_READ_KBD
    0;JMP 

    (NOT_PRESS)
        @current_key
        M = 0  // current_key = 0

    (END_READ_KBD)

    @prev_key
    D = M
    @current_key
    D = D - M
    @LOOP  // current_key == prev_key, goto LOOP
    D;JEQ

    @current_key
    D = M
    @prev_key
    M = D  // prev_key = current_key

    @SCREEN
    D = A
    @addr
    M = D  // addr = SCREEN, store memroy address, is a pointer

    @current_key
    D = M
    @CLEAR
    D;JEQ  // current_key = 0, goto CLEAR else goto BLANK

    (BLANK)  // BLANK the screen
        @addr
        D = M
        @KBD
        D = D - A
        @LOOP
        D;JEQ
        @addr
        A = M
        M = -1
        @addr
        M = M + 1
        @BLANK
        0;JMP

    (CLEAR)  // Blank the screen
        @addr
        D = M
        @KBD
        D = D - A
        @LOOP
        D;JEQ
        @addr
        A = M
        M = 0
        @addr
        M = M + 1
        @CLEAR
        0;JMP
