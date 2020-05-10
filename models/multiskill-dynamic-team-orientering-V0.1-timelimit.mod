/*********************************************
 * OPL 12.4 Model
 * Author: cgarcia
 * Creation Date: Feb 12, 2020 at 2:36:50 AM
 *********************************************/

 execute PARAMS {
   cplex.tilim = 1200; // time limit in seconds
 }

 int numWorkers = ...;
 int numRoles = ...;
 int numNodes = ...;
 range Workers = 1..numWorkers;
 range Roles = 1..numRoles;
 range Nodes = 1..numNodes;
 range JobNodes = 2..numNodes - 1;
 range NodesPlus = 2..numNodes;
 range NodesMinus = 1..numNodes - 1;
 float wStart[Nodes] = ...;
 float wEnd[Nodes] = ...;
 float p[Nodes] = ...;
 int d[Roles][JobNodes] = ...;
 int e[Workers][Roles] = ...;
 float r[JobNodes] = ...;
 float b[Workers][Roles][JobNodes] = ...;
 float t[Nodes][Nodes] = ...;
 float M = ...;
 
 dvar int+ x[Workers][Nodes][Nodes] in 0..1; 
 dvar int+ xp[Workers][Nodes][Nodes] in 0..1;
 dvar int+ y[JobNodes] in 0..1; 
 dvar int+ u[Workers][Roles][JobNodes] in 0..1; 
 dvar float+ a[Workers][Nodes]; 
 dvar float+ s[Nodes]; 
 
 maximize sum(j in JobNodes) (r[j] * y[j]) + sum(h in Workers, i in Roles, j in JobNodes) (b[h][i][j] * u[h][i][j]);
 
 constraints {
 	forall(h in Workers, k in JobNodes) {
 	  sum(j in NodesMinus) x[h][j][k] == sum(j in NodesPlus) x[h][k][j]; // constraint 2
 	  forall(i in Roles) u[h][i][k] <= e[h][i]; // constraint 3
 	  sum(i in Roles) u[h][i][k] == sum(j in NodesMinus) x[h][j][k]; // constraint 5
 	  forall(j in NodesMinus) x[h][j][k] <= y[k];  // constraint 6	    
    }  	 
    forall (i in Roles, j in JobNodes) {
 	  sum(h in Workers) (e[h][i] * u[h][i][j]) == d[i][j] * y[j]; // constraint 4
    }
    forall(h in Workers, k in Nodes) { //NodesPlus
 	  a[h][k] <= s[k]; // constraint 7
 	  forall(j in Nodes) { //NodesMinus
 	    a[h][k] >= s[j] + p[j] + (t[j][k] * x[h][j][k]) - (M *  xp[h][j][k]); // constraint 8
 	    x[h][j][k] + xp[h][j][k] == 1; // constraint 10
      } 	    
 	  
  	} 	  
    forall(j in Nodes) wStart[j] <= s[j] <= wEnd[j]; // constraint 9    
    forall(h in Workers) {
      sum(j in NodesPlus) x[h][1][j] == 1; // constraint 11
      sum(j in NodesMinus) x[h][j][numNodes] == 1; // constraint 12
    }      
 }   
 