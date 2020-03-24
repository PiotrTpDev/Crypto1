#include <stdio.h>
#include <stdlib.h>
#include "sodium.h"

#define MAX 1500
#define uint_size sizeof(unsigned int) * 8    //32

unsigned int predict_next(unsigned int *previous, int i, int mod){
   return (previous[i-3] + previous[i-31] ) % mod;
}

double predict_bits() {
  int i,k = 0, mod = 2147483648;
  double good = 0.0, total = 0.0, count = 0.0;
  unsigned int previous[MAX];
  unsigned int prediction, tmp; //2^31

  srand(time(NULL));


  for( i = 0 ; i < 32 ; i++ ) {
    previous[i] = random();
  }

  for( i = 32; i < MAX-1; i++){
    k++;
    prediction = predict_next(previous, i, mod);

    tmp = random();
    previous[i] = tmp;

    unsigned int x = prediction ^ tmp;
    count = 0.0;
      
    for (int j = 0; j < (uint_size ); ++j) {
      if (!(x & (1 << j))) {
        count = count + 1.0;
      }
    }

    total = total + count;
    //printf("%f\n",count);
  }

  return total/(uint_size * MAX);
    
}

double distinguisher(){

  int i,j, algorithm, mod = 2147483648; 
  int sequence_size = 100, guess;
  double good_guesses = 0.0, total_guessses = 0.0;
  int generated_sequence[sequence_size];

  srand(time(NULL));

  for(i = 0; i < 1000; i++){

    algorithm = random() % 2;

    if(algorithm == 0){
      for (j = 0; j < sequence_size; j++){
        generated_sequence[j] = random();
      }
    }else{
      for (j = 0; j < sequence_size; j++){
        generated_sequence[j] = randombytes_uniform(2147483647);
      }
    }

    unsigned int tmp = predict_next(generated_sequence,32, mod);

    if(generated_sequence[32] == tmp || generated_sequence[32] == tmp + 1){
      guess = 0;
    }else{
      guess = 1;
    }

    if (guess == algorithm){
      good_guesses = good_guesses + 1.0;
    }

    total_guessses = total_guessses + 1.0;
  }

  return good_guesses/total_guessses;

}

int main(){
  
  printf("%f\n", predict_bits());
  //printf("%f\n", distinguisher());

  return(0);
}
