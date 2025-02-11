#include <cinolib/meshes/trimesh.h>
#include <cinolib/find_intersections.h>

using namespace cinolib;

bool manifold(const Trimesh<> & m)
{
    for(uint vid=0; vid<m.num_verts(); ++vid)
    {
        if(!m.vert_is_manifold(vid)) return false;
    }
    return true;
}

bool watertight(const Trimesh<> & m)
{
    for(uint eid=0; eid<m.num_edges(); ++eid)
    {
        if(m.edge_is_boundary(eid)) return false;
    }
    return true;
}

bool intersection_free(const Trimesh<> & m)
{
    std::set<ipair> intersections;
    find_intersections(m, intersections);
    return (intersections.empty());
}

extern "C" {
    void mesh_check(double *pts, int ptSz, int *tris, int triSz, int *checkVal)
    {
        std::vector<double> in_coords(pts, pts + ptSz);
        std::vector<uint> in_tris(tris, tris + triSz);
        
        Trimesh<> m(in_coords, in_tris);
        
        *checkVal = 0;
        
        if (manifold(m))
        *checkVal += 1;
        
        if (watertight(m))
        *checkVal += 2;
        
        if (intersection_free(m))
        *checkVal += 4;
    }
}

