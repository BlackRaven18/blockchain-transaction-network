import '@xyflow/react/dist/style.css';
import './App.css';
import { Box, Grid2, Typography } from '@mui/material';
import CustomFlow from './components/CustomFlow';
import { ReactFlowProvider } from '@xyflow/react';
import Header from './components/Header';
import SideMenu from './components/SideMenu';
import { useEffect } from 'react';
import { BlockchainProvider } from './contexts/BlockchainContext';

function App() {

    return (
        <BlockchainProvider >
            <ReactFlowProvider>
                <Box sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    height: '100%',
                }}>
                    <Header />
                    <Grid2 container sx={{ flex: 1 }}>
                        <Grid2 size={4} sx={{ backgroundColor: '#716b50' }}>
                            <SideMenu />
                        </Grid2>
                        <Grid2 size={8}>
                            <CustomFlow />
                        </Grid2>

                    </Grid2>
                </Box>
            </ReactFlowProvider >
        </BlockchainProvider>
    );
}

export default App;
