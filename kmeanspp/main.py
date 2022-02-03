import numpy as np
from random import randint
from manim import *


class Main(Scene):
    def construct(self):
        # range [low,high,steps]
        grid = Axes(x_range=[0, 40, 2], y_range=[
                    0, 20, 2], tips=False,).add_coordinates()
        self.add(grid)

        def distance(p1, p2):
            return np.sum((p1 - p2)**2)

        def addPointToGrid(x, y):
            pointX = grid.c2p(x, y)
            self.add(Dot(pointX))

        def generatePointsInRange(n, lowX, highX, lowY, highY):
            points = []
            while len(points) != n:
                ppx = randint(lowX, highX)
                ppy = randint(lowY, highY)
                cflag = 0
                for p in points:
                    if(p == [ppx, ppy]):
                        cflag = 1
                        break
                if (cflag == 1):
                    continue
                points.append([ppx, ppy])
            return points

        def CentroidSelectionWithPoint(centroid):
            x = centroid[0]
            y = centroid[1]
            pointX = grid.c2p(x, y)
            circle = Circle(fill_opacity=0.4, fill_color=RED).move_to(pointX)
            dot = Dot(pointX).set_color(RED)
            self.play(DrawBorderThenFill(circle))
            self.play(Transform(circle, dot))
            self.add(dot)

        def kppviz(data, k):
            centroids = []
            centroids.append(data[np.random.randint(
                data.shape[0]), :])

            # Animate first centroid selection
            CentroidSelectionWithPoint(centroids[0])

            for c_id in range(k - 1):
                dist = []
                marrows = []
                lines2Plot = []
                for i in range(data.shape[0]):
                    point = data[i, :]
                    d = sys.maxsize

                    arrows = []
                    braces = []
                    bracetexts = []
                    tmp_centroid = 0
                    for j in range(len(centroids)):
                        temp_dist = distance(point, centroids[j])
                        d = min(d, temp_dist)
                        if d == temp_dist:
                            tmp_centroid = centroids[j]
                        
                        # ARROW ANIMATION
                        arrow_from = grid.c2p(point[0], point[1])
                        arrow_to = grid.c2p(centroids[j][0], centroids[j][1])
                        arrow = Arrow(arrow_from, arrow_to,buff=0).set_color(ORANGE)
                        arrows.append(arrow)
                        
                        brace = Brace(arrow, direction=arrow.copy().rotate(PI / 2).get_unit_vector())
                        braces.append(brace)

                        bracetext = brace.get_text(str(temp_dist))
                        bracetexts.append(bracetext)

                        if(i == 0):
                            self.play(GrowArrow(arrow), run_time=0.5)
                        self.add(arrow, brace, bracetext)
                        if(i == 0):
                            self.wait()
                        if(j == len(centroids) - 1):
                            self.wait(0.4)
                        # ARROW ANIMATION END
                    # Remove all arrows for centroids    
                    for x in range(len(centroids)):   
                        self.remove(arrows[x], braces[x], bracetexts[x])
                    dist.append(d)
                    lines2Plot.append([tmp_centroid,point])
                
                #plot all lines b4 choosing the max
                linesObj = []
                for line in lines2Plot :
                    fromxx = line[0][0]
                    fromyy = line[0][1]
                    toxx = line[1][0]
                    toyy = line[1][1]
                    dot = Dot(grid.c2p(fromxx, fromyy))
                    dot2 = Dot(grid.c2p(toxx, toyy))
                    line = Line(dot.get_center(), dot2.get_center()).set_color(TEAL)
                    self.add(line)
                    linesObj.append(line)
                self.wait()
                    
                dist = np.array(dist)
                next_centroid = data[np.argmax(dist), :]
                
                fromCentroid = 0
                for c in centroids:
                    distanceFrom_next_centroid = distance(next_centroid , c)
                    if(distanceFrom_next_centroid == dist[np.argmax(dist)]):
                        fromCentroid = c
                        break

                arrow_from = grid.c2p(fromCentroid[0], fromCentroid[1])
                arrow_to = grid.c2p(next_centroid[0], next_centroid[1])
                arrow = Arrow(arrow_from, arrow_to,buff=0).set_color(ORANGE)
                brace = Brace(arrow, direction=arrow.copy().rotate(PI / 2).get_unit_vector())
                bracetext = brace.get_text(str(dist[np.argmax(dist)])+ " [MAX]")
                self.play(GrowArrow(arrow), run_time=2)
                self.add(arrow, brace, bracetext)

                #REMOVE ALL LINE2PLOT
                for l in linesObj:
                    self.remove(l)
                # Animate centroid selection
                CentroidSelectionWithPoint(next_centroid)
                self.remove(arrow, brace, bracetext)
                
                centroids.append(next_centroid)
                dist = []
            return centroids

        # Generating clusters
        clusters = []
        clusters.append(generatePointsInRange(5, 32, 38, 14, 18))
        clusters.append(generatePointsInRange(4, 22, 28, 4, 8))
        clusters.append(generatePointsInRange(6, 2, 12, 14, 18))
        clusters.append(generatePointsInRange(4, 6, 12, 4, 8))
        # add more clusters here

        # Get all points for clusters
        points = []
        for cluster in clusters:
            for point in cluster:
                points.append(point)

        # Data
        data = np.array(points)
        # Plot all points
        for p in data:
            addPointToGrid(p[0], p[1])

        # Get Centroids
        centroids = kppviz(data, k=4)
        # print(centroids)
        self.wait(5)

class Intro(Scene):
    def construct(self):
        text = Text("KMeans++ Coordinate Visualization").scale(0.8)
        self.play(Write(text))
        grid = Axes(x_range=[0, 40, 2], y_range=[
                    0, 20, 2], tips=False,).add_coordinates()
        self.wait(2)
        self.play(GrowFromCenter(grid))
        self.wait()
        