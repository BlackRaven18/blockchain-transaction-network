import { Background, Controls, Node, ReactFlow } from "@xyflow/react";
import { useState } from "react";
import 'react-json-view-lite/dist/index.css';
import { useBlockchain } from "../contexts/Blockchain";
import FloatingEdge from "../flow/edges/FloatingEdge";
import FloatingNode from "../flow/nodes/FloatingNode";
import NodeModal from "./modals/NodeModal";

const edgeTypes = {
    floating: FloatingEdge
};

const nodeTypes = {
    floating: FloatingNode,
};

export default function CustomFlow() {
    const { flowNodes, flowEdges } = useBlockchain()
    const [openModal, setOpenModal] = useState(false);
    const [selectedNode, setSelectedNode] = useState<Node>();

    const handleOpenModal = (node: any) => {
        setOpenModal(true)
        setSelectedNode(node)
    };
    const handleCloseModal = () => setOpenModal(false);

    return (
        <>
            <ReactFlow
                nodes={flowNodes}
                edges={flowEdges}
                onNodeClick={(event, node) => handleOpenModal(node)}
                onNodesChange={() => { }}
                edgeTypes={edgeTypes}
                nodeTypes={nodeTypes}
                fitView
                style={{ backgroundColor: 'gray' }}
            >
                <Background />
                <Controls />
            </ReactFlow>

            <NodeModal open={openModal} handleCloseModal={handleCloseModal} selectedNode={selectedNode} />
        </>
    )
}