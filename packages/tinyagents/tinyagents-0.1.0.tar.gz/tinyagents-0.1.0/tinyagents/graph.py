from typing import Any, Optional

from tinyagents.types import NodeOutput
from tinyagents.callbacks import BaseCallback
from tinyagents.callbacks import BaseCallback, StdoutCallback
from tinyagents.utils import check_for_response

class Graph:
    _graph: list

    def __init__(self):
        self._graph = []

    def compile(self, callback: BaseCallback = StdoutCallback()):
        return GraphRunner(self, callback=callback)
    
    def next(self, node: Any):
        self._graph.append(node)

    def __str__(self):
        return "".join([f" {node.name} ->" for node in self._graph])[:-3].strip()
    
    def __or__(self, node: Any):
        self.next(node)
        return self
    
    def get_order(self):
        """ Get the static order of nodes """
        return self._graph
    
    @property
    def root(self):
        order = self.get_order()
        return order[0] if len(order) > 0 else None

class GraphRunner:
    """ A class for executing the graph """

    def __init__(self, graph: Graph, callback: Optional[BaseCallback] = None):
        self._graph = graph
        self.callback = callback

    def execute(self, x: Any):
        if self.callback: self.callback.flow_start(inputs=x)

        response = None
        for node in self._graph.get_order():
            if response:
                break

            input = self._get_content(x)

            x = node.execute(input, callback=self.callback)

            response = check_for_response(x)
        
        if self.callback: self.callback.flow_end(outputs=response)

        return response

    @staticmethod
    def _get_content(x):
        """ Extract the content from the inputs """
        if isinstance(x, list):
            if len(x) > 0 and isinstance(x[0], NodeOutput):
                return [output.content for output in x]
            
        if isinstance(x, NodeOutput):
            return x.content
        
        return x