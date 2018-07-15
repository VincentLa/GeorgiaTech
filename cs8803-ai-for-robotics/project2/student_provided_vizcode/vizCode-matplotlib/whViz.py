
def drawWH(wh, boxes, pos):
    f = plt.figure()
    ax = plt.gca()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(0, len(wh[0]))
    plt.ylim(-len(wh),0)
    ax.add_artist(plt.Circle((pos[0][0],pos[0][1]),0.25,color='g'))
    for p in range(1,len(pos)):
        ax.add_artist(plt.Circle((pos[p][0],pos[p][1]),0.25,color='r'))
    
    for box in boxes:
        ax.add_artist(patches.Rectangle((box[0]-0.1,box[1]-0.1),0.2,0.2))
        
    for row in range(len(wh)):
        for col in range(len(wh[0])):
            ch = wh[row][col]
            if ch == '#':
                p = (col,-row)
                ax.add_artist(patches.Rectangle((p[0],p[1]-1),1,1, color='k'))
                
    for i in range(len(pos)-1):
        pc = pos[i]
        qc = pos[i+1]
        ux = qc[0] - pc[0]
        uy = qc[1] - pc[1]
        d = sqrt(ux*ux+uy*uy)
        if (d > 1e-2):
            ux /= d
            uy /= d
            u = (uy * 0.25, -ux * 0.25)       # orthogonal unit vector times length
            p = (pc[0] - u[0], pc[1] - u[1])
            q = (qc[0] - u[0], qc[1] - u[1])
            for i in range(2):
                plt.plot([p[0],q[0]],[p[1],q[1]],'k-')
                p = (pc[0] + u[0], pc[1] + u[1])
                q = (qc[0] + u[0], qc[1] + u[1])
