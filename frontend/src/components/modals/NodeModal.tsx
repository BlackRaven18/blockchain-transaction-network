import { Button, Divider, Modal, Stack, Typography } from "@mui/material";
import { postInjectNodeDamageError, postInjectTransactionVoteError, postResetNodeDamageError, postResetTransactionVoteError } from "../../api/node";
import JSONModal from "./JSONModal";

interface NodeModalProps {
    open: boolean;
    handleCloseModal: () => void;
    selectedNode: any;
}

export default function NodeModal(props: NodeModalProps) {

    const injectNodeDamageError = async () => {
        await postInjectNodeDamageError(props.selectedNode?.id);
    }

    const resetNodeDamageError = async () => {
        await postResetNodeDamageError(props.selectedNode?.id);
    }

    const injectTransactionVoteError = async () => {
        await postInjectTransactionVoteError(props.selectedNode?.id);
    }

    const resetTransactionVoteError = async () => {
        await postResetTransactionVoteError(props.selectedNode?.id);
    }

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
                        <Button variant="contained" onClick={() => injectNodeDamageError()}>Inject Node Damage</Button>
                        <Button variant="contained" onClick={() => resetNodeDamageError()}>Reset Node Damage</Button>
                    </Stack>

                    <Divider sx={{ width: "100%", fontSize: "18px" }} > Inject Transaction Vote Error</Divider>
                    <Stack direction={"row"} spacing={2}>
                        <Button variant="contained" onClick={() => injectTransactionVoteError()}>Inject Transaction Vote Error</Button>
                        <Button variant="contained" onClick={() => resetTransactionVoteError()}>Reset Transaction Vote Error</Button>
                    </Stack>

                </Stack>
            </Modal>
        </>
    )
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