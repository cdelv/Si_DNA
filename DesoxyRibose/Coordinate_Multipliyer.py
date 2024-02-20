def process_coordinates(input_file, output_file, factor):
    with open(input_file, 'r') as input_file, open(output_file, 'w') as output_file:
        for line in input_file:
            if line.strip():
                parts = line.split()
                # Extract coordinates and convert to float
                x, y, z = map(float, parts[:3])
                # Multiply coordinates by the factor
                x *= factor
                y *= factor
                z *= factor
                # Format the output line
                output_line = f"{x:.8f}   {y:.8f}   {z:.8f}   {parts[3]}       {parts[4]}  {parts[5]}\n"
                # Write the formatted line to the output file
                output_file.write(output_line)

if __name__ == "__main__":
    input_file = "input.txt"
    output_file = "output.txt"
    factor = float(input("Enter the multiplication factor: "))
    
    process_coordinates(input_file, output_file, factor)
    print(f"Coordinates multiplied by {factor} and saved to {output_file}")
