# Software_Implement-paillier
## reruirements
1.python3.8.20(or other versions)  
2.gmpy2 (for large integer operation)  
3.screts (for random number)  

## crypto algorithm module
1.you can choose the length of the numbers used in this module(more than 0,it is better to be more than 10)  
2.after generating the key ,you will see the public key and private key in the window(this is not interprocess safe),all keys are stored in a unsafe process.  
So it is recommended to use this for experiments.directly using this is unsafe. 
3.you can enter 2 message and see their ciphertext.their product and decrypted product can be their sum.this is what we called homomorphic encryption.

## electronic vote module
1.enter the number of voters(only have one vote)
2.enter the number of candidates
3.vote as a voter(vote should be integer,0 or 1)
4.you will see the result of every round(encrypted) and the final(both encrypted and decrypted).
