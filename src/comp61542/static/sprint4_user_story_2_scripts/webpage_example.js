var redraw, g, renderer;



window.onload = function() {
	
/*	var width = $(document).width() - 80;
	var height = $(document).height() - 80;
*/
	var width = 800;
	var height = 600;
	g = new Graph();
	 
	g.addEdge("strawberry", "cherry");
	g.addEdge("strawberry", "apple");
/*	g.addEdge("strawberry", "tomato"); */
	 
	g.addEdge("tomato", "apple");
	g.addEdge("tomato", "kiwi");
	 
	g.addEdge("cherry", "apple");
	g.addEdge("cherry", "kiwi");
	 
	var layouter = new Graph.Layout.Spring(g);
	layouter.layout();
	 
	/* draw the graph using the RaphaelJS draw implementation */
	renderer = new Graph.Renderer.Raphael('canvas', g, width, height);
	renderer.draw();

	redraw = function() {
	    layouter.layout();
	    renderer.draw();
	};
	hide = function(id) {
	    g.nodes[id].hide();
	};
	show = function(id) {
	    g.nodes[id].show();
	};
}

