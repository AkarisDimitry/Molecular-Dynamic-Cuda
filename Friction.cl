__kernel void compute_forces(__global float4* positions, __global float4* velocity, __global float4* forces) {
    int gid = get_global_id(0);
    forces[gid] += -(float)eta * velocity[gid];
}