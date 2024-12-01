import { BaseEdge, getStraightPath, useInternalNode } from '@xyflow/react';

import { getEdgeParams } from '../../utils';

interface FloatingEdgeProps {
    id: string;
    source: string;
    target: string;
    markerEnd?: string;
    style?: React.CSSProperties;
}

function FloatingEdge({ id, source, target, markerEnd, style }: FloatingEdgeProps) {
    const sourceNode = useInternalNode(source);
    const targetNode = useInternalNode(target);

    if (!sourceNode || !targetNode) {
        return null;
    }

    const { sx, sy, tx, ty } = getEdgeParams(sourceNode, targetNode);

    const [edgePath] = getStraightPath({
        sourceX: sx,
        sourceY: sy,
        targetX: tx,
        targetY: ty,
    });

    return (
        <>
            <BaseEdge path={edgePath} markerEnd={markerEnd} />
            <circle r="8" fill="#ff0073">
                <animateMotion dur="2s" repeatCount="indefinite" path={edgePath} />
            </circle>
        </>
        // <path
        //   id={id}
        //   className="react-flow__edge-path"
        //   d={edgePath}
        //   markerEnd={markerEnd}
        //   style={style}
        // />
    );
}

export default FloatingEdge;