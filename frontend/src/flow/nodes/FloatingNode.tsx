import { Icon, Stack, styled, Typography } from '@mui/material';
import { Handle, Position, useConnection } from '@xyflow/react';
import HourglassBottomIcon from '@mui/icons-material/HourglassBottom';

interface NodeProps {
    id: string;
    data: any;
}

const AnimatedHourglass = styled(HourglassBottomIcon)({
    animation: "spin 2s linear infinite", // Define the animation
    "@keyframes spin": {
      "0%": { transform: "rotate(0deg)" },
      "100%": { transform: "rotate(360deg)" },
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
                <Stack direction={"column"}>
                    {id}
                    <Typography style={{ fontSize: "10px" }}>{"state:" + data?.state || "no info"}</Typography>
                    <HourglassBottomIcon />
                </Stack>
            </div>
        </div>
    );
}