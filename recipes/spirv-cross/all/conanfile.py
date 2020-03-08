from conans import ConanFile, tools, CMake
import os


class SpirvcrossConan(ConanFile):
    name = "spirv-cross"
    homepage = "https://github.com/KhronosGroup/SPIRV-Cross"
    description = "SPIRV-Cross is a practical tool and library for performing reflection on SPIR-V and disassembling SPIR-V back to high level languages."
    topics = ("conan", "spirv", "spirv-v", "vulkan", "opengl", "opencl", "hlsl", "khronos")
    url = "https://github.com/conan-io/conan-center-index"
    settings = "os", "compiler", "arch", "build_type"
    exports_sources = ["CMakeLists.txt"]
    license = "Apache-2.0"
    generators = "cmake"

    #
    # The library by default builds static libraries,
    # but if you set SPIRV_CROSS_SHARED=TRUE, it will
    # build spirv-cross-c.so, which is the shared equivalent of
    # spirv-cross-c.a.  All other libs are static libraries regardless.
    #
    # The shared library is a C-only interface and does not provide a C++
    # interface. C++ must use static libraries only.
    #
    # For this reason, the shared option is disabled for now. If anyone
    # has a good way to organize it, feel free to update the recipe.
    #
    #options = {
    #    #"shared": [True, False],
    #    "fPIC": [True, False]
    #}
    #default_options = {
    #    #"shared": True,
    #    "fPIC": True
    #}

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])

        extracted_dir = "SPIRV-Cross-" + self.version.replace(".", "-")
        os.rename(extracted_dir, self._source_subfolder)

    def configure(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def _configure_cmake(self):
        cmake = CMake(self)

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
        tools.rmdir( os.path.join(self.package_folder, "share/spirv_cross_c/cmake"))
        tools.rmdir( os.path.join(self.package_folder, "share/spirv_cross_core/cmake"))
        tools.rmdir( os.path.join(self.package_folder, "share/spirv_cross_cpp/cmake"))
        tools.rmdir( os.path.join(self.package_folder, "share/spirv_cross_c_shared/cmake"))
        tools.rmdir( os.path.join(self.package_folder, "share/spirv_cross_glsl/cmake"))
        tools.rmdir( os.path.join(self.package_folder, "share/spirv_cross_hlsl/cmake"))
        tools.rmdir( os.path.join(self.package_folder, "share/spirv_cross_msl/cmake"))
        tools.rmdir( os.path.join(self.package_folder, "share/spirv_cross_reflect/cmake"))
        tools.rmdir( os.path.join(self.package_folder, "share/spirv_cross_util/cmake"))

    def package_info(self):
        self.cpp_info.libs.append("spirv-cross-glsl")
        self.cpp_info.libs.append("spirv-cross-hlsl")
        self.cpp_info.libs.append("spirv-cross-cpp")
        self.cpp_info.libs.append("spirv-cross-reflect")
        self.cpp_info.libs.append("spirv-cross-msl")
        self.cpp_info.libs.append("spirv-cross-util")
        self.cpp_info.libs.append("spirv-cross-core")
