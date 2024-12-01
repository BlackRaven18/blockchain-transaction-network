import React, { memo } from 'react';
import {
  type BuiltInNode,
  type NodeProps,
  Handle,
  Position,
} from '@xyflow/react';
 
 
const BiDirectionalNode = ({ data }: NodeProps<BuiltInNode>) => {
  return (
    <div>
      {data.label}
      <Handle type="source" position={Position.Top} id="a" />
      <Handle type="source" position={Position.Right} id="b" />
      <Handle type="source" position={Position.Bottom} id="c" />
      <Handle type="source" position={Position.Left} id="d" />
    </div>
  );
};
 
export default memo(BiDirectionalNode);