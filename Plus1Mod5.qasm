// Name of Experiment: Plus1Mod5 v1
// Description: Computes modular multiplication x-> 7x (mod 15).
Initial state x=1

OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];
creg c[3];

cx q[2],q[3];
cx q[1],q[4];
x q[2];
if(c==1) cx q[2],q[4];
cx q[3],q[1];
cx q[4],q[0];
measure q[0] -> c[2];
measure q[1] -> c[1];
measure q[2] -> c[0];
