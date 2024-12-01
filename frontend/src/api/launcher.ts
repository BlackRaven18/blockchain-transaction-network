import axios from "axios"
import { Block } from "typescript"
import { BlockchainConfig } from "../types"

const LAUNCHER_URL = 'http://localhost:8000/api/v1'

const startNetwork = async () => {
    return await axios.post(`${LAUNCHER_URL}/start-network`)
}

const establishConnections = async () => {
    return await axios.post(`${LAUNCHER_URL}/establish-network-connections`)
}

const getConfig = async (): Promise<BlockchainConfig> => {
    return await axios
        .get(`${LAUNCHER_URL}/config`)
        .then((response) => response.data)
}

export {
    startNetwork,
    establishConnections,
    getConfig,
}