from conans import ConanFile, tools, CMake
import os


class PmpConan(ConanFile):
    name = "pmp"
    homepage = "https://github.com/pmp-library/pmp-library/"
    description = "The Polygon Mesh Processing Library http://www.pmp-library.org"
    topics = ("conan", "pmp", "geometry")
    url = "https://github.com/conan-io/conan-center-index"
    settings = "os", "compiler", "arch", "build_type"
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    license = "MIT"

    options = {
        "shared": [True, False],
        "fPIC": [True, False]
    }
    default_options = {
        "shared": True,
        "fPIC": True
    }

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def requirements(self):
        self.requires.add("eigen/3.3.7")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        extracted_dir = "pmp-library-" + self.version
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

    def package_info(self):
        self.cpp_info.libs = ["pmp"]
