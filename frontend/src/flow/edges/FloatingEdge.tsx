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
                <g>
                    <path
                        d="M2,2 L14,2 L14,10 L2,10 Z M2,2 L8,6 L14,2"
                        fill="#ff0073"
                        stroke="black"
                        strokeWidth="0.5"
                    >
                        <animateMotion dur="2s" repeatCount="indefinite" path={edgePath} />
                    </path>
                </g>
            )}
        </>
    );
}

export default FloatingEdge;