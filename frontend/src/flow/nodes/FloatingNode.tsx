import { Divider, Stack, styled, Typography } from '@mui/material';
import { Handle, Position, useConnection } from '@xyflow/react';
import HourglassBottomIcon from '@mui/icons-material/HourglassBottom';
import PowerOffIcon from '@mui/icons-material/PowerOff';
import { Dangerous } from '@mui/icons-material';

interface NodeProps {
    id: string;
    data: any;
}

const BusyHourglass = styled(HourglassBottomIcon)({
    animation: "spin 2s linear infinite",
    "@keyframes spin": {
        "0%": { transform: "rotate(0deg)" },
        "100%": { transform: "rotate(360deg)" },
    },
});

const IdleHourglass = styled(HourglassBottomIcon)({
    animation: "bounce 2s linear infinite",
    "@keyframes bounce": {
        "0%": { transform: "rotate(45deg)" },
        "50%": { transform: "rotate(-45deg)" },
        "100%": { transform: "rotate(45deg)" },
    },
});

const showIcon = (state: string) => {
    switch (state) {
        case "down":
            return <PowerOffIcon />;
        case "damaged":
            return <Dangerous />;
        case "idle":
            return <IdleHourglass />;
        default:
            return <BusyHourglass />;
    }
}

export default function FloatingNode({ id, data }: NodeProps) {
    const connection = useConnection();

    const isTarget = connection.inProgress && connection.fromNode.id !== id;

    return (
        <div className="customNode">
            <div
                className="customNodeBody"
            >
                {!connection.inProgress && (
                    <Handle
                        className="customHandle"
                        position={Position.Right}
                        type="source"
                    />
                )}

                {(!connection.inProgress || isTarget) && (
                    <Handle className="customHandle" position={Position.Left} type="target" isConnectableStart={false} />
                )}
                <Stack direction={"column"} style={{ alignItems: "center" }}>
                    {id}
                    <Divider sx={{ width: "100%", bgcolor: "black" }} />
                    <Typography style={{ fontSize: "10px" }}>{data?.state || "no info"}</Typography>

                    {showIcon(data?.state || "idle")}
                </Stack>
            </div>
        </div>
    );
}