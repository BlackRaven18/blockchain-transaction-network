import { BaseEdge, getStraightPath, useInternalNode } from '@xyflow/react';

import { getEdgeParams } from '../../utils';

interface FloatingEdgeProps {
    id: string;
    source: string;
    target: string;
    markerEnd?: string;
    style?: React.CSSProperties;
    data?: {
        showAnimation?: boolean; 
    };
}

function FloatingEdge({ id, source, target, markerEnd, style, data }: FloatingEdgeProps) {

    const sourceNode = useInternalNode(source);
    const targetNode = useInternalNode(target);

    console.log(data?.showAnimation);

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
            {data?.showAnimation && (
                <circle r="8" fill="#ff0073">
                    <animateMotion dur="2s" repeatCount="indefinite" path={edgePath} />
                </circle>
            )}
        </>
    );
}

export default FloatingEdge;