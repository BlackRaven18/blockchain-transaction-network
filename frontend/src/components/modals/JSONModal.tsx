import { Box, Button, Modal } from "@mui/material";
import React, { useEffect, useState } from "react";
import { JsonView, allExpanded, darkStyles } from "react-json-view-lite";
import { getNodeBlockchain, getNodeRegisteredClients } from "../../api/launcher";

interface JSONModalProps {
    nodeId: string,
    buttonTitle: string,
    action: "get-blockchain" | "get-clients"
}

const style = {
    position: 'absolute',
    alignItems: 'center',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    maxHeight: '80%',
    width: '50%',
    bgcolor: '#282A36',
    border: '2px solid #000',
    boxShadow: 24,
    overflow: 'scroll',
    p: 4,
};

export default function JSONModal(props: JSONModalProps) {
    const [open, setOpen] = useState(false);
    const [data, setData] = useState('');

    const handleOpen = () => {
        setOpen(true);
    };
    const handleClose = () => {
        setOpen(false);
    };

    useEffect(() => {

        if(props.action === "get-blockchain") {
            getNodeBlockchain(props.nodeId)
                .then((response) => setData(response))
                .catch((error) => {
                    console.log(error)
                    setData('Could not fetch blockchain')
                });
        } else if(props.action === "get-clients") {
            getNodeRegisteredClients(props.nodeId)
                .then((response) => setData(response))
                .catch((error) => {
                    console.log(error)
                    setData('Could not fetch clients')
                })
        } else {
            setData('Unknown action, sorry...')
        }

    }, [open])


    return (
        <React.Fragment>
            <Button variant="contained" onClick={handleOpen}>{props.buttonTitle}</Button>
            <Modal
                open={open}
                onClose={handleClose}
                aria-labelledby="child-modal-title"
                aria-describedby="child-modal-description"
            >
                <Box sx={style}>
                    <JsonView data={data} shouldExpandNode={allExpanded} style={darkStyles} />
                </Box>
            </Modal>
        </React.Fragment>
    );
}