import { Edge } from "@xyflow/react";

export interface BlockchainNode {
    id: string;
    host: string;
    port: number;
    db: {
        host: string;
        port: number;
        index: number;
    };
}

export interface BlockchainConfig {
    logger_port: number;
    max_block_size: number;
    min_approvals_to_accept_transaction: number;
    mining_difficulty: number;
    nodes: BlockchainNode[];
}
