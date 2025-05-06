#include <stdio.h>

void calcula(int c) {
  printf("calcula %d\n", c);
  c++;
  printf("calcula %d\n", c);
}

int main() {

  int c = 10; 

  printf("main %d\n", c);
  calcula(c);
  printf("main %d\n", c);

}