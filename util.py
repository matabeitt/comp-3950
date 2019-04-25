import numpy as np
import networkx as nx
import heapq as heap

INFECTION_RATE = 0.3
INFECTION_DURATION = 3


def read(filename):
    data = []
    with open(filename) as fp:
        # data.append(fp.read())
        l = fp.readlines()
        for pair in l:
            pair = pair.replace("\n", "")
            x,y = pair.split(" ")
            x = int(x)
            y = int(y)
            data.append((x,y))

    return data


def printf(filename, data):
    with open(filename, "w") as fp:
        for item in data:
            fp.write(str(item)+"\n")


def prob_death(num_days):
    return np.maximum(0.3 * (0.8**num_days), 0.1)


def prob_trans(num_days):
    return np.maximum(0.2 * (0.9**num_days), 0.1)


def make_graph(data):
    graph = nx.Graph()

    for item in data:
        graph.add_edge(*item)

    return graph


def initialise(graph):
    infected = 0
    for node in graph.nodes:
        infect = np.random.random()
        attr = {
            node: {
                'infected': True if infect < INFECTION_RATE else False,
                'date_infected': 0 if infect < INFECTION_RATE else 0,
                'duration': np.int(np.ceil(np.random.exponential(INFECTION_DURATION, size=1)[0])),
                'dead': False,
                'date_dead': None,
                'immune': True if infect < INFECTION_RATE else False
            }
        }
        nx.set_node_attributes(graph, attr)
        if infect < INFECTION_RATE:
            infected += 1

    return graph, infected


def simulate (graph, days=30):

    total_infected = 0
    total_dead = 0

    for day in range(1, days):
        """
        For each of 30 days, perform the following simulation on
        a social network of rabbits.
        """
        for node in graph.nodes:
            """
            For each rabbit in the social network, perform the 
            following checks and operations
            """
            days_left = graph.nodes[node]['duration'] - day # Days left for this node to be infectious

            if graph.nodes[node]['infected'] is True \
                and graph.nodes[node]['dead'] is False :
                """
                If the rabbit is infected
                """
                if days_left > 0:
                    """
                    If the rabbit is still supposed to be infected 
                    attempt to infect its neighbor rabbits as well 
                    as compute its possibility of dying.
                    """

                    transmission_threshold = prob_trans(days_left)

                    for v in nx.neighbors(graph, node):
                        """
                        For all neighbors of this node that can still 
                        transmit the disease, randomly decide if each 
                        neighbor becomes infected or not.
                        """
                        infected = np.random.random() < transmission_threshold
                        duration = np.int(np.ceil(np.random.exponential(INFECTION_DURATION, size=1)[0]))

                        if not (graph.nodes[v]['immune'] is True or \
                            graph.nodes[v]['dead'] is True or \
                            graph.nodes[v]['infected'] is True) and infected:
                            """
                            Only infect neighbors that are not already 
                            infected or neighbors that can be infected.
                            """
                            graph.nodes[v].update({
                                'infected': True if infected else False,
                                'date_infected': day if infected else 0,
                                'duration': duration+day if infected else 0,
                                'dead': False,
                                'date_dead': None,
                                'immune': False
                            })

                            total_infected += 1

                    death_threshold = prob_death(days_left)
                    dead = np.random.random() < death_threshold

                    if dead:
                        """
                        This node has to die, update its values
                        """
                        graph.nodes[node].update({
                            'infected': False,
                            'dead': True,
                            'date_dead': day,
                            'immune': True
                        })

                        total_dead += 1

                if days_left == 0:
                    """
                    If the rabbit has outlived its infection then 
                    make the specific rabbit immune to the 
                    infection
                    """
                    graph.nodes[node].update({
                        'infected': False,
                        'immune': True
                    })

    return graph, total_infected, total_dead

