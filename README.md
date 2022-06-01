# riscvsim_py
an riscv rv32i simulator in python inspired from https://github.com/johnwinans/rvddt
1. Pre requisites
    1. Install python3.
    2. Install Python Prompt Toolkit 3.0 : pip3 install prompt_toolkit.
    3. Install RISC V crosscompiler and set its bin directory in the PATH env variable.

2. get the simulator
    1. git clone git@github.com:varunmadhavam/riscvsim_py.git

3. Run tests
    1. cd riscvsim_py
    2. make test

4. Run helloworld
    1. cd riscvsim_py
    2. make

5. Run your own C program
    1. Add the new source code and headers to sw/app/main_app src and include respectively
    2. Edit the Makefile in sw/app/main_app and append the new sources to FIRMWARE_OBJS as object files
    3. make

6. Help
    1. Within the simulator enter h|help to get the help menu.