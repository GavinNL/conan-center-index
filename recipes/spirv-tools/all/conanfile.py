from conans import ConanFile, tools, CMake
import os


class SpirvtoolsConan(ConanFile):
    name = "spirv-tools"
    homepage = "https://github.com/KhronosGroup/SPIRV-Tools/"
    description = "SPIRV-Tools "
    topics = ("conan", "sprv", "vulkan", "hlsl")
    url = "https://github.com/conan-io/conan-center-index"
    settings = "os", "compiler", "arch", "build_type"
    exports_sources = ["CMakeLists.txt"]
    license = "Apache-2.0"
    generators = "cmake"


    # Shared/static disabled because the orignal cmake creates both?
    # To Do: Perhaps delete the shared library shared==True?
    #options = {
    #    "shared": [True, False],
    #    "fPIC": [True, False]
    #}
    #default_options = {
    #    "shared": False,
    #    "fPIC": True
    #}

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
        # This is handled by the original cmake file?
        #if self.settings.os == "Windows":
        #    self.options.remove("fPIC")
        #if self.options.shared:
        #    del self.options.fPIC
        pass


    def _configure_cmake(self):
        # Printing out the root-path of where the spirv-headers was installed
        # this is just for debugging. Will remove later.
        #
        # wget https://github.com/KhronosGroup/SPIRV-Tools/archive/v2019.2.tar.gz
        # tar -xvf v2019.2.tar.gz
        # cd SPIRV-Tools-2019.2
        # mkdir build && cd build
        # cmake .. -DSPIRV-Headers_SOURCE_DIR=THE_PATH_PRINTED_OUT_BY_THE_FOLLOWING_CODE -DSPIRV_WERROR=False
        # make
        print("********")
        print(self.deps_cpp_info["spirv-headers"].rootpath)
        print("********")

        cmake = CMake(self)

        # The orignal CMake header was weird, it asks the user to check out the
        # spirv-headers tools into their src/external folder instead of using
        # a find_package( )
        # Luckily it also allows you to specify where the headers were installed
        # to.
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
        ## The original CMakeLists creates an en example called: spirv-tools-cpp-example
        ## It links to these two libraries.
        ## The test_package.cpp is a copy of the spirv-tools-cpp-example.cpp file
        ## but for some reason it is giving linking errors when tryign to
        ## create the test_package.cpp
        #
        self.cpp_info.libs.append("SPIRV-Tools-opt")
        self.cpp_info.libs.append("SPIRV-Tools")
