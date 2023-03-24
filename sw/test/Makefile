
RISCV_GNU_TOOLCHAIN_INSTALL_PREFIX = /opt/tools/compilers/riscV/rv32i

# Give the user some easy overrides for local configuration quirks.
# If you change one of these and it breaks, then you get to keep both pieces.
SHELL = bash
PYTHON = python3

FIRMWARE_OBJS = $(addsuffix .o,$(basename $(wildcard src/*.S)))
GCC_WARNS  = -Werror -Wall -Wextra -Wshadow -Wundef -Wpointer-arith -Wcast-qual -Wcast-align -Wwrite-strings
GCC_WARNS += -Wredundant-decls -Wstrict-prototypes -Wmissing-prototypes -pedantic # -Wconversion
TOOLCHAIN_PREFIX = $(RISCV_GNU_TOOLCHAIN_INSTALL_PREFIX)/bin/riscv32-unknown-elf-

# Add things like "export http_proxy=... https_proxy=..." here
GIT_ENV = true

all: firmware/firmware.hex


firmware/firmware.hex: firmware/firmware.bin firmware/makehex.py
	$(PYTHON) firmware/makehex.py $< 32768 > $@

firmware/firmware.bin: firmware/firmware.elf
	$(TOOLCHAIN_PREFIX)objcopy -O binary $< $@
	chmod -x $@

firmware/firmware.elf: $(FIRMWARE_OBJS) sections.lds
	$(TOOLCHAIN_PREFIX)gcc -Os -mabi=ilp32 -march=rv32i -ffreestanding -nostdlib -nostartfiles -o $@ \
		-Wl,--build-id=none,-Bstatic,-T,sections.lds,-Map,firmware/firmware.map,--strip-debug \
		$(FIRMWARE_OBJS)
	chmod -x $@

src/%.o: src/%.S src/riscv_test.h src/test_macros.h
	$(TOOLCHAIN_PREFIX)gcc -c -mabi=ilp32 -march=rv32i -o $@ -DTEST_FUNC_NAME=$(notdir $(basename $<)) \
		-DTEST_FUNC_TXT='"$(notdir $(basename $<))"' -DTEST_FUNC_RET=$(notdir $(basename $<))_ret $<

disass: firmware/firmware.elf
	$(TOOLCHAIN_PREFIX)objdump -d -M no-aliases -M numeric firmware/firmware.elf
	
clean:
	rm -vrf $(FIRMWARE_OBJS) firmware/firmware.elf firmware/firmware.bin firmware/firmware.hex firmware/firmware.map firmware/*.S

.PHONY: test  clean disass
