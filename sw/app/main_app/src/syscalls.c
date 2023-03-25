#include <sys/stat.h>

int _close(int file) {
    return -1;
}

int _fstat(int file, struct stat *st){
    return -1;
}

int _getpid() {
    return 1;
}

int _isatty(int file){
    return -1;
}

int _kill(int pid, int sig){
    return -1;
}

off_t _lseek(int file, off_t ptr, int dir){
    return 0;
}

ssize_t _read(int file, void *ptr, size_t len){
    return 0;
}

ssize_t _write(int file, const void *ptr, size_t len){
    return -1;
}