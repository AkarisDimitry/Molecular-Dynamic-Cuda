__kernel void integrate_step1(__global float4* positions, __global float4* velocities, __global float4* forces) {
    int gid = get_global_id(0);

    velocities[gid] += 0.5f * (float)dt * forces[gid];
    positions[gid] += (float)dt * velocities[gid];

}

__kernel void integrate_step2(__global float4* positions, __global float4* velocities, __global float4* forces) {
    int gid = get_global_id(0);

    velocities[gid] += 0.5f * (float)dt * forces[gid];

}