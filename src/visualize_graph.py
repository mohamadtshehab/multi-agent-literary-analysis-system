from IPython.display import Image, display

def visualize_graph(graph):
        # Generate Mermaid diagram
        mermaid_png = graph.get_graph().draw_mermaid_png()
        display(Image(mermaid_png))
        #save the image to a file
        with open('graph.png', 'wb') as f:
            f.write(mermaid_png)
        print("(🎨) Graph saved to graph.png")