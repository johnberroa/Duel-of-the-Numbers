OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];
creg c[3];

// Inputs.
{}x q[0];
{}x q[1];
{}x q[2];

// Program.
x q[4];
cx q[2],q[4];
cx q[2],q[3];
x q[2];
cx q[2],q[4];
cx q[1],q[4];
cx q[3],q[1];
cx q[1],q[4];
cx q[4],q[0];
measure q[0] -> c[2];
measure q[1] -> c[1];
measure q[2] -> c[0];
