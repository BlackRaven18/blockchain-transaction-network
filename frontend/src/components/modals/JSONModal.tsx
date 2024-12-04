import { Button, Modal, Box } from "@mui/material";
import React, { useEffect, useState } from "react";
import SyntaxHighlighter from "react-syntax-highlighter";
import { dracula } from "react-syntax-highlighter/dist/esm/styles/hljs";
import { getNodeBlockchain } from "../../api/launcher";
import { JsonView, allExpanded, darkStyles, defaultStyles } from "react-json-view-lite";

interface JSONModalProps {
    nodeId: string,
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
        getNodeBlockchain(props.nodeId)
            .then((response) => setData(response))
            .catch((error) => {
                console.log(error)
                setData('Could not fetch data')
            });
    }, [open])


    return (
        <React.Fragment>
            <Button variant="contained" onClick={handleOpen}>Show chain</Button>
            <Modal
                open={open}
                onClose={handleClose}
                aria-labelledby="child-modal-title"
                aria-describedby="child-modal-description"
            >
                <Box sx={style}>
                    {/* <SyntaxHighlighter language="json" style={dracula}>
                        {JSON.stringify(data, null, 2)}
                    </SyntaxHighlighter> */}
                    <JsonView data={data} shouldExpandNode={allExpanded} style={darkStyles} />
                </Box>
            </Modal>
        </React.Fragment>
    );
}