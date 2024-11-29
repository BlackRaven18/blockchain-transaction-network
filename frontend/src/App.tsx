import './App.css';
import { Grid2, Typography } from '@mui/material';

function App() {
    return (
        <Grid2 container sx={{ height: '100svh' }}>
            <Grid2 size={4} sx={{ backgroundColor: 'red' }}>
                <Typography>
                    This will be a menu
                </Typography>
            </Grid2>
            <Grid2 size={8} sx={{ backgroundColor: 'blue' }}>
                <Typography>
                    This will be a network structure
                </Typography>
            </Grid2>

        </Grid2>
    );
}

export default App;
