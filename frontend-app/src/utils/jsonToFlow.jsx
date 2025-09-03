// Converts backend JSON into React Flow nodes + edges
const jsonToFlow = (data) => {
  if (!data || !data.code) {
    return { nodes: [], edges: [], isJson: false };
  }

  let jsonString = data.code;
  const match = jsonString.match(/```json\n([\s\S]*?)\n```/);
  if (match && match[1]) {
    jsonString = match[1];
  }

  try {
    const rungs = JSON.parse(jsonString);
    const nodes = [];
    const edges = [];
    const nodeWidth = 100;
    const nodeHeight = 40;
    const paddingX = 50;

    rungs.forEach((rung, rungIndex) => {
      let currentX = paddingX;
      let rungY = rungIndex * (nodeHeight + 80) + paddingX;

      const leftRailId = `rail_${rung.id}_left`;
      nodes.push({
        id: leftRailId,
        position: { x: 0, y: rungY },
        data: { label: "PWR" },
        style: { width: "10px", backgroundColor: "gray" },
      });

      rung.elements.forEach((element, elementIndex) => {
        const nodeId = `${rung.id}_${element.tag}_${elementIndex}`;
        nodes.push({
          id: nodeId,
          type: "default",
          position: { x: currentX, y: rungY },
          data: { label: element.tag, type: element.type },
          style: {
            width: nodeWidth,
            height: nodeHeight,
            backgroundColor: "#f0f0f0",
          },
        });

        if (elementIndex === 0) {
          edges.push({
            id: `e-${leftRailId}-${nodeId}`,
            source: leftRailId,
            target: nodeId,
            animated: true,
          });
        } else {
          const prevNodeId = `${rung.id}_${rung.elements[elementIndex - 1].tag}_${
            elementIndex - 1
          }`;
          edges.push({
            id: `e-${prevNodeId}-${nodeId}`,
            source: prevNodeId,
            target: nodeId,
            animated: true,
          });
        }

        currentX += nodeWidth + 50;
      });

      const rightRailId = `rail_${rung.id}_right`;
      nodes.push({
        id: rightRailId,
        position: { x: currentX, y: rungY },
        data: { label: "GND" },
        style: { width: "10px", backgroundColor: "gray" },
      });

      const lastNodeId = `${rung.id}_${rung.elements[rung.elements.length - 1].tag}_${
        rung.elements.length - 1
      }`;
      edges.push({
        id: `e-${lastNodeId}-${rightRailId}`,
        source: lastNodeId,
        target: rightRailId,
        animated: true,
      });
    });

    return { nodes, edges, isJson: true };
  } catch (e) {
    console.error("Failed to parse JSON:", e);
    return { nodes: [], edges: [], isJson: false };
  }
};

export default jsonToFlow;
