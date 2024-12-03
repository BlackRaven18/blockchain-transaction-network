import { createContext, PropsWithChildren, useContext, useEffect, useState } from "react";
import useWebSocket from 'react-use-websocket';
import { getConfig } from "../api/launcher";

const BlockchainLoggerContext = createContext({
    isConnected: false
})

export const BlockchainLoggerProvider = ({ children }: PropsWithChildren) => {
    const [isConnected, setIsConnected] = useState(false);
    const [loggerURL, setLoggerURL] = useState("");

    useEffect(() => {
        getConfig()
            .then((config) => {
                setLoggerURL(`ws://localhost:${config.logger_port}/register-consumer`);
            })
            .catch((err) => console.log(err))
    }, [])

    const {
        sendMessage,
        sendJsonMessage,
        lastMessage,
        lastJsonMessage,
        readyState,
        getWebSocket,
      } = useWebSocket(loggerURL, {

        onOpen: () => console.log('opened'),
        onMessage: (message) => console.log(message.data),
        onClose: () => console.log('closed'),
        //Will attempt to reconnect on all close events, such as server shutting down
        shouldReconnect: (closeEvent) => true,

      });

    return (
        <BlockchainLoggerContext.Provider value={{ isConnected }}>
            {children}
        </BlockchainLoggerContext.Provider>
    )
}

export const useBlockchainLogger = () => useContext(BlockchainLoggerContext);