from conans import ConanFile, tools, CMake
import os

class GlslangConan(ConanFile):
    name = "glslang"
    homepage = "https://github.com/KhronosGroup/glslang/"
    description = "JSON for Modern C++ parser and generator."
    topics = ("conan", "sprv", "opengl", "vulkan", "hlsl")
    url = "https://github.com/conan-io/conan-center-index"
    settings = "os", "compiler", "arch", "build_type"
    exports_sources = ["CMakeLists.txt"]
    license = "Various"
    generators = "cmake"

    options = {
        "fPIC": [True, False],
        "shared": [True, False],
        "hlsl": [True, False]
    }
    default_options = {
        "fPIC": True,
        "shared": False,
        "hlsl" : True
    }

    def requirements(self):
        if self.options.hlsl:
            self.requires.add("spirv-tools/2019.2")

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "glslang-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def configure(self):
        pass
        #if self.settings.os == "Windows":
        #    self.options.remove("fPIC")

        #if self.options.shared:
        #    del self.options.fPIC


    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["ENABLE_CTEST"] = False
        cmake.definitions["BUILD_TESTING"] = False
        cmake.definitions["ENABLE_GLSLANG_BINARIES"] = True
        cmake.definitions["ENABLE_HLSL"] = self.options.hlsl
        #cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared

        #cmake.configure()
        cmake.configure(build_folder=self._build_subfolder)
        #cmake.configure(source_folder=self._source_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE*", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()


    def package_info(self):
        # Error KB-H019, complaining that the cmake --build . --target install
        # placed the cmake files in the wrong directory?
        self.cpp_info.builddirs.append("lib/cmake")

        # When building the static libraries, tools.collect_libs(self) does
        # not produce the correct link order.
        self.cpp_info.libs.append("SPVRemapper")
        self.cpp_info.libs.append("SPIRV")
        self.cpp_info.libs.append("glslang")
        self.cpp_info.libs.append("HLSL")
        self.cpp_info.libs.append("SPVRemapper")
        self.cpp_info.libs.append("OGLCompiler")
        self.cpp_info.libs.append("OSDependent")

        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
