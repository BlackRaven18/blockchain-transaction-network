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

export {
    startLogger,
    startNetwork,
    getConfig
}