import axios from "axios"
import { BlockchainConfig } from "../types"

const LAUNCHER_URL = 'http://localhost:8000/api/v1'

const axiosInstance = axios.create({
    baseURL: LAUNCHER_URL,
    timeout: 15000, 
  });

const startLogger = async () => {
    return await axiosInstance.post('/run-logger')
}

const startNetwork = async () => {
    return await axiosInstance.post('/start-network')
}

const getConfig = async (): Promise<BlockchainConfig> => {
    return await axiosInstance.get('/config')
        .then((response) => response.data)
}

const getNodeBlockchain = async (nodeId: string) => {

    const config = await getConfig()

    const node = config.nodes.find((node) => node.id === nodeId)

    if (!node) {
        throw new Error("Node not found")
    }

    return await axiosInstance.get(`http://${node.host}:${node.port}/api/v1/chain`)
        .then((response) => response.data)
}

const getNodeRegisteredClients = async (nodeId: string) => {

    const config = await getConfig()

    const node = config.nodes.find((node) => node.id === nodeId)

    if (!node) {
        throw new Error("Node not found")
    }

    return await axiosInstance.get(`http://${node.host}:${node.port}/api/v1/clients`)
        .then((response) => response.data)
}

export {
    startLogger,
    startNetwork,
    getConfig,
    getNodeBlockchain,
    getNodeRegisteredClients
}