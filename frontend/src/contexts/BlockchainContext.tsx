import React, { createContext, useState, useEffect, useContext, PropsWithChildren } from 'react';
import { getConfig } from '../api/launcher';
import { BlockchainNode } from '../types';

const BlockchainContext = createContext({
    nodes: [] as BlockchainNode[],
    // setNodes: () => {},
});

export const BlockchainProvider = ({ children }: PropsWithChildren) => {
    const [nodes, setNodes] = useState<BlockchainNode[]>([])


    useEffect(() => {
        console.log("BlockchainProvider call...")
        getNodes()
    }, [])

    const getNodes = () => {
        getConfig()
            .then((config) => {
                console.log(config)
                setNodes(config.nodes)
            })
            .catch((err) => console.log(err))
    }
    return (
        <BlockchainContext.Provider value={{ nodes }}>
            {children}
        </BlockchainContext.Provider>
    )
}

export const useBlockchain = () => useContext(BlockchainContext);

