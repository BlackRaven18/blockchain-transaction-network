import { Backdrop, Box, Button, CircularProgress, Divider, Stack, TextField, Typography } from "@mui/material";
import { useEffect, useRef, useState } from "react";
import { startLogger, startNetwork } from "../api/launcher";
import { useBlockchain } from "../contexts/Blockchain";
import { useBlockchainLogger } from "../contexts/BlockchainLogger";

export default function SideMenu() {

    const logContainterRef = useRef<HTMLDivElement>(null)

    const { isNetworkStarting, setIsNetworkStarting } = useBlockchain()
    const { loggerHistory } = useBlockchainLogger()

    const [isLoggerRunning, setIsLoggerRunning] = useState(false)
    const [isNetworkReady, setIsNetworkReady] = useState(false)

    const launchLogger = async () => {
        await startLogger()
        setIsLoggerRunning(true)
    }

    const launchNetwork = async () => {
        setIsNetworkStarting(true)

        await startNetwork()

        setIsNetworkReady(true)
    }

    return (
        <>
            <Stack direction={"column"} spacing={5} sx={styles.container}>
                <Box style={{ textAlign: "center", marginTop: "15px" }}>
                    <Typography variant="h5"> Network Options</Typography>
                    <Divider/>
                </Box>

                <Button variant="contained" disabled={isLoggerRunning} onClick={async () => await launchLogger()}> Start logger </Button>
                <Button variant="contained" disabled={!isLoggerRunning || isNetworkReady} onClick={async () => launchNetwork()}>Start Network</Button>

                <Divider />

                <Stack sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                    <Typography variant="h5" sx={{marginBottom: "10px" }}>Logs</Typography>
                    <Divider sx={{ width: "100%", bgcolor: "black" }} />
                    <Box ref={logContainterRef} style={{ width: "100%", height: "450px", overflow: "auto" }}>
                        <TextField 
                            sx={{ width: "100%", backgroundColor: "black", "& .MuiInputBase-input": { color: "white", fontSize: "18px" } }}
                            multiline
                            value={loggerHistory.join("\n")}
                            spellCheck={false}
                            />
                    </Box>
                </Stack>

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
        margin: "10px"
    }
}