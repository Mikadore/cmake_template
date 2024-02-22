from invoke import task
from pathlib import Path
from dataclasses import dataclass

import tomllib, sys, os, itertools

"""
The project's root directory path
"""
PROJECT_ROOT = str(Path(__file__).resolve().parent)

"""
Returns the full path given a path relative to the project root
"""
def p(relative_path):
    return PROJECT_ROOT + '/' + relative_path

@dataclass
class ProjectConfig:
    @dataclass
    class Toolchain:
        cxx_compiler: str
        c_compiler: str
        linker: str

    @dataclass
    class Deps:
        packages: list[str | dict]
        link_names: list[str]
        link_tests: list[str]

    toolchain: Toolchain
    deps: Deps

def load_config():
    config_path = p('config.toml')

    try:
        config_data = open(config_path).read()
    except:
        print(f"Couldn't read project configuration at {config_path}")
        sys.exit(1)

    try:
        config = tomllib.loads(config_data)
    except:
        print("Config isn't valid TOML")
        sys.exit(0)

    return ProjectConfig(
        toolchain=ProjectConfig.Toolchain(
            cxx_compiler = config['toolchain'].get('cxx_compiler', 'g++') if 'toolchain' in config else 'g++',
            c_compiler = config['toolchain'].get('c_compiler', 'gcc') if 'toolchain' in config else 'gcc',
            linker = config['toolchain'].get('linker', 'ld') if 'toolchain' in config else 'ld',
        ),
        deps=ProjectConfig.Deps(
            packages=config['deps'].get('packages', []) if 'deps' in config else [],
            link_names=config['deps'].get('link_names', []) if 'deps' in config else [],
            link_tests=config['deps'].get('link_tests', []) if 'deps' in config else [],
        )
    )

PROJECT = load_config()

def generate_dependency_file(filepath, packages):
    def format_cpm_entry(config_entry):
        entry_type = type(config_entry).__name__
        match entry_type:
            case "dict":
                options = ' '.join(config_entry['options'])
                return (
                    "cpmaddpackage(\n"
                    f"\tNAME {config_entry['name']}\n" 
                    f"\tVERSION {config_entry['version']}\n"
                    f"\tGITHUB_REPOSITORY \"{config_entry['github_repository']}\"\n" 
                    f"\tOPTIONS \"{options}\")\n")
            case "str":
                return f"cpmaddpackage(\"{config_entry}\")"
            case _:
                raise ValueError(f"package entry can only be of type dict or str. got {entry_type}")

    with open(filepath, "w") as output:
        output.write("include(cmake/lib/CPM.cmake)\n")
        for entry in packages:
            output.write(format_cpm_entry(entry))
            output.write('\n')




@task
def clean(c):
    c.run(f"rm -rf {p('dist')}")

@task
def generate(c):
    result_dir = p('dist')

    c.run(f"rm -rf {result_dir} && mkdir {result_dir}")
    c.run(f"cp {p('cmake/CMakeLists.txt')} {result_dir}")
    c.run(f"mkdir {result_dir}/cmake && cp -r {p('cmake/lib')} {result_dir}/cmake")

    generate_dependency_file(f'{result_dir}/cmake/Dependencies.cmake', PROJECT.deps.packages)

    os.chdir(p('src'))
    lib_src_files = list(itertools.chain.from_iterable([[p(f'src/{root}/{file}') for file in files] for root, dir, files in os.walk('lib')]))
    bin_src_files = [p(f'src/bin/{binsrc}') for binsrc in os.listdir('bin')]
    test_src_files = [p(f'src/test/{testsrc}') for testsrc in os.listdir('test')]
    
    lib_srcs = ' '.join(lib_src_files)
    link_names = ' '.join(PROJECT.deps.link_names)
    link_tests = ' '.join(PROJECT.deps.link_tests)
    
    c.run(f"mkdir {result_dir}/lib")
    c.run(f"mkdir {result_dir}/bin")
    c.run(f"mkdir {result_dir}/tests")
    with open(f'{result_dir}/lib/CMakeLists.txt', "w") as output:
        output.write("add_library(lib)\n")
        output.write(f"target_sources(\n\tlib PUBLIC FILE_SET CXX_MODULES BASE_DIRS {p('src')} FILES\n\t\t{lib_srcs})\n")

        output.write(f"target_link_libraries(lib PRIVATE {link_names})\n")
        output.write(f"target_link_libraries(lib PRIVATE myproject_options myproject_warnings)\n")
    with open(f'{result_dir}/bin/CMakeLists.txt', "w") as output:
        for bin_src in bin_src_files:
            bin_name = bin_src.split('.')[0].split('/')[-1]
            output.write(f"add_executable({bin_name} {bin_src})\n")
            output.write(f"target_link_libraries({bin_name} PRIVATE lib {link_names})\n")
            output.write(f"target_link_libraries({bin_name} PRIVATE myproject_options myproject_warnings)\n")
    with open(f'{result_dir}/tests/CMakeLists.txt', "w") as output:
        output.write(f"add_executable(tests {' '.join(test_src_files)})\n")
        output.write(f"target_link_libraries(tests PRIVATE lib {link_names} {link_tests})\n")
        output.write(f"target_link_libraries(tests PRIVATE myproject_options myproject_warnings)\n")

    
        
@task(generate)
def build(c, debug=False):
    src_dir = p("dist")
    build_dir = f"{src_dir}/build"
    build_mode = "Debug" if debug else "Release"
    
    c.run(f"mkdir -p {build_dir}")
    with c.cd(build_dir):
        definitions = {
            "CMAKE_CXX_COMPILER": PROJECT.toolchain.cxx_compiler,
            "CMAKE_C_COMPILER": PROJECT.toolchain.c_compiler,
            "CMAKE_BUILD_TYPE": build_mode,
        }

        def format_cmake_arg(key, val):
            if type(val) == bool:
                val = 'ON' if val else 'OFF'
            return f"-D{key}={val}" 

        definitions_arg = ' '.join([format_cmake_arg(key, val) for key, val in definitions.items()])

        c.run(f"cmake {definitions_arg} -S{src_dir} -B{build_dir} -G Ninja")
        c.run(f"ninja")
        