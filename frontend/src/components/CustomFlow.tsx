import { ReactFlow, Background, Controls, Position, MarkerType } from "@xyflow/react";
import { useBlockchain } from "../contexts/BlockchainContext";
import BiDirectionalEdge from "../flow/edges/BiDirectionalEdge";
import BiDirectionalNode from "../flow/nodes/BiDirectionalNode";
import FloatingEdge from "../flow/edges/FloatingEdge";
import FloatingNode from "../flow/nodes/FloatingNode";

const edgeTypes = {
    bidirectional: BiDirectionalEdge,
    floating: FloatingEdge
};

const nodeTypes = {
    bidirectional: BiDirectionalNode,
    floating: FloatingNode,
};

const connectionLineStyle = {
    stroke: '#b1b1b7',
};

const defaultEdgeOptions = {
    type: 'floating',
    markerEnd: {
        type: MarkerType.ArrowClosed,
        color: '#b1b1b7',
    },
};

export default function CustomFlow() {
    const { nodes } = useBlockchain()

    const numberOfNodes = nodes.length;

    // Promień okręgu
    const radius = 200;

    const initialNodes = nodes.map((node, index) => {

        const angle = (2 * Math.PI * index) / numberOfNodes;

        // Obliczanie pozycji węzła na okręgu
        const x = radius * Math.cos(angle);
        const y = radius * Math.sin(angle);

        return {
            id: node.id,
            position: { x, y },
            data: { label: node.id },
            type: "floating",
        };
    });

    const initialEdges = nodes.flatMap((sourceNode) =>
        nodes.map((targetNode) => {
                return {
                    id: `edge-${sourceNode.id}-${targetNode.id}`,
                    source: sourceNode.id,
                    target: targetNode.id,
                    type: "floating",
                    markerEnd: {
                        type: MarkerType.ArrowClosed,
                        color: '#b1b1b7',
                    },
                };
        }).filter(edge => edge.source !== edge.target) // Usuwamy wartości null
    );

    return (
        <ReactFlow
            nodes={initialNodes}
            edges={initialEdges}
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