import { Box, Button } from "@mui/material";
import { useBlockchain } from "../contexts/Blockchain";

export default function SideMenu() {

    const { toggleAnimation, animateServerEdges } = useBlockchain()

    return (
        <Box sx={{textAlign: 'center', justifyContent: 'center'}}>
            <Button variant="contained">Start</Button>
            <Button variant="contained" onClick={() => toggleAnimation()}>Show animation</Button>
            <Button variant="contained" onClick={() => animateServerEdges("server1")}>Animate Server 1 Edges</Button>

        </Box>
    )
}