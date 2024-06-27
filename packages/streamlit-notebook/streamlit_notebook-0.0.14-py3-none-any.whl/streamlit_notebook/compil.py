import os

def compile_python_files(output_filename="all.txt"):
    with open(output_filename, "w", encoding="utf-8") as outfile:
        for filename in os.listdir('.'):
            if filename.endswith(".py"):
                with open(filename, "r", encoding="utf-8") as infile:
                    outfile.write(f"### {filename}\n")
                    outfile.write(infile.read())
                    outfile.write("\n\n")

if __name__ == "__main__":
    compile_python_files()