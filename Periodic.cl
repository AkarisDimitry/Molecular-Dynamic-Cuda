__kernel void Periodic(__global float4* positions, __global float4* velocities, float4 boundary_max, float4 L) {
    int gid = get_global_id(0);
    float4 pos = positions[gid];
    float4 new_pos;
    float4 boundary_min = (float4)(0.0f, 0.0f, 0.0f, 0.0f);

    new_pos = select(pos, pos - L, isgreater(pos, boundary_max));
    new_pos = select(new_pos, new_pos + L, isless(new_pos, boundary_min));

    positions[gid] = new_pos;
}
