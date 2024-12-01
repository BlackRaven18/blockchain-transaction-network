import { ReactFlow, Background, Controls, Position, MarkerType } from "@xyflow/react";
import { useBlockchain } from "../contexts/BlockchainContext";
import FloatingEdge from "../flow/edges/FloatingEdge";
import FloatingNode from "../flow/nodes/FloatingNode";

const edgeTypes = {
    floating: FloatingEdge
};

const nodeTypes = {
    floating: FloatingNode,
};

export default function CustomFlow() {
    const { flowNodes, flowEdges } = useBlockchain()

    return (
        <ReactFlow
            nodes={flowNodes}
            edges={flowEdges}
            onNodeClick={(node) => console.log(node)}
            edgeTypes={edgeTypes}
            nodeTypes={nodeTypes}
            fitView
            style={{ backgroundColor: 'gray' }}
        >
            <Background />
            <Controls />
        </ReactFlow>
    )
}