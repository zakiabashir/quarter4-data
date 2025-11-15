'use client';

import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';
import { useSelector } from 'react-redux';
import { RootState } from '@/lib/store';

export default function AnimatedStateGraph() {
  const svgRef = useRef<SVGSVGElement | null>(null);
  const { states, transitions } = useSelector((state: RootState) => state.pda);
  const { currentState } = useSelector((state: RootState) => state.simulation);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;

    svg.selectAll('*').remove(); // Clear previous render

    const simulation = d3.forceSimulation<d3.SimulationNodeDatum, d3.SimulationLinkDatum>()
      .force('link', d3.forceLink().id((d: any) => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2));

    const nodes = states.map(s => ({ id: s }));
    const links = transitions.map(t => ({
      source: t.fromState,
      target: t.toState,
      label: `${t.input},${t.stackTop}/${t.pushSymbol}`
    }));

    const link = svg.append('g')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6)
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke-width', 1);

    const node = svg.append('g')
      .attr('stroke', '#fff')
      .attr('stroke-width', 1.5)
      .selectAll('circle')
      .data(nodes)
      .join('circle')
      .attr('r', 15)
      .attr('fill', d => (d.id === currentState ? 'red' : 'blue'))
      .call(d3.drag<SVGCircleElement, d3.SimulationNodeDatum>()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended));

    const label = svg.append('g')
      .attr('class', 'labels')
      .selectAll('text')
      .data(nodes)
      .join('text')
      .attr('class', 'node-label')
      .attr('font-size', '10px')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .text((d: any) => d.id);

    const linkLabel = svg.append('g')
      .attr('class', 'link-labels')
      .selectAll('text')
      .data(links)
      .join('text')
      .attr('class', 'link-label')
      .attr('font-size', '8px')
      .attr('fill', '#000')
      .text((d: any) => d.label);

    simulation.nodes(nodes as d3.SimulationNodeDatum[]).on('tick', ticked);
    simulation.force<d3.ForceLink<d3.SimulationNodeDatum, d3.SimulationLinkDatum>>('link')?.links(links);

    function ticked() {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node
        .attr('cx', (d: any) => d.x)
        .attr('cy', (d: any) => d.y);

      label
        .attr('x', (d: any) => d.x)
        .attr('y', (d: any) => d.y);

      linkLabel
        .attr('x', (d: any) => (d.source.x + d.target.x) / 2)
        .attr('y', (d: any) => (d.source.y + d.target.y) / 2);
    }

    function dragstarted(event: d3.D3DragEvent<SVGCircleElement, d3.SimulationNodeDatum, any>) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event: d3.D3DragEvent<SVGCircleElement, d3.SimulationNodeDatum, any>) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }

    function dragended(event: d3.D3DragEvent<SVGCircleElement, d3.SimulationNodeDatum, any>) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }

  }, [states, transitions, currentState]);

  return (
    <div className="w-full h-full">
      <svg ref={svgRef} className="w-full h-full border rounded-md bg-white"></svg>
    </div>
  );
}
