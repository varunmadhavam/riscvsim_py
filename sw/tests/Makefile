RISCV_GNU_TOOLCHAIN_INSTALL_PREFIX = /opt/riscv32
COMPILER_ARCH=im
# Give the user some easy overrides for local configuration quirks.
# If you change one of these and it breaks, then you get to keep both pieces.
FIRMWARE_OBJS = $(addsuffix .o,$(basename $(wildcard src/*.S)))
#GCC_WARNS  = -Wall -Wextra -Wshadow -Wundef -Wpointer-arith -Wcast-qual -Wcast-align -Wwrite-strings
#GCC_WARNS += -Wredundant-decls -Wstrict-prototypes -Wmissing-prototypes -pedantic # -Wconversion
TOOLCHAIN_PREFIX = $(RISCV_GNU_TOOLCHAIN_INSTALL_PREFIX)$(COMPILER_ARCH)/bin/riscv32-unknown-elf-
	
firmware/firmware.hex: firmware/firmware.bin firmware/firmware.srec firmware/makehex.py
	$(PYTHON) firmware/makehex.py $<  > $@

firmware/firmware.bin: firmware/firmware.elf
	$(TOOLCHAIN_PREFIX)objcopy -O binary $< $@

firmware/firmware.srec: firmware/firmware.elf
	$(TOOLCHAIN_PREFIX)objcopy -O srec $< $@

firmware/start.o: firmware/start.S
	$(TOOLCHAIN_PREFIX)gcc -c -mabi=ilp32 -march=rv32$(COMPILER_ARCH)  -o $@ $<

firmware/firmware.elf: $(FIRMWARE_OBJS)  src/sections.lds
	$(TOOLCHAIN_PREFIX)gcc -Os -I./include -mabi=ilp32 -march=rv32$(COMPILER_ARCH) -ffreestanding -nostdlib -o $@ \
		-Wl,--build-id=none,-Bstatic,-T,src/sections.lds,-Map,firmware/firmware.map,--strip-debug \
		$(FIRMWARE_OBJS) -lgcc 
	chmod -x $@

src/%.o: src/%.S
	$(TOOLCHAIN_PREFIX)gcc -c -I./include -mabi=ilp32 -march=rv32$(COMPILER_ARCH) -o $@ -DTEST_FUNC_NAME=$(notdir $(basename $<)) \
		-DTEST_FUNC_TXT='"$(notdir $(basename $<))"' -DTEST_FUNC_RET=$(notdir $(basename $<))_ret $<

clean:
	rm -vrf $(FIRMWARE_OBJS) firmware/firmware.elf firmware/firmware.bin firmware/firmware.hex firmware/firmware.map firmware/firmware.coe firmware/firmware.srec

disass: firmware/firmware.elf
	/opt/riscv32i/bin/riscv32-unknown-elf-objdump -d -M no-aliases -M numeric firmware/firmware.elf
	
.PHONY: clean
