import numpy as np

# Function to read the input from input.txt
def read_input(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    n = len([line for line in lines if not line.startswith('truck')])
    city_map = []
    for i in range(n):
        city_map.append(lines[i].strip().split(','))

    # Convert 'N' to a large number (as it represents no road)
    for i in range(n):
        for j in range(n):
            if city_map[i][j] == 'N':
                city_map[i][j] = float('inf')
            else:
                city_map[i][j] = int(city_map[i][j])

    city_map = np.array(city_map)

    # Read the truck information
    trucks = []
    for i in range(n, len(lines)):
        truck_info = lines[i].strip().split('#')
        truck_number = int(truck_info[0].split('_')[1])
        capacity = int(truck_info[1])
        trucks.append((truck_number, capacity))

    return city_map, trucks


# Function to calculate the distance of a route
def calculate_distance(route, city_map):
    total_distance = 0
    start = 0  # 'a' is node 0
    for node in route:
        total_distance += city_map[start][node]
        start = node
    total_distance += city_map[start][0]  # Return to starting point
    return total_distance


# Function to generate initial random routes
def generate_initial_routes(trucks, delivery_points):
    routes = {}
    assigned = set()
    for truck, capacity in trucks:
        route = []
        for _ in range(capacity):
            point = np.random.choice(delivery_points)
            while point in assigned:
                point = np.random.choice(delivery_points)
            route.append(point)
            assigned.add(point)
        routes[truck] = route
    return routes


# Hill-Climbing algorithm
def hill_climb(routes, city_map, trucks, delivery_points):
    current_routes = routes
    current_distance = sum([calculate_distance(route, city_map) for route in current_routes.values()])

    improved = True
    while improved:
        improved = False
        for truck in current_routes:
            for i in range(len(current_routes[truck])):
                for j in range(i + 1, len(current_routes[truck])):
                    # Swap two delivery points
                    new_routes = current_routes.copy()
                    new_routes[truck][i], new_routes[truck][j] = new_routes[truck][j], new_routes[truck][i]

                    # Calculate new distance
                    new_distance = sum([calculate_distance(route, city_map) for route in new_routes.values()])

                    # If the new distance is better, accept the new routes
                    if new_distance < current_distance:
                        current_routes = new_routes
                        current_distance = new_distance
                        improved = True

    return current_routes, current_distance


# Function to write the output to a file
def write_output(routes, total_distance, output_file):
    with open(output_file, 'w') as file:
        for truck, route in routes.items():
            file.write(f"truck_{truck}#" + ','.join([chr(point + 97) for point in route]) + '\n')
        file.write(str(total_distance) + '\n')


# Main function
def main(input_file, output_file):
    # Step 1: Read input
    city_map, trucks = read_input(input_file)

    # List of delivery points (1 to n, excluding the courier station which is node 0)
    delivery_points = list(range(1, len(city_map)))

    # Step 2: Generate initial random routes
    initial_routes = generate_initial_routes(trucks, delivery_points)

    # Step 3: Apply Hill-Climbing algorithm
    final_routes, total_distance = hill_climb(initial_routes, city_map, trucks, delivery_points)

    # Step 4: Write output
    write_output(final_routes, total_distance, output_file)


# Example usage
if __name__ == "__main__":
    main("new.txt", "123456A.txt")
