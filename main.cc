
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <cmath>

#define F(a) (a)

inline void delay(int) {}
inline unsigned long millis(void) { return 0; }

struct serial {
  void begin(int i) {}
  void print(int i) { printf("%d",i); }
  void println(int i) { printf("%d\n",i); }
  void print(const char *s) { printf("%s",s); }
  void println(const char *s) { printf("%s\n",s); }
  void println(void) { printf("\n"); }
  void flush(void) { }
  bool operator!() { return false; } 
} Serial;

#define min(a,b)   ((a)<=(b)?(a):(b))
#define max(a,b)   ((a)>=(b)?(a):(b))

#include "common.h"

int main(int argc, char *argv[])
{
  setup();
  for (int i=0; i<N_ITERATION; i++) loop();
  return 0;
}


