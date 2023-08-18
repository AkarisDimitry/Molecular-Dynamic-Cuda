__kernel void compute_forces(__global float4* positions, __global float4* velocity, __global float4* forces  ) 
{
    // Get the global thread ID
    int id = get_global_id(0);

    // Initialize force to zero
    forces[id] = (float4)(0.0f, 0.0f, 0.0f, 0.0f);

    // Loop over all particles
    for (int j = 0; j < N; j++) 
    {
        if (j != id) 
        {
            // Calculate the displacement vector and distance
            float4 rij = positions[j] - positions[id];

            rij = select(rij, rij - boundary_max, isgreater(rij, 0.5f * boundary_max));
            rij = select(rij, rij + boundary_max, isless(rij, -0.5f * boundary_max));

            float distSqr = dot(rij, rij);
            float distSqr6 = distSqr*distSqr*distSqr;
            float distSqr12 = distSqr6*distSqr6;

            // Calculate the Lennard-Jones force
            float factor = 24.0f * 3.0f * (2.0f  / distSqr12 - 1.0f / distSqr6) / distSqr;
            float4 force = factor * rij * 0.01f;

            // Add force contribution to total force
            forces[id] -= force;
        }
    }
}