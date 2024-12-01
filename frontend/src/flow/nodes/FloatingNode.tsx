import { Handle, Position, useConnection } from '@xyflow/react';

interface NodeProps {
    id: string;
}

export default function FloatingNode({ id }: NodeProps) {
    const connection = useConnection();

    const isTarget = connection.inProgress && connection.fromNode.id !== id;

    return (
        <div className="customNode">
            <div
                className="customNodeBody"
            >
                {!connection.inProgress && (
                    <Handle
                        className="customHandle"
                        position={Position.Right}
                        type="source"
                    />
                )}

                {(!connection.inProgress || isTarget) && (
                    <Handle className="customHandle" position={Position.Left} type="target" isConnectableStart={false} />
                )}

                {id}
            </div>
        </div>
    );
}