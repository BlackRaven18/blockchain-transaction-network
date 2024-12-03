import axios from "axios"
import { BlockchainConfig } from "../types"

const LAUNCHER_URL = 'http://localhost:8000/api/v1'

const startLogger = async () => {
    return await axios.post(`${LAUNCHER_URL}/run-logger`)
}

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
    startLogger,
    startNetwork,
    establishConnections,
    getConfig,
}