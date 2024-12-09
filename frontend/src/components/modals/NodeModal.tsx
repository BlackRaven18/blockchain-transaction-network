import { Backdrop, Button, CircularProgress, Divider, Modal, Stack, Typography } from "@mui/material";
import { postInjectBlockMiningError, postInjectNodeDamageError, postInjectTransactionVoteError, postResetBlockMiningError, postResetNodeDamageError, postResetTransactionVoteError } from "../../api/node";
import JSONModal from "./JSONModal";
import { useState } from "react";
import { AxiosResponse } from "axios";

interface NodeModalProps {
    open: boolean;
    handleCloseModal: () => void;
    selectedNode: any;
}

export default function NodeModal(props: NodeModalProps) {
    const [loading, setLoading] = useState(false);

    const withLoadingDelay = async (action: () => Promise<AxiosResponse>) => {
        setLoading(true);
        await action();
        setTimeout(() => {
            setLoading(false);
        }, 1500);
    };


    const injectNodeDamageError = () => withLoadingDelay(() => postInjectNodeDamageError(props.selectedNode?.id));
    const resetNodeDamageError = () => withLoadingDelay(() => postResetNodeDamageError(props.selectedNode?.id));
    const injectTransactionVoteError = () => withLoadingDelay(() => postInjectTransactionVoteError(props.selectedNode?.id));
    const resetTransactionVoteError = () => withLoadingDelay(() => postResetTransactionVoteError(props.selectedNode?.id));
    const injectBlockMiningError = () => withLoadingDelay(() => postInjectBlockMiningError(props.selectedNode?.id));
    const resetBlockMiningError = () => withLoadingDelay(() => postResetBlockMiningError(props.selectedNode?.id));

    return (
        <>
            <Modal
                open={props.open}
                onClose={props.handleCloseModal}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Stack direction={"column"} spacing={2} sx={style}>
                    <Typography variant="h5">{props.selectedNode?.id}</Typography>
                    <Divider sx={{ width: "100%", bgcolor: "black" }} />

                    <JSONModal nodeId={props.selectedNode?.id} buttonTitle="Show blockchain" action="get-blockchain" />
                    <JSONModal nodeId={props.selectedNode?.id} buttonTitle="Show registered clients" action="get-clients" />

                    <Typography variant="h6" sx={{ paddingTop: "20px" }}>Error Injection</Typography>
                    <Divider sx={{ width: "100%", bgcolor: "black" }} />

                    <JSONModal nodeId={props.selectedNode?.id} buttonTitle="Health Check" action="health-check" />

                    <Divider sx={{ width: "100%", fontSize: "18px" }} > Inject Node Damage Error</Divider>
                    <Stack direction={"row"} spacing={2}>
                        <Button variant="contained" onClick={injectNodeDamageError}>Inject Node Damage</Button>
                        <Button variant="contained" onClick={resetNodeDamageError}>Reset Node Damage</Button>
                    </Stack>

                    <Divider sx={{ width: "100%", fontSize: "18px" }} > Inject Transaction Vote Error</Divider>
                    <Stack direction={"row"} spacing={2}>
                        <Button variant="contained" onClick={injectTransactionVoteError}>Inject Transaction Vote Error</Button>
                        <Button variant="contained" onClick={resetTransactionVoteError}>Reset Transaction Vote Error</Button>
                    </Stack>

                    <Divider sx={{ width: "100%", fontSize: "18px" }} > Inject Block Mining Error</Divider>
                    <Stack direction={"row"} spacing={2}>
                        <Button variant="contained" onClick={injectBlockMiningError}>Inject Block Mining Error</Button>
                        <Button variant="contained" onClick={resetBlockMiningError}>Reset Block Mining Error</Button>
                    </Stack>

                    <LoadingBackdrop open={loading} />

                </Stack>
            </Modal>
        </>
    )
}

const LoadingBackdrop = ({ open }: { open: boolean }) => {
    return (
        <Backdrop
            sx={(theme) => ({ color: '#fff', zIndex: theme.zIndex.drawer + 1 })}
            open={open}
        >
            <Stack direction={"column"} spacing={2} sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                <CircularProgress color="inherit" />
                <h3>Loading...</h3>
            </Stack>
        </Backdrop>
    );
}

const style = {
    position: 'absolute',
    alignItems: 'center',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
};
