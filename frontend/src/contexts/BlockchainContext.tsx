import { Edge, MarkerType, Node } from '@xyflow/react';
import { createContext, PropsWithChildren, useContext, useEffect, useState } from 'react';
import { getConfig } from '../api/launcher';
import { BlockchainNode } from '../types';

const BlockchainContext = createContext({
    nodes: [] as BlockchainNode[],
    flowNodes: [] as Node[],
    flowEdges: [] as Edge[],
    toggleAnimation: () => {}
});

export const BlockchainProvider = ({ children }: PropsWithChildren) => {
    const [nodes, setNodes] = useState<BlockchainNode[]>([])
    const [flowNodes, setFlowNodes] = useState<Node[]>([])
    const [flowEdges, setFlowEdges] = useState<Edge[]>([])

    // flow nodes radius 
    const radius = 150;

    useEffect(() => {
        getNodes()
    }, [])

    const getNodes = () => {
        getConfig()
            .then((config) => {
                setNodes(config.nodes)
                getFlowNodes(config.nodes)
                getFlowEdges(config.nodes)
            })
            .catch((err) => console.log(err))
    }

    const getFlowNodes = (nodes: BlockchainNode[]) => {
        const numberOfNodes = nodes.length;

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

        setFlowNodes(initialNodes);
    }

    const getFlowEdges = (nodes: BlockchainNode[]) => {
        const initialEdges = nodes.flatMap((sourceNode) =>
            nodes.map((targetNode) => {
                    return {
                        id: `edge-${sourceNode.id}-${targetNode.id}`,
                        source: sourceNode.id,
                        target: targetNode.id,
                        type: "floating",
                        data: { showAnimation: false },
                        markerEnd: {
                            type: MarkerType.ArrowClosed,
                            color: '#b1b1b7',
                        },
                    };
            }).filter(edge => edge.source !== edge.target) // Usuwamy wartości null
        );

        setFlowEdges(initialEdges);
    }

    const toggleAnimation = () => {
        const updatedEdges = flowEdges.map((edge) => ({
            ...edge,
            data: {
                ...edge.data,
                showAnimation: !edge.data?.showAnimation,
            }
        }));
        setFlowEdges(updatedEdges);
    }

    return (
        <BlockchainContext.Provider value={{ nodes, flowNodes, flowEdges, toggleAnimation }}>
            {children}
        </BlockchainContext.Provider>
    )
}

export const useBlockchain = () => useContext(BlockchainContext);

