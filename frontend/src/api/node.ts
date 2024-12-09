import axios from "axios"
import { getConfig } from "./launcher";

const getNode = async (nodeId: string) => {
    const config = await getConfig();

    const node = config.nodes.find((node) => node.id === nodeId) ?? null;

    return node
}

const getNodeBlockchain = async (nodeId: string) => {

    const node = await getNode(nodeId);

    if (!node) {
        throw new Error("Node not found")
    }

    return await axios.get(`http://${node.host}:${node.port}/api/v1/chain`)
        .then((response) => response.data)
}

const getNodeRegisteredClients = async (nodeId: string) => {

    const node = await getNode(nodeId);

    if (!node) {
        throw new Error("Node not found")
    }

    return await axios.get(`http://${node.host}:${node.port}/api/v1/clients`)
        .then((response) => response.data)
}

const getNodeHealth = async (nodeId: string) => {

    const node = await getNode(nodeId);

    if (!node) {
        throw new Error("Node not found")
    }

    return await axios.get(`http://${node.host}:${node.port}/api/v1/health`)
        .then((response) => response.data)
}

const postInjectNodeDamageError = async (nodeId: string) => {

    const node = await getNode(nodeId);

    if (!node) {
        throw new Error("Node not found")
    }

    return await axios.post(`http://${node.host}:${node.port}/api/v1/inject-node-damage-error`)
}

const postResetNodeDamageError = async (nodeId: string) => {

    const node = await getNode(nodeId);

    if (!node) {
        throw new Error("Node not found")
    }

    return await axios.post(`http://${node.host}:${node.port}/api/v1/reset-node-damage-error`)
}


export {
    getNodeBlockchain,
    getNodeRegisteredClients,
    getNodeHealth,
    postInjectNodeDamageError,
    postResetNodeDamageError,
}