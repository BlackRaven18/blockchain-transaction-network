import { Button, Stack } from "@mui/material";
import { useState } from "react";
import { establishConnections, startLogger, startNetwork } from "../api/launcher";
import { useBlockchain } from "../contexts/Blockchain";

export default function SideMenu() {

    const { showEdges } = useBlockchain()

    const [isLoggerRunning, setIsLoggerRunning] = useState(false)
    const [isNetworkRunning, setIsNetworkRunning] = useState(false)
    const [isNodesConnected, setIsNodesConnected] = useState(false)

    const launchLogger = async () => {
        await startLogger()
        setIsLoggerRunning(true)
    }

    const launchNetwork = async () => {
        await startNetwork()
        setIsNetworkRunning(true)
    }

    const connectNodes = async () => {
        await establishConnections()
        setIsNodesConnected(true)
        showEdges()
    }

    return (
        <Stack direction={"column"} spacing={5} sx={styles.container}>
            <Button variant="contained" disabled={isLoggerRunning} onClick={async () => await launchLogger() }> Start logger </Button>
            <Button variant="contained" disabled={!isLoggerRunning || isNetworkRunning} onClick={async () => launchNetwork()}>Start Network</Button>
            <Button variant="contained" disabled={!isNetworkRunning || isNodesConnected} onClick={async () => connectNodes()}>Connect Nodes</Button>
            {/* <Button variant="contained" disabled={!isNodesConnected} onClick={() => toggleAnimation()}>Show animation</Button>
            <Button variant="contained" disabled={!isNodesConnected} onClick={() => animateServerEdges("server1")}>Animate Server 1 Edges</Button> */}
        </Stack>
    )
}

const styles = {
    container: {
        margin: "10px",
    }
}