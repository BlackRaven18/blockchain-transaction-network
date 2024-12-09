import { Modal, Stack, Typography, Divider, Button } from "@mui/material";
import JSONModal from "./JSONModal";

interface NodeModalProps {
    open: boolean;
    handleCloseModal: () => void;
    selectedNode: any;
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

export default function NodeModal(props: NodeModalProps) {

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
                    {/* <Button variant="contained" onClick={() => { }}>Connect to other nodes</Button> */}

                    <JSONModal nodeId={props.selectedNode?.id} buttonTitle="Show blockchain" action="get-blockchain"/>
                    <JSONModal nodeId={props.selectedNode?.id} buttonTitle="Show registered clients" action="get-clients"/>
                </Stack>
            </Modal>
        </>
    )
}