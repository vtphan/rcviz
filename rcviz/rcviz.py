# callviz : a small recursion call graph vizualization decorator
# Copyright (c) Ran Dugal 2014
# Licensed under the GPLv2, which is available at
# http://www.gnu.org/licenses/gpl-2.0.html


import inspect
import pygraphviz as gviz
import logging
import copy

COLORS = ['lightgrey','khaki','coral','turquoise','deepskyblue','gold','darkorange','goldenrod','olivedrab2','yellow','green','thistle','cyan','moccasin','red']

class callgraph(object):
	'''singleton class that stores global graph data
	   draw graph using pygraphviz
	'''

	_callers = {} # caller_fn_id : node_data
	_counter = 1  # track call order
	_unwindcounter = 1 # track unwind order
	_frames = [] # keep frame objects reference

	@staticmethod
	def reset():
		callgraph._callers = {}
		callgraph._counter = 1
		callgraph._frames = []
		callgraph._unwindcounter = 1

	@staticmethod
	def get_callers():
		return callgraph._callers

	@staticmethod
	def get_counter():
		return callgraph._counter

	@staticmethod
	def get_unwindcounter():
		return callgraph._unwindcounter

	@staticmethod
	def increment():
		callgraph._counter += 1

	@staticmethod
	def increment_unwind():
		callgraph._unwindcounter  += 1

	@staticmethod
	def get_frames():
		return callgraph._frames

	@staticmethod
	def render(filename=None, show_null_returns=True, annotate=False):

		if not filename:
			filename = "out.svg"

		g = gviz.AGraph(strict=False, directed=True)
		g.graph_attr['label']='nodes=%s' % len(callgraph._callers)

		# create nodes
		for frame_id, node in callgraph._callers.items():
			node_options = dict(shape='Mrecord', fontsize=13, labelfontsize=13)

			if annotate:
				node_options['fillcolor'] = COLORS[node.ret[-1]] if isinstance(node.ret[-1], int) else node.ret[-1]
				node_options['style'] = 'filled'
				node.ret = node.ret[0] if len(node.ret) > 1 else None

			if not show_null_returns and node.ret is None:
				node_options['label'] = "{ %s(%s) }" % (node.fn_name, node.argstr())
			else:
			   node_options['label'] = "{ %s(%s) | %s }" % (node.fn_name, node.argstr(), node.ret)

			g.add_node(frame_id, **node_options)



		# edge colors
		step = 200 / callgraph._counter
		cur_color = 0

		# create edges
		for frame_id, node in callgraph._callers.items():
			child_nodes = []
			for child_id, counter, unwind_counter in node.child_methods:
				child_nodes.append(child_id)
				cur_color = step * counter
				color = "#%2x%2x%2x" % (int(cur_color), int(cur_color), int(cur_color))
				label = "%s (&uArr;%s)" % (counter, unwind_counter)
				g.add_edge( frame_id, child_id, label=label, color= color, fontsize=8, labelfontsize=8, fontcolor="#999999" )

			# order edges l to r
			if len(child_nodes) > 1:
				sg = g.add_subgraph(child_nodes, rank='same')
				sg.graph_attr['rank']='same'
				prev_node = None
				for child_node in child_nodes:
					if prev_node:
						sg.add_edge( prev_node,  child_node, color="#ffffff" )
					prev_node = child_node

			#logging.info( "%s, %s" % (frame_id, node) )

		g.layout()

		g.draw(path=filename, prog='dot')

		print ("callviz: rendered to %s" % filename)

class node_data(object):

	def __init__(self, _args=None, _kwargs=None, _fnname="", _ret=None, _childmethods=[]):
		self.args  	= _args
		self.kwargs = _kwargs
		self.fn_name = _fnname
		self.ret	= _ret
		self.child_methods = _childmethods	# [ (method, gcounter) ]

	def __str__(self):
		return "%s -> child_methods: %s" % (self.nodestr(), self.child_methods)

	def nodestr(self):
		return "%s = %s(%s)" % (self.ret, self.fn_name, self.argstr())

	def argstr(self):
		s_args =  ",".join( [str(arg) for arg in self.args] )
		s_kwargs = ",".join( [(str(k), str(v)) for (k,v) in self.kwargs.items()] )
		return "%s%s" % (s_args, s_kwargs)

class viz(object):
	''' decorator to construct the call graph with args and return values as labels '''
	def __init__(self, wrapped):
		self._verbose = False
		self.wrapped = wrapped
		self.first_call = False
		self.i = 0
		# print ("__init__", id(self), wrapped)

	def __call__(self, *args, **kwargs):
		# print("__call__", args, kwargs, viz.i)
		if self.i==0:
			callgraph.reset()
		local_i = self.i
		self.i += 1

		g_callers = callgraph.get_callers()
		g_frames  = callgraph.get_frames()

		# find the caller frame, and add self as a child node
		caller_frame_id = None

		fullstack = inspect.stack()

		if (self._verbose):
			logging.debug("full stack: %s" % str(fullstack))

		if len (fullstack) > 2:
			caller_frame_id = id(fullstack[2][0])
			if ( self._verbose ):
				logging.debug("caller frame: %s %s" % (caller_frame_id, fullstack[2]))

		this_frame_id = id(fullstack[0][0])
		if (self._verbose):
			logging.info("this frame: %s %s" % (this_frame_id, fullstack[0]))

		if this_frame_id not in g_frames:
			g_frames.append( fullstack[0][0] )

		if  this_frame_id not in g_callers.keys():
			g_callers[this_frame_id] = node_data(copy.deepcopy(args), copy.deepcopy(kwargs), self.wrapped.__name__, None, [])

		edgeinfo = None
		if caller_frame_id:
			edgeinfo = [this_frame_id, callgraph.get_counter()]
			g_callers[caller_frame_id].child_methods.append( edgeinfo )
			callgraph.increment()

		# invoke wraped
		ret = self.wrapped(*args, **kwargs)

		if (self._verbose):
			logging.debug('unwinding frame id: %s' % this_frame_id)

		if edgeinfo:
			edgeinfo.append( callgraph.get_unwindcounter() )
			callgraph.increment_unwind()

		g_callers[this_frame_id].ret = copy.deepcopy(ret)

		# print(local_i)
		if local_i == 0:
			output_file = "{}.svg".format(self.wrapped.__name__)
			callgraph.render(output_file)

		return ret

