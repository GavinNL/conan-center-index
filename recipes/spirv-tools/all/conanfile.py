from conans import ConanFile, tools, CMake
import os


class SpirvtoolsConan(ConanFile):
    name = "spirv-tools"
    homepage = "https://github.com/KhronosGroup/SPIRV-Tools/"
    description = "SPIRV-Tools "
    topics = ("conan", "spirv", "spirv-v", "vulkan", "opengl", "opencl", "hlsl", "khronos")
    url = "https://github.com/conan-io/conan-center-index"
    settings = "os", "compiler", "arch", "build_type"
    exports_sources = ["CMakeLists.txt"]
    license = "Apache-2.0"
    generators = "cmake"


    # Shared/static disabled because the orignal cmake creates both?
    # To Do: Perhaps delete the shared library shared==True?
    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True
    }

    def requirements(self):
        self.requires.add("spirv-headers/1.5.1.corrected")

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "SPIRV-Tools-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def configure(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC



    def _configure_cmake(self):
        cmake = CMake(self)

        # Required by the project's CMakeLists.txt
        cmake.definitions["SPIRV-Headers_SOURCE_DIR"] = self.deps_cpp_info["spirv-headers"].rootpath

        # There are some switch( ) statements that are causing errors
        # need to turn this off
        cmake.definitions["SPIRV_WERROR"] = False

        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE*", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

        # Error KB-H020, complaining that .pc files are found
        tools.rmdir(os.path.join(self.package_folder, "lib/pkgconfig"))

        # Error KB-H019, complaining that .pc files are found
        tools.rmdir(os.path.join(self.package_folder, "lib/cmake"))


    def package_info(self):
        # The original CMakeLists.txt file builds SPIRV-Tools.a
        # and SPIRV-Tools-shared.so
        # linking to the SPIRV-Tools-shared.so gives the following error:
        # undefined reference to symbol '_ZNK8spvtools10SpirvTools11DisassembleERKSt6vectorIjSaIjEEPSsj'
        #
        # So not sure why the -shared.so object is being built.
        self.cpp_info.libs.append("SPIRV-Tools-reduce")
        self.cpp_info.libs.append("SPIRV-Tools-opt")
        self.cpp_info.libs.append("SPIRV-Tools")
        self.cpp_info.libs.append("SPIRV-Tools-shared")
