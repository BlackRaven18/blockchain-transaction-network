import { Background, Controls, Node, ReactFlow } from "@xyflow/react";
import { useState } from "react";
import 'react-json-view-lite/dist/index.css';
import { useBlockchain } from "../contexts/Blockchain";
import FloatingEdge from "../flow/edges/FloatingEdge";
import FloatingNode from "../flow/nodes/FloatingNode";
import NodeModal from "./modals/NodeModal";
import { Box, CircularProgress, Stack, Typography } from "@mui/material";

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

    if (flowNodes.length === 0) {
        return (
            <Stack  direction="column"  spacing={5} sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                <CircularProgress size={100}/>
                <Typography variant="h4" color="white">Fetching network structure from launcher...</Typography>
                <Typography variant="h5" color="white">(If this takes too long, please, make sure that the launcher is running)</Typography>
            </Stack>
        )
    }

    return (
        <>
            <ReactFlow
                nodes={flowNodes}
                edges={flowEdges}
                onNodeClick={(event, node) => handleOpenModal(node)}
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