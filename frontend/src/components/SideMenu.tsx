import { Backdrop, Button, CircularProgress, Stack } from "@mui/material";
import { useState } from "react";
import { startLogger, startNetwork } from "../api/launcher";
import { useBlockchain } from "../contexts/Blockchain";

export default function SideMenu() {

    const { isNetworkStarting, setIsNetworkStarting, resetServerEdgesAnimations } = useBlockchain()

    const [isLoggerRunning, setIsLoggerRunning] = useState(false)
    const [isNetworkReady, setIsNetworkReady] = useState(false)
    // const [isNetworkRunning, setIsNetworkRunning] = useState(false)

    const launchLogger = async () => {
        await startLogger()
        setIsLoggerRunning(true)
    }

    const launchNetwork = async () => {
        setIsNetworkStarting(true)

        await startNetwork()

        setIsNetworkReady(true)

        // setIsNetworkRunning(true)
    }

    return (
        <>
            <Stack direction={"column"} spacing={5} sx={styles.container}>
                <Button variant="contained" disabled={isLoggerRunning} onClick={async () => await launchLogger()}> Start logger </Button>
                <Button variant="contained" disabled={!isLoggerRunning || isNetworkReady} onClick={async () => launchNetwork()}>Start Network</Button>
                <Button variant="contained" disabled={!isNetworkStarting || !isNetworkReady} onClick={async () => resetServerEdgesAnimations()}>Reset Edges Animations (optional)</Button>
            </Stack>

            <Backdrop
                sx={(theme) => ({ color: '#fff', zIndex: theme.zIndex.drawer + 1 })}
                open={isNetworkStarting}
            >
                <Stack direction={"column"} spacing={2} sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }} >
                    <CircularProgress color="inherit" />
                    <h3>Starting network...</h3>
                </Stack>
            </Backdrop>
        </>
    )
}

const styles = {
    container: {
        margin: "10px",
    }
}