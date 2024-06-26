import os
import subprocess
import argparse
import time
import ast
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 生成 api.py 文件的内容
api_py_content = """
class Api:
    def hello(self, name: str) -> object:
        return {"message": f"Hello, {name}!"}
"""

# 生成 main.py 文件的内容
def getMainpy(project_name):
    return """
import webview
from api import Api

window = None

def create_window():
    global window
    window = webview.create_window(\""""+project_name+"""\", "./frontend/dist/index.html", width=800, height=600, js_api=Api())
    webview.start(debug=True)

def main():
    create_window()

if __name__ == "__main__":
    main()
"""

class Watcher:
    DIRECTORY_TO_WATCH = "."

    def __init__(self):
        self.observer = Observer()
        self.restart_event = threading.Event()

    def run(self):
        event_handler = Handler(self.restart_event)
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):
    def __init__(self, restart_event):
        self.restart_event = restart_event

    def on_any_event(self, event):
        if event.is_directory:
            return None
        elif event.event_type in ('modified', 'created'):
            if event.src_path == ".\\frontend\\src\\runtime\\api.ts":
                return None
            if event.src_path.endswith(".py"):
                print(f"Detected change in: {event.src_path}")
                self.restart_event.set()
            elif event.src_path.endswith((".ts", ".tsx")):
                print(f"Detected change in: {event.src_path}")
                self.restart_event.set()

def generate_ts_file(file_path):
    with open(file_path, "r") as source:
        tree = ast.parse(source.read())

    class ApiVisitor(ast.NodeVisitor):
        def __init__(self):
            self.methods = []

        def visit_FunctionDef(self, node):
            if node.name != "__init__":
                method_info = {
                    "name": node.name,
                    "args": [(arg.arg, self.get_arg_type(arg.annotation)) for arg in node.args.args if arg.arg != 'self']
                }
                self.methods.append(method_info)
            self.generic_visit(node)

        def get_arg_type(self, annotation):
            if isinstance(annotation, ast.Name):
                python_type = annotation.id
                if python_type == "str":
                    return "string"
                elif python_type == "int":
                    return "number"
                elif python_type == "float":
                    return "number"
                elif python_type == "bool":
                    return "boolean"
                else:
                    return "any"
            elif isinstance(annotation, ast.Subscript):
                return "Array<any>"
            else:
                return "any"

    visitor = ApiVisitor()
    visitor.visit(tree)
    ts_content = "// eslint-disable-next-line @typescript-eslint/no-explicit-any\n"
    ts_content += "const api = {\n"
    for method in visitor.methods:
        args = ", ".join([f"{arg[0]}: {arg[1]}" for arg in method["args"]])
        ts_content += f"  {method['name']}: async ({args}) => {{\n"
        ts_content += f"    // @ts-expect-error pywebview is a global variable\n"
        ts_content += f"    return await pywebview.api.{method['name']}({', '.join([arg[0] for arg in method['args']])})\n"
        ts_content += f"  }},\n"
    ts_content += "}\n\nexport default api\n"

    with open("frontend/src/runtime/api.ts", "w") as ts_file:
        ts_file.write(ts_content)

    print("api.ts file generated")

def build_frontend():
    print("Building frontend...")
    original_cwd = os.getcwd()
    try:
        os.chdir("./frontend")
        subprocess.run("yarn build", shell=True, check=True)
    finally:
        os.chdir(original_cwd)

def run_main(restart_event):
    while True:
        generate_ts_file("api.py")  # Generate TypeScript file initially
        build_frontend()
        print("Running main.py...")
        process = subprocess.Popen(["python", "main.py"])
        try:
            while not restart_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            process.terminate()
            process.wait()
            print("\nMain.py execution terminated.")
            break
        process.terminate()
        process.wait()
        print("Restarting main.py...")
        restart_event.clear()

def init_project(project_name):
    os.mkdir(project_name)
    os.chdir(project_name)
    print(f"Initializing project '{project_name}'...")
    subprocess.run(["yarn", "create", "vite", "-t", "react-ts", "frontend"], shell=True, check=True)
    os.mkdir("frontend/src/runtime")
    # 写入 api.py 文件
    with open("api.py", "w+") as f:
        f.write(api_py_content.strip())
    print("api.py file generated")

    # 写入 main.py 文件
    with open("main.py", "w+") as f:
        f.write(getMainpy(project_name=project_name).strip())
    print("main.py file generated")
    
    print(f"Project '{project_name}' initialized successfully.")

def main():
    parser = argparse.ArgumentParser(description='Kails CLI')
    parser.add_argument('command', choices=['run', 'init'], help='command to execute')
    parser.add_argument('project_name', nargs='?', help='name of the project to initialize')

    args = parser.parse_args()

    if args.command == 'run':
        build_frontend()
        watcher = Watcher()
        watcher_thread = threading.Thread(target=watcher.run)
        watcher_thread.start()
        run_main(watcher.restart_event)
    elif args.command == 'init':
        if not args.project_name:
            print("Error: Missing required argument 'project_name'")
            return
        init_project(args.project_name)

if __name__ == '__main__':
    main()
