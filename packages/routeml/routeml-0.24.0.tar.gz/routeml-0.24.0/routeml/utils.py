import re
import requests
import math
import random
import numpy as np


def routes_to_solution(routes):
    """
    Converts a list of routes into a solution (list of routes).

    Args:
        routes (list): List of routes, where each route is a list of nodes.

    Returns:
        list: Solution (list of routes).
    """
    solution = []
    for i, route in enumerate(routes):
        assert route[0] == 0
        assert route[-1] == 0
        # Skip depot node for all routes except the first one
        if i > 0:
            route = route[1:]
        solution += route
    return solution


def add_depot_to_routes(routes):
    """
    Adds the depot node to the beginning and end of each route.

    Args:
        routes (list): List of routes, where each route is a list of nodes.

    Returns:
        list: List of routes, where each route is a list of nodes, with the depot added.

    Raises:
        ValueError: If routes is not a list or a nested list.
    """
    if not isinstance(routes, list):
        raise ValueError("Routes must be a list")

    for route in routes:
        if not isinstance(route, list):
            raise ValueError("Routes must be a nested list")

        route.insert(0, 0)
        route.append(0)

    return routes


def solution_to_routes(solution, partial=False):
    """
    Converts a solution (list of nodes) into a list of routes.

    Args:
        solution (list): Solution (list of nodes).

    Returns:
        list: List of routes, where each route is a list of nodes.
    """
    routes = []
    route = []
    for node in solution:
        if node == 0 and route:
            route.append(0)
            routes.append(route)
            route = []
        route.append(node)
    if partial:
        routes.append(route)
    return routes


def solution_to_adjacency_matrix(cvrp_solution):
    """
    Converts a CVRP solution into a symmetric adjacency matrix.

    Args:
        cvrp_solution (list): CVRP solution (list of nodes).

    Returns:
        np.ndarray: Symmetric adjacency matrix.
    """
    num_nodes = max(cvrp_solution) + 1
    matrix = np.zeros((num_nodes, num_nodes))

    for i in range(len(cvrp_solution) - 1):
        matrix[cvrp_solution[i]][cvrp_solution[i + 1]] = 1
        matrix[cvrp_solution[i + 1]][cvrp_solution[i]] = 1
    return matrix


def column_normalize_adjacency_matrix(adj_matrix):
    """
    Normalize an adjacency matrix by column.

    Args:
        adj_matrix (np.ndarray): Binary adjacency matrix.

    Returns:
        np.ndarray: Normalized adjacency matrix.
    """
    col_sums = np.sum(adj_matrix, axis=0)
    normalized_matrix = adj_matrix / col_sums[np.newaxis, :]
    return normalized_matrix


def parse_vrplib_file(source):
    """
    Parses a VRPLIB file and returns a dictionary with the following keys:
    - name: Name of the problem.
    - comment: Comment of the problem.
    - type: Type of the problem.
    - dimension: Number of nodes.
    - edge_weight_type: Type of edge weight.
    - capacity: Capacity of the vehicles.
    - node_coords: Dict of node coordinates.
    - demand: Dict of node demands.
    - depot_ids: List of depot IDs.

    Args:
        source (str): URL or path to the VRPLIB file.

    Returns:
        dict: Dictionary with the parsed data.
    """
    if source.startswith('http://') or source.startswith('https://'):
        response = requests.get(source)
        content = response.text
    else:
        with open(source, 'r') as file:
            content = file.read()

    data = {}

    # Extracting problem information using regex
    name_match = re.search(r'NAME\s*:\s*(\S+)', content)
    if name_match:
        data['name'] = name_match.group(1)

    comment_match = re.search(r'COMMENT\s*:\s*"(.+)"', content)
    if comment_match:
        data['comment'] = comment_match.group(1)

    type_match = re.search(r'TYPE\s*:\s*(\S+)', content)
    if type_match:
        data['type'] = type_match.group(1)

    dimension_match = re.search(r'DIMENSION\s*:\s*(\d+)', content)
    if dimension_match:
        data['dimension'] = int(dimension_match.group(1))

    edge_weight_type_match = re.search(
        r'EDGE_WEIGHT_TYPE\s*:\s*(\S+)', content)
    if edge_weight_type_match:
        data['edge_weight_type'] = edge_weight_type_match.group(1)

    capacity_match = re.search(r'CAPACITY\s*:\s*(\d+)', content)
    if capacity_match:
        data['capacity'] = int(capacity_match.group(1))

    node_coords_match = re.search(
        r'NODE_COORD_SECTION\s*(.+?)\s*DEMAND_SECTION', content, re.DOTALL)
    if node_coords_match:
        node_coords_str = node_coords_match.group(1).strip()
        node_coords = []
        for line in node_coords_str.split('\n'):
            node_id, x, y = re.findall(
                r'(\d+)\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)', line)[0]
            node_coords.append([float(x), float(y)])
        data['node_coords'] = np.array(node_coords)

    # Extracting demand information
    demand_section_match = re.search(
        r'DEMAND_SECTION\s*(.+?)\s*DEPOT_SECTION', content, re.DOTALL)
    if demand_section_match:
        demand_section_str = demand_section_match.group(1).strip()
        demand = []
        for line in demand_section_str.split('\n'):
            node_id, demand_val = re.findall(r'(\d+)\s+(-?\d+)', line)[0]
            demand.append(int(demand_val))
        data['demand'] = np.array(demand)

    # Extracting depot information
    depot_section_match = re.search(
        r'DEPOT_SECTION\s*(.+?)\s*EOF', content, re.DOTALL)
    if depot_section_match:
        depot_section_str = depot_section_match.group(1).strip()
        depot_ids = [int(node_id) for node_id in re.findall(
            r'(\d+)\s*[^-0-9]', depot_section_str)]
        data['depot_ids'] = depot_ids

    return data


def parse_vrplib_solution(source):
    """
    Parses a solution file from the VRPLIB website and returns the routes and cost.

    Args:
        source (str): Path to the solution file or URL to the solution file.

    Returns:
        tuple: Tuple containing the routes (list of lists) and the cost (float).
    """
    route_regex = re.compile(r'Route #(\d+): (.+)')
    cost_regex = re.compile(r'Cost ([\d.]+)')

    if source.startswith('http://') or source.startswith('https://'):
        response = requests.get(source)
        solution_text = response.text
    else:
        with open(source, 'r') as file:
            solution_text = file.read()

    routes = []
    cost = None

    lines = solution_text.strip().split('\n')
    for line in lines:
        route_match = route_regex.match(line)
        if route_match:
            route_number = int(route_match.group(1))
            nodes = list(map(int, route_match.group(2).split()))
            routes.append(nodes)

        cost_match = cost_regex.match(line)
        if cost_match:
            cost = float(cost_match.group(1))

    return routes, cost


def get_cvrp_cost(routes_or_solution, coordinates, uchoa=False):
    """
    Compute the total cost of a CVRP solution.

    Args:
        routes_or_solution (list or solution): List of routes or a solution.
        coordinates (np.array): Array of node coordinates with shape (n_nodes, 2).
        uchoa (bool): Whether to round the distances to the nearest integer. Follows the 2014 paper.

    Returns:
        float: Total cost of the CVRP solution.
    """
    if isinstance(routes_or_solution, list) and isinstance(routes_or_solution[0], list):
        solution = routes_to_solution(routes_or_solution)
    elif isinstance(routes_or_solution, list):
        solution = routes_or_solution
    else:
        raise ValueError(
            "Invalid input. Expected a nested list of routes or a solution.")

    total_cost = 0.0
    for i in range(len(solution) - 1):
        node1 = solution[i]
        node2 = solution[i + 1]
        coord1 = coordinates[node1]
        coord2 = coordinates[node2]
        distance = math.dist(coord1, coord2)
        if uchoa:
            distance = round(distance)
        total_cost += distance

    return total_cost


def get_all_route_demands(routes, demand):
    """
    Compute the demand of each route.

    Args:
        routes (list): List of routes.

    Returns:
        route_demand (list): List containing the demand of each route.
    """
    route_demands = []
    for route in routes:
        route_demand = 0
        for node in route:
            try:
                route_demand += demand[node]
            except KeyError:
                raise Exception(
                    f"Node {node} not found in the demand dictionary")
        route_demands.append(route_demand)
    return route_demands


def get_route_demand(route, demands):
    """
    Compute the demand of a route.

    Args:
        route (list): List of nodes in the route.
        demands (list): List containing the corresponding demands for each node.

    Returns:
        int: Demand of the route.
    """
    route_demand = sum(map(lambda node: demands[node], route))
    return route_demand


def is_feasible(routes, demand, capacity):
    """
    Check if a CVRP solution is feasible.

    Args:
        routes (list): List of routes.
        demand (dict): Dictionary containing node IDs as keys and corresponding demand as values.
        capacity (int): Vehicle capacity.

    Returns:
        bool: True if the solution is feasible, False otherwise.
    """
    # Convert routes to a single solution
    solution = routes_to_solution(routes)

    # Check if each node appears only once
    if set(solution) != set(demand.keys()):
        return False

    # Compute the demand for each route
    for route in routes:
        total_demand = sum(demand[node] for node in route)
        if total_demand > capacity:
            return False

    return True


def get_cvrp_problem(num_nodes):
    """
    Generate a random CVRP problem.
    Follows: "https://arxiv.org/pdf/1802.04240.pdf"

    Args:
        num_nodes (int): Number of nodes in the problem. Excluding depot.

    Returns:
        tuple: Tuple containing the node coordinates (np.ndarray) and the demand (np.ndarray).
    """
    # Generate depot
    depot_id = 0
    depot_coords = np.array([random.uniform(0, 1), random.uniform(0, 1)])
    depot_demand = np.array([0])

    # Generate node coordinates array
    node_coords = np.empty((num_nodes + 1, 2))
    node_coords[depot_id] = depot_coords

    # Generate demand array
    demands = np.empty((num_nodes + 1))
    demands[depot_id] = depot_demand

    # Generate node coordinates and demand
    for node_id in range(1, num_nodes + 1):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        demand_val = random.randint(1, 9)
        node_coords[node_id] = np.array([float(x), float(y)])
        demands[node_id] = int(demand_val)

    return node_coords, demands


def pad_matrix(matrix, new_shape, constant_value=0):
    """
    Pads a matrix to the right and bottom with zeros.

    Args:
        matrix: the input matrix to pad.
        new_shape: the desired shape after padding.

    Returns:
        returns the padded matrix.

    ```python
    import numpy as np
    matrix = np.arange(10).reshape(2, 5)
    pad_matrix(matrix, (3, 6))
    array([[0, 1, 2, 3, 4, 0],
           [5, 6, 7, 8, 9, 0],
           [0, 0, 0, 0, 0, 0]])
    ```
    """
    assert len(new_shape) == len(
        matrix.shape), "new_shape and matrix dimensions must match"
    padding = [(0, new_dim - old_dim) if new_dim > old_dim else (0, 0)
               for old_dim, new_dim in zip(matrix.shape, new_shape)]
    return np.pad(matrix, padding, 'constant', constant_values=constant_value)


def get_submatrix(indices, matrix, new_shape):
    """
    Gets a submatrix from a matrix and pads it to the right and bottom with zeros.

    Args:
        indices: the indices to index on the matrix.
        matrix: the input matrix to index.
        new_shape: the desired shape after padding.

    Returns:
        returns the submatrix after indexing and padding.

    ```python
    import numpy as np
    matrix = np.arange(10).reshape(2, 5)
    indices = [1, 2, 3]
    array([[1, 2, 3, 0, 0, 0],
           [6, 7, 8, 0, 0, 0],
           [0, 0, 0, 0, 0, 0]])
    ```
    """
    submatrix = matrix[:, indices]
    return pad_matrix(submatrix, new_shape)


def get_random_solution(N):
    """
    Generates a random CVRP solution. Mostly for debugging purposes.

    Args:
        N (int): Number of nodes in the problem. Excluding depot.

    Returns:
        lst (list): List containing the solution.
    """
    # Generate a random list from 0 to N
    lst = list(range(N + 1))

    # Insert 0 at the end
    lst.append(0)

    # Randomly insert 1 to 5 zeros in between
    num_zeros = random.randint(1, 5)
    for _ in range(num_zeros):
        # Select a random index between 1 and len(lst)-1
        index = random.randint(1, len(lst) - 1)
        while lst[index] == 0 or lst[index-1] == 0:
            # Select a new index if adjacent elements are already 0
            index = random.randint(1, len(lst) - 1)
        lst.insert(index, 0)

    return lst


def get_logit_mask(sol, demands, capacity, city_size=None):
    """
    Gets a logit mask for a given solution. Note that this only takes a full solution.

    Args:
        sol (list): the solution to mask.
        demands (dict): the demands of each node.
        capacity (int): the capacity of the vehicle.
        city_size (int): the size of the city (including depot). If None, then it is assumed to 
        be the same as the number of nodes.

    Returns:
        mask (np.ndarray): the logit mask.
    """
    prob = set(sol)
    if city_size is None:
        mask = np.full((len(sol) - 1, len(prob)), 0.0)  # mark all as valid
    else:
        mask = np.full((len(sol) - 1, city_size), 0.0)  # mark all as valid

        # mark all nodes not in city as invalid
        mask[:, list(set(range(city_size)) - prob)] = float("-inf")
    # NOTE this loop is 100% correct, don't change this.
    for i in range(len(sol) - 1):
        # a is all nodes that I visited
        a = set(sol[:i+1])
        if sol[i] != 0:
            a.remove(0)
        # mark all visited nodes as invalid
        mask[i, list(a)] = float("-inf")

        # mark all infeasible demand nodes as invalid
        # this crazy implementation is due to cProfile saying
        # list comprehension is super slow. numpy is fast.
        c_nodes = list(set(prob) - set(sol[:i+1]) - set([0]))
        last_route = solution_to_routes(sol[:i+1], partial=True)[-1]
        cur_demand = get_route_demand(last_route, demands)
        c_demands = np.array([demands[c_node] for c_node in c_nodes])
        next_demands = c_demands + cur_demand
        sel = np.squeeze(np.argwhere(next_demands > capacity))
        infeasible_nodes = np.array(c_nodes)[sel]
        if a == set(prob):
            mask[i, :] = 0
        else:
            mask[i, infeasible_nodes.tolist()] = float("-inf")
    return mask


def get_graph_embedding(src_key_padding_mask, node_emb):
    """
    Given a source key padding mask and node embeddings, this function generates a graph embedding by summing 
    the embeddings at positions specified by the mask and normalizing by the number of nodes in the graph.

    The function works by inverting the src_key_padding_mask, adding an extra dimension to the mask to match 
    the node_emb's dimensions, and then extracts the node embeddings at the positions where mask is True. 
    The resulting embeddings are summed to obtain the graph embedding, which is then normalized by the number 
    of nodes in the graph.

    Args:
        src_key_padding_mask (torch.Tensor): A binary tensor of shape (batch_size, length), 
        where 0 indicates the position of nodes and 1 otherwise.
        node_emb (torch.Tensor): A tensor of node embeddings of shape (batch_size, length, node_emb_size).

    Returns:
        torch.Tensor: The graph embedding of shape (batch_size, node_emb_size). The embeddings are normalized 
        by the number of nodes in the graph.
    """
    mask = ~src_key_padding_mask
    if mask.sum() == 0:
        raise ValueError("The src_key_padding_mask cannot be all 1s.")
    mask = mask.unsqueeze(2).expand_as(node_emb)
    extracted_node_embs = node_emb * mask.float()
    graph_emb = extracted_node_embs.sum(dim=1)
    graph_emb = graph_emb / \
        (~src_key_padding_mask).sum(dim=1).unsqueeze(1).float()
    return graph_emb


def get_logit_mask_vector(prob, sol, demands, capacity, city_size):
    """
    Gets a logit mask for a given solution. 

    Args:
        prob (list): the list of nodes in the problem.
        sol (list): the solution to mask. Partial solution is fine.
        demands (dict): the demands of each node.
        capacity (int): the capacity of the vehicle.
        city_size (int): the size of the city (including depot).

    Returns:
        mask (np.ndarray): the logit mask for the last state.
    """

    # Initialize mask
    mask = np.zeros(city_size)

    # Nodes not in problem
    nodes_not_in_problem = set(range(city_size)) - set(prob)

    # Visited nodes
    visited_nodes = set(sol)

    # Nodes that violate capacity constraint
    nodes_violate_capacity = set()
    last_route = solution_to_routes(sol, partial=True)[-1]
    cur_demand = get_route_demand(last_route, demands)
    for node in prob:
        node_demand = demands[node]
        if cur_demand + node_demand > capacity:
            nodes_violate_capacity.add(node)

    # Mask
    mask[list(nodes_not_in_problem)] = float("-inf")
    mask[list(visited_nodes)] = float("-inf")
    mask[list(nodes_violate_capacity)] = float("-inf")

    if sol[-1] == 0:
        mask[0] = float("-inf")
    else:
        mask[0] = 0
    return mask


def get_invalid_nodes(sol, demands, capacity):
    num_nodes = len(demands)
    invalid_nodes = np.zeros(num_nodes, dtype=np.bool)
    last_route = solution_to_routes(sol, partial=True)[-1]
    cur_demand = get_route_demand(last_route, demands)

    # Mark nodes that exceed demand.
    for i in range(num_nodes):
        if cur_demand + demands[i] > capacity:
            invalid_nodes[i] = True

    # Mark visited nodes.
    visited = set(sol)
    invalid_nodes[list(visited)] = True

    if sol[-1] != 0:
        invalid_nodes[0] = False

    return invalid_nodes


def rotate_coords(coords, angle):
    """
    Rotates a set of coordinates around a given origin point by a specified angle.

    Args:
        coords (numpy.ndarray): Array of coordinates where each row represents a point (x, y).
        angle (float): The angle of rotation in degrees.

    Returns:
        numpy.ndarray: Array of rotated coordinates with the same shape as the input 'coords'.
    """
    # convert to radians
    angle = math.radians(angle)

    origin = coords[0]
    customers = coords[1:]

    diff = customers - origin

    x_mutate = np.array([math.cos(angle), -math.sin(angle)])
    qx = origin[0] + np.sum(diff * x_mutate, axis=1)

    y_mutate = np.array([math.sin(angle), math.cos(angle)])
    qy = origin[0] + np.sum(diff * y_mutate, axis=1)

    out = np.vstack([qx, qy])
    out = np.concatenate([np.expand_dims(origin, axis=1), out], axis=1)
    return out.T


def montreal_to_canonical(sol):
    node_to_canonical = {}
    for i, node in enumerate(sorted(set(sol))):
        node_to_canonical[node] = i
    return [node_to_canonical[node] for node in sol], node_to_canonical


def canonical_to_montreal(sol, node_to_canonical):
    canonical_to_node = {v: k for k, v in node_to_canonical.items()}
    return [canonical_to_node[node] for node in sol]


def estimate_batch_size(gpu_memory_bytes, input_shape, total_params):
    # Constants
    bytes_per_float32 = 4

    # Calculate input size
    input_size = 1
    for dim in input_shape:
        input_size *= dim

    # Sizes in bytes
    input_size_bytes = input_size * bytes_per_float32
    model_size_bytes = total_params * bytes_per_float32

    # A rough estimate of the memory needed for forward and backward passes
    # This is quite a rough estimate; the actual memory usage can be significantly higher
    # depending on the model architecture and specific operations used in the forward pass.
    forward_backward_bytes = 2 * model_size_bytes

    # An estimate of the memory needed for one batch
    batch_memory_bytes = input_size_bytes + \
        model_size_bytes + forward_backward_bytes

    # Estimate the maximum batch size that would fit in memory
    batch_size = gpu_memory_bytes // batch_memory_bytes

    return batch_size
