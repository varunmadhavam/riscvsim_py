
RISCV_GNU_TOOLCHAIN_INSTALL_PREFIX = /opt/tools/compilers/riscV/rv32i
FIRMWARE_OBJS = src/main.o src/ttyuart.o src/syscalls.o
TOOLCHAIN_PREFIX = $(RISCV_GNU_TOOLCHAIN_INSTALL_PREFIX)/bin/riscv32-unknown-elf-
	
all: firmware/firmware.bin firmware/firmware.srec

firmware/firmware.bin: firmware/firmware.elf
	$(TOOLCHAIN_PREFIX)objcopy -O binary $< $@

firmware/firmware.srec: firmware/firmware.elf
	$(TOOLCHAIN_PREFIX)objcopy -O srec $< $@

firmware/firmware.elf: $(FIRMWARE_OBJS) riscv.lds
	$(TOOLCHAIN_PREFIX)gcc -I./include -Os -specs=nosys.specs -mabi=ilp32 -march=rv32i -o $@ \
		-Wl,--build-id=none,-Bstatic,-T,riscv.lds,-Map,firmware/firmware.map,--strip-debug \
		$(FIRMWARE_OBJS)

src/%.o: src/%.c
	$(TOOLCHAIN_PREFIX)gcc -c -I./include -mabi=ilp32 -march=rv32i -Os --std=c99 -o $@ $<

disass: firmware/firmware.elf
	$(TOOLCHAIN_PREFIX)objdump -d -M no-aliases -M numeric firmware/firmware.elf

clean:
	rm -vrf $(FIRMWARE_OBJS) firmware/* src/*.o

.PHONY: clean
