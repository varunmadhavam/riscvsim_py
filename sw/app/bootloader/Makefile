
RISCV_GNU_TOOLCHAIN_INSTALL_PREFIX = /opt/tools/compilers/riscV/rv32i
TOOLCHAIN_PREFIX=$(RISCV_GNU_TOOLCHAIN_INSTALL_PREFIX)/bin/riscv32-unknown-elf-

FIRMWARE_OBJS=start.o

all: firmware.bin

firmware.bin: firmware.elf
	$(TOOLCHAIN_PREFIX)objcopy -O binary $< $@
	chmod -x $@

firmware.elf: start.o sections.lds
	$(TOOLCHAIN_PREFIX)gcc -Os -mabi=ilp32 -march=rv32i -ffreestanding -nostdlib -nostartfiles -o $@ \
		-Wl,--build-id=none,-Bstatic,-T,sections.lds,-Map,firmware.map,--strip-debug \
		$(FIRMWARE_OBJS)
	chmod -x $@

start.o: start.S
	$(TOOLCHAIN_PREFIX)gcc -c -mabi=ilp32 -march=rv32i -ffreestanding -nostdlib -nostartfiles -o $@ $<

disass: firmware.elf
	$(TOOLCHAIN_PREFIX)objdump -d -M no-aliases -M numeric firmware.elf
clean:
	rm -f firmware.bin firmware.elf start.o firmware.map
