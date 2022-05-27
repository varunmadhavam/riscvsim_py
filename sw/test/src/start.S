	.section .rst_vect

reset_vec:
	j start


	.section .text
/* Main program
 **********************************/

start:
	/* zero-initialize all registers */

	addi x1, zero, 0
	addi x2, zero, 0
	addi x3, zero, 0
	addi x4, zero, 0
	addi x5, zero, 0
	addi x6, zero, 0
	addi x7, zero, 0
	addi x8, zero, 0
	addi x9, zero, 0
	addi x10, zero, 0
	addi x11, zero, 0
	addi x12, zero, 0
	addi x13, zero, 0
	addi x14, zero, 0
	addi x15, zero, 0
	addi x16, zero, 0
	addi x17, zero, 0
	addi x18, zero, 0
	addi x19, zero, 0
	addi x20, zero, 0
	addi x21, zero, 0
	addi x22, zero, 0
	addi x23, zero, 0
	addi x24, zero, 0
	addi x25, zero, 0
	addi x26, zero, 0
	addi x27, zero, 0
	addi x28, zero, 0
	addi x29, zero, 0
	addi x30, zero, 0
	addi x31, zero, 0

	lui sp,(128*1024)>>12
	//jal ra,hello

	/* running tests from riscv-tests */


	#define TEST(n) \
	.global n; \
	addi x1, zero, 1000; \
	jal zero,n; \
	.global n ## _ret; \
	n ## _ret:

	TEST(lui)
	TEST(auipc)
	TEST(j)
	TEST(jal)
	TEST(jalr)

	TEST(beq)
	TEST(bne)
	TEST(blt)
	TEST(bge)
	TEST(bltu)
	TEST(bgeu)

	TEST(lb)
	TEST(lh)
	TEST(lw)
	TEST(lbu)
	TEST(lhu)

	TEST(sb)
	TEST(sh)
	TEST(sw)

	TEST(addi)
	TEST(slti) // also tests sltiu
	TEST(xori)
	TEST(ori)
	TEST(andi)
	TEST(slli)
	TEST(srli)
	TEST(srai)

	TEST(add)
	TEST(sub)
	TEST(sll)
	TEST(slt) // what is with sltu ?
	TEST(xor)
	TEST(srl)
	TEST(sra)
	TEST(or)
	TEST(and)

	TEST(simple)

	/* print "DONE\n" */
	lui a0,0x40000000>>12
	addi a1,zero,'A'
	sw a1,0(a0)
	addi a1,zero,'L'
	sw a1,0(a0)
	addi a1,zero,'L'
	sw a1,0(a0)
	addi a1,zero,' '
	sw a1,0(a0)
	addi a1,zero,'T'
	sw a1,0(a0)
	addi a1,zero,'E'
	sw a1,0(a0)
	addi a1,zero,'S'
	sw a1,0(a0)
	addi a1,zero,'T'
	sw a1,0(a0)
	addi a1,zero,'S'
	sw a1,0(a0)
	addi a1,zero,' '
	sw a1,0(a0)
	addi a1,zero,'P'
	sw a1,0(a0)
	addi a1,zero,'A'
	sw a1,0(a0)
	addi a1,zero,'S'
	sw a1,0(a0)
	addi a1,zero,'S'
	sw a1,0(a0)
	addi a1,zero,'E'
	sw a1,0(a0)
	addi a1,zero,'D'
	sw a1,0(a0)
	addi a1,zero,'\n'
	sw a1,0(a0)
	addi a1,zero,'D'
	sw a1,0(a0)
	addi a1,zero,'O'
	sw a1,0(a0)
	addi a1,zero,'N'
	sw a1,0(a0)
	addi a1,zero,'E'
	sw a1,0(a0)
	addi a1,zero,'\n'
	sw a1,0(a0)

	/*li a0, 0x20000000
	li a1, 123456789
	sw a1,0(a0)*/

	/* trap */
	ebreak
