#include <bits/stdc++.h>
#include <iostream> 


#define INF 999

using namespace std;

int main(){

    int M, L, l;
 


    cin >> M >> L >> l;
    int D[M][L] = {0};


    int i = 0; int j = 0;
    int x;

    long int size = 0;
    while (size < M*L){
        while (cin >> x){
            D[i][j] = x;
            size++;
            if(j==(L-1)){
                i++;
                j=0;
            }else{
                j++;
            }
        }
    }

    i = 0; j = 0;

    cout << D[0][0] << D[M-1][L-1];


    
}