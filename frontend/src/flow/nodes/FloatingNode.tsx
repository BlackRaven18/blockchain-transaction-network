import { Divider, Icon, Stack, styled, Typography } from '@mui/material';
import { Handle, Position, useConnection } from '@xyflow/react';
import HourglassBottomIcon from '@mui/icons-material/HourglassBottom';
import PowerOffIcon from '@mui/icons-material/PowerOff';

interface NodeProps {
    id: string;
    data: any;
}

const BusyHourglass = styled(HourglassBottomIcon)({
    animation: "spin 2s linear infinite", // Define the animation
    "@keyframes spin": {
        "0%": { transform: "rotate(0deg)" },
        "100%": { transform: "rotate(360deg)" },
    },
});

const IdleHourglass = styled(HourglassBottomIcon)({
    animation: "bounce 2s linear infinite", // Define the animation
    "@keyframes bounce": {
      "0%": { transform: "rotate(45deg)" },
      "50%": { transform: "rotate(-45deg)" },
      "100%": { transform: "rotate(45deg)" },
    },
  });

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
                    {data?.state === "down" && <PowerOffIcon />}
                    {data?.state === "idle" && <IdleHourglass />}
                    {data?.state !== "idle" && data?.state !== "down" && <BusyHourglass />}
                </Stack>
            </div>
        </div>
    );
}