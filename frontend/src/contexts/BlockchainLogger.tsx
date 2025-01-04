import { createContext, PropsWithChildren, useContext, useEffect, useState } from "react";
import useWebSocket from 'react-use-websocket';
import { getConfig } from "../api/launcher";
import { useBlockchain } from "./Blockchain";

const BlockchainLoggerContext = createContext({
    loggerHistory: [] as string[]
});

export const BlockchainLoggerProvider = ({ children }: PropsWithChildren) => {
    const { updateNodeState } = useBlockchain();
    const [loggerURL, setLoggerURL] = useState("");
    const [loggerHistory, setLoggerHistory] = useState<string[]>([]);

    useEffect(() => {
        getConfig()
            .then((config) => {
                setLoggerURL(`ws://localhost:${config.logger_port}/register-consumer`);
            })
            .catch((err) => console.log(err))
    }, [])

    const handleOnMessage = (message: string) => {
        const data = JSON.parse(message);
        console.log("Received message:", data);
        updateNodeState(data.source, data.status);
        loggerHistory.push(`${data.timestamp}: ${data.source} - ${data.status}`);
    }

    const {
        sendMessage,
        sendJsonMessage,
        lastMessage,
        lastJsonMessage,
        readyState,
        getWebSocket,
    } = useWebSocket(loggerURL, {

        onOpen: () => console.log('opened'),
        onMessage: (message) => {
            handleOnMessage(message.data)
        },
        onClose: () => console.log('closed'),

        //Will attempt to reconnect on all close events, such as server shutting down
        shouldReconnect: (closeEvent) => true,

    });

    return (
        <BlockchainLoggerContext.Provider value={{ loggerHistory }}>
            {children}
        </BlockchainLoggerContext.Provider>
    )
}

export const useBlockchainLogger = () => useContext(BlockchainLoggerContext);